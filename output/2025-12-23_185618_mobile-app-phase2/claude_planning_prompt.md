# Task Planning - Create Implementation Specification

You are a software architect creating a detailed implementation plan.

## Context
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
- `examples/` - Task specification examples (.md, .yaml, .json formats)
- `output/` - Timestamped run directories with complete artifact trails
- `scripts/` - Automation scripts (fully_automated.py)

**Testing Approach**: pytest framework (configured in pyproject.toml dev dependencies). Tests appear in generated code output directories rather than a dedicated tests/ folder.

**Notable Patterns**:
- **Separation of Duties**: Claude plans/decides, Codex implements, Gemini verifies (no agent reviews its own work)
- **Human-in-the-Loop**: Every stage requires explicit user confirmation before proceeding
- **Artifact Preservation**: All prompts and responses saved as plain text (Markdown/YAML/JSON) in timestamped directories
- **Prompt Template Pattern**: Hardcoded module-level constants with `.format()` placeholders
- **Dual-Mode Architecture**: Prompt-based (free) vs Automated (API calls with human review)

**Dependencies**: Minimal by design - typer, rich, pyyaml, pydantic. API SDKs (anthropic, google-generativeai) only used in automated mode.

**Code Style**: 
- Black formatting (100-char line length)
- Modern Python 3.11+ type hints (`list[str]`, not `List[str]`)
- `pathlib.Path` objects (never string concatenation)
- Rich console output (`console.print()` with color tags like `[cyan]text[/cyan]`)
- f-strings or `.format()` (no `%` formatting)
- Snake_case naming throughout

## Task Description
# TrustLink AI Guardian Mobile App - Phase 2: Core Features

Continue development of the TrustLink AI Guardian mobile app by implementing core user-facing features.

## Context

Phase 1 (Foundation) is complete with:
- ✅ Project initialization with Expo + TypeScript
- ✅ Supabase client configuration
- ✅ Authentication context with biometric support
- ✅ Theme configuration
- ✅ Main app structure

Phase 1 artifacts location: `/Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/`

## Objective

Implement the core user-facing features that enable users to navigate the app, view and create posts, manage their profile, and connect with other users.

## Requirements

### 1. Navigation System (Steps 5 from original plan)
- Implement React Navigation with bottom tab navigator
- Create 5 main tabs: Feed, Network, Messages, Notifications, Profile
- Set up stack navigators for detail views
- Implement protected route logic
- Add authentication navigator for login/signup screens

### 2. Feed Screen with Posts (Step 6)
- Implement infinite scroll feed using FlatList
- Display posts from Supabase with AI moderation badges
- Add pull-to-refresh functionality
- Show post interactions (likes, comments, shares)
- Implement optimistic updates for user actions
- Display loading skeletons for better UX

### 3. Post Creation with Camera (Step 7)
- Create post composer modal/screen
- Integrate camera capture with expo-camera
- Support photo selection from library
- Implement image compression before upload
- Upload images to Supabase Storage
- Show upload progress
- Add text input with rich formatting options

### 4. User Profiles (Step 8 - partial)
- Display user profile screen with posts, connections, stats
- Show AI trust scores and moderation metrics
- Implement profile editing
- Add profile picture upload with camera/gallery
- Display user's bio, skills, industry
- Show connection status and mutual connections

### 5. Connections Management (Step 8 - partial)
- Display connections list with trust scores
- Implement connection request sending
- Show pending connection requests
- Add accept/reject connection functionality
- Display trust score visualization (colors, badges)
- Show mutual connections count

### 6. UI Component Library (Step 18 - needed early)
- Create reusable components: Button, Card, Input, Avatar, Badge
- Implement consistent styling with theme
- Add loading states and error states
- Ensure accessibility (labels, roles, touch targets)
- Use React Native Paper components as base

## Constraints

- Build on existing Phase 1 foundation without breaking changes
- Maintain TypeScript strict typing
- Use existing Supabase schema from web app (no backend changes)
- Follow React Native performance best practices (FlatList, memoization)
- Ensure all interactive elements are accessible
- Support both iOS and Android
- Keep bundle size under 50MB

## Testing Requirements

- Unit tests for custom hooks (usePosts, useConnections)
- Component tests for UI components
- Integration test for post creation flow
- Integration test for connection request flow
- Test camera permissions and image upload
- Test navigation between screens

## Success Criteria

- Users can navigate between all main tabs
- Users can view infinite-scrolling feed of posts
- Users can create posts with text and images from camera/gallery
- Users can view their own and other users' profiles
- Users can send, accept, and reject connection requests
- Trust scores are displayed correctly
- All features work offline-first where applicable
- Performance: 60fps scrolling, <1s navigation transitions
- Test coverage >70% for new code
- No critical accessibility issues

## Implementation Priority

1. Navigation system (foundation for all screens)
2. UI component library (needed by all features)
3. Feed screen (core user experience)
4. Post creation (core user engagement)
5. Profile screen (user identity)
6. Connections (networking functionality)

## Deliverables

All code should be added to the existing generated_code/ directory structure, extending the Phase 1 foundation.


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
