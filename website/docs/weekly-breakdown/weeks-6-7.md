---
sidebar_position: 3
title: "Weeks 6-7: Robot Simulation with Gazebo"
---

# Weeks 6-7: Robot Simulation with Gazebo

## Learning Objectives

By the end of these two weeks, you will be able to:
- Set up Gazebo simulation environments for robot testing
- Understand URDF and SDF robot description formats
- Implement physics simulation and sensor simulation
- Integrate with Unity for robot visualization
- Simulate realistic physics, gravity, and collisions

## Overview

Robot simulation is crucial for developing and testing robotic systems before deployment on physical hardware. Gazebo provides a realistic physics engine that enables safe, cost-effective development and testing of robot behaviors.

### The Digital Twin Concept

A digital twin in robotics is a virtual replica of a physical robot that allows for:
- Testing algorithms in a safe environment
- Prototyping new behaviors without hardware risk
- Training AI models with synthetic data
- Debugging complex interactions

## Gazebo Simulation Environment Setup

### Installation and Basic Setup

Gazebo can be installed as part of the ROS 2 ecosystem:

```bash
sudo apt install ros-humble-gazebo-ros-pkgs
```

### Creating Your First Simulation

A basic Gazebo world file defines the environment:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="default">
    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Sun for lighting -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Your robot will be spawned here -->
    <include>
      <uri>model://your_robot</uri>
    </include>
  </world>
</sdf>
```

## URDF and SDF Robot Description Formats

### URDF (Unified Robot Description Format)

URDF describes robot structure in XML format:

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.2"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Wheel joint and link -->
  <joint name="wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <axis xyz="0 0 1"/>
  </joint>

  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </visual>
  </link>
</robot>
```

### SDF (Simulation Description Format)

SDF is more comprehensive than URDF and is used by Gazebo:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_robot">
    <link name="chassis">
      <pose>0 0 0.1 0 0 0</pose>
      <collision name="collision">
        <geometry>
          <box>
            <size>1.0 0.5 0.2</size>
          </box>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <box>
            <size>1.0 0.5 0.2</size>
          </box>
        </geometry>
      </visual>
      <inertial>
        <mass>10.0</mass>
        <inertia>
          <ixx>0.4</ixx>
          <ixy>0</ixy>
          <ixz>0</ixz>
          <iyy>1.25</iyy>
          <iyz>0</iyz>
          <izz>1.25</izz>
        </inertia>
      </inertial>
    </link>
  </model>
</sdf>
```

## Physics Simulation

### Configuring Physics Properties

Gazebo's physics engine can be configured for different scenarios:

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
  <real_time_update_rate>1000.0</real_time_update_rate>
  <gravity>0 0 -9.8</gravity>
</physics>
```

### Gravity and Environmental Forces

- Gravity is defined as a 3D vector (default: 0 0 -9.8)
- Additional forces can be applied to simulate wind, magnetic fields, etc.
- Environmental conditions can be varied to test robot robustness

### Collision Detection

Gazebo provides multiple collision detection options:
- ODE (Open Dynamics Engine) - Default, good for most applications
- Bullet - Better for complex contact scenarios
- Simbody - Advanced multibody dynamics

## Sensor Simulation

### Simulating LiDAR Sensors

```xml
<sensor name="lidar_sensor" type="ray">
  <pose>0.2 0 0.1 0 0 0</pose>
  <ray>
    <scan>
      <horizontal>
        <samples>360</samples>
        <resolution>1.0</resolution>
        <min_angle>-3.14159</min_angle>
        <max_angle>3.14159</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>30.0</max>
      <resolution>0.01</resolution>
    </range>
  </ray>
  <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
    <topic_name>/laser_scan</topic_name>
    <frame_name>lidar_link</frame_name>
  </plugin>
</sensor>
```

### Depth Camera Simulation

```xml
<sensor name="depth_camera" type="depth">
  <camera>
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
    <frame_name>camera_link</frame_name>
    <topic_name>/depth_camera/image_raw</topic_name>
  </plugin>
</sensor>
```

### IMU Simulation

```xml
<sensor name="imu_sensor" type="imu">
  <always_on>true</always_on>
  <update_rate>100</update_rate>
  <topic>__default_topic__</topic>
  <plugin name="imu_plugin" filename="libgazebo_ros_imu.so">
    <topicName>imu</topicName>
    <bodyName>imu_link</bodyName>
    <serviceName>imu_service</serviceName>
    <gaussianNoise>0.01</gaussianNoise>
    <updateRateHZ>100.0</updateRateHZ>
  </plugin>
</sensor>
```

## Unity Integration for Visualization

Unity can complement Gazebo by providing high-fidelity rendering:

### Unity Robotics Hub

The Unity Robotics Hub provides:
- High-quality visualization
- VR/AR capabilities for immersive testing
- Advanced rendering effects
- Realistic lighting and materials

### Communication Bridge

Unity can communicate with ROS 2 using:
- ROS TCP Connector for direct communication
- Custom bridges for specific data types
- Message serialization for complex data

## Best Practices for Simulation

1. **Progressive Complexity**: Start with simple models and gradually increase complexity
2. **Validation**: Compare simulation results with real-world data when possible
3. **Domain Randomization**: Vary simulation parameters to improve real-world transfer
4. **Performance**: Balance simulation fidelity with computational requirements
5. **Safety**: Use simulation to test edge cases safely

## Next Steps

In the upcoming weeks, we'll explore the NVIDIA Isaac platform, which provides advanced perception and training capabilities that can be tested in simulation environments like Gazebo.

## Cross-References

- [Module 2: The Digital Twin (Gazebo & Unity)](/docs/module-2/intro)
- [Module 3: The AI-Robot Brain (NVIDIA Isaac™)](/docs/module-3/intro)
- [Weeks 8-10: NVIDIA Isaac Platform](/docs/weekly-breakdown/weeks-8-10)