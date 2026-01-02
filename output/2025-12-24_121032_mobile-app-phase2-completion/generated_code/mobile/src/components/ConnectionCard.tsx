import React from 'react';
import { View, StyleSheet, TouchableOpacity } from 'react-native';
import { Text } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { MainTabParamList } from '../navigation/types';
import { Avatar } from './ui/Avatar';
import { Badge } from './ui/Badge';
import { Button } from './ui/Button';
import { Card } from './ui/Card';
import type { Connection } from '../hooks/useConnections';

interface ConnectionCardProps {
  connection: Connection;
  onAccept?: (connectionId: string) => void;
  onReject?: (connectionId: string) => void;
  onMessage?: (userId: string) => void;
}

export function ConnectionCard({
  connection,
  onAccept,
  onReject,
  onMessage,
}: ConnectionCardProps) {
  const navigation = useNavigation<NativeStackNavigationProp<MainTabParamList>>();

  const handleProfilePress = () => {
    navigation.navigate('Profile', { userId: connection.connected_user_id });
  };

  const getTrustBadgeVariant = (score: number) => {
    if (score >= 80) return 'success';
    if (score >= 50) return 'warning';
    return 'error';
  };

  const getTrustLabel = (score: number) => {
    if (score >= 80) return 'High Trust';
    if (score >= 50) return 'Medium Trust';
    return 'Low Trust';
  };

  const isPending = connection.status === 'pending';

  return (
    <Card style={styles.container}>
      <TouchableOpacity
        onPress={handleProfilePress}
        style={styles.content}
        accessibilityRole="button"
        accessibilityLabel={`View ${connection.profile.full_name}'s profile`}
      >
        <Avatar
          imageUrl={connection.profile.avatar_url}
          name={connection.profile.full_name}
          size="large"
        />

        <View style={styles.info}>
          <Text variant="titleMedium" style={styles.name}>
            {connection.profile.full_name}
          </Text>
          {connection.profile.industry && (
            <Text variant="bodySmall" style={styles.industry}>
              {connection.profile.industry}
            </Text>
          )}
          {connection.profile.bio && (
            <Text variant="bodySmall" numberOfLines={2} style={styles.bio}>
              {connection.profile.bio}
            </Text>
          )}

          {!isPending && (
            <Badge
              variant={getTrustBadgeVariant(connection.trust_score)}
              size="small"
              style={styles.trustBadge}
            >
              {getTrustLabel(connection.trust_score)} ({connection.trust_score})
            </Badge>
          )}
        </View>
      </TouchableOpacity>

      {isPending && onAccept && onReject && (
        <View style={styles.actions}>
          <Button
            onPress={() => onAccept(connection.id)}
            variant="primary"
            size="small"
          >
            Accept
          </Button>
          <Button
            onPress={() => onReject(connection.id)}
            variant="outline"
            size="small"
          >
            Reject
          </Button>
        </View>
      )}

      {!isPending && onMessage && (
        <View style={styles.actions}>
          <Button
            onPress={() => onMessage(connection.connected_user_id)}
            variant="outline"
            size="small"
            icon="message-outline"
          >
            Message
          </Button>
        </View>
      )}
    </Card>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 12,
  },
  content: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  info: {
    marginLeft: 12,
    flex: 1,
  },
  name: {
    marginBottom: 4,
  },
  industry: {
    color: '#6b7280',
    marginBottom: 4,
  },
  bio: {
    color: '#6b7280',
    marginTop: 4,
  },
  trustBadge: {
    marginTop: 8,
    alignSelf: 'flex-start',
  },
  actions: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
});
