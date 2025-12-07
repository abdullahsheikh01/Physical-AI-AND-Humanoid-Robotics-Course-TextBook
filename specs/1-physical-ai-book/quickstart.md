# Quickstart Guide: Physical AI & Humanoid Robotics E-book

## Overview
This guide provides a quick setup and development workflow for the Physical AI & Humanoid Robotics E-book built with Docusaurus.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Git for version control
- Text editor or IDE

## Setup Instructions

### 1. Clone and Initialize
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Navigate to website directory
cd website

# Install dependencies
npm install
```

### 2. Local Development
```bash
# Start development server
npm run start

# Open http://localhost:3000 to view the e-book
```

### 3. Project Structure
```
website/
├── blog/                    # Blog posts (e.g., "Benefits to learn this Course?")
├── docs/                    # Main e-book content
│   ├── intro/              # Introduction content
│   ├── module-1/           # Module 1: The Robotic Nervous System (ROS 2)
│   ├── module-2/           # Module 2: The Digital Twin (Gazebo & Unity)
│   ├── module-3/           # Module 3: The AI-Robot Brain (NVIDIA Isaac™)
│   ├── module-4/           # Module 4: Vision-Language-Action (VLA)
│   └── weekly-breakdown/   # Week-by-week content
├── src/
│   ├── components/         # Custom React components with CSS Modules
│   ├── css/               # Global styles
│   └── theme/             # Custom theme overrides
├── static/                # Static assets (images, etc.)
├── docusaurus.config.js   # Main configuration
└── sidebars.js           # Navigation configuration
```

## Adding Content

### 1. Adding a New Page
```bash
# Create a new MDX file in the appropriate module directory
# Example: website/docs/module-1/ros2-nodes.mdx
```

### 2. Creating a New Module Section
1. Create a new directory in `website/docs/module-X/`
2. Add MDX files for each topic
3. Update `website/sidebars.js` to include the new content in navigation

### 3. Using Custom Components
```mdx
import {ThemeToggle} from '@site/src/components/ThemeToggle';
import {Assessment} from '@site/src/components/Assessment';

# ROS 2 Nodes

<ThemeToggle />

<Assessment
  title="Node Implementation"
  description="Create a basic ROS 2 node"
  requirements={["Create publisher", "Create subscriber"]}
/>
```

## Styling with CSS Modules

### Creating a Custom Component with CSS Modules
```jsx
// website/src/components/RoboticTheme/RoboticTheme.jsx
import React from 'react';
import styles from './RoboticTheme.module.css';

export default function RoboticTheme({children}) {
  return <div className={styles.roboticContainer}>{children}</div>;
}
```

```css
/* website/src/components/RoboticTheme/RoboticTheme.module.css */
.roboticContainer {
  border: 2px solid #0066cc;
  border-radius: 8px;
  padding: 16px;
  background-color: var(--ifm-color-emphasis-100);
  margin: 16px 0;
}
```

## Dark/Light Mode Toggle
The site includes a built-in dark/light mode toggle that can be added to any page:
```mdx
import BrowserOnly from '@docusaurus/BrowserOnly';

<BrowserOnly>
  {() => {
    const DarkLightToggle = require('@theme/ColorModeToggle').default;
    return <DarkLightToggle className="navbar__toggle" />;
  }}
</BrowserOnly>
```

## Building for Production
```bash
# Build the static site
npm run build

# The output will be in the build/ directory
# Deploy the contents of build/ to your web server
```

## Common Commands

| Command | Description |
|---------|-------------|
| `npm run start` | Start local development server |
| `npm run build` | Build static site for production |
| `npm run serve` | Serve the built site locally |
| `npm run deploy` | Deploy to GitHub Pages (if configured) |

## Content Creation Guidelines

### Module Structure
Each module should include:
- Learning objectives
- Technical concepts with examples
- Practical exercises
- Assessment components
- Cross-references to related content

### Weekly Breakdown
- Each week should have 2-3 focused topics
- Include practical examples and exercises
- Link to relevant assessments
- Provide clear learning objectives

### Assessments
- Include clear requirements and success criteria
- Provide examples or templates where appropriate
- Link to relevant module content
- Include submission guidelines