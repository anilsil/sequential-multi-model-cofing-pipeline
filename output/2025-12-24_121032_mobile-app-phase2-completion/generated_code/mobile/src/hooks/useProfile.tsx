import { useQuery } from '@tanstack/react-query';
import { supabase } from '../lib/supabase';

export interface Profile {
  id: string;
  full_name: string;
  avatar_url?: string;
  bio?: string;
  industry?: string;
  location?: string;
  skills?: string[];
  created_at: string;
  posts_count?: number;
  connections_count?: number;
  avg_trust_score?: number;
  spam_rate?: number;
  toxicity_rate?: number;
}

async function fetchProfile(userId: string): Promise<Profile> {
  const { data, error } = await supabase
    .from('profiles')
    .select(`
      id,
      full_name,
      avatar_url,
      bio,
      industry,
      location,
      skills,
      created_at
    `)
    .eq('id', userId)
    .single();

  if (error) throw error;

  // TODO: Fetch aggregated stats (posts_count, connections_count, etc.)
  // This requires separate queries or database functions
  const profile: Profile = {
    ...data,
    posts_count: 0,
    connections_count: 0,
    avg_trust_score: 0,
    spam_rate: 0,
    toxicity_rate: 0,
  };

  return profile;
}

export function useProfile(userId: string) {
  return useQuery({
    queryKey: ['profile', userId],
    queryFn: () => fetchProfile(userId),
    enabled: !!userId,
  });
}
