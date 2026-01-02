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
objective: Implement navigation, feed, post creation, profiles, and connections management for TrustLink AI Guardian mobile app
requirements:
  - Implement React Navigation with bottom tab navigator (Feed, Network, Messages, Notifications, Profile)
  - Create stack navigators for detail views and authentication flow
  - Build infinite-scroll feed screen with FlatList, pull-to-refresh, and optimistic updates
  - Display posts with AI moderation badges and interaction metrics from Supabase
  - Create post composer with camera integration using expo-camera
  - Support image upload to Supabase Storage with compression and progress tracking
  - Implement user profile screen showing posts, connections, stats, and AI trust scores
  - Add profile editing with profile picture upload from camera/gallery
  - Build connections management with trust score visualization
  - Implement connection request sending, accepting, and rejecting
  - Create reusable UI component library (Button, Card, Input, Avatar, Badge)
  - Use React Native Paper components as base with custom theming
  - Ensure offline-first capability where applicable using AsyncStorage
  - Maintain 60fps scrolling performance and <1s navigation transitions
  - Support both iOS and Android platforms
files_to_modify:
  - generated_code/App.tsx
  - generated_code/app.json
  - generated_code/package.json
  - generated_code/src/contexts/AuthContext.tsx
  - generated_code/src/config/supabase.ts
new_files:
  - generated_code/src/navigation/AppNavigator.tsx
  - generated_code/src/navigation/AuthNavigator.tsx
  - generated_code/src/navigation/TabNavigator.tsx
  - generated_code/src/navigation/types.ts
  - generated_code/src/components/common/Button.tsx
  - generated_code/src/components/common/Card.tsx
  - generated_code/src/components/common/Input.tsx
  - generated_code/src/components/common/Avatar.tsx
  - generated_code/src/components/common/Badge.tsx
  - generated_code/src/components/common/LoadingSkeleton.tsx
  - generated_code/src/components/posts/PostCard.tsx
  - generated_code/src/components/posts/PostComposer.tsx
  - generated_code/src/components/posts/AIBadge.tsx
  - generated_code/src/components/profile/ProfileHeader.tsx
  - generated_code/src/components/profile/ProfileStats.tsx
  - generated_code/src/components/profile/ProfileEditor.tsx
  - generated_code/src/components/connections/ConnectionCard.tsx
  - generated_code/src/components/connections/TrustScoreBadge.tsx
  - generated_code/src/components/connections/ConnectionRequestItem.tsx
  - generated_code/src/screens/FeedScreen.tsx
  - generated_code/src/screens/NetworkScreen.tsx
  - generated_code/src/screens/MessagesScreen.tsx
  - generated_code/src/screens/NotificationsScreen.tsx
  - generated_code/src/screens/ProfileScreen.tsx
  - generated_code/src/screens/PostDetailScreen.tsx
  - generated_code/src/screens/EditProfileScreen.tsx
  - generated_code/src/screens/UserProfileScreen.tsx
  - generated_code/src/hooks/usePosts.ts
  - generated_code/src/hooks/useConnections.ts
  - generated_code/src/hooks/useProfile.ts
  - generated_code/src/hooks/useImageUpload.ts
  - generated_code/src/hooks/useCamera.ts
  - generated_code/src/types/post.ts
  - generated_code/src/types/connection.ts
  - generated_code/src/types/profile.ts
  - generated_code/src/utils/imageCompression.ts
  - generated_code/src/utils/storage.ts
  - generated_code/__tests__/hooks/usePosts.test.ts
  - generated_code/__tests__/hooks/useConnections.test.ts
  - generated_code/__tests__/components/PostCard.test.tsx
  - generated_code/__tests__/components/Button.test.tsx
  - generated_code/__tests__/integration/post-creation.test.tsx
  - generated_code/__tests__/integration/connection-flow.test.tsx
