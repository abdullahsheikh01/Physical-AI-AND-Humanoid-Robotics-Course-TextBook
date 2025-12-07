---
sidebar_position: 2
title: "ROS 2 Package Development Project"
---

# ROS 2 Package Development Project

## Overview

In this assessment, you will develop a complete ROS 2 package that demonstrates your understanding of ROS 2 concepts, including nodes, topics, services, actions, and parameter management. You will create a package that simulates a simple robot with sensors and actuators, implementing the core concepts learned in Module 1.

## Learning Objectives

By completing this project, you will demonstrate ability to:
- Create and structure a ROS 2 package following best practices
- Implement multiple interconnected nodes with different responsibilities
- Design and implement topic-based communication patterns
- Create and use custom message and service definitions
- Implement action servers for long-running tasks
- Use parameter management for configurable behavior
- Test and validate ROS 2 nodes and their interactions

## Project Requirements

### 1. Package Structure
Create a ROS 2 package with the following structure:
```
robot_controller/
├── CMakeLists.txt
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
├── test/
└── robot_controller/
    ├── __init__.py
    ├── robot_simulator.py          # Main simulation node
    ├── sensor_processor.py         # Sensor data processing node
    ├── motion_controller.py        # Movement control node
    ├── path_planner.py             # Path planning node
    ├── utils/
    │   ├── robot_model.py          # Robot kinematics/model
    │   └── navigation.py           # Navigation utilities
    └── interfaces/
        ├── msg/
        └── srv/
```

### 2. Core Nodes

#### Robot Simulator Node (`robot_simulator.py`)
- Simulate a differential drive robot with position tracking
- Publish odometry data on `/odom` topic
- Subscribe to velocity commands on `/cmd_vel` topic
- Simulate sensor data (laser scan, IMU, etc.)
- Handle robot state and physics simulation

#### Sensor Processor Node (`sensor_processor.py`)
- Subscribe to simulated sensor data
- Process sensor information for obstacle detection
- Publish processed sensor data
- Implement basic filtering and noise handling

#### Motion Controller Node (`motion_controller.py`)
- Subscribe to velocity commands
- Interface with the simulated robot
- Implement velocity limiting and safety checks
- Publish robot status and feedback

#### Path Planner Node (`path_planner.py`)
- Provide path planning services
- Accept goal poses and return navigation paths
- Consider obstacles from sensor data
- Publish visualization markers for paths

### 3. Custom Message Definitions

Create the following custom message types in `robot_controller/interfaces/msg/`:

**RobotStatus.msg**
```
# Current robot status information
string state           # Current state (idle, moving, error, etc.)
float64 battery_level  # Battery level (0.0-1.0)
bool emergency_stop    # Emergency stop status
float64[] joint_angles # Joint angles if applicable
```

**SensorData.msg**
```
# Processed sensor information
sensor_msgs/LaserScan laser_scan
sensor_msgs/Imu imu_data
geometry_msgs/Point[] obstacles  # Detected obstacle positions
bool obstacle_detected
float32 min_distance
```

### 4. Custom Service Definitions

Create the following service in `robot_controller/interfaces/srv/`:

**NavigateTo.srv**
```
# Request
geometry_msgs/PoseStamped goal_pose
float32 speed_limit

# Response
bool success
string message
nav_msgs/Path planned_path
```

### 5. Action Definitions

Create an action for long-running navigation tasks in `robot_controller/interfaces/action/`:

**Navigate.action**
```
# Goal
geometry_msgs/PoseStamped target_pose

# Result
bool success
string message
float32 total_distance
int32 obstacle_encounters

# Feedback
float32 distance_traveled
float32 distance_remaining
geometry_msgs/Pose current_pose
string status
```

## Implementation Steps

### Step 1: Package Setup
```bash
# Create the package
ros2 pkg create --build-type ament_python robot_controller
cd robot_controller
```

### Step 2: Define Messages and Services
Create the custom message and service definition files in the appropriate directories.

### Step 3: Implement Core Nodes
Implement each node with proper ROS 2 patterns:

```python
# Example structure for robot_simulator.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64
import math
import numpy as np

class RobotSimulatorNode(Node):
    def __init__(self):
        super().__init__('robot_simulator')

        # Initialize robot state
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.linear_vel = 0.0
        self.angular_vel = 0.0

        # Create publishers
        self.odom_publisher = self.create_publisher(Odometry, '/odom', 10)
        self.scan_publisher = self.create_publisher(LaserScan, '/scan', 10)

        # Create subscribers
        self.cmd_vel_subscriber = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # Create timer for simulation updates
        self.timer = self.create_timer(0.1, self.update_simulation)

        self.get_logger().info('Robot Simulator Node initialized')

    def cmd_vel_callback(self, msg):
        """Handle velocity commands"""
        self.linear_vel = msg.linear.x
        self.angular_vel = msg.angular.z

    def update_simulation(self):
        """Update robot state based on current velocities"""
        # Simple differential drive kinematics
        dt = 0.1  # Time step

        # Update position
        self.x += self.linear_vel * math.cos(self.theta) * dt
        self.y += self.linear_vel * math.sin(self.theta) * dt
        self.theta += self.angular_vel * dt

        # Normalize theta to [-pi, pi]
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))

        # Publish odometry
        self.publish_odometry()

    def publish_odometry(self):
        """Publish odometry message"""
        odom_msg = Odometry()
        odom_msg.header.stamp = self.get_clock().now().to_msg()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'

        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.orientation.z = math.sin(self.theta / 2)
        odom_msg.pose.pose.orientation.w = math.cos(self.theta / 2)

        odom_msg.twist.twist.linear.x = self.linear_vel
        odom_msg.twist.twist.angular.z = self.angular_vel

        self.odom_publisher.publish(odom_msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotSimulatorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Step 4: Implement Service Server
```python
# Example path planner service
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from robot_controller.srv import NavigateTo
import math

