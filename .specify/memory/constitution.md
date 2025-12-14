<!--
Sync Impact Report:
- Version change: 1.1.0 → 1.2.0
- Modified principles: Added Chat History Persistence principle for chatbot feature
- Added sections: Chat History Persistence
- Removed sections: None
- Templates requiring updates: ✅ updated - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics E-book Constitution

## Core Principles

### Physical AI & Humanoid Robotics Book Frontend
The frontend of the book must be built using Docusaurus (https://docusaurus.io/docs). All book functionality and navigation must leverage Docusaurus's built-in features and architecture patterns. This ensures consistent documentation structure, search capabilities, and deployment options.
<!-- Rationale: Docusaurus provides a proven, scalable solution for documentation sites with built-in features like versioning, search, and responsive design -->

### Book Content Structure
The book's content must contain 4 modules with weekly breakdowns and assessments based on the 4 modules. Each module must have clearly defined learning objectives, content sections, practical examples, and assessment components. Weekly breakdowns must provide structured learning paths that guide users through progressive complexity.
<!-- Rationale: Structured learning with clear modules and assessments ensures comprehensive coverage and measurable progress -->

### Code Quality and Responsiveness
The E-book's Docusaurus code must be clean and responsive across all devices. All components must follow responsive design principles, pass accessibility standards, and maintain consistent performance across desktop, tablet, and mobile devices. Code must follow clean architecture principles with clear separation of concerns.
<!-- Rationale: Responsive design ensures accessibility for all users regardless of device, while clean code promotes maintainability -->

### Styling Standards
Book styling must be implemented using CSS Modules only. No other CSS frameworks or methodologies may be used. All styling must be component-scoped using CSS Modules to prevent style conflicts and ensure maintainability.
<!-- Rationale: CSS Modules provide encapsulation and prevent style conflicts while maintaining simplicity in styling approach -->

### Content Integrity Standards
All content must have claims verified against sources, maintain zero plagiarism, and pass fact-checking review. All sources must be properly cited, and content accuracy must be validated through authoritative references. The book frontend must be responsive and maintain clean code standards.
<!-- Rationale: Academic integrity and accuracy are essential for an educational resource on advanced technical topics -->

### Constraint Compliance
Tailwind CSS must not be used anywhere in the project. All styling must adhere to CSS Modules as specified in the styling standards principle. Any third-party styling libraries must be evaluated for compliance with this constraint.
<!-- Rationale: Maintaining consistency with the specified styling approach and avoiding conflicting styling methodologies -->

### Chatbot Widget Component
The chatbot feature must be implemented as a React-based widget component that integrates seamlessly with the Docusaurus frontend. The widget must be responsive, accessible, and maintain consistent styling with the existing book design. The component should provide an intuitive interface for users to interact with the AI assistant functionality.
<!-- Rationale: A well-designed chatbot widget enhances user experience by providing interactive help and guidance within the educational context -->

### Agentic Backend Logic with OpenAI Agents SDK
The backend logic for the chatbot must utilize OpenAI's Agents SDK to implement intelligent, context-aware responses. The agentic system must be capable of understanding user queries related to Physical AI and Humanoid Robotics content, retrieving relevant information, and providing helpful responses. The implementation must follow best practices for agent design, including proper memory management, tool usage, and safety measures.
<!-- Rationale: Using OpenAI Agents SDK provides advanced AI capabilities that can understand and respond to complex technical queries related to the book content -->

### FastAPI Integration
Both frontend and backend components of the chatbot feature must connect through FastAPI as the primary API framework. FastAPI must be used for all backend endpoints, providing type safety, automatic API documentation, and high performance. The API layer must implement proper authentication, rate limiting, and error handling for production readiness.
<!-- Rationale: FastAPI provides excellent performance, automatic documentation, and type safety, making it ideal for connecting the chatbot frontend and backend components -->

### Chat History Persistence
The frontend chatbot widget must send the complete chat history to the FastAPI backend with each new message request. This ensures that the backend has full context of the conversation to provide coherent, contextually relevant responses. The frontend must maintain and transmit the entire conversation history including user messages and bot responses to enable proper contextual understanding by the agentic backend system.
<!-- Rationale: Complete chat history transmission enables the backend to maintain conversation context and provide more intelligent, coherent responses based on the full interaction history -->

## Content Integrity and Plagiarism Prevention
All content must be original work or properly attributed to original sources. Automated plagiarism detection tools must be used during content creation and updates. All technical claims, data, and concepts must be verified against authoritative sources in the field of Physical AI and Humanoid Robotics. Any reproduced content must include proper attribution and comply with copyright requirements.

## Development Workflow and Quality Gates
All code changes must pass responsive design testing across multiple device sizes before merging. Content changes must undergo fact-checking validation. Styling changes must be verified to use only CSS Modules and not violate the Tailwind CSS constraint. All pull requests must include verification of compliance with the core principles before approval. For chatbot features, additional testing must include API endpoint validation, agent response accuracy, and integration testing between frontend and backend components. Additionally, chat history persistence functionality must be validated to ensure complete conversation context is maintained.

## Governance

All development and content creation must comply with this constitution. Any changes to the core principles require formal amendment procedures with stakeholder approval. Code reviews must verify compliance with all principles, particularly the styling constraints and technical requirements. The project team must use this constitution as the authoritative guide for all technical and content decisions. New features like the chatbot must undergo additional architectural review to ensure they align with the overall project goals and maintain system integrity.

**Version**: 1.2.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-14
