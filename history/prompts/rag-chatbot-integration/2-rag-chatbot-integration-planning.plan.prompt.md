---
id: 2
title: rag-chatbot-integration-planning
stage: plan
date: 2025-12-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-chatbot-integration
branch: 001-rag-chatbot-integration
user: Claude Code
command: /sp.plan
labels: ["plan", "chatbot", "rag", "architecture"]
links:
  spec: specs/001-rag-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot-integration/plan.md
  - specs/001-rag-chatbot-integration/research.md
  - specs/001-rag-chatbot-integration/data-model.md
  - specs/001-rag-chatbot-integration/quickstart.md
  - specs/001-rag-chatbot-integration/contracts/openapi.yaml
tests: []
---

## Prompt

```
Your task is to generate a complete, step-by-step development plan for specification written in spec.md that includes:

- System architecture plan

- Frontend development plan

- Agentic Backend development plan consists of:

    - RAG pipeline plan (Cohere + Qdrant + Gemini)

    - Agent implementation plan using OpenAI Agents SDK Python

    - FastAPI connectivity and streaming plan
```

## Response

```
# Implementation Plan: RAG Chatbot Integration

**Branch**: `001-rag-chatbot-integration` | **Date**: 2025-12-08 | **Spec**: [RAG Chatbot Integration Spec](./spec.md)
**Input**: Feature specification from `/specs/001-rag-chatbot-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Retrieval-Augmented Generation (RAG) chatbot system that integrates with the Physical AI & Humanoid Robotics E-book frontend. The system consists of a React-based chatbot widget positioned at the bottom right of the website, with a backend powered by Cohere embeddings, Qdrant vector database, and Gemini 2.0 Flash model. The backend utilizes OpenAI Agents SDK Python to create an intelligent agent that retrieves context before answering, with responses streamed via FastAPI connectivity.

## Technical Context

