import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug/',
    component: ComponentCreator('/__docusaurus/debug/', '546'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config/',
    component: ComponentCreator('/__docusaurus/debug/config/', '8a8'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content/',
    component: ComponentCreator('/__docusaurus/debug/content/', '2da'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData/',
    component: ComponentCreator('/__docusaurus/debug/globalData/', '178'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata/',
    component: ComponentCreator('/__docusaurus/debug/metadata/', 'd6c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry/',
    component: ComponentCreator('/__docusaurus/debug/registry/', '6e3'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes/',
    component: ComponentCreator('/__docusaurus/debug/routes/', 'cab'),
    exact: true
  },
  {
    path: '/404/',
    component: ComponentCreator('/404/', 'b69'),
    exact: true
  },
  {
    path: '/blog/',
    component: ComponentCreator('/blog/', '7dc'),
    exact: true
  },
  {
    path: '/blog/2025/01/01/benefits-of-physical-ai-course/',
    component: ComponentCreator('/blog/2025/01/01/benefits-of-physical-ai-course/', 'b51'),
    exact: true
  },
  {
    path: '/blog/archive/',
    component: ComponentCreator('/blog/archive/', '1d9'),
    exact: true
  },
  {
    path: '/blog/authors/',
    component: ComponentCreator('/blog/authors/', '347'),
    exact: true
  },
  {
    path: '/blog/authors/physical-ai-team/',
    component: ComponentCreator('/blog/authors/physical-ai-team/', 'cce'),
    exact: true
  },
  {
    path: '/blog/tags/',
    component: ComponentCreator('/blog/tags/', 'e17'),
    exact: true
  },
  {
    path: '/blog/tags/ai/',
    component: ComponentCreator('/blog/tags/ai/', '5e6'),
    exact: true
  },
  {
    path: '/blog/tags/education/',
    component: ComponentCreator('/blog/tags/education/', '065'),
    exact: true
  },
  {
    path: '/blog/tags/humanoid-robotics/',
    component: ComponentCreator('/blog/tags/humanoid-robotics/', 'a45'),
    exact: true
  },
  {
    path: '/blog/tags/physical-ai/',
    component: ComponentCreator('/blog/tags/physical-ai/', '54f'),
    exact: true
  },
  {
    path: '/blog/tags/robotics/',
    component: ComponentCreator('/blog/tags/robotics/', 'fd0'),
    exact: true
  },
  {
    path: '/markdown-page/',
    component: ComponentCreator('/markdown-page/', '54d'),
    exact: true
  },
  {
    path: '/tags/',
    component: ComponentCreator('/tags/', 'cc3'),
    exact: true
  },
  {
    path: '/docs/',
    component: ComponentCreator('/docs/', '48b'),
    routes: [
      {
        path: '/docs/',
        component: ComponentCreator('/docs/', '206'),
        routes: [
          {
            path: '/docs/',
            component: ComponentCreator('/docs/', '10a'),
            routes: [
              {
                path: '/docs/assessments/',
                component: ComponentCreator('/docs/assessments/', '2fa'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/assessments/capstone-humanoid/',
                component: ComponentCreator('/docs/assessments/capstone-humanoid/', '255'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/assessments/gazebo-simulation/',
                component: ComponentCreator('/docs/assessments/gazebo-simulation/', '7e0'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/assessments/intro/',
                component: ComponentCreator('/docs/assessments/intro/', '875'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/assessments/isaac-perception/',
                component: ComponentCreator('/docs/assessments/isaac-perception/', 'b62'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/assessments/ros2-project/',
                component: ComponentCreator('/docs/assessments/ros2-project/', '2ed'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/guidelines/content-creation-guidelines/',
                component: ComponentCreator('/docs/guidelines/content-creation-guidelines/', 'cd0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro/',
                component: ComponentCreator('/docs/intro/', 'e44'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro/why-physical-ai-matters/',
                component: ComponentCreator('/docs/intro/why-physical-ai-matters/', '4e0'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-1/',
                component: ComponentCreator('/docs/module-1/', '3dd'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1/hands-on-examples/',
                component: ComponentCreator('/docs/module-1/hands-on-examples/', 'b4e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1/intro/',
                component: ComponentCreator('/docs/module-1/intro/', '52e'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-1/rclpy-bridge/',
                component: ComponentCreator('/docs/module-1/rclpy-bridge/', 'a97'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-1/ros2-nodes-topics-services/',
                component: ComponentCreator('/docs/module-1/ros2-nodes-topics-services/', '55f'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-1/urdf-humanoids/',
                component: ComponentCreator('/docs/module-1/urdf-humanoids/', 'b4c'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-2/',
                component: ComponentCreator('/docs/module-2/', 'ca2'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2/gazebo-physics-collisions/',
                component: ComponentCreator('/docs/module-2/gazebo-physics-collisions/', 'b3e'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-2/intro/',
                component: ComponentCreator('/docs/module-2/intro/', 'cf1'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-2/sensor-simulation/',
                component: ComponentCreator('/docs/module-2/sensor-simulation/', '924'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-2/sim-to-real/',
                component: ComponentCreator('/docs/module-2/sim-to-real/', '548'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2/unity-rendering-interaction/',
                component: ComponentCreator('/docs/module-2/unity-rendering-interaction/', '4a8'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-3/',
                component: ComponentCreator('/docs/module-3/', '72b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3/ai-control/',
                component: ComponentCreator('/docs/module-3/ai-control/', '273'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3/intro/',
                component: ComponentCreator('/docs/module-3/intro/', '529'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-3/isaac-ros/',
                component: ComponentCreator('/docs/module-3/isaac-ros/', '06f'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-3/isaac-sim/',
                component: ComponentCreator('/docs/module-3/isaac-sim/', '7a5'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-3/nav2-bipedal/',
                component: ComponentCreator('/docs/module-3/nav2-bipedal/', '158'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-4/',
                component: ComponentCreator('/docs/module-4/', 'c39'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4/capstone-project/',
                component: ComponentCreator('/docs/module-4/capstone-project/', '495'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-4/cognitive-planning/',
                component: ComponentCreator('/docs/module-4/cognitive-planning/', 'ba2'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-4/intro/',
                component: ComponentCreator('/docs/module-4/intro/', 'b64'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/module-4/multimodal-integration/',
                component: ComponentCreator('/docs/module-4/multimodal-integration/', '440'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4/voice-to-action/',
                component: ComponentCreator('/docs/module-4/voice-to-action/', '33a'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/weekly-breakdown/',
                component: ComponentCreator('/docs/weekly-breakdown/', '6e9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/weekly-breakdown/week-13/',
                component: ComponentCreator('/docs/weekly-breakdown/week-13/', '649'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/weekly-breakdown/weeks-1-2/',
                component: ComponentCreator('/docs/weekly-breakdown/weeks-1-2/', '7c2'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/weekly-breakdown/weeks-11-12/',
                component: ComponentCreator('/docs/weekly-breakdown/weeks-11-12/', 'cb5'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/weekly-breakdown/weeks-3-5/',
                component: ComponentCreator('/docs/weekly-breakdown/weeks-3-5/', '3a8'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/weekly-breakdown/weeks-6-7/',
                component: ComponentCreator('/docs/weekly-breakdown/weeks-6-7/', '347'),
                exact: true,
                sidebar: "physicalAISidebar"
              },
              {
                path: '/docs/weekly-breakdown/weeks-8-10/',
                component: ComponentCreator('/docs/weekly-breakdown/weeks-8-10/', '16e'),
                exact: true,
                sidebar: "physicalAISidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'e5f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
