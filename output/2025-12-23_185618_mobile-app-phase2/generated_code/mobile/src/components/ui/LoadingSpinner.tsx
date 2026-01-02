import React from 'react';
import { ActivityIndicator } from 'react-native-paper';
import { View, StyleSheet } from 'react-native';
import { theme } from '../../theme';

interface LoadingSpinnerProps {
  size?: 'small' | 'large';
  overlay?: boolean;
}

export function LoadingSpinner({ size = 'large', overlay = false }: LoadingSpinnerProps) {
  if (overlay) {
    return (
      <View style={styles.overlay}>
        <ActivityIndicator
          size={size}
          color={theme.colors.primary}
          accessibilityLabel="Loading"
        />
      </View>
    );
  }

  return (
    <View style={styles.inline}>
      <ActivityIndicator
        size={size}
        color={theme.colors.primary}
        accessibilityLabel="Loading"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  inline: {
    padding: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
