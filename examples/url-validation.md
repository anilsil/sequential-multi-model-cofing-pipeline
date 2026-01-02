# Add Email Validation Function

Create a utility function to validate email addresses.

## Requirements

- Function should accept a string and return boolean
- Validate email format using regex
- Handle edge cases (empty string, null, invalid formats)
- Add comprehensive unit tests

## Constraints

- Use existing utility file pattern (if exists)
- No external dependencies for validation
- Follow existing code style

## Testing

- Test valid emails: user@example.com, name.last@domain.co.uk
- Test invalid emails: @example.com, user@, no-at-sign.com
- Test edge cases: empty, null, very long emails
