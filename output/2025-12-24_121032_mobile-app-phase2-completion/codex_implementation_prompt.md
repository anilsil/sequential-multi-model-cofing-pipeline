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
task_name: trustlink-mobile-phase2-completion
objective: Complete remaining 30% of Phase 2 by implementing core screens, components, and hooks for TrustLink mobile app
requirements:
  - Implement FeedScreen with infinite scroll using existing usePosts hook
  - Create PostCard component displaying post content, author info, AI scores, and trust indicators
  - Build CreatePostScreen with image upload functionality using expo-image-picker and expo-camera
  - Implement ProfileScreen showing user info, stats, AI metrics, and posts list
  - Create EditProfileScreen with form validation and avatar upload
  - Build ConnectionsScreen with tab switching for connections and requests
  - Create ConnectionCard component with trust score display and action buttons
  - Implement OnboardingScreen with multi-step form and progress indicator
  - Create placeholder screens for Network, Messages, and Notifications
  - Build useProfile hook for fetching user profiles from Supabase
  - Build useUpdateProfile mutation hook with avatar upload to Supabase Storage
  - Build useConnections hook for fetching connections with status filtering
  - Build useImageUpload utility hook for compression and upload to Supabase Storage
  - All implementations must use existing UI components from Phase 2 foundation
  - Maintain TypeScript strict typing throughout
  - Implement optimistic UI updates for mutations
  - Support both iOS and Android platforms
  - Include proper accessibility labels and minimum 44pt touch targets
  - Handle loading states, error states, and empty states consistently
files_to_modify:
  - mobile/package.json
new_files:
  - mobile/src/screens/FeedScreen.tsx
  - mobile/src/screens/CreatePostScreen.tsx
  - mobile/src/screens/ProfileScreen.tsx
  - mobile/src/screens/EditProfileScreen.tsx
  - mobile/src/screens/ConnectionsScreen.tsx
  - mobile/src/screens/OnboardingScreen.tsx
  - mobile/src/screens/NetworkScreen.tsx
  - mobile/src/screens/MessagesScreen.tsx
  - mobile/src/screens/NotificationsScreen.tsx
  - mobile/src/components/PostCard.tsx
  - mobile/src/components/ConnectionCard.tsx
  - mobile/src/hooks/useProfile.tsx
  - mobile/src/hooks/useUpdateProfile.tsx
  - mobile/src/hooks/useConnections.tsx
  - mobile/src/hooks/useImageUpload.tsx
implementation_steps:
  - Step 1: Add new dependencies to package.json (expo-camera, expo-image-picker, expo-image-manipulator if not present)
  - Step 2: Create useProfile hook querying Supabase profiles table by userId with TanStack Query
  - Step 3: Create useConnections hook querying Supabase connections table with status filtering
  - Step 4: Create useImageUpload hook with compression logic and Supabase Storage upload functionality
  - Step 5: Create useUpdateProfile mutation hook with avatar upload integration
  - Step 6: Implement PostCard component with all UI elements (avatar, content, images, AI badges, trust score, action buttons)
  - Step 7: Integrate useLikePost hook in PostCard for optimistic like updates
  - Step 8: Implement ConnectionCard component with trust score display and conditional action buttons
  - Step 9: Create FeedScreen with FlatList, infinite scroll using usePosts onEndReached, RefreshControl, and floating action button
  - Step 10: Build CreatePostScreen with multiline Input, image picker integration, preview, useCreatePost submission
  - Step 11: Implement ProfileScreen with conditional rendering for current user vs other users, stats display, posts FlatList
  - Step 12: Create EditProfileScreen with form inputs for all profile fields and avatar picker
  - Step 13: Build ConnectionsScreen with tab switching between My Connections and Requests using React Navigation Material Top Tabs or custom tabs
  - Step 14: Implement OnboardingScreen with multi-step form flow and progress indicator
  - Step 15: Create placeholder screens for NetworkScreen, MessagesScreen, NotificationsScreen with basic structure
  - Step 16: Test all screens integrate correctly with existing TabNavigator and navigation types
  - Step 17: Verify all components use existing UI library components (Button, Card, Avatar, Badge, Input, LoadingSpinner, EmptyState)
  - Step 18: Test image upload flow end-to-end on both iOS and Android
  - Step 19: Verify optimistic updates work correctly for likes and post creation
  - Step 20: Test accessibility with screen reader and verify touch target sizes