**Language/Version**: Python 3.11 (Backend), JavaScript/TypeScript (Frontend)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Cohere, Qdrant, React
**Storage**: Qdrant vector database, potential local storage for session data
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application (Linux server for backend, cross-browser for frontend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Response generation time under 5 seconds for 95% of queries, support 100 concurrent users
**Constraints**: <2 second p95 latency for response generation, maintain conversation history, streaming responses
**Scale/Scope**: Support 100 concurrent users, handle various query types related to Physical AI and Humanoid Robotics content

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **✓ Docusaurus Frontend Compliance**: Chatbot widget will integrate with existing Docusaurus frontend as a React component
- **✓ CSS Modules Styling**: Widget styling will use CSS Modules as required, no Tailwind CSS
- **✓ OpenAI Agents SDK**: Backend will implement agentic logic using OpenAI Agents SDK as specified
- **✓ FastAPI Integration**: All backend endpoints will use FastAPI framework as required
- **✓ Content Integrity**: Responses will be based on verified Physical AI and Humanoid Robotics content

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── chat_models.py          # Data models for chat entities
│   │   └── embedding_models.py     # Models for embeddings and vector storage
│   ├── services/
│   │   ├── embedding_service.py    # Cohere integration for embeddings
│   │   ├── vector_db_service.py    # Qdrant vector database operations
│   │   ├── llm_service.py          # Gemini model integration
│   │   ├── rag_service.py          # RAG pipeline implementation
│   │   ├── agent_service.py        # OpenAI Agents SDK implementation
│   │   └── session_service.py      # Conversation session management
│   ├── api/
│   │   ├── v1/
│   │   │   ├── chat.py             # Chat endpoints
│   │   │   ├── embeddings.py       # Embedding endpoints
│   │   │   └── health.py           # Health check endpoints
│   │   └── __init__.py
│   ├── agents/
│   │   └── rag_agent.py            # Custom RAG agent implementation
│   ├── config/
│   │   └── settings.py             # Configuration settings
│   └── main.py                     # FastAPI application entry point
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/
│   │   └── ChatbotWidget/
│   │       ├── ChatbotWidget.jsx   # Main chatbot widget component
│   │       ├── ChatWindow.jsx      # Chat interface window
│   │       ├── ChatButton.jsx      # "Ask me" button component
│   │       ├── Message.jsx         # Individual message component
│   │       └── styles.module.css   # CSS Modules styling
│   ├── services/
│   │   └── apiService.js           # API communication layer
│   └── hooks/
│       └── useChat.js              # Chat functionality hooks
└── tests/
    ├── unit/
    └── integration/
```

**Structure Decision**: Selected Option 2 (Web application) to separate frontend and backend concerns. The frontend will integrate with the existing Docusaurus setup as a React component, while the backend will be a dedicated FastAPI application handling the RAG pipeline and agent functionality.

## System Architecture Plan

The RAG Chatbot system follows a microservice architecture pattern with clear separation between frontend and backend components:

### Frontend Architecture
- **React Component**: A self-contained ChatbotWidget component that integrates with Docusaurus
- **State Management**: Local React state for UI interactions and conversation history
- **API Communication**: FastAPI endpoints for sending queries and receiving streaming responses
- **Styling**: CSS Modules to comply with project constitution

### Backend Architecture
- **FastAPI Application**: RESTful API endpoints for chat functionality
- **RAG Pipeline**: Cohere embeddings → Qdrant vector search → Gemini response generation
- **Agent Layer**: OpenAI Agents SDK managing conversation flow and context retrieval
- **Streaming**: Server-Sent Events or WebSocket for streaming responses to frontend

### Data Flow
1. User submits query via chatbot widget
2. Frontend sends query to FastAPI backend
3. Backend processes query through RAG pipeline:
   - Generate embeddings using Cohere
   - Search Qdrant vector database for relevant chunks
   - Use OpenAI Agent with Gemini model to generate contextual response
4. Response streamed back to frontend via FastAPI
5. Conversation history maintained in session

## Frontend Development Plan

### Phase 1: Component Structure
1. **Create ChatbotWidget Component**
   - Position at bottom right of website (fixed positioning)
   - Implement pop-up and close functionality
   - Design clean, modern UI that matches website theme
   - Create "Ask me" button visible when widget is minimized

2. **Design UI Components**
   - Chat window with message history display
   - Input area with text field and send button
   - Loading indicators for response generation
   - Error handling display

3. **Implement CSS Modules Styling**
   - Create styles.module.css following project constitution
   - Ensure responsive design across device sizes
   - Maintain accessibility standards

### Phase 2: Functionality Implementation
1. **API Integration**
   - Implement service layer for FastAPI communication
   - Create hooks for chat functionality (useChat)
   - Handle streaming responses from backend

2. **State Management**
   - Manage conversation history in component state
   - Handle opening/closing of chat window
   - Preserve session across page navigation

3. **User Experience Features**
   - Typing indicators during response generation
   - Message history persistence
   - Smooth animations for open/close actions

## Agentic Backend Development Plan

### RAG Pipeline Plan (Cohere + Qdrant + Gemini)

1. **Embedding Service Setup**
   - Integrate Cohere API for text embedding generation
   - Implement embedding preprocessing and normalization
   - Create utility functions for embedding operations

2. **Vector Database Integration**
   - Set up Qdrant vector database connection
   - Implement document indexing and retrieval functions
   - Configure similarity search parameters and thresholds

3. **Knowledge Base Processing**
   - Create document ingestion pipeline for Physical AI content
   - Implement chunking strategy for content segmentation
   - Set up embedding generation and storage for knowledge base

4. **RAG Service Implementation**
   - Implement query processing and embedding generation
   - Create vector search functionality to retrieve relevant chunks
   - Design context formatting for LLM consumption

### Agent Implementation Plan using OpenAI Agents SDK Python

1. **Agent Architecture Design**
   - Create custom agent class inheriting from OpenAI Agent framework
   - Implement required context retrieval before response generation
   - Design memory management for conversation history

2. **Tool Integration**
   - Create custom tools for RAG pipeline access
   - Implement retrieval tool for fetching relevant context
   - Design response validation tools

3. **Streaming Implementation**
   - Use Runner.run_streamed method for response streaming
   - Implement proper event handling for stream management
   - Create middleware for stream processing and formatting

4. **Safety and Validation**
   - Implement response validation and filtering
   - Add content moderation tools
   - Create fallback mechanisms for edge cases

### FastAPI Connectivity and Streaming Plan

1. **API Endpoint Design**
   - Create /chat endpoint for query submission and response streaming
   - Implement /health endpoint for system monitoring
   - Design /embeddings endpoint for embedding operations

2. **Streaming Response Implementation**
   - Use FastAPI's StreamingResponse for server-sent events
   - Implement proper connection management
   - Handle client disconnections gracefully

3. **Session Management**
   - Create session tracking for conversation history
   - Implement session persistence mechanisms
   - Design session cleanup and timeout handling

4. **Error Handling and Logging**
   - Implement comprehensive error handling
   - Add logging for debugging and monitoring
   - Create structured error responses for frontend

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple service architecture | RAG pipeline requires separate embedding, vector DB, and LLM services | Single service would create tight coupling and scalability issues |
| External API dependencies | Cohere, Qdrant, and Gemini are specified requirements | Internal alternatives don't meet performance/quality requirements specified |
```

## Outcome

Successfully created a comprehensive implementation plan for the RAG Chatbot Integration feature. The plan includes:

1. Complete system architecture plan with frontend and backend components
2. Detailed frontend development plan for the React-based chatbot widget
3. Comprehensive backend development plan covering:
   - RAG pipeline implementation using Cohere, Qdrant, and Gemini
   - Agent implementation using OpenAI Agents SDK Python
   - FastAPI connectivity and streaming implementation

The plan also includes technical context, project structure, constitution check, data models, API contracts, and quickstart guide. All components are designed to comply with the project constitution requirements including CSS Modules styling and Docusaurus integration.