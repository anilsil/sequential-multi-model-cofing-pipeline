# Implementation Task

You are an implementation agent. Your ONLY job is to write clean, working code based on the specification.

## STRICT RULES:
1. Follow the task specification EXACTLY.
2. Follow existing repository patterns.
3. NO new dependencies unless specified.
4. Add tests for all new functionality.
5. Output code in the specified format ONLY.
6. DO NOT write any explanations or conversational text.

## TASK SPECIFICATION:
task_name: mobile-app-phase2-core-features
objective: Implement core mobile app features including navigation, feed with posts, post creation with camera, user profiles, and connections management
requirements:
  - Implement React Navigation with bottom tab and stack navigators
  - Create Feed screen with infinite scroll FlatList pulling posts from Supabase
  - Add post creation modal with camera capture and gallery selection using expo-camera and expo-image-picker
  - Build user profile screen displaying posts, connections, AI trust scores, and moderation metrics
  - Implement connections management with request sending, accepting, and rejecting
  - Create reusable UI component library with Button, Card, Input, Avatar, Badge components
  - Add pull-to-refresh and optimistic updates for better UX
  - Upload images to Supabase Storage with compression and progress indicators
  - Display AI moderation badges on posts
  - Show trust score visualizations with colors and badges
  - Support offline-first where applicable
  - Maintain TypeScript strict typing throughout
  - Ensure accessibility with proper labels, roles, and touch targets
  - Achieve 60fps scrolling and sub-1s navigation transitions

files_to_modify:
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/package.json
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/app/_layout.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/tsconfig.json

new_files:
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/app/(tabs)/_layout.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/app/(tabs)/feed.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/app/(tabs)/network.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/app/(tabs)/messages.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/app/(tabs)/notifications.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/app/(tabs)/profile.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/app/post/create.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/app/post/[id].tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/app/profile/[userId].tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/app/profile/edit.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/ui/Button.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/ui/Card.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/ui/Input.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/ui/Avatar.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/ui/Badge.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/ui/LoadingSkeleton.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/feed/PostCard.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/feed/PostList.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/feed/AIModerationBadge.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/post/PostComposer.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/post/ImagePicker.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/profile/ProfileHeader.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/profile/ProfileStats.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/profile/TrustScoreDisplay.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/connections/ConnectionCard.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/connections/ConnectionList.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/components/connections/ConnectionRequest.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/hooks/usePosts.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/hooks/useConnections.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/hooks/useProfile.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/hooks/useImageUpload.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/hooks/useInfiniteScroll.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/services/posts.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/services/connections.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/services/profiles.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/services/storage.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/utils/imageCompression.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/utils/trustScoreColors.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/types/post.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/types/connection.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/types/profile.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/__tests__/hooks/usePosts.test.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/__tests__/hooks/useConnections.test.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/__tests__/components/PostCard.test.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/__tests__/components/Button.test.tsx
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/__tests__/integration/postCreation.test.ts
  - /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/__tests__/integration/connectionRequest.test.ts

implementation_steps:
  - Step 1: Install required dependencies - @react-navigation/native, @react-navigation/bottom-tabs, @react-navigation/native-stack, react-native-paper, expo-camera, expo-image-picker, expo-image-manipulator, react-native-safe-area-context, react-native-screens
  - Step 2: Create TypeScript types for Post, Connection, and Profile in types/ directory matching Supabase schema from web app
  - Step 3: Build reusable UI component library - Button, Card, Input, Avatar, Badge, LoadingSkeleton with theme integration and accessibility support
  - Step 4: Implement React Navigation structure with bottom tabs layout in app/(tabs)/_layout.tsx using Expo Router file-based routing
  - Step 5: Create Supabase service modules for posts.ts, connections.ts, profiles.ts, storage.ts with proper error handling
  - Step 6: Implement usePosts hook with infinite scroll, pull-to-refresh, and optimistic updates using React Query or SWR
  - Step 7: Build PostCard component displaying post content, author info, AI moderation badges, and interaction buttons
  - Step 8: Create Feed screen with FlatList, infinite scroll, loading skeletons, and pull-to-refresh functionality
  - Step 9: Implement useImageUpload hook with compression using expo-image-manipulator and Supabase Storage upload with progress
  - Step 10: Build PostComposer component with text input, camera/gallery integration, image preview, and upload progress
  - Step 11: Create post creation screen/modal at app/post/create.tsx with form validation and error handling
  - Step 12: Implement useProfile and useConnections hooks for fetching and mutating user data
  - Step 13: Build ProfileHeader, ProfileStats, and TrustScoreDisplay components with color-coded trust score visualization
  - Step 14: Create profile screen at app/(tabs)/profile.tsx showing user's own profile with posts, connections, and stats
  - Step 15: Implement profile detail screen at app/profile/[userId].tsx for viewing other users' profiles
  - Step 16: Build profile editing screen at app/profile/edit.tsx with image upload and form fields
  - Step 17: Create ConnectionCard, ConnectionList, and ConnectionRequest components for connections UI
  - Step 18: Implement network screen at app/(tabs)/network.tsx showing connections list with trust scores and pending requests
  - Step 19: Add connection request logic to services/connections.ts with accept/reject mutations
  - Step 20: Implement placeholder screens for messages and notifications tabs (basic UI only, no functionality)
  - Step 21: Add navigation guards in app/_layout.tsx to redirect unauthenticated users to login
  - Step 22: Write unit tests for usePosts and useConnections hooks using Jest and React Native Testing Library
  - Step 23: Write component tests for Button, PostCard with snapshot testing and interaction testing
  - Step 24: Create integration tests for post creation flow and connection request flow
  - Step 25: Test camera permissions, image selection, compression, and upload on both iOS and Android
  - Step 26: Perform performance testing - measure FlatList scrolling fps, navigation transition times, and bundle size
  - Step 27: Run accessibility audit using React Native Accessibility tools ensuring all interactive elements have labels

