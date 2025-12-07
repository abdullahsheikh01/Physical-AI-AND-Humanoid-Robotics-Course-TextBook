---
sidebar_position: 3
title: "Gazebo Simulation Implementation"
---

# Gazebo Simulation Implementation

## Overview

In this assessment, you will implement a complete Gazebo simulation environment for a robot, integrating the ROS 2 concepts learned in Module 1 with the simulation techniques from Module 2. You will create a realistic simulation world, model a robot with proper URDF, configure physics properties, and implement sensor simulation that integrates with ROS 2.

## Learning Objectives

By completing this project, you will demonstrate ability to:
- Create realistic Gazebo simulation environments
- Model robots using URDF with proper kinematics and dynamics
- Configure physics properties for realistic simulation
- Implement sensor simulation with ROS 2 integration
- Validate simulation behavior against real-world expectations
- Optimize simulation performance for real-time operation

## Project Requirements

### 1. Simulation Environment
Create a complete simulation world that includes:
- Indoor environment with rooms, furniture, and obstacles
- Proper lighting and visual appearance
- Physics properties that match real-world behavior
- Multiple test scenarios for different robot capabilities

### 2. Robot Model
Develop a URDF model for a wheeled robot with:
- Accurate kinematics and joint definitions
- Proper mass and inertia properties
- Realistic visual and collision geometries
- Appropriate joint limits and dynamics

### 3. Sensor Integration
Implement sensor simulation including:
- Laser scanner (LiDAR) for navigation
- RGB camera for perception
- IMU for orientation and acceleration
- Optional: depth camera, force/torque sensors

### 4. ROS 2 Integration
Integrate with ROS 2 through:
- Gazebo ROS plugins for communication
- Proper TF tree configuration
- Standard ROS message types for sensors
- Control interfaces for robot movement

## Implementation Steps

### Step 1: Create Simulation World

Create a world file `robot_world.sdf`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="robot_world">
    <!-- Physics configuration -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000.0</real_time_update_rate>
      <gravity>0 0 -9.8</gravity>

      <ode>
        <solver>
          <type>quick</type>  <!-- Fast solver for real-time -->
          <iters>10</iters>   <!-- Number of iterations -->
          <sor>1.3</sor>      <!-- Successive over-relaxation -->
        </solver>
        <constraints>
          <cfm>0.0</cfm>      <!-- Constraint Force Mixing -->
          <erp>0.2</erp>      <!-- Error Reduction Parameter -->
          <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
          <contact_surface_layer>0.001</contact_surface_layer>
        </constraints>
      </ode>
    </physics>

    <!-- Environment -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Custom environment elements -->
    <!-- Room with furniture -->
    <model name="room_walls">
      <pose>0 0 1.5 0 0 0</pose>
      <static>true</static>

      <!-- Walls -->
      <link name="wall_north">
        <pose>0 5 1.5 0 0 0</pose>
        <collision name="collision">
          <geometry>
            <box>
              <size>10 0.2 3</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>10 0.2 3</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
      </link>

      <link name="wall_south">
        <pose>0 -5 1.5 0 0 0</pose>
        <collision name="collision">
          <geometry>
            <box>
              <size>10 0.2 3</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>10 0.2 3</size>
            </box>
          </geometry>
        </visual>
      </link>

      <link name="wall_east">
        <pose>5 0 1.5 0 0 0</pose>
        <collision name="collision">
          <geometry>
            <box>
              <size>0.2 10 3</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.2 10 3</size>
            </box>
          </geometry>
        </visual>
      </link>

      <link name="wall_west">
        <pose>-5 0 1.5 0 0 0</pose>
        <collision name="collision">
          <geometry>
            <box>
              <size>0.2 10 3</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.2 10 3</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- Furniture -->
    <model name="table">
      <pose>2 0 0.4 0 0 0</pose>
      <link name="table_base">
        <inertial>
          <mass>10.0</mass>
          <inertia>
            <ixx>1.0</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>1.0</iyy>
            <iyz>0.0</iyz>
            <izz>1.0</izz>
          </inertia>
        </inertial>
        <collision name="collision">
          <geometry>
            <box>
              <size>1.0 0.8 0.8</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1.0 0.8 0.8</size>
            </box>
          </geometry>
          <material>
            <ambient>0.6 0.4 0.2 1</ambient>
            <diffuse>0.6 0.4 0.2 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Add more furniture, obstacles, etc. -->
  </world>
