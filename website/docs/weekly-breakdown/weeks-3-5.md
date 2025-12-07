---
sidebar_position: 2
title: "Weeks 3-5: ROS 2 Fundamentals"
---

# Weeks 3-5: ROS 2 Fundamentals

## Learning Objectives

By the end of these three weeks, you will be able to:
- Understand ROS 2 architecture and core concepts
- Implement Nodes, topics, services, and actions
- Build ROS 2 packages with Python
- Create launch files and manage parameters
- Bridge Python agents to ROS controllers using rclpy

## Overview

Robot Operating System 2 (ROS 2) provides the middleware foundation for robot control. It enables different components of a robot system to communicate and coordinate effectively, forming what we call "The Robotic Nervous System."

### ROS 2 Architecture

ROS 2 uses a distributed architecture where different processes (nodes) communicate over a network. This design enables:
- Modular robot software development
- Reusable components across different robots
- Scalable systems with multiple computational units

## Core Concepts

### Nodes

Nodes are the fundamental building blocks of a ROS 2 system. Each node performs a specific function:

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Topics and Message Passing

Topics enable asynchronous communication between nodes using a publish-subscribe pattern:
- Publishers send messages to topics
- Subscribers receive messages from topics
- Multiple publishers and subscribers can use the same topic

### Services

Services provide synchronous request-response communication:
- A client sends a request
- A server processes the request and returns a response
- Useful for operations that require confirmation or results

### Actions

Actions handle long-running tasks with feedback:
- Goal: Request for a long-running operation
- Feedback: Periodic updates during execution
- Result: Final outcome when the operation completes

## Building ROS 2 Packages with Python

### Package Structure

```
ros2_package/
├── CMakeLists.txt
├── package.xml
├── setup.py
├── setup.cfg
└── ros2_package/
    ├── __init__.py
    └── nodes/
        ├── publisher_node.py
        └── subscriber_node.py
```

### Creating a Package

```bash
ros2 pkg create --build-type ament_python my_robot_package
```

### Launch Files

Launch files coordinate the startup of multiple nodes:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_robot_package',
            executable='publisher_node',
            name='publisher_node'
        ),
        Node(
            package='my_robot_package',
            executable='subscriber_node',
            name='subscriber_node'
        )
    ])
```

## Bridging Python Agents to ROS Controllers

### Using rclpy

The rclpy library provides Python bindings for ROS 2:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class AgentBridge(Node):
    def __init__(self):
        super().__init__('agent_bridge')
        self.publisher = self.create_publisher(String, 'agent_commands', 10)
        self.subscription = self.create_subscription(
            String,
            'sensor_data',
            self.sensor_callback,
            10)

    def sensor_callback(self, msg):
        # Process sensor data and generate agent responses
        agent_response = self.process_with_ai_agent(msg.data)
        self.publisher.publish(String(data=agent_response))

    def process_with_ai_agent(self, sensor_data):
        # Implementation of AI agent logic
        return f"Processed: {sensor_data}"
```

## Parameter Management

ROS 2 provides a flexible parameter system:

```python
class ParameterizedNode(Node):
    def __init__(self):
        super().__init__('parameterized_node')

        # Declare parameters with default values
        self.declare_parameter('robot_name', 'default_robot')
        self.declare_parameter('max_velocity', 1.0)

        # Get parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.max_velocity = self.get_parameter('max_velocity').value
```

## Best Practices

1. **Modularity**: Keep nodes focused on single responsibilities
2. **Error Handling**: Implement robust error handling for physical systems
3. **Safety**: Include safety checks and emergency stops
4. **Testing**: Develop comprehensive tests for robot behaviors
5. **Documentation**: Document message types and node interfaces

## Next Steps

In the following weeks, we'll explore robot simulation environments where you can test your ROS 2 nodes safely before deploying them on physical robots.

## Cross-References

- [Module 1: The Robotic Nervous System (ROS 2)](/docs/module-1/intro)
- [Weeks 6-7: Robot Simulation with Gazebo](/docs/weekly-breakdown/weeks-6-7)