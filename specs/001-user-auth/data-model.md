# Data Model: User Authentication System

## User Entity

**Description**: Represents a registered user in the textbook application

**Fields**:
- `id` (string): Unique identifier for the user (UUID format)
- `email` (string): User's email address (unique, required)
- `emailVerified` (boolean): Whether the email has been verified (default: false)
- `name` (string): User's full name (optional)
- `image` (string): URL to user's profile image (optional, from OAuth providers)
- `createdAt` (timestamp): Account creation timestamp
- `updatedAt` (timestamp): Last update timestamp
- `passwordHash` (string): Hashed password for email/password accounts (nullable)

**Relationships**:
- One-to-many with Session (user can have multiple active sessions)
- One-to-many with Account (user can have multiple OAuth provider accounts linked)

## Session Entity

**Description**: Represents an active user session with secure tokens

**Fields**:
- `id` (string): Unique session identifier
- `userId` (string): Reference to the user who owns this session
- `token` (string): Session token (secure random string)
- `expiresAt` (timestamp): Session expiration timestamp
- `createdAt` (timestamp): Session creation timestamp
- `updatedAt` (timestamp): Last update timestamp
- `userAgent` (string): Browser/device information (optional)
- `ipAddress` (string): IP address of the session (optional)

**Relationships**:
- Many-to-one with User (belongs to a single user)

## Account Entity

**Description**: Represents OAuth provider accounts linked to users

**Fields**:
- `id` (string): Unique account identifier
- `userId` (string): Reference to the user who owns this account
- `providerId` (string): OAuth provider identifier (e.g., 'google', 'github')
- `providerAccountId` (string): Provider-specific account identifier
- `accessToken` (string): OAuth access token (encrypted)
- `refreshToken` (string): OAuth refresh token (encrypted, optional)
- `expiresAt` (timestamp): Token expiration timestamp (optional)
- `createdAt` (timestamp): Account link creation timestamp
- `updatedAt` (timestamp): Last update timestamp

**Relationships**:
- Many-to-one with User (belongs to a single user)

## Validation Rules

### User Validation:
- Email must be in valid format
- Email must be unique across all users
- Password must meet security requirements (min 8 chars, mixed case, numbers, special chars for email/password accounts)
- Name must not exceed 100 characters

### Session Validation:
- Session tokens must be securely random and unique
- Session expiration must be within reasonable limits (max 30 days)
- Sessions must be invalidated after logout

### Account Validation:
- Each user can only have one account per provider
- Provider account IDs must be unique within provider type

## State Transitions

### User States:
- `pending`: New user registration, email verification required
- `active`: User account is active and verified
- `suspended`: Account temporarily suspended (security reasons)
- `deleted`: Account marked for deletion (with retention period)

### Session States:
- `active`: Session is currently valid and can be used
- `expired`: Session has passed its expiration time
- `revoked`: Session was manually invalidated (logout)

## Security Considerations

- Passwords must be hashed using bcrypt or similar secure algorithm
- Session tokens must be securely random and of sufficient length
- OAuth tokens must be encrypted when stored
- All sensitive data should be stored with appropriate encryption
- Session fixation attacks should be prevented
- Rate limiting should be implemented for authentication endpoints