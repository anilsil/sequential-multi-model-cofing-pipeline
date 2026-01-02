import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface BadgeProps {
  label: string;
  variant?: 'success' | 'warning' | 'error' | 'info';
  size?: 'small' | 'medium';
}

export function Badge({ label, variant = 'info', size = 'medium' }: BadgeProps) {
  const getColor = () => {
    switch (variant) {
      case 'success':
        return { bg: '#D1FAE5', text: '#065F46' }; // green
      case 'warning':
        return { bg: '#FEF3C7', text: '#92400E' }; // yellow
      case 'error':
        return { bg: '#FEE2E2', text: '#991B1B' }; // red
      default:
        return { bg: '#DBEAFE', text: '#1E40AF' }; // blue
    }
  };

  const colors = getColor();
  const sizeStyle = size === 'small' ? styles.small : styles.medium;

  return (
    <View
      style={[
        styles.badge,
        sizeStyle,
        { backgroundColor: colors.bg },
      ]}
      accessible
      accessibilityLabel={`${variant} badge: ${label}`}
    >
      <Text style={[styles.text, { color: colors.text }]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
    alignSelf: 'flex-start',
  },
  small: {
    paddingHorizontal: 6,
    paddingVertical: 2,
  },
  medium: {
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  text: {
    fontSize: 12,
    fontWeight: '600',
  },
});
