import React from 'react';
import { Avatar as PaperAvatar } from 'react-native-paper';
import { StyleSheet, View } from 'react-native';

interface AvatarProps {
  imageUrl?: string | null;
  name?: string;
  size?: 'small' | 'medium' | 'large';
}

export function Avatar({ imageUrl, name, size = 'medium' }: AvatarProps) {
  const getSize = () => {
    switch (size) {
      case 'small':
        return 32;
      case 'large':
        return 80;
      default:
        return 48;
    }
  };

  const getInitials = () => {
    if (!name) return '?';
    const parts = name.trim().split(' ');
    if (parts.length >= 2) {
      return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
  };

  const avatarSize = getSize();

  if (imageUrl) {
    return (
      <View style={styles.container} accessible accessibilityLabel={`Profile picture of ${name || 'user'}`}>
        <PaperAvatar.Image
          size={avatarSize}
          source={{ uri: imageUrl }}
        />
      </View>
    );
  }

  return (
    <View style={styles.container} accessible accessibilityLabel={`${name || 'User'}'s initials`}>
      <PaperAvatar.Text
        size={avatarSize}
        label={getInitials()}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    justifyContent: 'center',
    alignItems: 'center',
  },
});
