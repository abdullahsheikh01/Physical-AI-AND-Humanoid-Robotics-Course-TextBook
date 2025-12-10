---
description: "Task list for RAG Chatbot Backend Implementation"
---

# Tasks: RAG Chatbot Backend

**Input**: Design documents from `/specs/001-rag-chatbot-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No explicit testing requirements in the feature specification.
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` at repository root
- **FastAPI app**: `backend/fastapi_app.py`
- **Agent backend**: `backend/agentic_backend.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with backend directory
- [X] T002 Install required dependencies (FastAPI, OpenAI Agents SDK, Cohere, Qdrant, python-dotenv)
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create agentic_backend.py file with basic structure
- [X] T005 [P] Load Environment Variables using `load_dotenv` of `dotenv` in agentic_backend.py
- [X] T006 [P] Write Python code that begins by disabling tracing using the set_tracing_disabled function from the OpenAI Agents SDK by setting the disabled parameter to True. Then load the Gemini API key from the environment using os.getenv and store it in a variable named gemini_api_key. After that, initialize an asynchronous OpenAI-compatible provider using the AsyncOpenAI class from the OpenAI Agents SDK, passing the Gemini API key to the api_key parameter and setting the base_url to the Gemini-compatible endpoint at "https://generativelanguage.googleapis.com/v1beta/openai/". Finally, create a chat completion model instance using the OpenAIChatCompletionsModel class from the OpenAI Agents SDK, specifying "gemini-2.0-flash" as the model name and passing the previously created provider instance to the openai_client parameter. The code should be clean, direct, and focused on correctly configuring the Gemini model through the OpenAI Agents SDK in agentic_backend.py
- [X] T007 [P] Write Python code that initializes a Cohere client by creating an instance of cohere.Client and passing the API key string as the constructor argument. After setting up the Cohere client, create a Qdrant connection by instantiating a QdrantClient object, providing the Qdrant URL through the url parameter and supplying the API key through the api_key parameter. The code should clearly establish both the Cohere client and the Qdrant client so they can be used later for embedding generation and vector search operations in agentic_backend.py
- [X] T008 [P] Write a Python function named `get_embedding` that uses the Cohere Python client to generate an embedding vector using the Cohere Embed v3 model. The function should accept a text string as input and call the Cohere client's embed method using the model name "embed-english-v3.0" and the input_type set to "search_query." The function should pass the input text inside a list to the texts parameter. After receiving the response, the function should return only the first embedding from the response object. The structure should be clean, include a short docstring explaining that the function returns an embedding vector using Cohere Embed v3, and handle everything in a simple, readable way in agentic_backend.py
- [X] T009 [P] Write a Python function decorated with the `@function_tool` decorator from the OpenAI Agents SDK. The function should be named `retrieve` and accept a single parameter called `query`. Inside the function, call an existing get_embedding function to generate an embedding for the query. Then perform a vector search using a Qdrant client instance named qdrant by calling its query_points method with the collection name "humanoid_ai_book," the generated embedding as the query vector, and a limit of 5 results. After receiving the search results, extract the "text" field from the payload of each returned point and return these extracted text strings as a list. The function should be concise, readable, and focused on retrieval based on embeddings in agentic_backend.py
- [X] T010 [P] Write Python code that creates an instance of the Agent class from the OpenAI Agents SDK. The agent should be named "Assistant" and include a multi-line instruction string explaining that it is an AI tutor for the Physical AI & Humanoid Robotics textbook. The instructions must tell the agent to always call the retrieve tool first with the user's question, to answer only using the content returned by that tool, and to respond with "I don't know" if the relevant information is not present in the retrieved results. Pass the previously initialized model instance to the model parameter, and provide the retrieve function as the only entry in the tools list. The created agent should be cleanly structured and ready to be used by a runner in agentic_backend.py
- [X] T011 [P] Write a Python function named `run_agent` that synchronously runs the previously created agent using the Runner.run_sync method from the OpenAI Agents SDK. The function should call Runner.run_sync by passing the agent instance as the first argument and providing a variable named INPUTFROMFASTAPI as the value of the input parameter, representing the incoming message from a FastAPI endpoint. The function should store the result returned by the runner in a variable and return that result. The implementation should be simple and focused solely on executing the agent with the incoming FastAPI input in agentic_backend.py
- [X] T012 Create fastapi_app.py with basic FastAPI structure
- [X] T013 [P] Add CORS middleware to FastAPI application in fastapi_app.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Chatbot Widget (Priority: P1) 🎯 MVP

**Goal**: Create a FastAPI which receives input from frontend and gives response by using `agentic_backend`'s function `run_agent`.

**Independent Test**: Can be fully tested by submitting a query to the FastAPI endpoint and verifying it calls the agentic_backend's run_agent function and returns a response.

### Implementation for User Story 1

- [X] T014 [US1] Create a FastAPI which receives input from frontend and give response by using `agentic_backend`'s function `run_agent` in fastapi_app.py
- [X] T015 [US1] Implement request/response validation models in fastapi_app.py
- [X] T016 [US1] Add error handling for chat endpoint in fastapi_app.py
- [X] T017 [US1] Implement health check endpoint in fastapi_app.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T018 Add comprehensive logging to both backend files
- [ ] T019 [P] Documentation updates in docs/
- [ ] T020 Code cleanup and refactoring
- [ ] T021 Performance optimization
- [ ] T022 Security hardening
- [ ] T023 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational tasks together:
Task: "Load Environment Variables using load_dotenv of dotenv in agentic_backend.py"
Task: "Configure OpenAI-compatible provider with Gemini API in agentic_backend.py"
Task: "Initialize Cohere and Qdrant clients in agentic_backend.py"
Task: "Implement get_embedding function using Cohere in agentic_backend.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
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