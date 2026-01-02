# TrustLink AI Guardian Mobile App Development

Create a native mobile application for TrustLink AI Guardian professional networking platform with AI-powered content moderation and trust scoring.

## Objective

Transform the existing React web application into a cross-platform mobile app (iOS & Android) that provides full feature parity while optimizing for mobile user experience, offline capabilities, and native device integration.

## Requirements

### Technical Stack
- Use **React Native** for cross-platform development (leverages existing React/TypeScript codebase)
- Integrate **Expo** for simplified build and deployment workflow
- Maintain **Supabase** backend integration (authentication, database, real-time)
- Use **React Native Paper** or **NativeBase** for mobile-optimized UI components
- Implement **React Navigation** for mobile-first navigation patterns
- Use **TanStack Query** (React Query) for data fetching and caching (same as web)

### Core Features (Feature Parity)
- **Authentication & Onboarding**
  - Supabase Auth integration with session persistence
  - Multi-step onboarding flow optimized for mobile screens
  - Biometric authentication (Face ID, Touch ID, fingerprint)
  - Social login options (Google, LinkedIn, Apple Sign-In)

- **Feed & Content**
  - Infinite scroll feed with pull-to-refresh
  - Post creation with camera integration and image upload
  - AI content moderation badges (spam, toxicity, AI-generated scores)
  - Rich media support (images, videos, links)
  - Trust-based content filtering

- **Professional Networking**
  - Connection management with trust score visualization
  - Profile viewing and editing
  - Skill endorsements
  - Network visualization (adapted for mobile - simplified D3 or native graphics)
  - Connection requests and recommendations

- **Messaging & Notifications**
  - Real-time chat with Supabase subscriptions
  - Push notifications (FCM for Android, APNs for iOS)
  - In-app notifications center
  - Unread message badges
  - Typing indicators and read receipts

- **AI Features**
  - AI Guardian widget (bottom sheet or modal for content analysis)
  - AI Assistant chat interface
  - Trust score insights and analytics
  - Content authenticity verification

- **Additional Features**
  - Job board with saved jobs and applications
  - User settings and preferences
  - Profile customization
  - Blocked users management
  - Analytics dashboard (mobile-optimized charts)

### Mobile-Specific Enhancements
- **Offline Support**
  - Cache feed posts for offline viewing
  - Queue actions (posts, messages) when offline
  - Sync when connection restored
  - Offline indicators and messaging

- **Native Device Integration**
  - Camera and photo library access for profile pictures and posts
  - Push notification permissions and handling
  - Deep linking (open specific profiles, posts from notifications)
  - Share sheet integration (share posts to other apps)
  - Biometric authentication for app unlock

- **Performance Optimization**
  - Lazy loading and code splitting
  - Image optimization and caching
  - Virtualized lists for long feeds
  - Optimistic UI updates
  - Background data sync

- **Mobile UX Patterns**
  - Bottom tab navigation (Feed, Network, Messages, Notifications, Profile)
  - Stack navigation for detail views
  - Swipe gestures (swipe to delete, pull to refresh)
  - Bottom sheets for actions and filters
  - Mobile-optimized forms with proper keyboard handling
  - Haptic feedback for interactions

## Constraints

### Architecture Constraints
- Reuse existing **TypeScript types** from web app (`src/types/index.ts`, `src/integrations/supabase/types.ts`)
- Maintain **Supabase integration** architecture (no backend changes)
- Use same **authentication flow** (Supabase Auth with OAuth providers)
- Preserve **data models** and API contracts
- Follow React Native best practices and folder structure

### Code Sharing Strategy
- Share **TypeScript types** between web and mobile
- Share **API client logic** and Supabase integration
- Share **business logic hooks** where possible (with platform-specific adapters)
- **DO NOT share UI components** - build native mobile UI from scratch
- Create **shared package** for common utilities, types, and API layer

### Platform Requirements
- **Minimum Versions**: iOS 13+, Android 8.0+ (API level 26+)
- **Expo SDK**: Use latest stable version (SDK 50+)
- **React Native**: 0.73+ with new architecture support
- Support both **portrait and landscape** orientations (with responsive layouts)
- Follow **iOS Human Interface Guidelines** and **Material Design** principles

### Security & Privacy
- Secure token storage using **react-native-keychain** or Expo SecureStore
- Implement **certificate pinning** for API requests
- Handle **app backgrounding** securely (clear sensitive data from memory)
- Request minimal permissions (explain why each permission is needed)
- Comply with **App Store** and **Google Play** privacy policies

### Performance Constraints
- App launch time < 2 seconds on mid-range devices
- Smooth scrolling at 60 fps on feed and lists
- Image loading with progressive enhancement
- Bundle size optimization (< 50 MB download size)
- Memory usage < 150 MB for typical usage

## Implementation Phases

### Phase 1: Project Setup & Core Infrastructure (Week 1-2)
- Initialize Expo/React Native project with TypeScript
- Set up folder structure following React Native conventions
- Configure Supabase client for React Native
- Implement authentication flow (login, signup, session management)
- Set up React Navigation structure
- Create shared types package

### Phase 2: Core Features (Week 3-6)
- Implement feed with infinite scroll and pull-to-refresh
- Build post creation with camera integration
- Create profile screens (view and edit)
- Implement connection management
- Set up real-time messaging
- Integrate AI post analysis display

