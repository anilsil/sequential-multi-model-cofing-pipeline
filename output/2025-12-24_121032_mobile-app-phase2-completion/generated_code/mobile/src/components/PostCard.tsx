import React from 'react';
import { View, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { Text, IconButton } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { MainTabParamList } from '../navigation/types';
import { Avatar } from './ui/Avatar';
import { Badge } from './ui/Badge';
import { Card } from './ui/Card';
import { useLikePost } from '../hooks/usePosts';
import type { Post } from '../hooks/usePosts';

interface PostCardProps {
  post: Post;
}

export function PostCard({ post }: PostCardProps) {
  const navigation = useNavigation<NativeStackNavigationProp<MainTabParamList>>();
  const likeMutation = useLikePost();

  const handleLike = () => {
    likeMutation.mutate({
      postId: post.id,
      liked: post.user_has_liked,
    });
  };

  const handleProfilePress = () => {
    navigation.navigate('Profile', { userId: post.user_id });
  };

  const getTrustColor = (score?: number) => {
    if (!score) return '#gray';
    if (score >= 80) return '#22c55e';
    if (score >= 50) return '#eab308';
    return '#ef4444';
  };

  const getAIBadgeColor = (score: number) => {
    if (score < 30) return 'success';
    if (score < 70) return 'warning';
    return 'error';
  };

  return (
    <Card style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          onPress={handleProfilePress}
          style={styles.authorContainer}
          accessibilityRole="button"
          accessibilityLabel={`View ${post.profiles.full_name}'s profile`}
        >
          <Avatar
            imageUrl={post.profiles.avatar_url}
            name={post.profiles.full_name}
            size="medium"
          />
          <View style={styles.authorInfo}>
            <Text variant="titleMedium">{post.profiles.full_name}</Text>
            <Text variant="bodySmall" style={styles.timestamp}>
              {new Date(post.created_at).toLocaleDateString()}
            </Text>
          </View>
        </TouchableOpacity>
      </View>

      <View style={styles.content}>
        <Text variant="bodyMedium">{post.content}</Text>
      </View>

      {post.image_url && (
        <Image
          source={{ uri: post.image_url }}
          style={styles.image}
          resizeMode="cover"
          accessibilityLabel="Post image"
        />
      )}

      {post.ai_post_analysis && (
        <View style={styles.aiBadges}>
          <Badge
            variant={getAIBadgeColor(post.ai_post_analysis.spam_score)}
            size="small"
          >
            Spam: {post.ai_post_analysis.spam_score}%
          </Badge>
          <Badge
            variant={getAIBadgeColor(post.ai_post_analysis.toxicity_score)}
            size="small"
          >
            Toxicity: {post.ai_post_analysis.toxicity_score}%
          </Badge>
          <Badge
            variant={getAIBadgeColor(post.ai_post_analysis.ai_generated_score)}
            size="small"
          >
            AI: {post.ai_post_analysis.ai_generated_score}%
          </Badge>
        </View>
      )}

      <View style={styles.actions}>
        <TouchableOpacity
          onPress={handleLike}
          style={styles.actionButton}
          accessibilityRole="button"
          accessibilityLabel={post.user_has_liked ? 'Unlike post' : 'Like post'}
          accessibilityState={{ selected: post.user_has_liked }}
        >
          <IconButton
            icon={post.user_has_liked ? 'heart' : 'heart-outline'}
            size={20}
            iconColor={post.user_has_liked ? '#ef4444' : '#6b7280'}
          />
          <Text variant="bodySmall">{post.likes_count}</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.actionButton}
          accessibilityRole="button"
          accessibilityLabel="View comments"
        >
          <IconButton icon="comment-outline" size={20} iconColor="#6b7280" />
          <Text variant="bodySmall">{post.comments_count}</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.actionButton}
          accessibilityRole="button"
          accessibilityLabel="Share post"
        >
          <IconButton icon="share-outline" size={20} iconColor="#6b7280" />
        </TouchableOpacity>
      </View>
    </Card>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 12,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  authorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  authorInfo: {
    marginLeft: 12,
    flex: 1,
  },
  timestamp: {
    color: '#6b7280',
    marginTop: 2,
  },
  content: {
    marginBottom: 12,
  },
  image: {
    width: '100%',
    height: 300,
    borderRadius: 8,
    marginBottom: 12,
  },
  aiBadges: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 12,
    flexWrap: 'wrap',
  },
  actions: {
    flexDirection: 'row',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
    paddingTop: 8,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 16,
    minWidth: 44,
    minHeight: 44,
  },
});
