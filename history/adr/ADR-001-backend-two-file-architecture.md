# ADR-001: Backend Architecture - Two-File Structure

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-09
- **Feature:** RAG Chatbot Integration
- **Context:** Need to establish a clean, maintainable backend architecture for the RAG chatbot that separates HTTP concerns from AI logic while ensuring scalability and testability.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Implement a two-file backend architecture consisting of:
- **FastAPI Handler** (`backend/main.py`): Handles HTTP requests/responses, CORS, validation, authentication, and logging
- **AI Agent Module** (`backend/agent.py`): Contains LLM provider (OpenAI-compatible Gemini), embeddings (Cohere), vector DB connection (Qdrant), retrieve tool, and agent execution logic

The FastAPI handler imports and dynamically calls the AI agent for each request, maintaining clear separation of concerns.

## Consequences

### Positive

- Clear separation of HTTP concerns vs AI logic, improving maintainability
- Simplified testing with isolated components for HTTP handling and AI functionality
- Reduced coupling between web framework and AI components
- Easier debugging and monitoring of individual components
- Scalable architecture that allows independent evolution of HTTP layer and AI logic
- Environment variable management centralized in the appropriate components

### Negative

- Potential complexity in inter-component communication
- Requires careful interface design between components
- May need additional abstraction layers for complex interactions
- Could lead to over-segmentation if requirements become more complex

## Alternatives Considered

**Monolithic Approach**: Single file containing both FastAPI endpoints and AI agent logic
- Why rejected: Would create tight coupling, reduce testability, and make maintenance difficult

**Multi-File Architecture**: Separate files for embeddings, vector DB, LLM, tools, and API endpoints
- Why rejected: Would introduce unnecessary complexity for a simple RAG chatbot, increasing cognitive load without proportional benefits

**Microservice Architecture**: Separate services for API handling and AI processing
- Why rejected: Premature optimization for a simple RAG chatbot, adding operational complexity without clear benefits

## References

- Feature Spec: specs/001-rag-chatbot-integration/spec.md
- Implementation Plan: specs/001-rag-chatbot-integration/plan.md
- Related ADRs: None
- Evaluator Evidence: history/prompts/001-rag-chatbot-integration/001-backend-architecture.spec.prompt.md