import React from 'react';
import { View, StyleSheet, ScrollView, FlatList, RefreshControl } from 'react-native';
import { Text } from 'react-native-paper';
import { useRoute, useNavigation } from '@react-navigation/native';
import type { RouteProp } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { MainTabParamList } from '../navigation/types';
import { Avatar } from '../components/ui/Avatar';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { PostCard } from '../components/PostCard';
import { useProfile } from '../hooks/useProfile';
import { usePosts } from '../hooks/usePosts';
import { useAuth } from '../contexts/AuthContext';

type ProfileScreenRouteProp = RouteProp<MainTabParamList, 'Profile'>;
type ProfileScreenNavigationProp = NativeStackNavigationProp<MainTabParamList, 'Profile'>;

export function ProfileScreen() {
  const route = useRoute<ProfileScreenRouteProp>();
  const navigation = useNavigation<ProfileScreenNavigationProp>();
  const { user } = useAuth();

  const userId = route.params?.userId || user?.id;
  const isOwnProfile = userId === user?.id;

  const { data: profile, isLoading, refetch, isRefetching } = useProfile(userId);
  const { data: postsData } = usePosts(); // TODO: Filter by userId

  const userPosts = postsData?.pages.flatMap(page => page.posts.filter(p => p.user_id === userId)) || [];

  const handleEditProfile = () => {
    navigation.navigate('EditProfile');
  };

  const handleConnect = () => {
    // TODO: Implement connection request
  };

  const handleMessage = () => {
    // Navigate to messages
    navigation.navigate('Messages');
  };

  if (isLoading) {
    return <LoadingSpinner fullScreen />;
  }

  if (!profile) {
    return (
      <View style={styles.container}>
        <Text>Profile not found</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={<RefreshControl refreshing={isRefetching} onRefresh={refetch} />}
    >
      <Card style={styles.header}>
        <View style={styles.avatarContainer}>
          <Avatar imageUrl={profile.avatar_url} name={profile.full_name} size="xlarge" />
        </View>

        <Text variant="headlineMedium" style={styles.name}>
          {profile.full_name}
        </Text>

        {profile.industry && (
          <Text variant="bodyMedium" style={styles.industry}>
            {profile.industry}
          </Text>
        )}

        {profile.location && (
          <Text variant="bodySmall" style={styles.location}>
            📍 {profile.location}
          </Text>
        )}

        {profile.bio && (
          <Text variant="bodyMedium" style={styles.bio}>
            {profile.bio}
          </Text>
        )}

        <View style={styles.stats}>
          <View style={styles.stat}>
            <Text variant="titleLarge">{profile.posts_count || 0}</Text>
            <Text variant="bodySmall" style={styles.statLabel}>
              Posts
            </Text>
          </View>
          <View style={styles.stat}>
            <Text variant="titleLarge">{profile.connections_count || 0}</Text>
            <Text variant="bodySmall" style={styles.statLabel}>
              Connections
            </Text>
          </View>
          <View style={styles.stat}>
            <Text variant="titleLarge">{profile.avg_trust_score || 0}</Text>
            <Text variant="bodySmall" style={styles.statLabel}>
              Trust Score
            </Text>
          </View>
        </View>

        <View style={styles.aiMetrics}>
          <Badge variant="success" size="small">
            Spam: {profile.spam_rate || 0}%
          </Badge>
          <Badge variant="warning" size="small">
            Toxicity: {profile.toxicity_rate || 0}%
          </Badge>
        </View>

        {isOwnProfile ? (
          <Button onPress={handleEditProfile} variant="outline" fullWidth icon="pencil">
            Edit Profile
          </Button>
        ) : (
          <View style={styles.actions}>
            <Button onPress={handleConnect} variant="primary" style={{ flex: 1 }}>
              Connect
            </Button>
            <Button onPress={handleMessage} variant="outline" style={{ flex: 1 }} icon="message">
              Message
            </Button>
          </View>
        )}
      </Card>

      <View style={styles.postsSection}>
        <Text variant="titleMedium" style={styles.sectionTitle}>
          Posts
        </Text>
        {userPosts.map(post => (
          <PostCard key={post.id} post={post} />
        ))}
        {userPosts.length === 0 && (
          <Text variant="bodyMedium" style={styles.noPosts}>
            No posts yet
          </Text>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  header: {
    margin: 16,
    padding: 20,
    alignItems: 'center',
  },
  avatarContainer: {
    marginBottom: 16,
  },
  name: {
    fontWeight: 'bold',
    marginBottom: 4,
  },
  industry: {
    color: '#6b7280',
    marginBottom: 4,
  },
  location: {
    color: '#6b7280',
    marginBottom: 12,
  },
  bio: {
    textAlign: 'center',
    marginBottom: 20,
  },
  stats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    marginBottom: 16,
    paddingVertical: 16,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: '#e5e7eb',
  },
  stat: {
    alignItems: 'center',
  },
  statLabel: {
    color: '#6b7280',
    marginTop: 4,
  },
  aiMetrics: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 16,
  },
  actions: {
    flexDirection: 'row',
    gap: 12,
    width: '100%',
  },
  postsSection: {
    padding: 16,
  },
  sectionTitle: {
    marginBottom: 12,
    fontWeight: 'bold',
  },
  noPosts: {
    textAlign: 'center',
    color: '#6b7280',
    marginTop: 20,
  },
});