implementation_steps:
  - Step 1: Install required dependencies (react-navigation, react-navigation-bottom-tabs, react-navigation-stack, expo-camera, expo-image-picker, react-native-paper, expo-image-manipulator)
  - Step 2: Create navigation type definitions in src/navigation/types.ts with screen param lists for all navigators
  - Step 3: Build reusable UI components (Button, Card, Input, Avatar, Badge, LoadingSkeleton) in src/components/common/ using React Native Paper as base with theme integration
  - Step 4: Create type definitions for posts, connections, and profiles in src/types/ matching Supabase schema from web app
  - Step 5: Implement TabNavigator with 5 tabs (Feed, Network, Messages, Notifications, Profile) using bottom-tabs navigator with icons and labels
  - Step 6: Create AuthNavigator for login/signup screens using stack navigator
  - Step 7: Build AppNavigator that switches between AuthNavigator and TabNavigator based on authentication state from AuthContext
  - Step 8: Implement usePosts hook with TanStack Query for fetching posts, infinite scroll, and optimistic updates (like, comment, share)
  - Step 9: Create PostCard component displaying post content, author info, AI moderation badge, and interaction buttons with proper accessibility labels
  - Step 10: Build FeedScreen with FlatList, infinite scroll using onEndReached, pull-to-refresh with RefreshControl, and loading skeletons
  - Step 11: Implement useCamera hook wrapping expo-camera with permission handling and camera capture functionality
  - Step 12: Create useImageUpload hook for Supabase Storage upload with compression using expo-image-manipulator and progress tracking
  - Step 13: Build PostComposer modal with text input, camera/gallery picker, image preview, upload progress, and post submission
  - Step 14: Implement useProfile hook for fetching and updating user profiles with TanStack Query mutations
  - Step 15: Create ProfileHeader component showing avatar, name, bio, industry, and trust score badges
  - Step 16: Build ProfileStats component displaying post count, connection count, and AI metrics
  - Step 17: Implement ProfileScreen showing user's posts in FlatList, connections summary, and edit button (own profile only)
  - Step 18: Create ProfileEditor component with form inputs for bio, skills, industry, and profile picture upload from camera/gallery
  - Step 19: Implement useConnections hook for fetching connections, sending requests, and accepting/rejecting requests with TanStack Query
  - Step 20: Create ConnectionCard component showing user info, mutual connections count, trust score visualization, and action buttons
  - Step 21: Build TrustScoreBadge component with color-coded trust score display (red/yellow/green based on score ranges)
  - Step 22: Implement NetworkScreen with tabs for connections list and pending requests using SectionList
  - Step 23: Create ConnectionRequestItem component for pending requests with accept/reject buttons
  - Step 24: Add navigation between screens (FeedScreen -> PostDetailScreen, ProfileScreen -> EditProfileScreen, NetworkScreen -> UserProfileScreen)
  - Step 25: Implement offline-first capabilities using AsyncStorage for caching posts and connection data
  - Step 26: Add loading states, error boundaries, and empty states for all screens
  - Step 27: Update App.tsx to use AppNavigator instead of basic structure from Phase 1
  - Step 28: Add accessibility labels, roles, and touch target sizes (minimum 44x44) to all interactive elements
  - Step 29: Optimize FlatList performance with React.memo, useMemo, useCallback, and getItemLayout where possible
  - Step 30: Write unit tests for usePosts, useConnections hooks verifying data fetching and mutations
  - Step 31: Write component tests for PostCard, Button, and other UI components using React Native Testing Library
  - Step 32: Create integration tests for post creation flow (camera -> upload -> post) and connection request flow (send -> accept/reject)
  - Step 33: Test camera permissions flow and graceful degradation when permissions denied
  - Step 34: Performance test scrolling at 60fps and navigation transitions under 1s using Expo development build
