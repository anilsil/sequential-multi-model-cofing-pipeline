import React, { useState } from 'react';
import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { Text, SegmentedButtons } from 'react-native-paper';
import { useAuth } from '../contexts/AuthContext';
import { ConnectionCard } from '../components/ConnectionCard';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { EmptyState } from '../components/ui/EmptyState';
import { useConnections } from '../hooks/useConnections';

type TabValue = 'accepted' | 'pending';

export function ConnectionsScreen() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<TabValue>('accepted');

  const { data: connections, isLoading, refetch, isRefetching } = useConnections(
    user?.id || '',
    activeTab
  );

  const handleAcceptConnection = async (connectionId: string) => {
    // TODO: Implement accept connection mutation
    console.log('Accept connection:', connectionId);
  };

  const handleRejectConnection = async (connectionId: string) => {
    // TODO: Implement reject connection mutation
    console.log('Reject connection:', connectionId);
  };

  const handleMessage = (userId: string) => {
    // TODO: Navigate to message screen with userId
    console.log('Message user:', userId);
  };

  if (isLoading) {
    return <LoadingSpinner fullScreen />;
  }

  const isEmpty = !connections || connections.length === 0;

  return (
    <View style={styles.container}>
      <View style={styles.tabContainer}>
        <SegmentedButtons
          value={activeTab}
          onValueChange={(value) => setActiveTab(value as TabValue)}
          buttons={[
            {
              value: 'accepted',
              label: 'My Connections',
            },
            {
              value: 'pending',
              label: 'Requests',
            },
          ]}
        />
      </View>

      {isEmpty ? (
        <EmptyState
          icon={activeTab === 'accepted' ? 'account-group' : 'account-clock'}
          title={
            activeTab === 'accepted'
              ? 'No connections yet'
              : 'No pending requests'
          }
          description={
            activeTab === 'accepted'
              ? 'Start connecting with professionals in your network'
              : 'When someone sends you a connection request, it will appear here'
          }
        />
      ) : (
        <FlatList
          data={connections}
          keyExtractor={item => item.id}
          renderItem={({ item }) => (
            <ConnectionCard
              connection={item}
              onAccept={activeTab === 'pending' ? handleAcceptConnection : undefined}
              onReject={activeTab === 'pending' ? handleRejectConnection : undefined}
              onMessage={activeTab === 'accepted' ? handleMessage : undefined}
            />
          )}
          contentContainerStyle={styles.listContent}
          refreshControl={
            <RefreshControl refreshing={isRefetching} onRefresh={refetch} />
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  tabContainer: {
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  listContent: {
    padding: 16,
  },
});
