import { useQuery } from '@tanstack/react-query';
import { supabase } from '../lib/supabase';

export interface Connection {
  id: string;
  user_id: string;
  connected_user_id: string;
  status: 'pending' | 'accepted' | 'rejected';
  trust_score: number;
  created_at: string;
  profile: {
    id: string;
    full_name: string;
    avatar_url?: string;
    industry?: string;
    bio?: string;
  };
}

async function fetchConnections(
  userId: string,
  status?: 'pending' | 'accepted' | 'rejected'
): Promise<Connection[]> {
  let query = supabase
    .from('connections')
    .select(`
      id,
      user_id,
      connected_user_id,
      status,
      trust_score,
      created_at,
      profiles!connections_connected_user_id_fkey (
        id,
        full_name,
        avatar_url,
        industry,
        bio
      )
    `)
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

  if (status) {
    query = query.eq('status', status);
  }

  const { data, error } = await query;

  if (error) throw error;

  return data.map(conn => ({
    ...conn,
    profile: conn.profiles,
  })) as Connection[];
}

export function useConnections(userId: string, status?: 'pending' | 'accepted' | 'rejected') {
  return useQuery({
    queryKey: ['connections', userId, status],
    queryFn: () => fetchConnections(userId, status),
    enabled: !!userId,
  });
}