</sdf>
```

### Step 2: Robot URDF Model

Create a robot URDF file `robot_model.urdf.xacro`:

```xml
<?xml version="1.0"?>
<robot name="simulated_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Constants -->
  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="wheel_radius" value="0.1" />
  <xacro:property name="wheel_width" value="0.05" />
  <xacro:property name="wheel_separation" value="0.4" />
  <xacro:property name="robot_length" value="0.5" />
  <xacro:property name="robot_width" value="0.4" />
  <xacro:property name="robot_height" value="0.3" />

  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <origin xyz="0 0 ${robot_height/2}" rpy="0 0 0"/>
      <geometry>
        <box size="${robot_length} ${robot_width} ${robot_height}"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 ${robot_height/2}" rpy="0 0 0"/>
      <geometry>
        <box size="${robot_length} ${robot_width} ${robot_height}"/>
      </geometry>
    </collision>

    <inertial>
      <origin xyz="0 0 ${robot_height/2}" rpy="0 0 0"/>
      <mass value="10.0"/>
      <inertia
        ixx="0.416"
        ixy="0.0"
        ixz="0.0"
        iyy="0.641"
        iyz="0.0"
        izz="0.241"/>
    </inertial>
  </link>

  <!-- Wheels -->
  <xacro:macro name="wheel" params="prefix joint_x joint_y">
    <joint name="${prefix}_wheel_joint" type="continuous">
      <parent link="base_link"/>
      <child link="${prefix}_wheel"/>
      <origin xyz="${joint_x} ${joint_y} 0" rpy="${-M_PI/2} 0 0"/>
      <axis xyz="0 0 1"/>
    </joint>

    <link name="${prefix}_wheel">
      <visual>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
        <material name="black">
          <color rgba="0 0 0 1"/>
        </material>
      </visual>

      <collision>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
      </collision>

      <inertial>
        <mass value="1.0"/>
        <inertia
          ixx="0.01"
          ixy="0.0"
          ixz="0.0"
          iyy="0.01"
          iyz="0.0"
          izz="0.02"/>
      </inertial>
    </link>

    <!-- Gazebo plugin for wheel control -->
    <gazebo reference="${prefix}_wheel">
      <material>Gazebo/Black</material>
      <mu1>1.0</mu1>
      <mu2>1.0</mu2>
      <kp>1000000.0</kp>
      <kd>100.0</kd>
    </gazebo>
  </xacro:macro>

  <!-- Instantiate wheels -->
  <xacro:wheel prefix="front_left" joint_x="${robot_length/2}" joint_y="${wheel_separation/2}"/>
  <xacro:wheel prefix="front_right" joint_x="${robot_length/2}" joint_y="${-wheel_separation/2}"/>
  <xacro:wheel prefix="back_left" joint_x="${-robot_length/2}" joint_y="${wheel_separation/2}"/>
  <xacro:wheel prefix="back_right" joint_x="${-robot_length/2}" joint_y="${-wheel_separation/2}"/>

  <!-- Sensors -->
  <!-- Laser Scanner -->
  <joint name="laser_joint" type="fixed">
    <parent link="base_link"/>
    <child link="laser_link"/>
    <origin xyz="${robot_length/2 + 0.05} 0 ${robot_height - 0.05}" rpy="0 0 0"/>
  </joint>

  <link name="laser_link">
    <visual>
      <geometry>
        <cylinder radius="0.02" length="0.04"/>
      </geometry>
      <material name="red">
        <color rgba="0.8 0 0 1"/>
      </material>
    </visual>
  </link>

  <!-- Camera -->
  <joint name="camera_joint" type="fixed">
    <parent link="base_link"/>
    <child link="camera_link"/>
    <origin xyz="${robot_length/2 + 0.02} 0 ${robot_height/2}" rpy="0 0 0"/>
  </joint>

  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
      <material name="green">
        <color rgba="0 0.8 0 1"/>
      </material>
    </visual>
  </link>

  <!-- IMU -->
  <joint name="imu_joint" type="fixed">
    <parent link="base_link"/>
    <child link="imu_link"/>
    <origin xyz="0 0 ${robot_height/2}" rpy="0 0 0"/>
  </joint>

  <link name="imu_link"/>

  <!-- Gazebo plugins -->
  <gazebo reference="base_link">
    <material>Gazebo/Blue</material>
    <mu1>0.2</mu1>
    <mu2>0.2</mu2>
  </gazebo>

  <!-- Differential drive plugin -->
  <gazebo>
    <plugin name="differential_drive" filename="libgazebo_ros_diff_drive.so">
      <ros>
        <namespace>/robot</namespace>
        <remapping>cmd_vel:=cmd_vel</remapping>
        <remapping>odom:=odom</remapping>
      </ros>
      <update_rate>30</update_rate>
      <left_joint>front_left_wheel_joint</left_joint>
      <right_joint>front_right_wheel_joint</right_joint>
      <wheel_separation>${wheel_separation}</wheel_separation>
      <wheel_diameter>${2 * wheel_radius}</wheel_diameter>
      <max_wheel_torque>20</max_wheel_torque>
      <max_wheel_acceleration>1.0</max_wheel_acceleration>
      <publish_odom>true</publish_odom>
      <publish_odom_tf>true</publish_odom_tf>
      <publish_wheel_tf>true</publish_wheel_tf>
      <odometry_frame>odom</odometry_frame>
      <robot_base_frame>base_link</robot_base_frame>
    </plugin>
  </gazebo>

  <!-- Laser scanner plugin -->
  <gazebo reference="laser_link">
    <sensor name="laser" type="ray">
      <pose>0 0 0 0 0 0</pose>
      <ray>
        <scan>
          <horizontal>
            <samples>360</samples>
            <resolution>1</resolution>
            <min_angle>-3.14159</min_angle>
            <max_angle>3.14159</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.1</min>
          <max>10.0</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <plugin name="laser_controller" filename="libgazebo_ros_ray_sensor.so">
        <ros>
          <namespace>/robot</namespace>
          <remapping>~/out:=scan</remapping>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
        <frame_name>laser_link</frame_name>
      </plugin>
    </sensor>
  </gazebo>

  <!-- Camera plugin -->
  <gazebo reference="camera_link">
    <sensor name="camera" type="camera">
      <always_on>true</always_on>
      <update_rate>30</update_rate>
      <camera name="head">
        <horizontal_fov>1.047</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>
          <far>10</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <ros>
          <namespace>/robot</namespace>
          <remapping>~/image_raw:=image_raw</remapping>
          <remapping>~/camera_info:=camera_info</remapping>
        </ros>
        <frame_name>camera_link</frame_name>
      </plugin>
    </sensor>
  </gazebo>

  <!-- IMU plugin -->
  <gazebo reference="imu_link">
    <sensor name="imu_sensor" type="imu">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <visualize>true</visualize>
      <plugin name="imu_plugin" filename="libgazebo_ros_imu.so">
        <ros>
          <namespace>/robot</namespace>
          <remapping>~/out:=imu</remapping>
        </ros>
        <frame_name>imu_link</frame_name>
        <body_name>base_link</body_name>
        <update_rate>100</update_rate>
      </plugin>
    </sensor>
  </gazebo>

