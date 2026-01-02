# Task Planning - Create Implementation Specification

You are a software architect creating a detailed implementation plan.

## Context
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
- `examples/` - Task specification examples (.md, .yaml, .json)
- `scripts/` - Automation scripts (`fully_automated.py`, `fully_automated_with_codex.py`)
- `output/` - Timestamped pipeline run artifacts

**Testing Approach**: pytest framework (in `dev` dependencies), though no test files found in main codebase yet

**Notable Patterns**:
- **Agent pattern**: Separation of duties (Claude plans/decides, Codex implements, Gemini verifies)
- **Human-in-the-loop**: Blocks for user confirmation at each stage
- **Prompt generation**: Hardcoded templates with `.format()` placeholders
- **Artifact preservation**: All outputs saved as plain text (Markdown, YAML, JSON) in timestamped directories

**Dependencies**: Minimal core dependencies (typer, rich, pyyaml, pydantic). AI SDKs optional for automation mode.

**Code Style**: Black formatter (100-char lines), Ruff linter, lenient mypy, `pathlib.Path` for all file operations, Rich console for all user output.

## Task Description
# TrustLink Mobile App - Phase 2 Completion

Complete the remaining 30% of Phase 2 core features for the TrustLink AI Guardian mobile app.

## Objective

Implement the remaining screens and components to complete Phase 2, building on the approved foundation (navigation system, UI component library, and data hooks from previous Phase 2 work).

## Context

**Previous Phase 2 Work (APPROVED - 70% complete):**
- ✅ Complete navigation system (RootNavigator, TabNavigator, AuthNavigator, linking)
- ✅ UI component library (Button, Card, Avatar, Badge, Input, LoadingSpinner, EmptyState)
- ✅ Data hooks (usePosts with infinite scroll, useLikePost, useCreatePost)
- ✅ Authentication screens (LoginScreen, SignupScreen)

**Location of Phase 2 Foundation:**
`/Users/anilsharma/webkins/trustlink-aigardian-main/agentic-code/output/2025-12-23_185618_mobile-app-phase2/generated_code/mobile/`

## Requirements

### 1. FeedScreen Implementation
**File**: `src/screens/FeedScreen.tsx`

**Features**:
- Use `usePosts` hook from previous phase for data fetching
- Implement infinite scroll with `FlatList` and `onEndReached`
- Pull-to-refresh functionality with `RefreshControl`
- Display posts using `PostCard` component (to be created)
- Show loading states with `LoadingSpinner`
- Show empty state when no posts available
- Floating action button for creating new posts (navigates to CreatePostScreen)

### 2. PostCard Component
**File**: `src/components/PostCard.tsx`

**Features**:
- Display post content, author info, timestamp
- Show user avatar and name (clickable to navigate to profile)
- Display post images if available
- Show AI moderation badges (spam score, toxicity score, AI-generated score)
- Trust score indicator with color coding
- Like, comment, share action buttons
- Display like count and comment count
- Use optimistic updates for like action
- Proper accessibility labels

### 3. CreatePostScreen
**File**: `src/screens/CreatePostScreen.tsx`

**Features**:
- Text input for post content (multiline with character counter)
- Image picker integration (camera OR gallery)
- Image preview with option to remove
- Submit button that calls `useCreatePost` hook
- Loading state during submission
- Navigate back to feed after successful post
- Form validation (content not empty)
- Keyboard-aware scroll view

**Camera Integration**:
- Use `expo-image-picker` for gallery selection
- Use `expo-camera` for camera capture
- Handle permissions (camera, photo library)
- Image compression before upload
- Progress indicator during upload

### 4. ProfileScreen
**File**: `src/screens/ProfileScreen.tsx`

