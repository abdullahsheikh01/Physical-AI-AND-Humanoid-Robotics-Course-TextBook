---
sidebar_position: 1
title: Content Creation Guidelines
---

# Content Creation Guidelines

This document provides guidelines for creating new content for the Physical AI & Humanoid Robotics E-book. Follow these guidelines to ensure consistency, quality, and maintainability of the course materials.

## Table of Contents

- [Content Structure](#content-structure)
- [Writing Style](#writing-style)
- [Code Examples](#code-examples)
- [Images and Media](#images-and-media)
- [Cross-References](#cross-references)
- [Accessibility](#accessibility)
- [SEO Best Practices](#seo-best-practices)
- [Review Process](#review-process)

## Content Structure

### File Organization

```
website/
├── docs/
│   ├── intro/                 # Introduction content
│   ├── module-1/              # Module 1: The Robotic Nervous System (ROS 2)
│   ├── module-2/              # Module 2: The Digital Twin (Gazebo & Unity)
│   ├── module-3/              # Module 3: The AI-Robot Brain (NVIDIA Isaac™)
│   ├── module-4/              # Module 4: Vision-Language-Action (VLA)
│   ├── weekly-breakdown/      # Weekly content from Weeks 1-2 to Week 13
│   ├── assessments/           # Assessment materials
│   └── guidelines/            # This document and other guidelines
```

### Document Template

Each document should follow this template:

```markdown
---
sidebar_position: [number]
title: "[Title]"
---

# [Title]

## Learning Objectives

By the end of this lesson, you will be able to:
- [Objective 1]
- [Objective 2]
- [Objective 3]

## Introduction

[Overview of the topic and its importance]

## [Main Section 1]

[Content for the first main section]

### Subsection

[Detailed content for subsection]

## [Main Section 2]

[Content for the second main section]

## Best Practices

[Important recommendations and best practices]

## Hands-On Exercise

[Practical exercise for the learner]

## Summary

[Recap of key points covered]

## Next Steps

[What comes next in the learning path]

## Cross-References

- [Related content in the course]
- [External resources]
```

## Writing Style

### Tone and Voice

- Use an informative, professional tone that is accessible to learners
- Write in active voice wherever possible
- Use second person ("you") to address the reader directly
- Avoid jargon or explain it when necessary

### Formatting

- Use proper heading hierarchy (H1, H2, H3, etc.)
- Keep paragraphs short (2-4 sentences)
- Use bullet points and numbered lists for clarity
- Bold important terms when introducing them

### Technical Content

- Provide context before diving into technical details
- Use analogies to explain complex concepts
- Include practical examples alongside theory
- Anticipate common questions and address them

## Code Examples

### Syntax Highlighting

Always use proper syntax highlighting:

```python
# Good example
def example_function():
    """This is a well-documented function."""
    return "Hello, World!"
```

### Code Structure

- Include comments explaining complex code
- Use meaningful variable names
- Break complex examples into smaller chunks
- Show both successful and error scenarios when relevant

### Inline Code

Use inline code for specific terms: `ROS 2`, `rclpy`, `differential_drive`.

## Images and Media

### Image Alt Text

Always include descriptive alt text for images:

```markdown
![Diagram showing ROS 2 node architecture with publishers and subscribers](./assets/ros2-architecture.png)
```

### Image Captions

Add captions for complex diagrams:

```markdown
![Flowchart of cognitive planning process](./assets/planning-flowchart.png)

*Figure 1: The cognitive planning process translates natural language commands into robot actions.*
```

### File Sizes

- Optimize images for web (under 500KB when possible)
- Use appropriate formats (PNG for diagrams, JPEG for photos)
- Use WebP format when browser support allows

## Cross-References

### Internal Links

Use relative paths for internal links:

```markdown
[Module 1: The Robotic Nervous System (ROS 2)](/docs/module-1/intro)
[Weeks 1-2: Introduction to Physical AI](/docs/weekly-breakdown/weeks-1-2)
```

### Navigation

Include relevant cross-references at the bottom of each document:

```markdown
## Cross-References

- [Module 1 Introduction](/docs/module-1/intro)
- [ROS 2 Nodes, Topics, and Services](/docs/module-1/ros2-nodes-topics-services)
- [Weeks 3-5: ROS 2 Fundamentals](/docs/weekly-breakdown/weeks-3-5)
```

## Accessibility

### Headings

- Use proper heading hierarchy
- Don't skip heading levels
- Make headings descriptive

### Links

- Use descriptive link text
- Indicate if links open in new tabs
- Ensure sufficient color contrast

### Images

- Provide meaningful alt text
- Avoid using images to convey critical information alone
- Include transcripts for audio/video content

## SEO Best Practices

### Titles

- Keep titles under 60 characters
- Include relevant keywords
- Make titles descriptive and compelling

### Meta Descriptions

- Write unique descriptions for each page
- Keep descriptions under 160 characters
- Include primary keywords

### Keywords

- Include relevant keywords naturally
- Don't over-optimize (keyword stuffing)
- Focus on terms your audience would search for

## Review Process

### Self-Review Checklist

Before submitting new content, ensure:

- [ ] Learning objectives are clear and achievable
- [ ] Content is technically accurate
- [ ] Code examples are tested and functional
- [ ] Images are properly formatted and captioned
- [ ] Cross-references are accurate
- [ ] Content follows the established structure
- [ ] Grammar and spelling are correct
- [ ] Accessibility guidelines are followed

### Peer Review

All content should undergo peer review focusing on:
- Technical accuracy
- Clarity and accessibility
- Completeness
- Consistency with course style

## Common Mistakes to Avoid

- Providing outdated information
- Using inconsistent terminology
- Including broken links or images
- Forgetting to update navigation
- Neglecting to test code examples
- Ignoring accessibility requirements

## Questions

If you have questions about content creation, contact the course maintainers or refer to the contributor documentation.

---

*Last updated: 2025-12-07*