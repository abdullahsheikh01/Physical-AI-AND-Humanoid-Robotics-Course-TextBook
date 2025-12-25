<!--
Sync Impact Report:
- Version change: 1.1.0 → 1.2.0
- Modified principles: Added new principles for authentication standards
- Added sections: Better-Auth User Management, Data Privacy Compliance, Session Management for Logout, Neon Serverless Postgres Integration with pg Pool
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

### Better-Auth User Management
User authentication and management must be implemented using Better-Auth, a framework-agnostic authentication and authorization library for TypeScript. Better-Auth must be used for all user-related operations including registration, login, password management, and user profile management. The authentication system must support multiple authentication methods including email/password, social logins, and optional two-factor authentication.
<!-- Rationale: Better-Auth provides a comprehensive, secure, and extensible authentication framework with built-in security features and plugin ecosystem -->

### Data Privacy Compliance
All user data handling must comply with applicable data privacy regulations including GDPR, CCPA, and other relevant privacy laws. User data must be encrypted at rest and in transit. The system must implement proper data retention policies, provide users with data export and deletion capabilities, and maintain detailed audit logs of data access and modifications. All authentication and user management operations must follow privacy-by-design principles.
<!-- Rationale: Compliance with data privacy regulations is essential for protecting user information and maintaining trust in the educational platform -->

### Session Management for Logout
The authentication system must implement proper session management with secure logout functionality. Sessions must have appropriate expiration times and support both automatic and manual logout. The system must properly invalidate session tokens on logout and prevent session replay attacks. Long-lived sessions must be configurable with appropriate security measures.
<!-- Rationale: Proper session management ensures user security and privacy by preventing unauthorized access to user accounts -->

### Neon Serverless Postgres Integration with pg Pool
Database operations must use Neon Serverless Postgres as the primary database solution with direct integration using pg Pool for connection management. The system must implement efficient connection pooling to handle concurrent database operations while maintaining low latency. Database queries must be properly parameterized to prevent SQL injection, and the connection pool must be configured with appropriate limits and timeouts for optimal performance.
<!-- Rationale: Neon Serverless Postgres provides scalable, serverless database capabilities with automatic scaling, while pg Pool ensures efficient and secure database connection management -->

## Content Integrity and Plagiarism Prevention
All content must be original work or properly attributed to original sources. Automated plagiarism detection tools must be used during content creation and updates. All technical claims, data, and concepts must be verified against authoritative sources in the field of Physical AI and Humanoid Robotics. Any reproduced content must include proper attribution and comply with copyright requirements.

## Development Workflow and Quality Gates
All code changes must pass responsive design testing across multiple device sizes before merging. Content changes must undergo fact-checking validation. Styling changes must be verified to use only CSS Modules and not violate the Tailwind CSS constraint. All pull requests must include verification of compliance with the core principles before approval. For chatbot features, additional testing must include API endpoint validation, agent response accuracy, and integration testing between frontend and backend components. For authentication features, additional testing must include security validation, user management workflows, and database integration testing.

## Governance

All development and content creation must comply with this constitution. Any changes to the core principles require formal amendment procedures with stakeholder approval. Code reviews must verify compliance with all principles, particularly the styling constraints and technical requirements. The project team must use this constitution as the authoritative guide for all technical and content decisions. New features like the chatbot must undergo additional architectural review to ensure they align with the overall project goals and maintain system integrity. Authentication-related features must undergo security review to ensure compliance with the Better-Auth and data privacy principles.

**Version**: 1.2.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-25
