---
description: "Task list for RAG Chatbot with Delete History Feature Implementation"
---

# Tasks: RAG Chatbot with Delete History Feature

**Input**: Design documents from `/specs/001-rag-chatbot-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Feature**: RAG Chatbot with Delete History functionality

**Tests**: No explicit testing requirements in the feature specification.
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` at repository root
- **Frontend**: `website/src/components/ChatbotWidget/` for chatbot components
- **Services**: `website/src/services/` for API services

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure with backend and website directories
- [ ] T002 Install required dependencies (FastAPI, React, Docusaurus, OpenAI Agents SDK, Cohere, Qdrant, python-dotenv)
- [ ] T003 [P] Configure linting and formatting tools for both backend and frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create agentic_backend.py file with basic structure
- [ ] T005 [P] Load Environment Variables using `load_dotenv` of `dotenv` in agentic_backend.py
- [ ] T006 [P] Write Python code that begins by disabling tracing using the set_tracing_disabled function from the OpenAI Agents SDK by setting the disabled parameter to True. Then load the Gemini API key from the environment using os.getenv and store it in a variable named gemini_api_key. After that, initialize an asynchronous OpenAI-compatible provider using the AsyncOpenAI class from the OpenAI Agents SDK, passing the Gemini API key to the api_key parameter and setting the base_url to the Gemini-compatible endpoint at "https://generativelanguage.googleapis.com/v1beta/openai/". Finally, create a chat completion model instance using the OpenAIChatCompletionsModel class from the OpenAI Agents SDK, specifying "gemini-2.0-flash" as the model name and passing the previously created provider instance to the openai_client parameter. The code should be clean, direct, and focused on correctly configuring the Gemini model through the OpenAI Agents SDK in agentic_backend.py
- [ ] T007 [P] Write Python code that initializes a Cohere client by creating an instance of cohere.Client and passing the API key string as the constructor argument. After setting up the Cohere client, create a Qdrant connection by instantiating a QdrantClient object, providing the Qdrant URL through the url parameter and supplying the API key through the api_key parameter. The code should clearly establish both the Cohere client and the Qdrant client so they can be used later for embedding generation and vector search operations in agentic_backend.py
- [ ] T008 [P] Write a Python function named `get_embedding` that uses the Cohere Python client to generate an embedding vector using the Cohere Embed v3 model. The function should accept a text string as input and call the Cohere client's embed method using the model name "embed-english-v3.0" and the input_type set to "search_query." The function should pass the input text inside a list to the texts parameter. After receiving the response, the function should return only the first embedding from the response object. The structure should be clean, include a short docstring explaining that the function returns an embedding vector using Cohere Embed v3, and handle everything in a simple, readable way in agentic_backend.py
- [ ] T009 [P] Write a Python function decorated with the `@function_tool` decorator from the OpenAI Agents SDK. The function should be named `retrieve` and accept a single parameter called `query`. Inside the function, call an existing get_embedding function to generate an embedding for the query. Then perform a vector search using a Qdrant client instance named qdrant by calling its query_points method with the collection name "humanoid_ai_book," the generated embedding as the query vector, and a limit of 5 results. After receiving the search results, extract the "text" field from the payload of each returned point and return these extracted text strings as a list. The function should be concise, readable, and focused on retrieval based on embeddings in agentic_backend.py
- [ ] T010 [P] Write Python code that creates an instance of the Agent class from the OpenAI Agents SDK. The agent should be named "Assistant" and include a multi-line instruction string explaining that it is an AI tutor for the Physical AI & Humanoid Robotics textbook. The instructions must tell the agent to always call the retrieve tool first with the user's question, to answer only using the content returned by that tool, and to respond with "I don't know" if the relevant information is not present in the retrieved results. Pass the previously initialized model instance to the model parameter, and provide the retrieve function as the only entry in the tools list. The created agent should be cleanly structured and ready to be used by a runner in agentic_backend.py
- [ ] T011 [P] Write a Python function named `run_agent` that synchronously runs the previously created agent using the Runner.run_sync method from the OpenAI Agents SDK. The function should call Runner.run_sync by passing the agent instance as the first argument and providing a variable named INPUTFROMFASTAPI as the value of the input parameter, representing the incoming message from a FastAPI endpoint. The function should store the result returned by the runner in a variable and return that result. The implementation should be simple and focused solely on executing the agent with the incoming FastAPI input in agentic_backend.py
- [ ] T012 Create fastapi_app.py with basic FastAPI structure
- [ ] T013 [P] Add CORS middleware to FastAPI application in fastapi_app.py
- [ ] T014 [P] Create a FastAPI which receives input from frontend and give response by using `agentic_backend`'s function `run_agent` in fastapi_app.py
- [ ] T015 [P] Implement request/response validation models in fastapi_app.py
- [ ] T016 [P] Add error handling for chat endpoint in fastapi_app.py
- [ ] T017 [P] Implement health check endpoint in fastapi_app.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Chatbot Widget (Priority: P1) 🎯 MVP

**Goal**: Create a chatbot widget that appears at the bottom right of the website with an "Ask me" button that opens the chat interface.

**Independent Test**: Can be fully tested by clicking the "Ask me" button and verifying the chat interface opens, then submitting a question and receiving a response that demonstrates the RAG functionality.

### Implementation for User Story 1

