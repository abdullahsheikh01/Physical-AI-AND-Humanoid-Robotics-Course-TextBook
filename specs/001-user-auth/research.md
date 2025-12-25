# Research: Better-Auth Integration with Neon Serverless Postgres

## Decision: Better-Auth with Neon Serverless Postgres using pg Pool

### Rationale:
- Better-Auth provides comprehensive authentication solution supporting email/password and OAuth providers (Google, GitHub)
- Neon Serverless Postgres offers automatic scaling and serverless database capabilities
- Direct pg Pool integration ensures efficient connection management without ORM overhead
- All components align with constitutional requirements for security and database integration

### Architecture Approach:
- Use Better-Auth as primary authentication framework with email/password as default method
- Integrate Google and GitHub OAuth providers using client ID and secret configuration
- Connect to Neon Serverless Postgres using pg Pool for direct database integration
- Implement secure session management with proper logout functionality
- Deploy in Next.js environment with appropriate middleware for session validation

## Technical Details:

### Better-Auth Configuration:
- Use `betterAuth()` function with database configuration for pg Pool
- Enable email/password authentication with `emailAndPassword: { enabled: true }`
- Configure social providers with Google and GitHub using environment variables
- Implement session management with proper expiration and security settings

### Neon Serverless Integration:
- Use `@neondatabase/serverless` package with pg Pool
- Configure WebSocket support for Node.js environments
- Implement proper connection pooling with automatic scaling
- Handle connection lifecycle in serverless functions appropriately

### OAuth Provider Setup:
- Google: Requires `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` environment variables
- GitHub: Requires `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` environment variables
- Both providers support refresh tokens and user profile access

### Session Management:
- Implement secure session handling with cookie-based authentication
- Provide logout functionality that invalidates sessions properly
- Support session revocation for security purposes
- Handle session persistence across user visits

## Next.js Integration:

### API Routes:
- Create `/api/auth/[...all]` route using `toNextJsHandler(auth)`
- Handle all authentication endpoints through Better-Auth
- Implement proper error handling and redirects

### Middleware:
- Use Next.js middleware for session validation on protected routes
- Implement optimistic cookie-based checks for performance
- Ensure secure validation in server components

### Environment Variables:
- `NEON_CONNECTION_STRING`: Database connection string for Neon
- `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`: Google OAuth credentials
- `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`: GitHub OAuth credentials
- `NEXTAUTH_SECRET`: Secret for JWT signing and session encryption