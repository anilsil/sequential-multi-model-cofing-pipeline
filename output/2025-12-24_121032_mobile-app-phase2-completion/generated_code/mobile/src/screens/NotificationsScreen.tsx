import React from 'react';
import { View, StyleSheet, FlatList } from 'react-native';
import { Text, List, Avatar as PaperAvatar } from 'react-native-paper';
import { EmptyState } from '../components/ui/EmptyState';

// Placeholder data for UI demonstration
const PLACEHOLDER_NOTIFICATIONS = [
  {
    id: '1',
    type: 'connection_request',
    title: 'New connection request',
    description: 'Sarah Johnson wants to connect',
    timestamp: '5 minutes ago',
    read: false,
  },
  {
    id: '2',
    type: 'post_like',
    title: 'Someone liked your post',
    description: 'Michael Chen liked your post about AI',
    timestamp: '1 hour ago',
    read: true,
  },
];

export function NotificationsScreen() {
  const notifications = []; // Empty for now - will be populated with real data

  if (notifications.length === 0) {
    return (
      <View style={styles.container}>
        <EmptyState
          icon="bell-outline"
          title="No notifications"
          description="You're all caught up! Notifications will appear here when you have new activity."
        />
        <View style={styles.info}>
          <Text variant="bodyMedium" style={styles.infoText}>
            You'll be notified about:
          </Text>
          <Text variant="bodySmall" style={styles.bulletPoint}>
            • Connection requests and acceptances
          </Text>
          <Text variant="bodySmall" style={styles.bulletPoint}>
            • Likes and comments on your posts
          </Text>
          <Text variant="bodySmall" style={styles.bulletPoint}>
            • New messages from connections
          </Text>
          <Text variant="bodySmall" style={styles.bulletPoint}>
            • Trust score changes and alerts
          </Text>
          <Text variant="bodySmall" style={styles.bulletPoint}>
            • AI moderation updates
          </Text>
        </View>
      </View>
    );
  }

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'connection_request':
        return 'account-plus';
      case 'post_like':
        return 'heart';
      case 'comment':
        return 'comment';
      case 'message':
        return 'message';
      default:
        return 'bell';
    }
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={notifications}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <List.Item
            title={item.title}
            description={item.description}
            left={props => (
              <PaperAvatar.Icon
                {...props}
                size={48}
                icon={getNotificationIcon(item.type)}
              />
            )}
            right={props => (
              <View style={styles.rightContainer}>
                <Text variant="bodySmall" style={styles.timestamp}>
                  {item.timestamp}
                </Text>
                {!item.read && <View style={styles.unreadBadge} />}
              </View>
            )}
            onPress={() => {}}
            style={[
              styles.notificationItem,
              !item.read && styles.unreadItem,
            ]}
          />
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  info: {
    margin: 16,
    padding: 16,
    backgroundColor: '#fff',
    borderRadius: 8,
  },
  infoText: {
    marginBottom: 12,
    fontWeight: 'bold',
  },
  bulletPoint: {
    color: '#6b7280',
    marginBottom: 8,
    marginLeft: 8,
  },
  notificationItem: {
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  unreadItem: {
    backgroundColor: '#eff6ff',
  },
  rightContainer: {
    alignItems: 'flex-end',
    justifyContent: 'center',
  },
  timestamp: {
    color: '#6b7280',
    marginBottom: 4,
  },
  unreadBadge: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#3b82f6',
  },
});
