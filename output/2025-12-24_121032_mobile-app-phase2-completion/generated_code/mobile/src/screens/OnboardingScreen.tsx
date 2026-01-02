import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { Text, ProgressBar } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { useUpdateProfile } from '../hooks/useUpdateProfile';

const TOTAL_STEPS = 3;

export function OnboardingScreen() {
  const navigation = useNavigation();
  const updateProfileMutation = useUpdateProfile();

  const [currentStep, setCurrentStep] = useState(1);
  const [fullName, setFullName] = useState('');
  const [industry, setIndustry] = useState('');
  const [location, setLocation] = useState('');
  const [bio, setBio] = useState('');
  const [skills, setSkills] = useState('');
  const [interests, setInterests] = useState('');

  const progress = currentStep / TOTAL_STEPS;

  const handleNext = () => {
    if (currentStep < TOTAL_STEPS) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSkip = () => {
    // Skip onboarding and go to main app
    navigation.reset({
      index: 0,
      routes: [{ name: 'Main' }],
    });
  };

  const handleFinish = async () => {
    try {
      await updateProfileMutation.mutateAsync({
        full_name: fullName,
        industry,
        location,
        bio,
        skills: skills ? skills.split(',').map(s => s.trim()) : undefined,
      });

      // Navigate to main app
      navigation.reset({
        index: 0,
        routes: [{ name: 'Main' }],
      });
    } catch (err) {
      console.error('Failed to save profile:', err);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <View>
            <Text variant="headlineMedium" style={styles.stepTitle}>
              Tell us about yourself
            </Text>
            <Text variant="bodyMedium" style={styles.stepDescription}>
              Let's start with the basics
            </Text>

            <Input
              label="Full Name *"
              value={fullName}
              onChangeText={setFullName}
              placeholder="John Doe"
            />

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
          </View>
        );

      case 2:
        return (
          <View>
            <Text variant="headlineMedium" style={styles.stepTitle}>
              What are your skills?
            </Text>
            <Text variant="bodyMedium" style={styles.stepDescription}>
              Add skills that you want to showcase
            </Text>

            <Input
              label="Skills"
              value={skills}
              onChangeText={setSkills}
              placeholder="JavaScript, React, Node.js (comma separated)"
              multiline
              numberOfLines={3}
            />

            <Input
              label="Bio"
              value={bio}
              onChangeText={setBio}
              placeholder="Tell us about yourself..."
              multiline
              numberOfLines={4}
            />
          </View>
        );

      case 3:
        return (
          <View>
            <Text variant="headlineMedium" style={styles.stepTitle}>
              What interests you?
            </Text>
            <Text variant="bodyMedium" style={styles.stepDescription}>
              Help us personalize your experience
            </Text>

            <Input
              label="Interests"
              value={interests}
              onChangeText={setInterests}
              placeholder="AI, Startups, Remote Work (comma separated)"
              multiline
              numberOfLines={3}
            />

            <View style={styles.summary}>
              <Text variant="titleMedium" style={styles.summaryTitle}>
                Your Profile Summary
              </Text>
              <Text variant="bodyMedium">Name: {fullName || 'Not set'}</Text>
              <Text variant="bodyMedium">Industry: {industry || 'Not set'}</Text>
              <Text variant="bodyMedium">Location: {location || 'Not set'}</Text>
            </View>
          </View>
        );

      default:
        return null;
    }
  };

  const canProceed = () => {
    if (currentStep === 1) {
      return fullName.trim().length > 0;
    }
    return true;
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <View style={styles.header}>
        <ProgressBar progress={progress} style={styles.progressBar} />
        <Text variant="bodySmall" style={styles.stepIndicator}>
          Step {currentStep} of {TOTAL_STEPS}
        </Text>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {renderStep()}
      </ScrollView>

      <View style={styles.footer}>
        <View style={styles.actions}>
          {currentStep > 1 && (
            <Button onPress={handleBack} variant="outline" style={{ flex: 1 }}>
              Back
            </Button>
          )}

          {currentStep < TOTAL_STEPS ? (
            <Button
              onPress={handleNext}
              disabled={!canProceed()}
              style={{ flex: 1 }}
            >
              Next
            </Button>
          ) : (
            <Button
              onPress={handleFinish}
              loading={updateProfileMutation.isPending}
              disabled={updateProfileMutation.isPending || !canProceed()}
              style={{ flex: 1 }}
            >
              Finish
            </Button>
          )}
        </View>

        <Button onPress={handleSkip} variant="outline" fullWidth style={styles.skipButton}>
          Skip for now
        </Button>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    padding: 16,
    paddingTop: 24,
  },
  progressBar: {
    height: 6,
    borderRadius: 3,
  },
  stepIndicator: {
    marginTop: 8,
    color: '#6b7280',
    textAlign: 'center',
  },
  scrollContent: {
    padding: 16,
    flexGrow: 1,
  },
  stepTitle: {
    marginBottom: 8,
    fontWeight: 'bold',
  },
  stepDescription: {
    marginBottom: 24,
    color: '#6b7280',
  },
  summary: {
    backgroundColor: '#f9fafb',
    padding: 16,
    borderRadius: 8,
    marginTop: 16,
  },
  summaryTitle: {
    marginBottom: 12,
    fontWeight: 'bold',
  },
  footer: {
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
  actions: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 12,
  },
  skipButton: {
    marginTop: 4,
  },
});
