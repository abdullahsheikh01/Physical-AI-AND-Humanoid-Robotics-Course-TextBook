# Data Model: Physical AI & Humanoid Robotics E-book

## Overview
This document describes the content structure and organization for the Physical AI & Humanoid Robotics E-book. Since this is a documentation site, the "data model" refers to the content organization and document structure.

## Content Entities

### E-book Content
- **Description**: The main educational material of the e-book
- **Attributes**:
  - title: string
  - content: markdown/MDX
  - module: reference to Module
  - week: integer (1-13)
  - prerequisites: array of content references
  - learningObjectives: array of strings
  - assessment: reference to Assessment
- **Relationships**: Belongs to one Module, belongs to one Week

### Module
- **Description**: Major content division covering specific aspects of Physical AI and Humanoid Robotics
- **Attributes**:
  - id: string (module-1, module-2, module-3, module-4)
  - title: string
  - description: string
  - learningObjectives: array of strings
  - duration: integer (weeks)
  - content: array of E-book Content references
  - assessments: array of Assessment references
- **Relationships**: Contains many E-book Content items, contains many Assessments

### Weekly Breakdown
- **Description**: Time-sequenced learning content spanning 13 weeks
- **Attributes**:
  - weekNumber: integer (1-13)
  - title: string
  - content: array of E-book Content references
  - learningObjectives: array of strings
  - duration: string (e.g., "Week 1-2", "Week 3-5")
- **Relationships**: Contains many E-book Content items

### Assessment
- **Description**: Practical evaluation components that validate user learning
- **Attributes**:
  - id: string
  - title: string
  - description: string
  - type: string (project, quiz, simulation)
  - module: reference to Module
  - requirements: array of strings
  - successCriteria: array of strings
- **Relationships**: Belongs to one Module

### Blog Post
- **Description**: Supplementary content like "Benefits to learn this Course?"
- **Attributes**:
  - id: string
  - title: string
  - date: date
  - authors: array of strings
  - content: markdown/MDX
  - tags: array of strings
- **Relationships**: Standalone entity

### User Interface Component
- **Description**: Custom Docusaurus components for enhanced functionality
- **Attributes**:
  - componentName: string
  - purpose: string
  - props: object
  - styling: CSS Module reference
- **Relationships**: Used in pages and content documents

## Content Structure Hierarchy

```
Physical AI & Humanoid Robotics E-book
├── Introduction: Why Physical AI Matters
├── Module 1: The Robotic Nervous System (ROS 2)
│   ├── Week 3-5: ROS 2 Fundamentals
│   └── Assessment: ROS 2 package development project
├── Module 2: The Digital Twin (Gazebo & Unity)
│   ├── Week 6-7: Robot Simulation with Gazebo
│   └── Assessment: Gazebo simulation implementation
├── Module 3: The AI-Robot Brain (NVIDIA Isaac™)
│   ├── Week 8-10: NVIDIA Isaac Platform
│   └── Assessment: Isaac-based perception pipeline
├── Module 4: Vision-Language-Action (VLA)
│   ├── Week 11-13: Humanoid Robot Development & Conversational Robotics
│   └── Assessment: Capstone - Simulated humanoid robot with conversational AI
└── Blog: Benefits to learn this Course?
```

## Navigation Model

### Main Navigation
- **Home**: Introduction and overview
- **Modules**: Links to 4 main modules
- **Weekly Breakdown**: Timeline view of 13 weeks
- **Assessments**: Collection of all assessments
- **Blog**: Supplementary content

### Sidebar Navigation
- **Module-based**: Each module has its own sidebar with:
  - Table of contents for the module
  - Week-by-week breakdown
  - Related assessments
  - Cross-references to other modules

## Content Relationships

### Cross-module References
- Technical concepts that span multiple modules
- Prerequisites between different weeks
- Building upon concepts from previous modules

### Assessment Dependencies
- Module-specific assessments
- Prerequisites for capstone project
- Progressive complexity from basic to advanced

## Content Validation Rules

### From Requirements
- Each module must have clearly defined learning objectives
- Weekly breakdowns must provide structured learning paths
- Assessments must validate practical skills
- Content must be accessible across all devices
- Dark/light mode must be supported
- Robotic theme must be consistently applied