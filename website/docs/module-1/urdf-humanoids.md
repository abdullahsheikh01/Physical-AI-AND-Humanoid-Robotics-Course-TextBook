---
sidebar_position: 4
title: "Understanding URDF for Humanoids"
---

# Understanding URDF (Unified Robot Description Format) for Humanoids

## Learning Objectives

By the end of this lesson, you will be able to:
- Create URDF files that describe humanoid robot structures
- Define joints, links, and kinematic chains for humanoids
- Implement proper kinematic models for bipedal locomotion
- Integrate URDF with Gazebo for physics simulation
- Validate URDF models for humanoid applications

## Introduction to URDF

URDF (Unified Robot Description Format) is an XML-based format used in ROS to describe robot models. For humanoid robots, URDF is essential for defining the complex kinematic structure with multiple limbs, joints, and degrees of freedom that characterize these robots.

### Why URDF for Humanoids?

Humanoid robots require special consideration in URDF because:
- **Complex Kinematics**: Multiple limbs with many degrees of freedom
- **Balance Requirements**: Need for accurate center of mass calculations
- **Manipulation Capabilities**: Complex hand and arm structures
- **Locomotion Patterns**: Bipedal walking requires precise joint coordination

## URDF Fundamentals

### Basic URDF Structure

A URDF file describes a robot as a collection of rigid bodies (links) connected by joints:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Links define rigid bodies -->
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

  <!-- Joints connect links -->
  <joint name="base_to_head" type="fixed">
    <parent link="base_link"/>
    <child link="head_link"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
  </joint>

  <link name="head_link">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </visual>
  </link>
</robot>
```

### Link Elements

Each link in a humanoid robot typically includes:

```xml
<link name="link_name">
  <!-- Visual properties for rendering -->
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <box size="0.1 0.1 0.1"/>  <!-- or cylinder, sphere, mesh -->
    </geometry>
    <material name="color">
      <color rgba="0.8 0.2 0.2 1.0"/>
    </material>
  </visual>

  <!-- Collision properties for physics simulation -->
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <box size="0.1 0.1 0.1"/>
    </geometry>
  </collision>

  <!-- Inertial properties for dynamics -->
  <inertial>
    <mass value="0.5"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
  </inertial>
</link>
```

## Humanoid-Specific URDF Considerations

### Typical Humanoid Structure

A humanoid robot typically has this kinematic structure:

```
base_link (torso)
├── head_link
├── left_upper_arm
│   ├── left_lower_arm
│   └── left_hand
├── right_upper_arm
│   ├── right_lower_arm
│   └── right_hand
├── left_upper_leg
│   └── left_lower_leg
│       └── left_foot
└── right_upper_leg
    └── right_lower_leg
        └── right_foot