- [ ] T018 [US1] Create ChatbotWidget React component in website/src/components/ChatbotWidget/ChatbotWidget.js
- [ ] T019 [P] [US1] Create CSS Modules styling for ChatbotWidget in website/src/components/ChatbotWidget/ChatbotWidget.module.css
- [ ] T020 [P] [US1] Create AskMeButton component that appears at bottom right of website
- [ ] T021 [P] [US1] Implement open/close functionality for the chat widget
- [ ] T022 [P] [US1] Create basic message display area in the chat widget
- [ ] T023 [P] [US1] Create input field and send button for user queries
- [ ] T024 [P] [US1] Integrate with API service to send queries to backend
- [ ] T025 [P] [US1] Display bot responses in the message area

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Get Contextually Relevant Answers (Priority: P1)

**Goal**: Ensure the system retrieves relevant information from the knowledge base before generating accurate, contextual responses.

**Independent Test**: Can be tested by asking specific questions about documented content and verifying that responses reference or incorporate information from the relevant knowledge base documents.

### Implementation for User Story 2

- [ ] T026 [US2] Enhance agent instructions to better utilize retrieved context
- [ ] T027 [P] [US2] Implement proper context formatting for the agent
- [ ] T028 [P] [US2] Add source citations to responses
- [ ] T029 [P] [US2] Improve retrieval quality by refining embedding and search parameters
- [ ] T030 [P] [US2] Add response validation to ensure answers are based on retrieved context

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - Experience Streaming Responses (Priority: P2)

**Goal**: Implement streaming responses that appear progressively rather than all at once.

**Independent Test**: Can be tested by submitting a query and observing that response text appears progressively rather than all at once.

### Implementation for User Story 3

- [ ] T031 [US3] Update agentic_backend.py to support streaming responses using Runner.run_streamed method
- [ ] T032 [P] [US3] Modify FastAPI endpoint to return streaming responses using StreamingResponse
- [ ] T033 [P] [US3] Update frontend to handle and display streaming responses progressively
- [ ] T034 [P] [US3] Add visual indicators for streaming state (e.g., typing indicators)

**Checkpoint**: At this point, User Story 3 should be fully functional and testable independently

---

## Phase 6: User Story 4 - Close Chat Interface (Priority: P2)

**Goal**: Allow users to close the chat interface while preserving conversation history.

**Independent Test**: Can be tested by opening the chat interface, then using the close functionality to hide it, and verifying it can be reopened to show the previous conversation.

### Implementation for User Story 4

- [ ] T035 [US4] Add close button functionality to the chat widget
- [ ] T036 [P] [US4] Implement state management to preserve conversation history when widget is closed
- [ ] T037 [P] [US4] Add reopen functionality that restores previous conversation
- [ ] T038 [P] [US4] Ensure "Ask me" button remains visible when chat is closed

**Checkpoint**: At this point, User Story 4 should be fully functional and testable independently

---

## Phase 7: User Story 5 - Clear Chat History (Priority: P2)

**Goal**: Implement a "Delete History" button in the chat widget header that clears all conversation history from frontend state with smooth fade-in animation.

**Independent Test**: Can be tested by opening the chat interface, sending some messages, clicking the "Delete History" button, and verifying that all conversation history is cleared from the frontend display and state.

### Implementation for User Story 5

- [x] T039 [US5] Create DeleteHistoryButton React component in website/src/components/ChatbotWidget/DeleteHistoryButton.js
- [x] T040 [P] [US5] Add the Delete History button to the chat widget header
- [x] T041 [P] [US5] Implement smooth fade-in animation for the Delete History button when widget opens
- [x] T042 [P] [US5] Add onClick handler to clear conversation history from frontend state
- [x] T043 [P] [US5] Implement visual feedback/confirmation when history is cleared
- [x] T044 [P] [US5] Ensure UI re-renders to reflect cleared history state
- [x] T045 [P] [US5] Verify that new messages start fresh without previous context
- [x] T046 [P] [US5] Handle edge case of deleting history during streaming responses
- [x] T047 [P] [US5] Add CSS Modules styling for DeleteHistoryButton in website/src/components/ChatbotWidget/DeleteHistoryButton.module.css

**Checkpoint**: At this point, User Story 5 should be fully functional and testable independently

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T048 Add comprehensive logging to both backend files
- [ ] T049 [P] Documentation updates in docs/
- [ ] T050 Code cleanup and refactoring
- [ ] T051 Performance optimization
- [ ] T052 Security hardening
- [ ] T053 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on User Story 1 for basic chat functionality
- **User Story 3 (P2)**: Depends on User Story 1 for basic chat functionality
- **User Story 4 (P2)**: Depends on User Story 1 for basic chat functionality
- **User Story 5 (P2)**: Depends on User Story 1 for basic chat functionality

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority
- Each story can be tested independently

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members
- Within each user story, tasks marked [P] can run in parallel

---

## Parallel Example: User Story 5 (Delete History)

```bash
# Launch all User Story 5 tasks together:
T039: Create DeleteHistoryButton React component
T040: Add Delete History button to widget header
T041: Implement smooth fade-in animation
T042: Add onClick handler to clear history
T043: Implement visual feedback
T044: Ensure UI re-renders properly
T045: Verify fresh conversation starts
T046: Handle edge case of deleting during streaming
T047: Add CSS Modules styling
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. **STOP and VALIDATE**: Test User Stories 1 & 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test with US1 → Deploy/Demo (Core functionality!)
4. Add User Stories 3, 4, 5 → Test each incrementally

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Stories 4 & 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Focus on completing US1 and US2 first for a functional MVP
- US5 (Delete History) can be implemented in parallel with other user stories once the basic widget exists