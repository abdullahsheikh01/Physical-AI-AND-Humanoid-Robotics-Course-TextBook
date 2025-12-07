---
id: 1
title: Create Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Dell
command: /sp.constitution
labels: [constitution,book,physical-ai,humanoid-robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Write a constitution according following for an E-book on "Physical AI & Humanoid Robotics":


## Core principles:
- Frontend of Book should be made using [Docusaurus](https://docusaurus.io/docs).
- Book's content should contain 4 modules and weekly-breakdown and assesments based on 4 modules.
- E-book's docusaurus code should be clean and responsive across all devices.
- Book's styling should be done with CSS Modules.

## Constraints:
- Do not use Tailwind CSS.

## Success criteria:
- All claims verified against sources
- Zero plagiarism detected
- Passes fact-checking review
- Book's frontend should be responsive and have a clean code

## Response snapshot

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

## Content Integrity and Plagiarism Prevention
All content in the E-book must be original work or properly attributed to original sources. Automated plagiarism detection tools must be used during content creation and updates. All technical claims, data, and concepts must be verified against authoritative sources in the field of Physical AI and Humanoid Robotics. Any reproduced content must include proper attribution and comply with copyright requirements.

## Development Workflow and Quality Gates
All code changes must pass responsive design testing across multiple device sizes before merging. Content changes must undergo fact-checking validation. Styling changes must be verified to use only CSS Modules and not violate the Tailwind CSS constraint. All pull requests must include verification of compliance with the core principles before approval.

## Governance

All development and content creation must comply with this constitution. Any changes to the core principles require formal amendment procedures with stakeholder approval. Code reviews must verify compliance with all principles, particularly the styling constraints and technical requirements. The project team must use this constitution as the authoritative guide for all technical and content decisions.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07

## Outcome

- ✅ Impact: Constitution created for Physical AI & Humanoid Robotics E-book project with 6 core principles and governance structure
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific constitution
- 🔁 Next prompts: Plan the book modules and content structure
- 🧠 Reflection: Constitution successfully incorporates all specified requirements including Docusaurus frontend, 4 modules structure, CSS Modules styling, and Tailwind CSS constraint

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All requirements implemented
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Create spec for the 4-book modules