```

### Complete Humanoid URDF Example

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">

  <!-- Torso/Body -->
  <link name="torso">
    <visual>
      <origin xyz="0 0 0.4" rpy="0 0 0"/>
      <geometry>
        <box size="0.3 0.2 0.8"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.4" rpy="0 0 0"/>
      <geometry>
        <box size="0.3 0.2 0.8"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5.0"/>
      <origin xyz="0 0 0.4" rpy="0 0 0"/>
      <inertia ixx="0.2" ixy="0.0" ixz="0.0" iyy="0.3" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Head -->
  <joint name="torso_to_head" type="fixed">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.75" rpy="0 0 0"/>
  </joint>

  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="skin_color">
        <color rgba="0.9 0.8 0.6 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.002" ixy="0.0" ixz="0.0" iyy="0.002" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>

  <!-- Left Arm -->
  <joint name="torso_to_left_shoulder" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="0.15 0 0.5" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
  </joint>

  <link name="left_upper_arm">
    <visual>
      <origin xyz="0 0 -0.15" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.15" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.8"/>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <inertia ixx="0.002" ixy="0.0" ixz="0.0" iyy="0.002" iyz="0.0" izz="0.0005"/>
    </inertial>
  </link>

  <joint name="left_shoulder_to_elbow" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_lower_arm"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="50" velocity="1.0"/>
  </joint>

  <link name="left_lower_arm">
    <visual>
      <origin xyz="0 0 -0.12" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.24"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.12" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.24"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <origin xyz="0 0 -0.12" rpy="0 0 0"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.0003"/>
    </inertial>
  </link>

  <!-- Left Hand (simplified as fixed link) -->
  <joint name="left_elbow_to_hand" type="fixed">
    <parent link="left_lower_arm"/>
    <child link="left_hand"/>
    <origin xyz="0 0 -0.24" rpy="0 0 0"/>
  </joint>

  <link name="left_hand">
    <visual>
      <geometry>
        <box size="0.1 0.08 0.05"/>
      </geometry>
      <material name="skin_color">
        <color rgba="0.9 0.8 0.6 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.1 0.08 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <!-- Right Arm (similar to left, mirrored) -->
  <joint name="torso_to_right_shoulder" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_arm"/>
    <origin xyz="-0.15 0 0.5" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
  </joint>

  <link name="right_upper_arm">
    <visual>
      <origin xyz="0 0 -0.15" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.15" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.8"/>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <inertia ixx="0.002" ixy="0.0" ixz="0.0" iyy="0.002" iyz="0.0" izz="0.0005"/>
    </inertial>
  </link>

  <joint name="right_shoulder_to_elbow" type="revolute">
    <parent link="right_upper_arm"/>
    <child link="right_lower_arm"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="50" velocity="1.0"/>
  </joint>

  <link name="right_lower_arm">
    <visual>
      <origin xyz="0 0 -0.12" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.24"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.12" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.24"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <origin xyz="0 0 -0.12" rpy="0 0 0"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.0003"/>
    </inertial>
  </link>

  <joint name="right_elbow_to_hand" type="fixed">
    <parent link="right_lower_arm"/>
    <child link="right_hand"/>
    <origin xyz="0 0 -0.24" rpy="0 0 0"/>
  </joint>

  <link name="right_hand">
    <visual>
      <geometry>
        <box size="0.1 0.08 0.05"/>
      </geometry>
      <material name="skin_color">
        <color rgba="0.9 0.8 0.6 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.1 0.08 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <!-- Left Leg -->
  <joint name="torso_to_left_hip" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_leg"/>
    <origin xyz="0.075 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="0.5" effort="200" velocity="1.0"/>
  </joint>

  <link name="left_upper_leg">
    <visual>
      <origin xyz="0 0 -0.25" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.06" length="0.5"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.25" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.06" length="0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <origin xyz="0 0 -0.25" rpy="0 0 0"/>
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_hip_to_knee" type="revolute">
    <parent link="left_upper_leg"/>
    <child link="left_lower_leg"/>
    <origin xyz="0 0 -0.5" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="1.57" effort="150" velocity="1.0"/>
  </joint>

  <link name="left_lower_leg">
    <visual>
      <origin xyz="0 0 -0.2" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.2" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.0008"/>
    </inertial>
  </link>

  <joint name="left_knee_to_foot" type="fixed">
    <parent link="left_lower_leg"/>
    <child link="left_foot"/>
    <origin xyz="0 0 -0.4" rpy="0 0 0"/>
  </joint>

  <link name="left_foot">
    <visual>
      <origin xyz="0 0 -0.025" rpy="0 0 0"/>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
      <material name="dark_grey">
        <color rgba="0.3 0.3 0.3 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.025" rpy="0 0 0"/>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <origin xyz="0 0 -0.025" rpy="0 0 0"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.002" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>

  <!-- Right Leg (mirrored from left) -->
  <joint name="torso_to_right_hip" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_leg"/>
    <origin xyz="-0.075 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="1.57" effort="200" velocity="1.0"/>
  </joint>

  <link name="right_upper_leg">
    <visual>
      <origin xyz="0 0 -0.25" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.06" length="0.5"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.25" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.06" length="0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <origin xyz="0 0 -0.25" rpy="0 0 0"/>
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="right_hip_to_knee" type="revolute">
    <parent link="right_upper_leg"/>
    <child link="right_lower_leg"/>
    <origin xyz="0 0 -0.5" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="1.57" effort="150" velocity="1.0"/>
  </joint>

  <link name="right_lower_leg">
    <visual>
      <origin xyz="0 0 -0.2" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.2" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.0008"/>
    </inertial>
  </link>

  <joint name="right_knee_to_foot" type="fixed">
    <parent link="right_lower_leg"/>
    <child link="right_foot"/>
    <origin xyz="0 0 -0.4" rpy="0 0 0"/>
  </joint>

  <link name="right_foot">
    <visual>
      <origin xyz="0 0 -0.025" rpy="0 0 0"/>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
      <material name="dark_grey">
        <color rgba="0.3 0.3 0.3 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.025" rpy="0 0 0"/>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <origin xyz="0 0 -0.025" rpy="0 0 0"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.002" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>
</robot>
```

