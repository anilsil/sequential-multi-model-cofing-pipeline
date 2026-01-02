import React from 'react';
import { TextInput } from 'react-native-paper';
import { StyleSheet, View, Text } from 'react-native';

interface InputProps {
  label: string;
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
  error?: string;
  helperText?: string;
  secureTextEntry?: boolean;
  multiline?: boolean;
  numberOfLines?: number;
  maxLength?: number;
  keyboardType?: 'default' | 'email-address' | 'numeric' | 'phone-pad';
  autoCapitalize?: 'none' | 'sentences' | 'words' | 'characters';
  disabled?: boolean;
}

export function Input({
  label,
  value,
  onChangeText,
  placeholder,
  error,
  helperText,
  secureTextEntry = false,
  multiline = false,
  numberOfLines = 1,
  maxLength,
  keyboardType = 'default',
  autoCapitalize = 'sentences',
  disabled = false,
}: InputProps) {
  return (
    <View style={styles.container}>
      <TextInput
        label={label}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        error={!!error}
        secureTextEntry={secureTextEntry}
        multiline={multiline}
        numberOfLines={multiline ? numberOfLines : undefined}
        maxLength={maxLength}
        keyboardType={keyboardType}
        autoCapitalize={autoCapitalize}
        disabled={disabled}
        mode="outlined"
        style={[styles.input, multiline && styles.multiline]}
        accessibilityLabel={label}
        accessibilityHint={helperText || error}
      />
      {error && <Text style={styles.errorText}>{error}</Text>}
      {!error && helperText && <Text style={styles.helperText}>{helperText}</Text>}
      {maxLength && (
        <Text style={styles.counter}>
          {value.length}/{maxLength}
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 8,
    minHeight: 44, // Minimum touch target
  },
  input: {
    backgroundColor: '#FFFFFF',
  },
  multiline: {
    minHeight: 100,
  },
  errorText: {
    color: '#EF4444',
    fontSize: 12,
    marginTop: 4,
    marginLeft: 12,
  },
  helperText: {
    color: '#64748B',
    fontSize: 12,
    marginTop: 4,
    marginLeft: 12,
  },
  counter: {
    color: '#64748B',
    fontSize: 12,
    textAlign: 'right',
    marginTop: 4,
    marginRight: 12,
  },
});
