import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  TouchableOpacity,
  Image,
  Alert,
} from 'react-native';
import { Text } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import * as ImagePicker from 'expo-image-picker';
import { Avatar } from '../components/ui/Avatar';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { useAuth } from '../contexts/AuthContext';
import { useProfile } from '../hooks/useProfile';
import { useUpdateProfile } from '../hooks/useUpdateProfile';

export function EditProfileScreen() {
  const navigation = useNavigation();
  const { user } = useAuth();
  const { data: profile } = useProfile(user?.id || '');
  const updateProfileMutation = useUpdateProfile();

  const [fullName, setFullName] = useState('');
  const [bio, setBio] = useState('');
  const [industry, setIndustry] = useState('');
  const [location, setLocation] = useState('');
  const [avatarUri, setAvatarUri] = useState<string | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (profile) {
      setFullName(profile.full_name || '');
      setBio(profile.bio || '');
      setIndustry(profile.industry || '');
      setLocation(profile.location || '');
    }
  }, [profile]);

  const requestGalleryPermission = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    return status === 'granted';
  };

  const handlePickAvatar = async () => {
    const hasPermission = await requestGalleryPermission();
    if (!hasPermission) {
      Alert.alert('Permission required', 'Please grant access to your photo library');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.8,
    });

    if (!result.canceled && result.assets[0]) {
      setAvatarUri(result.assets[0].uri);
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!fullName.trim()) {
      newErrors.fullName = 'Name is required';
    }

    if (bio.length > 500) {
      newErrors.bio = 'Bio must be less than 500 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    if (!validateForm()) {
      return;
    }

    try {
      await updateProfileMutation.mutateAsync({
        full_name: fullName.trim(),
        bio: bio.trim(),
        industry: industry.trim(),
        location: location.trim(),
        avatarUri: avatarUri || undefined,
      });

      navigation.goBack();
    } catch (err: any) {
      Alert.alert('Error', err.message || 'Failed to update profile');
    }
  };

  const currentAvatarUrl = avatarUri || profile?.avatar_url;

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.avatarSection}>
          {currentAvatarUrl ? (
            <Image source={{ uri: currentAvatarUrl }} style={styles.avatarImage} />
          ) : (
            <Avatar name={fullName} size="xlarge" />
          )}
          <Button
            onPress={handlePickAvatar}
            variant="outline"
            size="small"
            style={styles.changeAvatarButton}
          >
            Change Photo
          </Button>
        </View>

        <Input
          label="Full Name *"
          value={fullName}
          onChangeText={setFullName}
          placeholder="John Doe"
          error={errors.fullName}
        />

        <Input
          label="Bio"
          value={bio}
          onChangeText={setBio}
          placeholder="Tell us about yourself..."
          multiline
          numberOfLines={4}
          error={errors.bio}
        />

        <View style={styles.characterCount}>
          <Text variant="bodySmall" style={styles.countText}>
            {bio.length}/500
          </Text>
        </View>

        <Input
          label="Industry"
          value={industry}
          onChangeText={setIndustry}
          placeholder="Technology, Healthcare, etc."
        />

        <Input
          label="Location"
          value={location}
          onChangeText={setLocation}
          placeholder="San Francisco, CA"
        />

        <Button
          onPress={handleSave}
          loading={updateProfileMutation.isPending}
          disabled={updateProfileMutation.isPending}
          fullWidth
          size="large"
          style={styles.saveButton}
        >
          Save Changes
        </Button>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  scrollContent: {
    padding: 16,
  },
  avatarSection: {
    alignItems: 'center',
    marginBottom: 24,
  },
  avatarImage: {
    width: 120,
    height: 120,
    borderRadius: 60,
    marginBottom: 12,
  },
  changeAvatarButton: {
    marginTop: 8,
  },
  characterCount: {
    alignItems: 'flex-end',
    marginTop: -8,
    marginBottom: 12,
  },
  countText: {
    color: '#6b7280',
  },
  saveButton: {
    marginTop: 24,
  },
});
