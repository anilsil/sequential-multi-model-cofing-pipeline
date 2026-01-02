# Integration Decision - Review and Approve/Reject

You are making the final decision on whether to integrate generated code.

## Original Task Specification
```yaml
task_name: mobile-app-phase2-core-features
objective: Implement core user-facing features including navigation, feed, post creation, profiles, and connections management for TrustLink AI Guardian mobile app
requirements:
  - Implement React Navigation with bottom tab navigator (Feed, Network, Messages, Notifications, Profile)
  - Create stack navigators for detail views with protected route logic
  - Build infinite scroll feed using FlatList with pull-to-refresh
  - Display posts with AI moderation badges and interaction counts
  - Implement post creation with camera/gallery integration and image upload
  - Create user profile screen with stats, trust scores, and edit functionality
  - Build connections management with trust score visualization
  - Develop reusable UI component library (Button, Card, Input, Avatar, Badge)
  - Implement optimistic updates for user actions
  - Support offline-first functionality where applicable
  - Ensure accessibility compliance (labels, roles, touch targets)
  - Maintain TypeScript strict typing throughout
  - Achieve 60fps scrolling performance and <1s navigation transitions
files_to_modify:
  - generated_code/app/_layout.tsx
  - generated_code/app/index.tsx
  - generated_code/contexts/AuthContext.tsx
  - generated_code/package.json
new_files:
  - generated_code/navigation/AppNavigator.tsx
  - generated_code/navigation/AuthNavigator.tsx
  - generated_code/navigation/TabNavigator.tsx
  - generated_code/navigation/types.ts
  - generated_code/screens/FeedScreen.tsx
  - generated_code/screens/NetworkScreen.tsx
  - generated_code/screens/MessagesScreen.tsx
  - generated_code/screens/NotificationsScreen.tsx
  - generated_code/screens/ProfileScreen.tsx
  - generated_code/screens/PostDetailScreen.tsx
  - generated_code/screens/CreatePostScreen.tsx
  - generated_code/screens/EditProfileScreen.tsx
  - generated_code/screens/ConnectionRequestsScreen.tsx
  - generated_code/components/ui/Button.tsx
  - generated_code/components/ui/Card.tsx
  - generated_code/components/ui/Input.tsx
  - generated_code/components/ui/Avatar.tsx
  - generated_code/components/ui/Badge.tsx
  - generated_code/components/ui/LoadingSkeleton.tsx
  - generated_code/components/PostCard.tsx
  - generated_code/components/ConnectionCard.tsx
  - generated_code/components/ProfileHeader.tsx
  - generated_code/components/TrustScoreBadge.tsx
  - generated_code/components/ImagePicker.tsx
  - generated_code/hooks/usePosts.ts
  - generated_code/hooks/useConnections.ts
  - generated_code/hooks/useProfile.ts
  - generated_code/hooks/useImageUpload.ts
  - generated_code/hooks/useInfiniteScroll.ts
  - generated_code/services/posts.ts
  - generated_code/services/connections.ts
  - generated_code/services/storage.ts
  - generated_code/types/posts.ts
  - generated_code/types/connections.ts
  - generated_code/types/profile.ts
  - generated_code/utils/imageCompression.ts
  - generated_code/utils/permissions.ts
  - generated_code/__tests__/hooks/usePosts.test.ts
  - generated_code/__tests__/hooks/useConnections.test.ts
  - generated_code/__tests__/components/Button.test.tsx
  - generated_code/__tests__/components/PostCard.test.tsx
  - generated_code/__tests__/screens/FeedScreen.test.tsx
  - generated_code/__tests__/integration/postCreation.test.tsx
  - generated_code/__tests__/integration/connectionRequest.test.tsx
implementation_steps:
  - "Step 1: Install dependencies - Add @react-navigation/native, @react-navigation/bottom-tabs, @react-navigation/native-stack, react-native-paper, expo-camera, expo-image-picker, expo-image-manipulator, @tanstack/react-query to package.json"
  - "Step 2: Create navigation type definitions in navigation/types.ts with proper TypeScript types for all screen params"
  - "Step 3: Implement AuthNavigator with login/signup screens and navigation logic in navigation/AuthNavigator.tsx"
  - "Step 4: Create TabNavigator with bottom tabs (Feed, Network, Messages, Notifications, Profile) in navigation/TabNavigator.tsx"
  - "Step 5: Build AppNavigator with stack navigators for detail views and protected route logic in navigation/AppNavigator.tsx"
  - "Step 6: Update app/_layout.tsx to integrate navigation system with AuthContext"
  - "Step 7: Create UI component library - Button.tsx with variants (primary, secondary, ghost) and loading states"
  - "Step 8: Create UI components - Card.tsx with elevation and press states"
  - "Step 9: Create UI components - Input.tsx with error states and validation feedback"
  - "Step 10: Create UI components - Avatar.tsx with image loading and fallback initials"
  - "Step 11: Create UI components - Badge.tsx for trust scores and moderation indicators"
  - "Step 12: Create LoadingSkeleton.tsx for feed loading states"
  - "Step 13: Define post types in types/posts.ts matching Supabase schema"
  - "Step 14: Create posts service in services/posts.ts with fetchPosts, createPost, likePost functions"
  - "Step 15: Implement usePosts hook with React Query for infinite scroll and optimistic updates"
  - "Step 16: Create useInfiniteScroll hook for FlatList pagination"
  - "Step 17: Build TrustScoreBadge component with color-coded trust score display"
  - "Step 18: Create PostCard component with AI badges, interaction buttons, and press handlers"
  - "Step 19: Implement FeedScreen with FlatList, pull-to-refresh, infinite scroll, and loading skeletons"
  - "Step 20: Create PostDetailScreen with comments section and full post view"
  - "Step 21: Implement permissions utility in utils/permissions.ts for camera and media library"
  - "Step 22: Create imageCompression utility using expo-image-manipulator for optimizing uploads"
  - "Step 23: Build ImagePicker component with camera/gallery selection and preview"
  - "Step 24: Create storage service in services/storage.ts for Supabase Storage uploads with progress tracking"
  - "Step 25: Implement useImageUpload hook with compression and upload progress"
  - "Step 26: Build CreatePostScreen with text input, image picker, upload progress, and validation"
  - "Step 27: Define profile and connection types in types/profile.ts and types/connections.ts"
  - "Step 28: Create connections service in services/connections.ts with fetchConnections, sendRequest, acceptRequest, rejectRequest functions"
  - "Step 29: Implement useConnections hook with React Query and optimistic updates"
  - "Step 30: Create useProfile hook for fetching and updating user profiles"
  - "Step 31: Build ProfileHeader component with avatar, stats, edit button, and trust score"
  - "Step 32: Create ProfileScreen with user posts grid, connections list, and stats display"
  - "Step 33: Implement EditProfileScreen with form validation and image upload"
  - "Step 34: Build ConnectionCard component with trust score visualization and action buttons"
  - "Step 35: Create NetworkScreen with connections list and search functionality"
  - "Step 36: Implement ConnectionRequestsScreen with pending requests and accept/reject actions"
  - "Step 37: Create placeholder MessagesScreen and NotificationsScreen (basic UI, full functionality in Phase 3)"
  - "Step 38: Add error boundaries and error handling to all screens"
  - "Step 39: Implement offline-first caching strategy using React Query's cache persistence"
  - "Step 40: Add accessibility labels and roles to all interactive components"
testing_requirements:
  - Unit test usePosts hook with mocked Supabase client - test fetch, create, like, optimistic updates
  - Unit test useConnections hook - test fetch, send request, accept, reject, optimistic updates
  - Unit test useImageUpload hook - test compression, upload, progress tracking, error handling
  - Component test Button - test variants, loading states, disabled states, onPress callbacks
  - Component test PostCard - test rendering post data, AI badges, interaction buttons, press handlers
  - Component test ConnectionCard - test trust score colors, action buttons, mutual connections
  - Screen test FeedScreen - test infinite scroll, pull-to-refresh, loading states, empty states
  - Integration test post creation flow - camera permission → image capture → compression → upload → post creation
  - Integration test connection request flow - send request → pending state → accept/reject → update UI
  - Test camera and media library permissions handling with denied/granted scenarios
  - Test image compression reduces file size by at least 50% while maintaining quality
  - Test navigation between all screens without memory leaks
  - Test accessibility with screen reader - all buttons and inputs have proper labels
  - Performance test - FeedScreen maintains 60fps while scrolling through 100+ posts
  - Snapshot tests for all UI components to catch unintended visual regressions
constraints:
  - Do NOT modify Supabase schema or backend - use existing tables (profiles, posts, ai_post_analysis, connections, trust_scores)
  - Do NOT break Phase 1 code - extend existing AuthContext, supabaseClient, theme without modifying core logic
  - Do NOT install unnecessary dependencies - reuse React Native Paper components where possible
  - Follow existing TypeScript patterns from Phase 1 - strict typing, no any types
  - Use FlatList (not ScrollView) for all lists to ensure performance
  - Implement proper cleanup in useEffect hooks to prevent memory leaks
  - Keep bundle size under 50MB - use lazy loading for images and screens
  - Follow React Native performance best practices - memoize components, use React.memo, useMemo, useCallback
  - Ensure all images are compressed before upload - max 2MB per image
  - Use existing theme colors and spacing from theme/index.ts
  - Follow accessibility guidelines - minimum touch target 44x44, proper contrast ratios
  - Add proper error handling for all async operations - network errors, permission denials, validation errors
  - Use Supabase RLS policies for security - no client-side authorization checks
  - Test on both iOS and Android before finalizing
```

