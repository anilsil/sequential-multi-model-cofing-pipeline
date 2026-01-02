import { useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../lib/supabase';
import { useImageUpload } from './useImageUpload';

interface UpdateProfileData {
  full_name?: string;
  bio?: string;
  industry?: string;
  location?: string;
  skills?: string[];
  avatarUri?: string;
}

export function useUpdateProfile() {
  const queryClient = useQueryClient();
  const { uploadImage } = useImageUpload();

  return useMutation({
    mutationFn: async (data: UpdateProfileData) => {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('Not authenticated');

      let avatar_url = undefined;

      // Upload avatar if provided
      if (data.avatarUri) {
        avatar_url = await uploadImage(data.avatarUri, 'avatars', `users/${user.id}`);
        if (!avatar_url) throw new Error('Failed to upload avatar');
      }

      // Update profile
      const updateData: any = {};
      if (data.full_name) updateData.full_name = data.full_name;
      if (data.bio) updateData.bio = data.bio;
      if (data.industry) updateData.industry = data.industry;
      if (data.location) updateData.location = data.location;
      if (data.skills) updateData.skills = data.skills;
      if (avatar_url) updateData.avatar_url = avatar_url;

      const { data: profile, error } = await supabase
        .from('profiles')
        .update(updateData)
        .eq('id', user.id)
        .select()
        .single();

      if (error) throw error;
      return profile;
    },
    onMutate: async (newData) => {
      // Optimistic update
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;

      await queryClient.cancelQueries({ queryKey: ['profile', user.id] });
      const previousProfile = queryClient.getQueryData(['profile', user.id]);

      queryClient.setQueryData(['profile', user.id], (old: any) => ({
        ...old,
        ...newData,
      }));

      return { previousProfile };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      const { data: { user } } = supabase.auth.getUser();
      user.then(({ data: { user } }) => {
        if (user && context?.previousProfile) {
          queryClient.setQueryData(['profile', user.id], context.previousProfile);
        }
      });
    },
    onSettled: () => {
      const { data: { user } } = supabase.auth.getUser();
      user.then(({ data: { user } }) => {
        if (user) {
          queryClient.invalidateQueries({ queryKey: ['profile', user.id] });
        }
      });
    },
  });
}