## Joint Types for Humanoid Applications

### Revolute Joints

For rotational movement around a single axis:

```xml
<joint name="shoulder_joint" type="revolute">
  <parent link="torso"/>
  <child link="upper_arm"/>
  <origin xyz="0.15 0 0.5" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>  <!-- Rotate around Y-axis -->
  <limit lower="-2.0" upper="1.5" effort="100" velocity="1.0"/>
  <dynamics damping="0.5" friction="0.1"/>
</joint>
```

### Continuous Joints

For unlimited rotational movement:

```xml
<joint name="wheel_joint" type="continuous">
  <parent link="chassis"/>
  <child link="wheel"/>
  <axis xyz="0 1 0"/>
</joint>
```

### Fixed Joints

For permanent connections:

```xml
<joint name="fixed_joint" type="fixed">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
</joint>
```

### Prismatic Joints

For linear movement:

```xml
<joint name="prismatic_joint" type="prismatic">
  <parent link="base"/>
  <child link="slider"/>
  <axis xyz="0 0 1"/>  <!-- Move along Z-axis -->
  <limit lower="0" upper="0.5" effort="50" velocity="0.5"/>
</joint>
```

## Gazebo Integration

### Adding Gazebo-Specific Elements

```xml
<link name="sensor_link">
  <visual>
    <geometry>
      <box size="0.05 0.05 0.05"/>
    </geometry>
  </visual>
  <collision>
    <geometry>
      <box size="0.05 0.05 0.05"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="0.1"/>
    <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
  </inertial>

  <!-- Gazebo-specific visual properties -->
  <gazebo reference="sensor_link">
    <material>Gazebo/Blue</material>
    <turnGravityOff>false</turnGravityOff>
  </gazebo>
</link>

<!-- Gazebo plugin for sensors -->
<gazebo>
  <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
    <alwaysOn>true</alwaysOn>
    <updateRate>30.0</updateRate>
    <cameraName>head_camera</cameraName>
    <imageTopicName>image_raw</imageTopicName>
    <cameraInfoTopicName>camera_info</cameraInfoTopicName>
    <frameName>head_camera_optical_frame</frameName>
    <hackBaseline>0.07</hackBaseline>
    <distortionK1>0.0</distortionK1>
    <distortionK2>0.0</distortionK2>
    <distortionK3>0.0</distortionK3>
    <distortionT1>0.0</distortionT1>
    <distortionT2>0.0</distortionT2>
  </plugin>
</gazebo>
```

### Physics Properties

```xml
<gazebo reference="left_foot">
  <mu1>0.8</mu1>  <!-- Friction coefficient -->
  <mu2>0.8</mu2>
  <kp>1000000.0</kp>  <!-- Contact stiffness -->
  <kd>100.0</kd>     <!-- Contact damping -->
  <maxVel>1.0</maxVel>
  <minDepth>0.001</minDepth>
</gazebo>
```

## Humanoid-Specific Considerations

### Center of Mass and Balance

For humanoid robots, accurate inertial properties are crucial for balance:

