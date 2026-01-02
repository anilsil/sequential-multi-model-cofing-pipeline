# Task Planning - Create Implementation Specification

You are a software architect creating a detailed implementation plan.

## Context
## Repository Analysis

### 1. **Primary Language(s)**
Python 3.11+ (exclusively)

### 2. **Project Type**
CLI tool (command-line interface) - A prompt orchestrator for governed multi-agent coding workflows

### 3. **Key Frameworks**
- **Typer** - CLI framework with type-safe argument parsing
- **Rich** - Terminal UI formatting (colors, panels, tables, progress)
- **Pydantic v2** - Data validation and configuration management
- **PyYAML** - YAML parsing for task specs and responses
- Optional: `google-generativeai`, `anthropic` SDKs (for automated mode)

### 4. **Code Organization**
```
agentic_code/          # Main package
├── cli.py             # Typer CLI entry point
├── pipeline.py        # Pipeline orchestration (5-stage workflow)
├── automated_pipeline.py  # Automated execution variant
├── config.py          # Pydantic configuration model
├── utils.py           # File I/O, formatting, user interaction
└── agents/            # Agent implementations
    ├── claude.py      # Analysis, planning, decision prompts
    ├── codex.py       # Implementation prompts
    └── gemini.py      # Verification prompts
```

### 5. **Testing Approach**
- **Framework**: pytest (configured in `pyproject.toml`)
- **Location**: No native test directory found; tests appear in `output/*/generated_code/tests/` (user-generated artifacts)
- **Dev tools**: Black (formatting), Ruff (linting), mypy (type checking - lenient mode)

### 6. **Notable Patterns**
- **Human-in-the-loop**: Every pipeline stage requires explicit user confirmation and manual file saving
- **Prompt orchestration**: Generates prompts instead of making API calls (zero-cost architecture)
- **Separation of duties**: Different agents handle different stages (Claude plans/decides, Codex implements, Gemini verifies)
- **Artifact preservation**: All runs create timestamped directories with complete audit trails (Markdown, YAML, JSON)
- **Template-based prompts**: Hardcoded prompt templates with `.format()` placeholders

### 7. **Dependencies**
**Core**: `typer>=0.9.0`, `rich>=13.0.0`, `pyyaml>=6.0`, `pydantic>=2.0.0`  
**Optional automation**: `google-generativeai>=0.3.0`, `anthropic>=0.15.0`  
**Dev**: `pytest`, `black`, `ruff`, `mypy`

### 8. **Code Style**
- **Line length**: 100 characters (Black/Ruff)
- **Naming**: Snake_case for functions/variables, PascalCase for classes
- **Paths**: Exclusively `pathlib.Path` objects (never string concatenation)
- **Console output**: Rich library (`console.print()` with color tags like `[cyan]text[/cyan]`)
- **String formatting**: f-strings or `.format()` (no `%` formatting)
- **Type hints**: Modern Python 3.11+ syntax (`list[str]` not `List[str]`)
- **Docstrings**: Google-style with Args/Returns sections
- **Type checking**: Lenient (`disallow_untyped_defs = false`)

## Task Description
{'name': 'mobile-app-phase2', 'description': "# TrustLink AI Guardian Mobile App - Phase 2: Core Features\n\nContinue development of the TrustLink AI Guardian mobile app by implementing core user-facing features.\n\n## Context\n\nPhase 1 (Foundation) is complete with:\n- ✅ Project initialization with Expo + TypeScript\n- ✅ Supabase client configuration\n- ✅ Authentication context with biometric support\n- ✅ Theme configuration\n- ✅ Main app structure\n\nPhase 1 artifacts location: `/Users/anilsharma/webkins/trustlink-aigardian-main/output/2025-12-23_181637_mobile-app/generated_code/`\n\n## Objective\n\nImplement the core user-facing features that enable users to navigate the app, view and create posts, manage their profile, and connect with other users.\n\n## Requirements\n\n### 1. Navigation System (Steps 5 from original plan)\n- Implement React Navigation with bottom tab navigator\n- Create 5 main tabs: Feed, Network, Messages, Notifications, Profile\n- Set up stack navigators for detail views\n- Implement protected route logic\n- Add authentication navigator for login/signup screens\n\n### 2. Feed Screen with Posts (Step 6)\n- Implement infinite scroll feed using FlatList\n- Display posts from Supabase with AI moderation badges\n- Add pull-to-refresh functionality\n- Show post interactions (likes, comments, shares)\n- Implement optimistic updates for user actions\n- Display loading skeletons for better UX\n\n### 3. Post Creation with Camera (Step 7)\n- Create post composer modal/screen\n- Integrate camera capture with expo-camera\n- Support photo selection from library\n- Implement image compression before upload\n- Upload images to Supabase Storage\n- Show upload progress\n- Add text input with rich formatting options\n\n### 4. User Profiles (Step 8 - partial)\n- Display user profile screen with posts, connections, stats\n- Show AI trust scores and moderation metrics\n- Implement profile editing\n- Add profile picture upload with camera/gallery\n- Display user's bio, skills, industry\n- Show connection status and mutual connections\n\n### 5. Connections Management (Step 8 - partial)\n- Display connections list with trust scores\n- Implement connection request sending\n- Show pending connection requests\n- Add accept/reject connection functionality\n- Display trust score visualization (colors, badges)\n- Show mutual connections count\n\n### 6. UI Component Library (Step 18 - needed early)\n- Create reusable components: Button, Card, Input, Avatar, Badge\n- Implement consistent styling with theme\n- Add loading states and error states\n- Ensure accessibility (labels, roles, touch targets)\n- Use React Native Paper components as base\n\n## Constraints\n\n- Build on existing Phase 1 foundation without breaking changes\n- Maintain TypeScript strict typing\n- Use existing Supabase schema from web app (no backend changes)\n- Follow React Native performance best practices (FlatList, memoization)\n- Ensure all interactive elements are accessible\n- Support both iOS and Android\n- Keep bundle size under 50MB\n\n## Testing Requirements\n\n- Unit tests for custom hooks (usePosts, useConnections)\n- Component tests for UI components\n- Integration test for post creation flow\n- Integration test for connection request flow\n- Test camera permissions and image upload\n- Test navigation between screens\n\n## Success Criteria\n\n- Users can navigate between all main tabs\n- Users can view infinite-scrolling feed of posts\n- Users can create posts with text and images from camera/gallery\n- Users can view their own and other users' profiles\n- Users can send, accept, and reject connection requests\n- Trust scores are displayed correctly\n- All features work offline-first where applicable\n- Performance: 60fps scrolling, <1s navigation transitions\n- Test coverage >70% for new code\n- No critical accessibility issues\n\n## Implementation Priority\n\n1. Navigation system (foundation for all screens)\n2. UI component library (needed by all features)\n3. Feed screen (core user experience)\n4. Post creation (core user engagement)\n5. Profile screen (user identity)\n6. Connections (networking functionality)\n\n## Deliverables\n\nAll code should be added to the existing generated_code/ directory structure, extending the Phase 1 foundation.\n", 'requirements': [], 'constraints': []}

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