**Features**:
- Accept `userId` parameter (view any user's profile)
- If no userId, show current user's profile
- Display user info: avatar, name, bio, industry, location
- Show profile stats: posts count, connections count, trust score average
- Display AI moderation metrics (spam rate, toxicity rate)
- List user's posts with `FlatList` and `PostCard`
- Edit profile button (for current user only)
- Connect/Message buttons (for other users)
- Pull-to-refresh for profile data

### 5. EditProfileScreen
**File**: `src/screens/EditProfileScreen.tsx`

**Features**:
- Form with inputs for: name, bio, industry, location, skills
- Avatar picker (camera or gallery)
- Save button with loading state
- Form validation
- Use `useUpdateProfile` mutation hook (to be created)
- Navigate back after successful save

### 6. ConnectionsScreen
**File**: `src/screens/ConnectionsScreen.tsx`

**Features**:
- Use `useConnections` hook for data
- Display connections in `FlatList` with `ConnectionCard` component
- Show trust score for each connection
- Search/filter functionality
- Pull-to-refresh
- Navigate to profile on card tap
- Tab switching: "My Connections" and "Requests"

### 7. ConnectionCard Component
**File**: `src/components/ConnectionCard.tsx`

**Features**:
- Display user avatar, name, industry
- Show trust score with color-coded badge
- Connection status indicator
- Accept/Reject buttons for pending requests
- Message button for accepted connections
- Proper touch target sizes

### 8. OnboardingScreen
**File**: `src/screens/OnboardingScreen.tsx`

**Features**:
- Multi-step form (3 steps: Profile Info, Skills, Interests)
- Progress indicator showing current step
- Next/Previous navigation
- Skip button
- Final step submits and navigates to main app
- Form validation per step

### 9. Placeholder Screens

**NetworkScreen** (`src/screens/NetworkScreen.tsx`):
- Placeholder with title and description
- "Coming soon" message
- Navigation header

**MessagesScreen** (`src/screens/MessagesScreen.tsx`):
- Placeholder with conversations list UI shell
- Empty state: "No messages yet"

**NotificationsScreen** (`src/screens/NotificationsScreen.tsx`):
- Placeholder with notifications list UI shell
- Empty state: "No notifications"

### 10. Additional Hooks

**File**: `src/hooks/useProfile.tsx`
- Query hook for fetching user profile by ID
- Uses Supabase `profiles` table
- Returns profile data, loading state, error

**File**: `src/hooks/useUpdateProfile.tsx`
- Mutation hook for updating current user's profile
- Handles avatar upload to Supabase Storage
- Updates `profiles` table
- Optimistic updates

**File**: `src/hooks/useConnections.tsx`
- Query hook for fetching user connections
- Filter by status (accepted, pending)
- Uses Supabase `connections` table
- Returns connections array, loading state

**File**: `src/hooks/useImageUpload.tsx`
- Utility hook for image compression and upload
- Compress images to max 1MB
- Upload to Supabase Storage
- Return public URL
- Progress callback

## Constraints

### Code Reuse
- **MUST** use existing navigation setup from Phase 2 foundation
- **MUST** use existing UI components (Button, Card, Avatar, Badge, Input, etc.)
- **MUST** use existing hooks (usePosts, useLikePost, useCreatePost)
- **MUST** maintain TypeScript strict typing
- **MUST** follow existing code style and patterns

### Integration with Phase 2 Foundation
- All new screens should integrate with `TabNavigator.tsx` (already configured)
- Use existing theme system
- Use existing AuthContext
- Use existing Supabase client configuration
- No changes to navigation structure or dependencies

### Performance Requirements
- FlatList must render smoothly at 60fps
- Image loading with progressive enhancement
- Optimistic UI updates for mutations
- Lazy loading for images

### Accessibility
- All touchable elements minimum 44pt
- Proper accessibility labels and roles
- Screen reader support
- Keyboard navigation

### Platform Support
- Work on both iOS and Android
- Handle platform-specific behaviors (SafeAreaView, StatusBar)
- Test on both platforms

## Technical Stack

**Already configured from Phase 1/2:**
- React Native 0.73+
- Expo SDK 50+
- React Navigation 6.x
- TanStack Query 5.x
- Supabase client
- React Native Paper
- TypeScript

**New dependencies needed:**
- `expo-camera` - Camera access
- `expo-image-picker` - Gallery access
- `react-native-image-compress` - Image optimization (or use expo-image-manipulator)

## Files to Create

### Screens (9 files)
1. `src/screens/FeedScreen.tsx`
2. `src/screens/CreatePostScreen.tsx`
3. `src/screens/ProfileScreen.tsx`
4. `src/screens/EditProfileScreen.tsx`
5. `src/screens/ConnectionsScreen.tsx`
6. `src/screens/OnboardingScreen.tsx`
7. `src/screens/NetworkScreen.tsx` (placeholder)
8. `src/screens/MessagesScreen.tsx` (placeholder)
9. `src/screens/NotificationsScreen.tsx` (placeholder)

### Components (2 files)
10. `src/components/PostCard.tsx`
11. `src/components/ConnectionCard.tsx`

### Hooks (4 files)
12. `src/hooks/useProfile.tsx`
13. `src/hooks/useUpdateProfile.tsx`
14. `src/hooks/useConnections.tsx`
15. `src/hooks/useImageUpload.tsx`

**Total: 15 new files (~2500 lines of code)**

## Files to Reference (from Phase 2 foundation)

These files already exist and should be imported/used:
- `src/navigation/types.ts` - Navigation types
- `src/components/ui/Button.tsx`
- `src/components/ui/Card.tsx`
- `src/components/ui/Avatar.tsx`
- `src/components/ui/Badge.tsx`
- `src/components/ui/Input.tsx`
- `src/components/ui/LoadingSpinner.tsx`
- `src/components/ui/EmptyState.tsx`
- `src/hooks/usePosts.tsx`
- `src/hooks/useCreatePost.tsx` (if exists)
- `src/hooks/useLikePost.tsx` (if exists)
- `src/contexts/AuthContext.tsx` (from Phase 1)
- `src/services/supabase.ts` (from Phase 1)

## Success Criteria

- ✅ All 15 files created with complete implementations
- ✅ TypeScript compiles without errors
- ✅ All screens accessible via navigation
- ✅ FeedScreen displays posts with infinite scroll
- ✅ CreatePostScreen allows posting with images
- ✅ ProfileScreen shows user data and posts
- ✅ ConnectionsScreen displays connections list
- ✅ Image upload works for posts and profiles
- ✅ Optimistic updates work for likes and posts
- ✅ All components use existing UI library
- ✅ Accessibility labels on all interactive elements
- ✅ No runtime errors or console warnings

## Deliverables

1. **15 new TypeScript files** implementing screens, components, and hooks
2. **Updated package.json** (if new dependencies needed)
3. **Integration notes** for merging with Phase 2 foundation
4. **Implementation summary** documenting what was created

## Notes

- This builds directly on the approved Phase 2 foundation
- Focus on completing core functionality, polish comes in Phase 4
- Use placeholder data where real-time features aren't ready
- Follow React Native best practices throughout
- Maintain consistency with existing code style


## Your Job
Create a YAML specification that a developer can follow to implement this task.

## Required YAML Structure
```yaml
task_name: brief-descriptive-name
objective: One sentence describing the goal
requirements:
  - Specific requirement 1
  - Specific requirement 2
  - ...
files_to_modify:
  - path/to/file1.ext
  - path/to/file2.ext
new_files:
  - path/to/new_file1.ext
implementation_steps:
  - Step 1: Description
  - Step 2: Description
  - ...
testing_requirements:
  - Test requirement 1
  - Test requirement 2
constraints:
  - Do NOT modify X
  - Follow pattern Y
  - ...
```

## Critical Guidelines
- Be SPECIFIC about file paths and locations
- Follow existing repository patterns (from analysis above)
- Minimize scope - only what's truly necessary
- No new dependencies unless absolutely critical
- Consider backward compatibility
- Include comprehensive testing requirements

**Output ONLY the YAML specification (no markdown code blocks, no explanations):**