testing_requirements:
  - Unit test usePosts hook for fetchPosts, likePost, commentPost with mock Supabase client
  - Unit test useConnections hook for fetchConnections, sendRequest, acceptRequest, rejectRequest
  - Component test PostCard renders correctly with mock post data including AI badges
  - Component test Button handles press events and disabled states
  - Component test Avatar loads images and handles fallback
  - Integration test post creation: select image -> compress -> upload to storage -> create post record -> optimistic update
  - Integration test connection flow: send request -> recipient sees notification -> accept -> both users see connection
  - Test camera permission request and denial handling with appropriate error messages
  - Test image upload with progress tracking and error recovery
  - Test offline mode: posts are cached and displayed when network unavailable
  - Test navigation between all screens without memory leaks
  - Verify accessibility with screen reader (TalkBack/VoiceOver)
  - Performance test: 60fps scrolling with 100+ posts in feed
  - Performance test: navigation transitions complete in <1s
  - Test coverage >70% for new hooks and components
constraints:
  - Do NOT modify Supabase schema or backend - use existing tables (profiles, posts, ai_post_analysis, connections, trust_scores, notifications)
  - Do NOT break existing Phase 1 code (AuthContext, Supabase client config, theme configuration)
  - Follow existing TypeScript strict mode from tsconfig.json
  - Use existing color scheme and theme from Phase 1 theme.ts
  - Do NOT add dependencies larger than 5MB - keep total bundle under 50MB
  - Follow React Navigation v6 patterns for type-safe navigation
  - Use FlatList, not ScrollView, for lists longer than 10 items
  - Compress images to max 1080px width and 80% quality before upload
  - Follow React Native Performance best practices (avoid inline functions in render, use PureComponent/React.memo)
  - Ensure minimum touch target size of 44x44 for accessibility
  - Support both iOS and Android without platform-specific code where possible
  - Use React Native Paper components as base but customize with theme
  - Do NOT implement Messages screen functionality yet (placeholder only) - that's for Phase 3
  - Do NOT implement Notifications screen functionality yet (placeholder only) - that's for Phase 3

## REPOSITORY CONTEXT:
Based on my analysis of the repository, here's a comprehensive overview:

## Repository Analysis

**Primary Language**: Python 3.11+ (modern type hints like `list[str]`, uses pathlib extensively)

**Project Type**: CLI tool - A prompt orchestrator for governed multi-agent coding workflows

**Key Frameworks**:
- **Typer** - Type-safe CLI framework with automatic help generation
- **Rich** - Terminal formatting (colors, panels, tables, progress bars)
- **Pydantic v2** - Data validation and configuration management
- **PyYAML** - YAML parsing for task specs and agent responses
- **Google Generative AI & Anthropic SDKs** - AI integrations (optional/for automation mode)

**Code Organization**:
```
agentic_code/              # Main package
├── cli.py                 # Entry point (Typer CLI app)
├── pipeline.py            # AgenticPipeline orchestration
├── automated_pipeline.py  # AutomatedAgenticPipeline variant
├── config.py              # Pydantic Config model
├── utils.py               # File I/O, formatting helpers
└── agents/                # Agent implementations
    ├── claude.py          # Analysis, planning, decision prompts
    ├── codex.py           # Implementation prompts
    └── gemini.py          # Verification prompts
```

**Testing Approach**: pytest framework (tests in generated_code outputs, not core package tests yet)

**Notable Patterns**:
- **Separation of duties** - Each agent has specific role (Claude plans/decides, Codex implements, Gemini verifies)
- **Human-in-the-loop** - Every stage requires user approval via `wait_for_response()` and `confirm_action()`
- **Artifact preservation** - Timestamped output directories with complete audit trails (prompts, responses, decisions)
- **Prompt template pattern** - Hardcoded templates with `.format()` placeholders (e.g., `REPO_ANALYSIS_PROMPT`)

**Dependencies**:
- Core: typer (CLI), rich (terminal UI), pyyaml (parsing), pydantic (validation)
- Optional dev: pytest, black, ruff, mypy
- AI SDKs (for automation mode only, not required for manual prompt orchestration)

**Code Style**:
- Black formatter (100 char line length)
- Ruff linter
- Type hints (but lenient mypy - `disallow_untyped_defs = false`)
- `Path` objects over strings
- f-strings and `.format()` (no `%` formatting)
- Rich console output with color tags like `[cyan]text[/cyan]`

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