testing_requirements:
  - Unit tests for usePosts hook covering loading states, error handling, infinite scroll, and optimistic updates
  - Unit tests for useConnections hook covering fetching, sending requests, accepting, rejecting
  - Unit tests for useImageUpload hook covering compression, upload progress, error handling
  - Component tests for Button with different variants and states
  - Component tests for PostCard rendering post data, AI badges, interactions
  - Component tests for ConnectionCard showing trust scores and request actions
  - Integration test for complete post creation flow from camera capture to Supabase upload
  - Integration test for connection request flow from sending to accepting on both sides
  - Test camera and gallery permission requests on iOS and Android
  - Test image compression reduces file size while maintaining quality
  - Test FlatList performance with 100+ posts maintaining 60fps
  - Test navigation transitions complete in under 1 second
  - Test accessibility labels on all touchable elements using axe-rn or similar tool
  - Test offline-first functionality where applicable using network mocking
  - Achieve minimum 70% test coverage for new code measured by Jest coverage report

constraints:
  - Do NOT modify Phase 1 foundation files except app/_layout.tsx for navigation integration
  - Do NOT change Supabase schema - use existing tables from web app (profiles, posts, ai_post_analysis, connections, trust_scores)
  - Do NOT add heavy dependencies - keep total bundle size under 50MB
  - Follow TypeScript strict mode - no any types unless absolutely necessary
  - Use pathlib-style imports with @ alias configured in tsconfig.json
  - Follow React Native performance best practices - use React.memo, useMemo, useCallback where appropriate
  - Use FlatList for all scrollable lists, never ScrollView with .map()
  - Implement proper cleanup in useEffect hooks to prevent memory leaks
  - Use React Native Paper components as base for UI library to ensure consistency
  - Follow accessibility guidelines - minimum touch target size 44x44, contrast ratio 4.5:1
  - Use existing theme configuration from Phase 1 without modifications
  - Store all generated code in /Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/ directory
  - Follow snake_case for file names in services/ and utils/, PascalCase for components
  - Use Rich console output formatting in test reporters with color tags like [cyan]text[/cyan]

## REPOSITORY CONTEXT:
Now I have enough context to provide a comprehensive repository analysis.

---

## Repository Analysis

**Primary Language(s)**: Python 3.11+ (100% of codebase)

**Project Type**: CLI tool - A prompt orchestrator for governed multi-agent coding workflows

**Key Frameworks**: 
- **Typer** (CLI interface with type-safe argument parsing)
- **Rich** (terminal formatting with colors, panels, tables)
- **Pydantic v2** (configuration validation using BaseModel)
- **PyYAML** (YAML/JSON task specification parsing)
- **Anthropic & Google GenerativeAI SDKs** (for optional automated mode)

**Code Organization**: 
- `agentic_code/` - Main package with flat structure
  - `cli.py` - Typer CLI entry point
  - `pipeline.py` - Manual prompt orchestration
  - `automated_pipeline.py` - Automated API-based pipeline
  - `config.py` - Pydantic configuration models
  - `utils.py` - File I/O, formatting, user confirmation helpers
  - `agents/` - Specialized agent modules (claude.py, codex.py, gemini.py)
- `exa

## OUTPUT REQUIREMENTS:
You MUST output the code for each file using the following format. Do not add any other text or explanations.

-- FILE: path/to/your/file.py --
```python
# Your code here
```
-- ENDFILE --

-- FILE: path/to/your/test_file.py --
```python
# Your test code here
```
-- ENDFILE --

-- FILE: summary.md --
```markdown
### Implementation Summary
- **Files Created**: `path/to/your/file.py`, `path/to/your/test_file.py`
- **Key Decisions**: Brief explanation of any choices made.
- **How to Run**: Instructions on how to run or test the new code.
```
-- ENDFILE --

BEGIN IMPLEMENTATION NOW.
