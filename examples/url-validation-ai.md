# AI-Powered URL Validation System

Create a comprehensive URL validation system for detecting malicious, spam, and inauthentic URLs in user-generated content using AI agents.

## Objective

Implement an AI-powered URL validation and analysis system that integrates with the TrustLink AI Guardian platform to detect phishing attempts, spam URLs, malicious links, and assess URL authenticity in posts and messages.

## Requirements

### Core URL Validation
- Extract and validate URLs from post content and messages
- Validate URL format and structure (protocol, domain, path)
- Check for common URL obfuscation techniques (bit.ly redirects, URL shorteners)
- Detect suspicious TLDs and domains
- Handle edge cases (malformed URLs, international domains, encoded URLs)

### AI-Powered Analysis
- Integrate with existing `ai_post_analysis` table structure
- Add URL-specific analysis fields:
  - `url_spam_score` (0-1): Likelihood of spam/scam URL
  - `url_phishing_score` (0-1): Likelihood of phishing attempt
  - `url_malicious_score` (0-1): Likelihood of malware/malicious content
  - `url_authenticity_score` (0-1): URL legitimacy assessment
- Generate AI analysis using pattern matching and heuristics
- Store URL analysis results with timestamps

### Security Features
- Blacklist checking against known malicious domains
- Whitelist support for verified safe domains
- Real-time URL reputation checking
- Detect homograph attacks (Unicode lookalike domains)
- Identify shortened URL chains and unwrap them safely
- Rate limiting for URL submissions

### Integration Points
- Hook into post creation workflow (`usePosts.tsx`)
- Extend `PostCard.tsx` to display URL safety indicators
- Update `AIGuardianWidget.tsx` to show URL analysis
- Add URL warnings to chat messages (`chat_messages` table)
- Integrate with trust scoring system

### Database Schema Updates
- Add new fields to `ai_post_analysis` table:
  ```sql
  url_spam_score: number
  url_phishing_score: number
  url_malicious_score: number
  url_authenticity_score: number
  detected_urls: jsonb (array of analyzed URLs)
  url_analysis_timestamp: timestamp
  ```
- Create `url_blacklist` table for known malicious domains
- Create `url_whitelist` table for verified safe domains

### API Endpoints
- POST `/api/urls/analyze` - Analyze a single URL
- POST `/api/urls/batch-analyze` - Analyze multiple URLs
- GET `/api/urls/reputation/:domain` - Get domain reputation
- POST `/api/urls/report` - User-reported malicious URL
- GET `/api/urls/stats` - URL analysis statistics

## Constraints

- Use existing Supabase client pattern (`@/integrations/supabase/client`)
- Follow TanStack Query pattern for data fetching
- Use existing TypeScript types structure (`src/types/index.ts`)
- No external API calls (analyze URLs using local heuristics and patterns)
- Must work offline (no real-time external URL scanning services)
- Follow existing auth patterns for protected endpoints
- Maintain backward compatibility with existing posts

## Files to Modify

- `src/hooks/usePosts.tsx` - Add URL extraction and analysis on post creation
- `src/components/PostCard.tsx` - Display URL safety indicators
- `src/components/AIGuardianWidget.tsx` - Show URL analysis dashboard
- `src/integrations/supabase/types.ts` - Update AI analysis types
- `src/types/index.ts` - Add URL analysis types

## New Files to Create

- `src/utils/urlValidator.ts` - Core URL validation logic
- `src/utils/urlAnalyzer.ts` - AI-powered URL analysis
- `src/utils/urlExtractor.ts` - Extract URLs from text content
- `src/hooks/useUrlAnalysis.tsx` - React hook for URL analysis
- `src/components/URLSafetyBadge.tsx` - Visual indicator component
- `tests/utils/urlValidator.test.ts` - Unit tests for validation
- `tests/utils/urlAnalyzer.test.ts` - Unit tests for analysis

## Testing Requirements

### Unit Tests
- Test URL extraction from various text formats
- Test URL format validation (valid/invalid URLs)
- Test phishing detection patterns
- Test spam URL heuristics
- Test malicious domain detection
- Test URL obfuscation detection
- Test Unicode/homograph attack detection

### Integration Tests
- Test URL analysis during post creation
- Test URL warnings in PostCard display
- Test batch URL analysis
- Test database storage of URL analysis
- Test trust score impact from malicious URLs

### Edge Cases
- Very long URLs (>2000 characters)
- URLs with special characters and encoding
- Multiple URLs in single post
- Nested shortened URLs
- International domain names (IDN)
- IP address URLs
- Data URLs and javascript: protocol
- URLs without protocols

## Security Considerations

- Sanitize all URL inputs to prevent XSS
- Never automatically follow or execute URLs
- Prevent SQL injection in URL storage
- Rate limit URL analysis requests (max 100/minute per user)
- Log suspicious URL patterns for security review
- Don't expose internal blacklist logic to users
- Implement CSRF protection on URL submission endpoints
- Validate user permissions before URL analysis

## AI Analysis Heuristics

### Spam Detection (url_spam_score)
- Excessive use of URL shorteners
- URLs containing spam keywords (free, prize, winner, click-here)
- Suspicious query parameters (utm_source, tracking IDs)
- Multiple redirects
- Newly registered domains (<30 days)

### Phishing Detection (url_phishing_score)
- Homograph attacks (paypa1.com vs paypal.com)
- Lookalike domains (g00gle.com)
- HTTPS on suspicious domains
- Login/account keywords in URL path
- Brand impersonation patterns

### Malicious Detection (url_malicious_score)
- Known malware domains
- Executable file extensions in URL
- Suspicious file hosting domains
- Port numbers in URL (non-standard ports)
- IP addresses instead of domains

### Authenticity Assessment (url_authenticity_score)
- Domain age and registration
- HTTPS presence and certificate validity
- Brand verification (official domains)
- URL structure consistency
- Redirect chain analysis

## User Experience

- Non-intrusive warnings (don't block posting)
- Clear visual indicators (red/yellow/green badges)
- Detailed explanations for flagged URLs
- User ability to report false positives
- Trust score integration (low trust = stricter URL filtering)
- Admin dashboard for URL analysis trends

## Performance Requirements

- URL analysis must complete within 500ms
- Batch analysis: max 50 URLs per request
- Cache domain reputation for 24 hours
- Lazy load URL analysis in feed (don't block rendering)
- Optimize regex patterns for URL extraction