## Verification Findings
Code implemented by Codex CLI (verification skipped - no critical findings)

## Your Decision
Review the verification findings and decide:

1. **APPROVE** - Code meets quality standards, safe to integrate
2. **REJECT** - Critical issues found, must fix before integration
3. **APPROVE_WITH_NOTES** - Minor issues, can integrate with documented caveats

## Required Output Format (YAML)
```yaml
decision: APPROVE | REJECT | APPROVE_WITH_NOTES
rationale: |
  Clear explanation of why you made this decision.
  Reference specific findings.
  Explain risk assessment.

required_fixes:  # Only if REJECT
  - Fix 1
  - Fix 2

recommended_improvements:  # Optional enhancements
  - Improvement 1
  - Improvement 2

integration_notes:  # Important caveats or follow-up items
  - Note 1
  - Note 2
```

## Decision Criteria
- **HIGH severity issues** → Likely REJECT
- **Multiple MEDIUM issues** → Carefully evaluate
- **Only LOW issues** → Likely APPROVE or APPROVE_WITH_NOTES
- **Security vulnerabilities** → Always REJECT until fixed
- **Logic errors** → REJECT
- **Style/minor issues** → APPROVE_WITH_NOTES

**Output ONLY the YAML decision (no markdown code blocks, no explanations):**
