# Quickstart: Better-Auth Integration with Neon Serverless Postgres

## Prerequisites

- Node.js 18+
- Next.js 14.2+
- Neon Serverless Postgres database
- OAuth credentials for Google and GitHub

## Setup Steps

### 1. Install Dependencies

```bash
npm install better-auth @neondatabase/serverless pg
npm install better-auth/next-js @types/pg
```

### 2. Environment Variables

Create a `.env` file with the following variables:

```env
# Neon Database Connection
NEON_CONNECTION_STRING=your_neon_database_url

# OAuth Provider Credentials
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Better-Auth Secret
NEXTAUTH_SECRET=your_secure_random_secret
```

### 3. Better-Auth Configuration

Create `lib/auth/index.ts`:

```typescript
import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Configure WebSocket for Node.js environments (if needed)
import { neonConfig } from '@neondatabase/serverless';
import ws from 'ws';
neonConfig.webSocketConstructor = ws; // Only needed for Node.js v21 and below

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.NEON_CONNECTION_STRING,
  }),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true for production
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      // Get refresh token for Google
      accessType: "offline",
      prompt: "select_account consent",
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    updateAge: 24 * 60 * 60,      // Update session every 24 hours
  },
  user: {
    // Additional user fields can be added here
  }
});
```

### 4. Next.js API Route

Create `pages/api/auth/[...all].ts` (for pages router) or `app/api/auth/[...all]/route.ts` (for app router):

```typescript
// For pages router
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export default toNextJsHandler(auth);

// Disable body parsing for the auth route
export const config = {
  api: {
    bodyParser: false,
  },
};
```

### 5. Client-Side Setup

Create `lib/auth/client.ts`:

```typescript
import { createAuthClient } from "better-auth/client";
import { auth } from "@/lib/auth";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
  // Add any client plugins here if needed
});
```

### 6. Session Middleware

Create `middleware.ts` for session validation:

```typescript
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

// Apply middleware to protected routes
export async function middleware(request: NextRequest) {
  // Optimistic cookie check (not secure for sensitive data)
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    // For Next.js 15.2.0+ with Node.js runtime, you can do full session validation:
    // const session = await auth.api.getSession({
    //   headers: await headers()
    // });
    //
    // if (!session) {
    //   return NextResponse.redirect(new URL("/sign-in", request.url));
    // }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*'], // Apply to protected routes
};
```

### 7. Usage in Components

Example login component:

```tsx
"use client";
import { authClient } from "@/lib/auth/client";
import { useState } from "react";

export function SignInForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await authClient.signIn.email({
        email,
        password,
      });
      // Redirect on success
      window.location.href = "/dashboard";
    } catch (err) {
      setError("Invalid credentials");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Sign In</button>
      {error && <p>{error}</p>}
    </form>
  );
}
```

### 8. OAuth Login Buttons

```tsx
"use client";
import { authClient } from "@/lib/auth/client";

export function OAuthButtons() {
  return (
    <div>
      <button
        onClick={() => authClient.signIn.social({
          provider: "google",
          callbackURL: "/dashboard"
        })}
      >
        Sign in with Google
      </button>

      <button
        onClick={() => authClient.signIn.social({
          provider: "github",
          callbackURL: "/dashboard"
        })}
      >
        Sign in with GitHub
      </button>
    </div>
  );
}
```

## Running the Application

1. Set up your Neon Serverless Postgres database
2. Configure OAuth applications with Google and GitHub
3. Add environment variables to your `.env` file
4. Run the application: `npm run dev`

## Next Steps

- Implement user profile pages
- Add session management features
- Set up email verification (if required)
- Configure additional security measures
- Add unit and integration tests