import { useState } from 'react';
import { supabase } from '../lib/supabase';
import * as ImageManipulator from 'expo-image-manipulator';

const MAX_IMAGE_SIZE = 1024 * 1024; // 1MB
const MAX_IMAGE_DIMENSION = 1200;

interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

export function useImageUpload() {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState<UploadProgress | null>(null);
  const [error, setError] = useState<string | null>(null);

  const compressImage = async (uri: string): Promise<string> => {
    const manipResult = await ImageManipulator.manipulateAsync(
      uri,
      [
        {
          resize: {
            width: MAX_IMAGE_DIMENSION,
          },
        },
      ],
      {
        compress: 0.7,
        format: ImageManipulator.SaveFormat.JPEG,
      }
    );

    return manipResult.uri;
  };

  const uploadImage = async (
    uri: string,
    bucket: string = 'avatars',
    folder: string = 'uploads'
  ): Promise<string | null> => {
    setUploading(true);
    setError(null);
    setProgress({ loaded: 0, total: 100, percentage: 0 });

    try {
      // Compress image
      const compressedUri = await compressImage(uri);

      // Convert to blob
      const response = await fetch(compressedUri);
      const blob = await response.blob();

      // Generate unique filename
      const fileExt = uri.split('.').pop() || 'jpg';
      const fileName = `${folder}/${Date.now()}.${fileExt}`;

      // Upload to Supabase Storage
      const { data, error: uploadError } = await supabase.storage
        .from(bucket)
        .upload(fileName, blob, {
          contentType: `image/${fileExt}`,
          upsert: false,
        });

      if (uploadError) throw uploadError;

      // Get public URL
      const { data: { publicUrl } } = supabase.storage
        .from(bucket)
        .getPublicUrl(data.path);

      setProgress({ loaded: 100, total: 100, percentage: 100 });
      setUploading(false);

      return publicUrl;
    } catch (err: any) {
      setError(err.message || 'Failed to upload image');
      setUploading(false);
      return null;
    }
  };

  return {
    uploadImage,
    uploading,
    progress,
    error,
  };
}
