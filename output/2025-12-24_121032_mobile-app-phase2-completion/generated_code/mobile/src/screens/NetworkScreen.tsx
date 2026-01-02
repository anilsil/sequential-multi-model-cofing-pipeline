import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text } from 'react-native-paper';
import { EmptyState } from '../components/ui/EmptyState';

export function NetworkScreen() {
  return (
    <View style={styles.container}>
      <EmptyState
        icon="chart-network"
        title="Network Visualization"
        description="Interactive network graph showing your connections and their relationships. Coming soon!"
      />
      <View style={styles.info}>
        <Text variant="bodyMedium" style={styles.infoText}>
          This feature will display:
        </Text>
        <Text variant="bodySmall" style={styles.bulletPoint}>
          • Visual graph of your professional network
        </Text>
        <Text variant="bodySmall" style={styles.bulletPoint}>
          • Connection strength indicators
        </Text>
        <Text variant="bodySmall" style={styles.bulletPoint}>
          • Trust score visualizations
        </Text>
        <Text variant="bodySmall" style={styles.bulletPoint}>
          • Network insights and analytics
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
    padding: 16,
    justifyContent: 'center',
  },
  info: {
    marginTop: 32,
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
});
