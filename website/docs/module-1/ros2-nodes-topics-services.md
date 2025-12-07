---
sidebar_position: 2
title: "ROS 2 Nodes, Topics, and Services"
---

# ROS 2 Nodes, Topics, and Services

## Learning Objectives

By the end of this lesson, you will be able to:
- Create and manage ROS 2 nodes for different robot functions
- Implement topic-based communication between nodes
- Design service-based interactions for synchronous operations
- Understand the differences between topics and services
- Apply best practices for node design and communication

## Introduction to ROS 2 Architecture

ROS 2 uses a distributed computing architecture where different processes (nodes) communicate over a network. This design enables modular robot software development, allowing complex behaviors to be built from simple, reusable components.

### Core Communication Patterns

ROS 2 provides three primary communication patterns:
- **Topics**: Asynchronous publish-subscribe communication
- **Services**: Synchronous request-response communication
- **Actions**: Asynchronous goal-feedback-result communication

## ROS 2 Nodes

### What is a Node?

A node is a process that performs computation. In a robot system, nodes might handle:
- Sensor data processing
- Motion planning
- Path execution
- User interface
- Data logging

### Creating a Node

Here's a basic ROS 2 node in Python:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

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

### Node Lifecycle

Nodes have a well-defined lifecycle:
1. **Initialization**: Node is created and resources are allocated
2. **Configuration**: Parameters are loaded and connections are established
3. **Activation**: Node begins normal operation
4. **Deactivation**: Node stops operation gracefully
5. **Cleanup**: Resources are released

### Best Practices for Node Design

1. **Single Responsibility**: Each node should have one clear purpose
2. **Modularity**: Design nodes to be reusable across different robots
3. **Error Handling**: Implement robust error handling and recovery
4. **Logging**: Use appropriate logging levels for debugging and monitoring
5. **Parameterization**: Use parameters for configurable behavior

## Topics: Publish-Subscribe Communication

### Topic Communication Pattern

Topics enable asynchronous communication between nodes using a publish-subscribe pattern:
- Publishers send messages to topics
- Subscribers receive messages from topics
- Multiple publishers and subscribers can use the same topic
- Communication is decoupled in time and space

### Implementing a Publisher

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleDetector(Node):
    def __init__(self):
        super().__init__('obstacle_detector')
        # Create publisher for velocity commands
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        # Create subscriber for laser scan data
        self.scan_subscriber = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

    def scan_callback(self, msg):
        # Process laser scan to detect obstacles
        min_distance = min(msg.ranges)

        if min_distance < 0.5:  # Obstacle within 0.5m
            # Stop the robot
            cmd = Twist()
            cmd.linear.x = 0.0
            self.cmd_vel_publisher.publish(cmd)
        else:
            # Move forward
            cmd = Twist()
            cmd.linear.x = 0.5
            self.cmd_vel_publisher.publish(cmd)
```

### Implementing a Subscriber

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    def cmd_vel_callback(self, msg):
        self.get_logger().info(f'Received velocity command: linear.x={msg.linear.x}, angular.z={msg.angular.z}')
        # Here you would interface with the actual robot hardware
        self.execute_command(msg)

    def execute_command(self, cmd):
        # Interface with robot hardware to execute the command
        pass
```

### Topic QoS (Quality of Service)

QoS settings control how messages are delivered:

```python
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy

# Create a QoS profile for reliable communication
qos_profile = QoSProfile(
    depth=10,
    durability=QoSDurabilityPolicy.VOLATILE,
    reliability=QoSReliabilityPolicy.RELIABLE
)

# Use the QoS profile when creating a publisher
publisher = self.create_publisher(String, 'topic', qos_profile)
```

## Services: Request-Response Communication

### Service Communication Pattern

Services provide synchronous request-response communication:
- A client sends a request to a service
- A server processes the request and returns a response
- The client waits for the response before continuing

### Defining a Service

Create a service definition file (e.g., `GetPath.srv`):

```
# Request
geometry_msgs/PoseStamped start
geometry_msgs/PoseStamped goal
---
# Response
nav_msgs/Path path
bool success
string message
```

### Creating a Service Server