```xml
<inertial>
  <mass value="5.0"/>
  <origin xyz="0 0 0.4" rpy="0 0 0"/>  <!-- CoM location -->
  <!-- Moments of inertia - critical for balance simulation -->
  <inertia ixx="0.2" ixy="0.0" ixz="0.0" iyy="0.3" iyz="0.0" izz="0.1"/>
</inertial>
```

### Degrees of Freedom (DOF)

Humanoid robots typically have 20-30+ degrees of freedom:
- **Legs**: 6 DOF each (hip: 3, knee: 1, ankle: 2)
- **Arms**: 7 DOF each (shoulder: 3, elbow: 1, wrist: 3)
- **Torso**: 1-3 DOF for waist movement
- **Head**: 2-3 DOF for gaze direction

### Walking Kinematics

For bipedal locomotion, consider:

```xml
<!-- Hip joints with sufficient range for walking -->
<joint name="left_hip_yaw" type="revolute">
  <parent link="torso"/>
  <child link="left_thigh"/>
  <axis xyz="0 0 1"/>
  <limit lower="-0.5" upper="0.5" effort="200" velocity="1.0"/>
</joint>

<joint name="left_hip_roll" type="revolute">
  <parent link="torso"/>
  <child link="left_thigh"/>
  <axis xyz="1 0 0"/>
  <limit lower="-0.3" upper="0.3" effort="200" velocity="1.0"/>
</joint>

<joint name="left_hip_pitch" type="revolute">
  <parent link="left_thigh"/>
  <child link="left_shin"/>
  <axis xyz="0 1 0"/>
  <limit lower="-0.2" upper="2.0" effort="200" velocity="1.0"/>
</joint>
```

## Validation and Testing

### Checking URDF Validity

```bash
# Check if URDF is well-formed
check_urdf /path/to/robot.urdf

# Visualize the robot structure
urdf_to_graphiz /path/to/robot.urdf
```

### Common Issues and Solutions

1. **Floating Masses**: Ensure all links are connected to the tree
2. **Inconsistent Units**: Use consistent units (typically meters, kilograms)
3. **Inertial Issues**: Properly calculated moments of inertia
4. **Joint Limits**: Realistic limits for humanoid joints

## Advanced URDF Features

### Transmission Elements

Define how actuators connect to joints:

```xml
<transmission name="left_elbow_trans">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="left_elbow_joint">
    <hardwareInterface>PositionJointInterface</hardwareInterface>
  </joint>
  <actuator name="left_elbow_motor">
    <hardwareInterface>PositionJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

### Gazebo Plugins

For simulation-specific behavior:

```xml
<gazebo>
  <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
    <robotNamespace>/simple_humanoid</robotNamespace>
    <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
  </plugin>
</gazebo>
```

## Best Practices for Humanoid URDF

1. **Modular Design**: Organize URDF in include files for different body parts
2. **Realistic Inertials**: Use accurate mass and inertia values
3. **Consistent Naming**: Use clear, consistent naming conventions
4. **Documentation**: Comment complex URDF sections
5. **Validation**: Regularly validate URDF with tools
6. **Iteration**: Start simple and add complexity gradually

## Hands-On Exercise

Create a simplified humanoid URDF model with:
1. Torso, head, and basic limbs
2. Proper joint types and limits
3. Basic visual and collision geometries
4. Inertial properties for dynamics simulation
5. Gazebo integration for physics simulation

## Summary

URDF is fundamental to humanoid robotics as it defines the kinematic and dynamic structure of the robot. Proper URDF modeling is essential for simulation, control, and visualization of humanoid robots. Pay special attention to joint types, inertial properties, and geometric accuracy when modeling humanoid robots.

## Next Steps

Continue to the next module on [The Digital Twin (Gazebo & Unity)](/docs/module-2/intro) to learn how to simulate your humanoid robot in virtual environments.

## Cross-References

- [Module 1 Introduction](/docs/module-1/intro)
- [Module 2: The Digital Twin (Gazebo & Unity)](/docs/module-2/intro)
- [Weeks 6-7: Robot Simulation with Gazebo](/docs/weekly-breakdown/weeks-6-7)