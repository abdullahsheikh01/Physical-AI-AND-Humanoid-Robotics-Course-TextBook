---
id: 1
title: Integrate-better-auth
stage: plan
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: user-auth
branch: 001-user-auth
user: Dell
command: /sp.plan Integrate Better-Auth for auth: Use email/password as default, add Google and GitHub OAuth providers. Connect directly to Neon Serverless Postgres using pg Pool (no adapters like Kysely or Drizzle). Handle logout by invalidating sessions. Assume Next.js framework (adapt if needed); include setup for environment variables (e.g., NEON_CONNECTION_STRING, GOOGLE_CLIENT_ID). Use Context7 MCP to research and coordinate details on Better-Auth configuration with pg Pool, Neon connectivity (e.g., pooling for serverless), and best practices for secure auth in a textbook app. Research: Latest Better-Auth docs for direct Postgres integration via pg; Neon setup guides.
labels: [authentication, better-auth, neon, postgres, oauth, nextjs]
links:
  spec: specs/001-user-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-user-auth/plan.md
 - specs/001-user-auth/research.md
 - specs/001-user-auth/data-model.md
 - specs/001-user-auth/quickstart.md
 - specs/001-user-auth/contracts/auth-api.yaml
 - CLAUDE.md
tests:
---

## Prompt

Integrate Better-Auth for auth: Use email/password as default, add Google and GitHub OAuth providers. Connect directly to Neon Serverless Postgres using pg Pool (no adapters like Kysely or Drizzle). Handle logout by invalidating sessions. Assume Next.js framework (adapt if needed); include setup for environment variables (e.g., NEON_CONNECTION_STRING, GOOGLE_CLIENT_ID). Use Context7 MCP to research and coordinate details on Better-Auth configuration with pg Pool, Neon connectivity (e.g., pooling for serverless), and best practices for secure auth in a textbook app. Research: Latest Better-Auth docs for direct Postgres integration via pg; Neon setup guides.

## Response snapshot

Created comprehensive implementation plan for Better-Auth integration with Neon Serverless Postgres, including:

- Technical context with dependencies (Better-Auth v1.3.4, @neondatabase/serverless, pg, Next.js)
- Constitution check confirming compliance with project principles
- Detailed project structure for web application with backend/frontend separation
- Data models for User, Session, and Account entities
- API contracts for authentication endpoints
- Quickstart guide with setup steps and code examples
- Agent context updated with new technology information

## Outcome

- ✅ Impact: Complete plan for authentication system with Better-Auth and Neon Postgres
- 🧪 Tests: No tests required for this phase
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/auth-api.yaml
- 🔁 Next prompts: Ready for /sp.tasks to generate implementation tasks
- 🧠 Reflection: Plan addresses all requirements including OAuth providers, session management, and secure logout

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A