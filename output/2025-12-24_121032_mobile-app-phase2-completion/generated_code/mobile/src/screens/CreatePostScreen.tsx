import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Image,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { Text, IconButton } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import * as ImagePicker from 'expo-image-picker';
import * as Camera from 'expo-camera';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { useCreatePost } from '../hooks/usePosts';
import { useImageUpload } from '../hooks/useImageUpload';

const MAX_CONTENT_LENGTH = 5000;

export function CreatePostScreen() {
  const navigation = useNavigation();
  const createPostMutation = useCreatePost();
  const { uploadImage, uploading } = useImageUpload();

  const [content, setContent] = useState('');
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [error, setError] = useState('');

  const requestCameraPermission = async () => {
    const { status } = await Camera.requestCameraPermissionsAsync();
    return status === 'granted';
  };

  const requestGalleryPermission = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    return status === 'granted';
  };

  const handlePickImage = async () => {
    const hasPermission = await requestGalleryPermission();
    if (!hasPermission) {
      Alert.alert('Permission required', 'Please grant access to your photo library');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled && result.assets[0]) {
      setImageUri(result.assets[0].uri);
    }
  };

  const handleTakePhoto = async () => {
    const hasPermission = await requestCameraPermission();
    if (!hasPermission) {
      Alert.alert('Permission required', 'Please grant camera access');
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled && result.assets[0]) {
      setImageUri(result.assets[0].uri);
    }
  };

  const handleRemoveImage = () => {
    setImageUri(null);
  };

  const handleSubmit = async () => {
    if (!content.trim()) {
      setError('Please enter some content');
      return;
    }

    if (content.length > MAX_CONTENT_LENGTH) {
      setError(`Content must be less than ${MAX_CONTENT_LENGTH} characters`);
      return;
    }

    setError('');

    try {
      let imageUrl: string | undefined;

      // Upload image if present
      if (imageUri) {
        imageUrl = await uploadImage(imageUri, 'posts', 'images') || undefined;
      }

      // Create post
      await createPostMutation.mutateAsync({
        content: content.trim(),
        imageUrl,
      });

      // Navigate back to feed
      navigation.goBack();
    } catch (err: any) {
      setError(err.message || 'Failed to create post');
    }
  };

  const isSubmitting = createPostMutation.isPending || uploading;

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Input
          label="What's on your mind?"
          value={content}
          onChangeText={setContent}
          placeholder="Share your thoughts..."
          multiline
          numberOfLines={6}
          error={error}
          style={styles.input}
        />

        <View style={styles.characterCount}>
          <Text variant="bodySmall" style={styles.countText}>
            {content.length}/{MAX_CONTENT_LENGTH}
          </Text>
        </View>

        {imageUri && (
          <View style={styles.imageContainer}>
            <Image source={{ uri: imageUri }} style={styles.image} resizeMode="cover" />
            <IconButton
              icon="close-circle"
              size={30}
              iconColor="#ef4444"
              style={styles.removeButton}
              onPress={handleRemoveImage}
              accessibilityLabel="Remove image"
            />
          </View>
        )}

        <View style={styles.actions}>
          <Button
            onPress={handlePickImage}
            variant="outline"
            icon="image"
            disabled={isSubmitting}
          >
            Gallery
          </Button>
          <Button
            onPress={handleTakePhoto}
            variant="outline"
            icon="camera"
            disabled={isSubmitting}
          >
            Camera
          </Button>
        </View>

        <Button
          onPress={handleSubmit}
          loading={isSubmitting}
          disabled={isSubmitting || !content.trim()}
          fullWidth
          size="large"
          style={styles.submitButton}
        >
          {isSubmitting ? 'Posting...' : 'Post'}
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
  input: {
    minHeight: 150,
  },
  characterCount: {
    alignItems: 'flex-end',
    marginTop: 8,
    marginBottom: 16,
  },
  countText: {
    color: '#6b7280',
  },
  imageContainer: {
    position: 'relative',
    marginBottom: 16,
  },
  image: {
    width: '100%',
    height: 300,
    borderRadius: 8,
  },
  removeButton: {
    position: 'absolute',
    top: 8,
    right: 8,
    backgroundColor: '#fff',
  },
  actions: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 24,
  },
  submitButton: {
    marginTop: 8,
  },
});
