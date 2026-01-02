import React from 'react';
import { View, StyleSheet, FlatList } from 'react-native';
import { Text, List, Avatar as PaperAvatar } from 'react-native-paper';
import { EmptyState } from '../components/ui/EmptyState';

// Placeholder data for UI demonstration
const PLACEHOLDER_CONVERSATIONS = [
  {
    id: '1',
    name: 'Sarah Johnson',
    lastMessage: 'Thanks for connecting!',
    timestamp: '2 hours ago',
    unread: true,
  },
  {
    id: '2',
    name: 'Michael Chen',
    lastMessage: 'Let\'s schedule a meeting',
    timestamp: 'Yesterday',
    unread: false,
  },
];

export function MessagesScreen() {
  const conversations = []; // Empty for now - will be populated with real data in Phase 3

  if (conversations.length === 0) {
    return (
      <View style={styles.container}>
        <EmptyState
          icon="message-outline"
          title="No messages yet"
          description="Start a conversation with your connections. Real-time messaging coming in Phase 3!"
        />
        <View style={styles.info}>
          <Text variant="bodyMedium" style={styles.infoText}>
            Upcoming features:
          </Text>
          <Text variant="bodySmall" style={styles.bulletPoint}>
            • Real-time messaging with Supabase subscriptions
          </Text>
          <Text variant="bodySmall" style={styles.bulletPoint}>
            • Typing indicators and read receipts
          </Text>
          <Text variant="bodySmall" style={styles.bulletPoint}>
            • Message history and search
          </Text>
          <Text variant="bodySmall" style={styles.bulletPoint}>
            • Push notifications for new messages
          </Text>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={conversations}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <List.Item
            title={item.name}
            description={item.lastMessage}
            left={props => <PaperAvatar.Text {...props} size={48} label={item.name[0]} />}
            right={props => (
              <View style={styles.rightContainer}>
                <Text variant="bodySmall" style={styles.timestamp}>
                  {item.timestamp}
                </Text>
                {item.unread && <View style={styles.unreadBadge} />}
              </View>
            )}
            onPress={() => {}}
            style={styles.conversationItem}
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
  conversationItem: {
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
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
