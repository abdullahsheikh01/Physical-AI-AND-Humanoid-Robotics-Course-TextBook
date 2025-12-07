---
sidebar_position: 1
title: Module 1 - The Robotic Nervous System (ROS 2)
---

# Module 1: The Robotic Nervous System (ROS 2)

## Overview

This module focuses on ROS 2 (Robot Operating System 2), the middleware that serves as the nervous system for robot control. ROS 2 provides the communication infrastructure that allows different components of a robot to work together seamlessly.

## Learning Objectives

By the end of this module, you will be able to:
- Understand the architecture and core concepts of ROS 2
- Implement Nodes, Topics, and Services for robot communication
- Bridge Python Agents to ROS controllers using rclpy
- Understand URDF (Unified Robot Description Format) for humanoids

## Module Structure

This module is organized into the following sections:
1. [ROS 2 Nodes, Topics, and Services](./ros2-nodes-topics-services.md)
2. [Bridging Python Agents to ROS controllers using rclpy](./bridging-python-agents-ros.md)
3. [Understanding URDF (Unified Robot Description Format) for humanoids](./urdf-humanoids.md)

## What is ROS 2?

ROS 2 is the next generation of the Robot Operating System, designed to provide a flexible framework for writing robot software. Unlike the original ROS, ROS 2 is built on DDS (Data Distribution Service) which provides better support for:

- **Real-time systems**: Deterministic behavior for time-critical applications
- **Multi-robot systems**: Communication between multiple robots
- **Security**: Authentication, authorization, and encryption
- **Distributed systems**: Communication across different machines and networks

## The Nervous System Analogy

Just as the nervous system in biological organisms transmits signals between the brain and the body, ROS 2 serves as the communication backbone for robotic systems. It allows:

- **Sensors** to communicate with **processing units**
- **Planning algorithms** to communicate with **actuators**
- **Different subsystems** to coordinate their activities

## Why ROS 2 for Humanoid Robotics?

ROS 2 is particularly well-suited for humanoid robotics because:

- **Modularity**: Different parts of the robot (arms, legs, head) can be controlled by separate nodes
- **Standardization**: Common interfaces allow different components to work together
- **Community**: Large ecosystem of packages and tools for robotics development
- **Scalability**: Can handle the complexity of multi-joint humanoid systems

## Assessment

After completing this module, you will complete the **ROS 2 package development project** assessment to demonstrate your understanding of these concepts.

---

**Continue**: [ROS 2 Nodes, Topics, and Services](./ros2-nodes-topics-services.md) | **Next Module**: [Module 2: The Digital Twin (Gazebo & Unity)](/docs/module-2/index)