</robot>
```

### Step 3: Launch Files

Create a launch file `launch/simulation.launch.py`:

```python
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Launch configuration
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    world_file = LaunchConfiguration('world', default='robot_world.sdf')

    # Package names
    pkg_gazebo_ros = FindPackageShare('gazebo_ros')
    pkg_robot_description = FindPackageShare('robot_description')

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world': PathJoinSubstitution([pkg_robot_description, 'worlds', world_file]),
            'verbose': 'false',
        }.items()
    )

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': Command([
                'xacro ',
                PathJoinSubstitution([pkg_robot_description, 'urdf', 'robot_model.urdf.xacro'])
            ])
        }]
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'robot',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1'
        ],
        output='screen'
    )

    # RViz node (optional)
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', PathJoinSubstitution([pkg_robot_description, 'rviz', 'robot.rviz'])],
        parameters=[{'use_sim_time': use_sim_time}],
        condition=LaunchConfigurationEquals('rviz', 'true')
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='robot_world.sdf',
            description='Choose one of the world files from `/robot_description/worlds`'
        ),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),
        DeclareLaunchArgument(
            'rviz',
            default_value='false',
            description='Open RViz if true'
        ),
        gazebo,
        robot_state_publisher,
        spawn_entity,
    ])
```

### Step 4: Robot Controller Node

Create a simple controller node `robot_controller.py`:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
import math

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')

        # Publishers
        self.cmd_vel_publisher = self.create_publisher(Twist, '/robot/cmd_vel', 10)

        # Subscribers
        self.odom_subscriber = self.create_subscription(
            Odometry, '/robot/odom', self.odom_callback, 10)
        self.scan_subscriber = self.create_subscription(
            LaserScan, '/robot/scan', self.scan_callback, 10)

        # Timer for control loop
        self.control_timer = self.create_timer(0.1, self.control_loop)

        # Robot state
        self.current_pose = Pose()
        self.current_twist = Twist()
        self.scan_data = None
        self.control_state = 'idle'

        self.get_logger().info('Robot Controller initialized')

    def odom_callback(self, msg):
        """Update robot pose from odometry"""
        self.current_pose = msg.pose.pose
        self.current_twist = msg.twist.twist

    def scan_callback(self, msg):
        """Process laser scan data"""
        self.scan_data = msg

    def control_loop(self):
        """Main control loop"""
        if self.control_state == 'idle':
            self.execute_idle_behavior()
        elif self.control_state == 'navigate':
            self.execute_navigation_behavior()
        elif self.control_state == 'avoid_obstacles':
            self.execute_avoidance_behavior()

    def execute_idle_behavior(self):
        """Execute idle behavior - patrol around"""
        # Simple patrol behavior
        cmd = Twist()

        # Check if there are obstacles ahead
        if self.scan_data:
            front_scan = self.scan_data.ranges[0:30] + self.scan_data.ranges[-30:]
            min_front = min([r for r in front_scan if not math.isinf(r) and not math.isnan(r)])

            if min_front < 1.0:  # Obstacle detected
                self.control_state = 'avoid_obstacles'
                return

        # Move forward
        cmd.linear.x = 0.3
        cmd.angular.z = 0.0

        self.cmd_vel_publisher.publish(cmd)

    def execute_avoidance_behavior(self):
        """Execute obstacle avoidance"""
        if not self.scan_data:
            return

        # Simple wall following
        left_scan = self.scan_data.ranges[30:90]
        right_scan = self.scan_data.ranges[270:330]
        front_scan = self.scan_data.ranges[0:30] + self.scan_data.ranges[-30:]

        min_left = min([r for r in left_scan if not math.isinf(r) and not math.isnan(r)])
        min_right = min([r for r in right_scan if not math.isinf(r) and not math.isnan(r)])
        min_front = min([r for r in front_scan if not math.isinf(r) and not math.isnan(r)])

        cmd = Twist()

        if min_front < 0.5:  # Emergency stop
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5  # Turn
        elif min_left < 0.8:  # Too close to left wall
            cmd.linear.x = 0.2
            cmd.angular.z = -0.2  # Turn right
        elif min_right < 0.8:  # Too close to right wall
            cmd.linear.x = 0.2
            cmd.angular.z = 0.2  # Turn left
        else:  # Maintain course
            cmd.linear.x = 0.3
            cmd.angular.z = 0.0

        self.cmd_vel_publisher.publish(cmd)

        # Return to idle if clear
        if min_front > 1.5 and min_left > 1.0 and min_right > 1.0:
            self.control_state = 'idle'

    def execute_navigation_behavior(self):
        """Execute navigation behavior"""
        # Placeholder for navigation behavior
        cmd = Twist()
        cmd.linear.x = 0.2
        cmd.angular.z = 0.0
        self.cmd_vel_publisher.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    controller = RobotController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        controller.get_logger().info('Shutting down robot controller')
    finally:
        # Stop the robot
        stop_cmd = Twist()
        controller.cmd_vel_publisher.publish(stop_cmd)
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Testing Requirements

### 1. Basic Functionality Tests
- [ ] Robot spawns correctly in Gazebo
- [ ] All sensors publish data
- [ ] Robot responds to velocity commands
- [ ] TF tree is properly published
- [ ] Odommetry is accurate

### 2. Simulation Behavior Tests
- [ ] Physics simulation is realistic
- [ ] Collision detection works
- [ ] Sensor data is accurate
- [ ] Robot kinematics are correct

### 3. Integration Tests
- [ ] ROS 2 communication works
- [ ] Sensor data can be processed
- [ ] Control commands affect robot motion
- [ ] Multiple nodes can communicate

## Success Criteria

### Functional Requirements
- [ ] Robot model loads without errors
- [ ] All sensors publish valid data
- [ ] Robot moves according to commands
- [ ] Simulation runs in real-time
- [ ] TF tree is complete and accurate

### Quality Requirements
- [ ] URDF is well-structured and documented
- [ ] Physics parameters are realistic
- [ ] Sensor configurations are appropriate
- [ ] Launch files are properly organized
- [ ] Code follows ROS 2 conventions

### Performance Requirements
- [ ] Simulation runs at real-time or faster
- [ ] Sensor data updates at expected rates
- [ ] Communication latency is acceptable
- [ ] Memory usage remains stable

## Documentation Requirements

### 1. System Architecture
- Describe the overall system design
- Explain the relationship between components
- Document the simulation environment setup

### 2. Configuration Guide
- Provide instructions for setting up the simulation
- Document all configurable parameters
- Include troubleshooting information

### 3. Testing Procedures
- Document how to run tests
- Explain expected results
- Provide validation procedures

## Resources

- [Gazebo Documentation](http://gazebosim.org/tutorials)
- [ROS 2 with Gazebo](https://classic.gazebosim.org/tutorials?tut=ros2_overview)
- [URDF Tutorials](http://wiki.ros.org/urdf/Tutorials)
- [Xacro Documentation](http://wiki.ros.org/xacro)

## Evaluation Rubric

| Criteria | Points | Details |
|----------|--------|---------|
| URDF Model | 25 | Proper kinematics, dynamics, and visualization |
| Gazebo Integration | 25 | Realistic physics and sensor simulation |
| ROS 2 Integration | 20 | Proper communication and TF tree |
| Simulation Environment | 15 | Realistic and functional world |
| Testing and Validation | 10 | Comprehensive testing procedures |
| Documentation | 5 | Clear and complete documentation |

## Next Steps

After completing this assessment, proceed to the [Isaac-based Perception Pipeline](/docs/assessments/isaac-perception) assessment to apply your simulation knowledge with advanced perception systems.

## Cross-References

- [Module 2: The Digital Twin (Gazebo & Unity)](/docs/module-2/intro)
- [Simulating physics, gravity, and collisions in Gazebo](/docs/module-2/gazebo-physics-collisions)
- [Simulating sensors: LiDAR, Depth Cameras, and IMUs](/docs/module-2/sensor-simulation)