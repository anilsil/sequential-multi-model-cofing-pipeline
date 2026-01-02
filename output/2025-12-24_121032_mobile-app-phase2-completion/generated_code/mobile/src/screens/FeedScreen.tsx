import React from 'react';
import { View, StyleSheet, FlatList, RefreshControl, TouchableOpacity } from 'react-native';
import { FAB } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { MainTabParamList } from '../navigation/types';
import { PostCard } from '../components/PostCard';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { EmptyState } from '../components/ui/EmptyState';
import { usePosts } from '../hooks/usePosts';

type FeedScreenNavigationProp = NativeStackNavigationProp<MainTabParamList, 'Feed'>;

export function FeedScreen() {
  const navigation = useNavigation<FeedScreenNavigationProp>();
  const { data, isLoading, isFetchingNextPage, hasNextPage, fetchNextPage, refetch, isRefetching } = usePosts();

  const posts = data?.pages.flatMap(page => page.posts) || [];

  const handleLoadMore = () => {
    if (hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  };

  const handleCreatePost = () => {
    navigation.navigate('CreatePost');
  };

  if (isLoading) {
    return <LoadingSpinner fullScreen />;
  }

  if (posts.length === 0) {
    return (
      <View style={styles.container}>
        <EmptyState
          icon="post-outline"
          title="No posts yet"
          description="Be the first to share something with your network!"
        />
        <FAB
          icon="plus"
          style={styles.fab}
          onPress={handleCreatePost}
          accessibilityLabel="Create new post"
        />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={posts}
        keyExtractor={item => item.id}
        renderItem={({ item }) => <PostCard post={item} />}
        contentContainerStyle={styles.listContent}
        onEndReached={handleLoadMore}
        onEndReachedThreshold={0.5}
        refreshControl={
          <RefreshControl
            refreshing={isRefetching}
            onRefresh={refetch}
          />
        }
        ListFooterComponent={
          isFetchingNextPage ? (
            <View style={styles.footer}>
              <LoadingSpinner />
            </View>
          ) : null
        }
      />
      <FAB
        icon="plus"
        style={styles.fab}
        onPress={handleCreatePost}
        accessibilityLabel="Create new post"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  listContent: {
    padding: 16,
  },
  footer: {
    paddingVertical: 20,
  },
  fab: {
    position: 'absolute',
    right: 16,
    bottom: 16,
  },
});
