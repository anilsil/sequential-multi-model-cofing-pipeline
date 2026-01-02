import { useInfiniteQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../lib/supabase';

export interface Post {
  id: string;
  user_id: string;
  content: string;
  image_url?: string;
  created_at: string;
  profiles: {
    full_name: string;
    avatar_url?: string;
  };
  ai_post_analysis?: {
    spam_score: number;
    toxicity_score: number;
    ai_generated_score: number;
  };
  likes_count: number;
  comments_count: number;
  user_has_liked: boolean;
}

const PAGE_SIZE = 20;

async function fetchPosts(pageParam = 0) {
  const from = pageParam * PAGE_SIZE;
  const to = from + PAGE_SIZE - 1;

  const { data, error } = await supabase
    .from('posts')
    .select(`
      id,
      user_id,
      content,
      image_url,
      created_at,
      profiles!posts_user_id_fkey (
        full_name,
        avatar_url
      ),
      ai_post_analysis (
        spam_score,
        toxicity_score,
        ai_generated_score
      )
    `)
    .order('created_at', { ascending: false })
    .range(from, to);

  if (error) throw error;

  // TODO: Fetch likes_count, comments_count, user_has_liked
  // This requires aggregation queries or separate calls
  const postsWithCounts = data.map(post => ({
    ...post,
    likes_count: 0,
    comments_count: 0,
    user_has_liked: false,
  }));

  return { posts: postsWithCounts, nextPage: data.length === PAGE_SIZE ? pageParam + 1 : null };
}

export function usePosts() {
  return useInfiniteQuery({
    queryKey: ['posts'],
    queryFn: ({ pageParam = 0 }) => fetchPosts(pageParam),
    getNextPageParam: (lastPage) => lastPage.nextPage,
    initialPageParam: 0,
  });
}

export function useLikePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ postId, liked }: { postId: string; liked: boolean }) => {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('Not authenticated');

      if (liked) {
        // Unlike
        const { error } = await supabase
          .from('post_likes')
          .delete()
          .eq('post_id', postId)
          .eq('user_id', user.id);
        if (error) throw error;
      } else {
        // Like
        const { error } = await supabase
          .from('post_likes')
          .insert({ post_id: postId, user_id: user.id });
        if (error) throw error;
      }
    },
    onMutate: async ({ postId, liked }) => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ['posts'] });
      const previousPosts = queryClient.getQueryData(['posts']);

      queryClient.setQueryData(['posts'], (old: any) => {
        if (!old) return old;
        return {
          ...old,
          pages: old.pages.map((page: any) => ({
            ...page,
            posts: page.posts.map((post: Post) =>
              post.id === postId
                ? {
                    ...post,
                    user_has_liked: !liked,
                    likes_count: liked ? post.likes_count - 1 : post.likes_count + 1,
                  }
                : post
            ),
          })),
        };
      });

      return { previousPosts };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousPosts) {
        queryClient.setQueryData(['posts'], context.previousPosts);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
}

export function useCreatePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ content, imageUrl }: { content: string; imageUrl?: string }) => {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('Not authenticated');

      const { data, error } = await supabase
        .from('posts')
        .insert({
          user_id: user.id,
          content,
          image_url: imageUrl,
        })
        .select()
        .single();

      if (error) throw error;
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
}