testing_requirements:
  - Verify FeedScreen renders posts using usePosts hook and displays loading/empty states correctly
  - Test infinite scroll triggers data fetching when scrolling near end of list
  - Verify pull-to-refresh refetches posts data
  - Test PostCard displays all post properties correctly including AI scores and trust indicators
  - Verify like button triggers optimistic update and calls useLikePost hook
  - Test CreatePostScreen image picker opens camera and gallery on respective actions
  - Verify CreatePostScreen validates non-empty content before submission
  - Test post creation navigates back to feed and new post appears at top
  - Verify ProfileScreen displays correct data for current user and other users
  - Test ProfileScreen shows edit button only for current user
  - Verify EditProfileScreen saves changes and updates profile data
  - Test ConnectionsScreen displays connections from useConnections hook
  - Verify ConnectionCard shows correct trust score colors (green high, yellow medium, red low)
  - Test OnboardingScreen navigates through all steps and submits on final step
  - Verify all placeholder screens render without errors
  - Test navigation between all screens works correctly
  - Verify TypeScript compilation succeeds with no errors
  - Test on both iOS and Android platforms for platform-specific issues
  - Verify all interactive elements have minimum 44pt touch targets
  - Test with VoiceOver (iOS) and TalkBack (Android) screen readers
constraints:
  - Do NOT modify existing navigation setup from Phase 2 foundation (RootNavigator, TabNavigator, AuthNavigator)
  - Do NOT modify existing UI components in src/components/ui directory
  - Do NOT modify existing hooks (usePosts, useLikePost, useCreatePost)
  - Do NOT change navigation types or add new navigation stacks
  - Follow existing TypeScript patterns and type definitions from Phase 2
  - Use pathlib.Path patterns from Python codebase do NOT apply here - use standard TypeScript file paths
  - Do NOT introduce new state management libraries beyond TanStack Query and React Context
  - Follow React Native best practices for FlatList optimization (keyExtractor, getItemLayout if possible)
  - Use existing Supabase client configuration from src/services/supabase.ts
  - Use existing AuthContext for current user access
  - Follow existing code style matching Phase 2 foundation files
  - Maintain consistent error handling patterns across all hooks
  - Do NOT implement real-time features (messaging, notifications) - use placeholders only
  - Keep image uploads under 1MB after compression
  - Do NOT add analytics or tracking code
  - Do NOT implement complex animations in this phase

## REPOSITORY CONTEXT:
## Repository Analysis

**Primary Language**: Python 3.11+ (requires modern type hints)

**Project Type**: CLI tool (command-line interface) for orchestrating multi-agent AI workflows

**Key Frameworks**:
- **Typer**: CLI framework with type-safe argument parsing
- **Rich**: Terminal formatting (colors, panels, tables, progress)
- **Pydantic v2**: Configuration validation and data modeling
- **PyYAML**: YAML parsing for task specifications and responses
- **Anthropic SDK** & **Google Generative AI**: Optional for automated mode

**Code Organization**:
- `agentic_code/` - Main package directory
  - `cli.py` - Typer CLI entry point
  - `pipeline.py` - Orchestrates 5-stage workflow (prompt-based)
  - `automated_pipeline.py` - Automated execution variant
  - `config.py` - Pydantic configuration model
  - `utils.py` - File I/O, user interaction, Rich formatting helpers
  - `agents/` - Agent implementations (claude.py, codex.py, gemini.py)
- `examples/` - Task specification examples (.md, .y

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