class PathPlannerNode(Node):
    def __init__(self):
        super().__init__('path_planner')

        # Create service server
        self.srv = self.create_service(
            NavigateTo,
            'navigate_to',
            self.navigate_to_callback
        )

        self.get_logger().info('Path Planner Service ready')

    def navigate_to_callback(self, request, response):
        """Handle navigation requests"""
        start_pose = self.get_current_pose()
        goal_pose = request.goal_pose

        # Simple straight-line path planning
        path = self.plan_straight_path(start_pose, goal_pose)

        if path:
            response.success = True
            response.message = "Path planned successfully"
            response.planned_path = path
        else:
            response.success = False
            response.message = "Could not plan path"

        return response

    def plan_straight_path(self, start, goal):
        """Plan a simple straight-line path"""
        path = Path()
        path.header.stamp = self.get_clock().now().to_msg()
        path.header.frame_id = 'map'

        # Calculate intermediate points
        steps = 10
        for i in range(steps + 1):
            t = i / steps
            pose = PoseStamped()
            pose.header.stamp = self.get_clock().now().to_msg()
            pose.header.frame_id = 'map'

            pose.pose.position.x = start.pose.position.x + \
                t * (goal.pose.position.x - start.pose.position.x)
            pose.pose.position.y = start.pose.position.y + \
                t * (goal.pose.position.y - start.pose.position.y)

            path.poses.append(pose)

        return path
```

### Step 5: Add Parameters and Configuration
```python
# Example parameter usage in a node
class ConfigurableNode(Node):
    def __init__(self):
        super().__init__('configurable_node')

        # Declare parameters with default values
        self.declare_parameter('robot_name', 'default_robot')
        self.declare_parameter('max_velocity', 0.5)
        self.declare_parameter('safety_distance', 0.5)
        self.declare_parameter('simulation_speed', 1.0)

        # Get parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.max_velocity = self.get_parameter('max_velocity').value
        self.safety_distance = self.get_parameter('safety_distance').value
        self.simulation_speed = self.get_parameter('simulation_speed').value

        # Set up parameter callback
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        """Handle parameter changes"""
        for param in params:
            if param.name == 'max_velocity' and param.value <= 0:
                return SetParametersResult(
                    successful=False,
                    reason='Max velocity must be positive'
                )
        return SetParametersResult(successful=True)
```

## Testing Requirements

### 1. Unit Tests
Create unit tests for each component:
- Test message serialization/deserialization
- Test service request/response handling
- Test action goal/feedback/result processing
- Test parameter validation

### 2. Integration Tests
Test the complete system:
- Launch all nodes and verify communication
- Test service calls and verify responses
- Test action execution and feedback
- Verify parameter changes affect behavior

### 3. Performance Tests
- Test system performance under load
- Verify timing constraints are met
- Test memory usage and resource management

## Success Criteria

### Functional Requirements
- [ ] All nodes launch without errors
- [ ] Topics publish and subscribe correctly
- [ ] Services respond to requests appropriately
- [ ] Actions execute goals and provide feedback
- [ ] Parameters can be set and changed dynamically
- [ ] Custom messages and services work as expected

### Quality Requirements
- [ ] Code follows ROS 2 Python style guidelines
- [ ] Proper error handling and logging implemented
- [ ] Documentation included for all public interfaces
- [ ] Tests cover major functionality paths
- [ ] Package builds without warnings

### Performance Requirements
- [ ] System runs at real-time or faster
- [ ] Memory usage remains stable over time
- [ ] Communication latency is acceptable
- [ ] System handles error conditions gracefully

## Submission Guidelines

### 1. Code Submission
Submit your complete package with:
- All source code files
- Package configuration files
- Test files
- Launch files (if applicable)

### 2. Documentation
Include documentation for:
- Package overview and purpose
- Node descriptions and interfaces
- Message/service/action definitions
- Configuration parameters
- Testing procedures

### 3. Demonstration
Provide a demonstration script showing:
- Package building and installation
- Node launching and communication
- Service and action usage
- Parameter configuration

## Resources

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [Creating a ROS 2 Package](https://docs.ros.org/en/humble/Tutorials/Creating-Your-First-ROS2-Package.html)
- [ROS 2 Python Node Examples](https://docs.ros.org/en/humble/Tutorials/Writing-A-Simple-Py-Node.html)
- [ROS 2 Services and Actions](https://docs.ros.org/en/humble/Tutorials/Services.html)

## Evaluation Rubric

| Criteria | Points | Details |
|----------|--------|---------|
| Package Structure | 15 | Proper ROS 2 package organization |
| Node Implementation | 25 | Correct implementation of all nodes |
| Communication | 20 | Proper topic, service, action usage |
| Custom Interfaces | 15 | Well-defined messages and services |
| Testing | 15 | Comprehensive test coverage |
| Code Quality | 10 | Clean, documented, maintainable code |

## Next Steps

After completing this assessment, proceed to the [Gazebo Simulation Implementation](/docs/assessments/gazebo-simulation) assessment to apply your ROS 2 knowledge in a simulation environment.

## Cross-References

- [Module 1: The Robotic Nervous System (ROS 2)](/docs/module-1/intro)
- [ROS 2 Nodes, Topics, and Services](/docs/module-1/ros2-nodes-topics-services)
- [Bridging Python Agents to ROS controllers](/docs/module-1/rclpy-bridge)