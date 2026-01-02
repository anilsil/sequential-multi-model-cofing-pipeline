import React from 'react';
import { Card as PaperCard } from 'react-native-paper';
import { StyleSheet, TouchableOpacity, View } from 'react-native';

interface CardProps {
  children: React.ReactNode;
  onPress?: () => void;
  elevation?: number;
  padding?: 'none' | 'small' | 'medium' | 'large';
}

export function Card({
  children,
  onPress,
  elevation = 2,
  padding = 'medium',
}: CardProps) {
  const getPaddingStyle = () => {
    switch (padding) {
      case 'none':
        return styles.paddingNone;
      case 'small':
        return styles.paddingSmall;
      case 'large':
        return styles.paddingLarge;
      default:
        return styles.paddingMedium;
    }
  };

  const content = (
    <View style={getPaddingStyle()}>
      {children}
    </View>
  );

  if (onPress) {
    return (
      <PaperCard
        elevation={elevation}
        style={styles.card}
        accessibilityRole="button"
      >
        <TouchableOpacity onPress={onPress} activeOpacity={0.7}>
          {content}
        </TouchableOpacity>
      </PaperCard>
    );
  }

  return (
    <PaperCard elevation={elevation} style={styles.card}>
      {content}
    </PaperCard>
  );
}

const styles = StyleSheet.create({
  card: {
    marginVertical: 6,
    marginHorizontal: 12,
  },
  paddingNone: {
    padding: 0,
  },
  paddingSmall: {
    padding: 8,
  },
  paddingMedium: {
    padding: 16,
  },
  paddingLarge: {
    padding: 24,
  },
});
