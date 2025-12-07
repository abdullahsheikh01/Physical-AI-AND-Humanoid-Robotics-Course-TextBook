import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Main navigation sidebar for the Physical AI & Humanoid Robotics E-book
  tutorialSidebar: [
    {
     
      SAM:
      "FS"
      ,

      type: 'category',
      label: 'Introduction',
      items: ['intro/why-physical-ai-matters'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1/index',
        'module-1/ros2-nodes-topics-services',
        'module-1/bridging-python-agents-ros',
        'module-1/urdf-humanoids',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2/index',
        'module-2/gazebo-simulation',
        'module-2/unity-visualization',
        'module-2/sensor-simulation',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module-3/index',
        'module-3/isaac-sim',
        'module-3/isaac-ros',
        'module-3/nav2-path-planning',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4/index',
        'module-4/voice-to-action',
        'module-4/cognitive-planning',
        'module-4/capstone-project',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Weekly Breakdown',
      items: [
        'weekly-breakdown/weeks-1-2-intro',
        'weekly-breakdown/weeks-3-5-ros2',
        'weekly-breakdown/weeks-6-7-simulation',
        'weekly-breakdown/weeks-8-10-isaac',
        'weekly-breakdown/weeks-11-12-humanoid',
        'weekly-breakdown/week-13-conversational',
      ],
      collapsed: true,
    },
    {
      type: 'category',
      label: 'Assessments',
      items: [
        'assessments/ros2-project',
        'assessments/gazebo-implementation',
        'assessments/isaac-pipeline',
        'assessments/capstone-humanoid',
      ],
      collapsed: true,
    },
  ],
};

export default sidebars;