```python
import rclpy
from rclpy.node import Node
from your_package.srv import GetPath  # Your custom service
from nav_msgs.msg import Path

class PathPlanner(Node):
    def __init__(self):
        super().__init__('path_planner')
        self.srv = self.create_service(GetPath, 'get_path', self.get_path_callback)

    def get_path_callback(self, request, response):
        self.get_logger().info(f'Planning path from {request.start} to {request.goal}')

        # Implement path planning algorithm
        path = self.plan_path(request.start, request.goal)

        if path is not None:
            response.path = path
            response.success = True
            response.message = 'Path planning successful'
        else:
            response.success = False
            response.message = 'No path found'

        return response

    def plan_path(self, start, goal):
        # Implement your path planning algorithm here
        pass
```

### Creating a Service Client

```python
import rclpy
from rclpy.node import Node
from your_package.srv import GetPath
from geometry_msgs.msg import PoseStamped

class PathRequester(Node):
    def __init__(self):
        super().__init__('path_requester')
        self.cli = self.create_client(GetPath, 'get_path')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        self.send_request()

    def send_request(self):
        request = GetPath.Request()
        request.start = PoseStamped()  # Fill with actual start pose
        request.goal = PoseStamped()   # Fill with actual goal pose

        self.future = self.cli.call_async(request)
        self.future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        response = future.result()
        if response.success:
            self.get_logger().info(f'Received path with {len(response.path.poses)} waypoints')
        else:
            self.get_logger().error(f'Path planning failed: {response.message}')
```

## Comparing Topics vs Services

| Aspect | Topics | Services |
|--------|--------|----------|
| Communication Type | Asynchronous | Synchronous |
| Coupling | Loose (publishers don't know subscribers) | Tight (client knows server) |
| Performance | Higher throughput | Lower latency for request-response |
| Use Cases | Sensor data, continuous commands | Configuration, specific queries |
| Failure Handling | Publisher failure doesn't stop subscribers | Client waits for server response |

## Advanced Node Features

### Parameters

Nodes can have configurable parameters:

```python
class ParameterizedNode(Node):
    def __init__(self):
        super().__init__('parameterized_node')

        # Declare parameters with default values
        self.declare_parameter('robot_name', 'default_robot')
        self.declare_parameter('max_velocity', 1.0)
        self.declare_parameter('safety_distance', 0.5)

        # Get parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.max_velocity = self.get_parameter('max_velocity').value
        self.safety_distance = self.get_parameter('safety_distance').value

        # Set up parameter callback for dynamic reconfiguration
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'max_velocity' and param.value > 2.0:
                return SetParametersResult(successful=False, reason='Max velocity too high')
        return SetParametersResult(successful=True)
```

### Timers

Timers allow periodic execution:

```python
class TimedNode(Node):
    def __init__(self):
        super().__init__('timed_node')

        # Create a timer that calls the callback every 0.1 seconds
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.counter = 0

    def timer_callback(self):
        self.get_logger().info(f'Timer callback executed {self.counter} times')
        self.counter += 1
```

## Best Practices for Communication

1. **Message Design**: Keep messages focused and well-structured
2. **Topic Naming**: Use descriptive, consistent names
3. **QoS Selection**: Choose appropriate QoS settings for your use case
4. **Error Handling**: Handle communication failures gracefully
5. **Performance**: Consider bandwidth and timing requirements
6. **Security**: Use ROS 2 security features when needed

## Hands-On Exercise

Create a simple robot system with:
1. A sensor node that publishes simulated sensor data
2. A processing node that subscribes to sensor data and processes it
3. A control node that provides a service for commanding the robot
4. A client node that calls the control service based on processed data

## Summary

ROS 2 nodes, topics, and services form the foundation of robot software architecture. Understanding these concepts is essential for building modular, maintainable robot systems. Topics provide asynchronous communication for continuous data streams, while services provide synchronous request-response patterns for specific interactions.

## Next Steps

Continue to the next lesson on [Bridging Python Agents to ROS controllers using rclpy](/docs/module-1/rclpy-bridge) to learn how to connect AI agents to robot control systems.

## Cross-References

- [Module 1 Introduction](/docs/module-1/intro)
- [Bridging Python Agents to ROS controllers](/docs/module-1/rclpy-bridge)
- [Weeks 3-5: ROS 2 Fundamentals](/docs/weekly-breakdown/weeks-3-5)