### Phase 3: Advanced Features (Week 7-9)
- Implement push notifications (FCM/APNs)
- Add offline support with local caching
- Build network visualization (mobile-optimized)
- Create AI Guardian and AI Assistant interfaces
- Implement job board
- Add analytics dashboard

### Phase 4: Polish & Optimization (Week 10-11)
- Performance optimization (lazy loading, image caching)
- Add haptic feedback and animations
- Implement deep linking
- Add share functionality
- Comprehensive error handling
- Accessibility improvements (VoiceOver, TalkBack)

### Phase 5: Testing & Deployment (Week 12)
- Unit tests for business logic
- Integration tests for API calls
- E2E tests with Detox or Maestro
- Beta testing with TestFlight (iOS) and Google Play Internal Testing (Android)
- App store submission and review
- Production deployment

## Project Structure

```
trustlink-mobile/
├── src/
│   ├── components/           # Reusable mobile UI components
│   │   ├── PostCard.tsx
│   │   ├── ConnectionCard.tsx
│   │   ├── Avatar.tsx
│   │   └── ...
│   ├── screens/              # Screen components (one per route)
│   │   ├── FeedScreen.tsx
│   │   ├── ProfileScreen.tsx
│   │   ├── MessagesScreen.tsx
│   │   ├── NetworkScreen.tsx
│   │   └── ...
│   ├── navigation/           # React Navigation configuration
│   │   ├── RootNavigator.tsx
│   │   ├── TabNavigator.tsx
│   │   └── StackNavigator.tsx
│   ├── hooks/                # Custom hooks (reuse from web where possible)
│   │   ├── useAuth.tsx
│   │   ├── usePosts.tsx
│   │   ├── useConnections.tsx
│   │   └── ...
│   ├── services/             # API and business logic
│   │   ├── supabase.ts
│   │   ├── notifications.ts
│   │   ├── storage.ts
│   │   └── ...
│   ├── contexts/             # React Context providers
│   │   ├── AuthContext.tsx
│   │   └── ThemeContext.tsx
│   ├── types/                # TypeScript types (shared with web)
│   ├── utils/                # Utility functions
│   └── constants/            # App constants and config
├── assets/                   # Images, fonts, icons
├── app.json                  # Expo configuration
├── package.json
└── tsconfig.json
```

## Testing Strategy

### Unit Tests
- Test business logic hooks with Jest and React Native Testing Library
- Test utility functions and data transformations
- Test navigation flows and routing logic
- Mock Supabase client for isolated testing

### Integration Tests
- Test authentication flow end-to-end
- Test post creation and feed retrieval
- Test messaging with real-time updates
- Test offline sync and queue mechanisms

### E2E Tests
- Use **Detox** (iOS/Android) or **Maestro** for end-to-end testing
- Test critical user journeys:
  - Signup → Onboarding → First post
  - Login → Browse feed → Connect with user
  - View post → Send message → Receive notification
  - Create post with camera → AI analysis → Publish
- Test on both iOS and Android emulators

### Manual Testing
- Test on real devices (various iOS and Android models)
- Test different network conditions (3G, WiFi, offline)
- Test with different screen sizes and orientations
- Accessibility testing with screen readers
- Performance testing (memory leaks, battery usage)

## Dependencies

### Core Dependencies
```json
{
  "react-native": "~0.73.0",
  "expo": "~50.0.0",
  "react-navigation": "^6.x",
  "@react-navigation/native": "^6.x",
  "@react-navigation/bottom-tabs": "^6.x",
  "@react-navigation/native-stack": "^6.x",
  "@tanstack/react-query": "^5.x",
  "@supabase/supabase-js": "^2.x",
  "react-native-url-polyfill": "^2.x"
}
```

### UI & UX
```json
{
  "react-native-paper": "^5.x",
  "react-native-vector-icons": "^10.x",
  "react-native-gesture-handler": "^2.x",
  "react-native-reanimated": "^3.x",
  "react-native-safe-area-context": "^4.x"
}
```

### Device Integration
```json
{
  "expo-camera": "~14.x",
  "expo-image-picker": "~14.x",
  "expo-notifications": "~0.27.x",
  "expo-local-authentication": "~13.x",
  "expo-secure-store": "~12.x",
  "react-native-keychain": "^8.x"
}
```

### Utilities
```json
{
  "date-fns": "^3.x",
  "zustand": "^4.x",
  "@react-native-async-storage/async-storage": "^1.x",
  "react-native-mmkv": "^2.x"
}
```

## Deliverables

1. **Fully functional mobile app** for iOS and Android with feature parity to web
2. **App store listings** with screenshots, descriptions, and metadata
3. **Technical documentation** covering architecture, setup, and deployment
4. **Testing suite** with unit, integration, and E2E tests
5. **CI/CD pipeline** for automated builds and deployments (EAS Build)
6. **Shared code package** for types and business logic reuse between web and mobile

## Success Criteria

- App launches successfully on both iOS and Android
- All core features work as expected (auth, feed, messaging, networking)
- Push notifications deliver reliably
- Offline mode works with proper sync when online
- Performance metrics met (launch time, fps, memory)
- Passes App Store and Google Play review
- User feedback score > 4.5 stars on both platforms
- No critical bugs in production
- Smooth upgrade path from web to mobile for existing users
