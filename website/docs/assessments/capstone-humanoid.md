---
sidebar_position: 5
title: "Capstone: Simulated Humanoid Robot with Conversational AI"
---

# Capstone: Simulated Humanoid Robot with Conversational AI

## Overview

This capstone assessment integrates all modules learned throughout the Physical AI & Humanoid Robotics E-book into a complete, autonomous humanoid robot system. You will create a simulated humanoid robot that can understand voice commands, navigate environments, manipulate objects, and interact naturally with humans using conversational AI.

## Learning Objectives

By completing this project, you will demonstrate ability to:
- Integrate all four modules into a cohesive system
- Implement end-to-end voice command processing from speech to action
- Create a comprehensive system architecture combining perception, planning, and action
- Deploy and validate a complete humanoid robot system
- Evaluate system performance through comprehensive testing scenarios
- Document and present a complete autonomous humanoid solution

## Project Requirements

### 1. Complete System Architecture
Create a system that includes:
- **Voice Processing**: OpenAI Whisper for speech recognition
- **Cognitive Planning**: LLM-based command interpretation and planning
- **Perception**: Isaac Sim/ROS-based environment understanding
- **Navigation**: Isaac-based path planning and execution
- **Manipulation**: Object interaction capabilities
- **Safety Systems**: Comprehensive safety and error handling

### 2. Humanoid Robot Model
Develop a humanoid robot model with:
- Realistic kinematics and dynamics
- Proper joint configurations for bipedal locomotion
- Integrated sensors (LiDAR, cameras, IMUs)
- Manipulation capabilities (arms, hands)

### 3. Conversational AI Integration
Implement conversational capabilities with:
- Natural language understanding
- Context-aware dialogue management
- Task decomposition and execution
- Natural response generation

### 4. Simulation Environment
Create a realistic simulation environment with:
- Indoor scenes suitable for humanoid operation
- Interactive objects and furniture
- Multiple rooms and navigation challenges
- Dynamic elements for realistic testing

## Implementation Steps

### Step 1: System Architecture Design

Design the complete system architecture:

```python
# Example: Capstone system architecture
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Pose, Twist, Point
from sensor_msgs.msg import LaserScan, Image, Imu
from builtin_interfaces.msg import Time
import threading
import queue
import time
from typing import Dict, List, Any, Optional

class CapstoneHumanoidSystem(Node):
    def __init__(self):
        super().__init__('capstone_humanoid_system')

        # Initialize all subsystems
        self.voice_system = self.initialize_voice_system()
        self.cognitive_planner = self.initialize_cognitive_planner()
        self.perception_system = self.initialize_perception_system()
        self.navigation_system = self.initialize_navigation_system()
        self.manipulation_system = self.initialize_manipulation_system()
        self.safety_system = self.initialize_safety_system()

        # State management
        self.current_state = {
            'location': {'x': 0.0, 'y': 0.0, 'theta': 0.0, 'room': 'living_room'},
            'battery_level': 1.0,
            'gripper_status': 'open',
            'current_task': None,
            'system_status': 'idle',
            'last_command': '',
            'conversation_context': []
        }

        # Publishers and subscribers
        self.status_publisher = self.create_publisher(String, 'system_status', 10)
        self.speech_publisher = self.create_publisher(String, 'robot_speech', 10)
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Sensor subscriptions
        self.battery_subscriber = self.create_subscription(
            String, 'battery_status', self.battery_callback, 10)
        self.imu_subscriber = self.create_subscription(
            Imu, 'imu/data', self.imu_callback, 10)
        self.scan_subscriber = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, 10)
        self.camera_subscriber = self.create_subscription(
            Image, 'camera/image_raw', self.camera_callback, 10)

        # Main control loop
        self.control_thread = threading.Thread(target=self.main_control_loop)
        self.control_thread.daemon = True
        self.control_thread.start()

        # Command processing queue
        self.command_queue = queue.Queue()

        self.get_logger().info("Capstone Humanoid System initialized")

    def initialize_voice_system(self):
        """Initialize voice processing system"""
        from voice_to_action_system import VoiceToActionSystem
        return VoiceToActionSystem(
            model_size="small",
            device="cuda" if self.has_gpu() else "cpu"
        )

    def initialize_cognitive_planner(self):
        """Initialize cognitive planning system"""
        from cognitive_planning_system import CognitivePlanningSystem
        return CognitivePlanningSystem()

    def initialize_perception_system(self):
        """Initialize perception system"""
        from perception_system import PerceptionSystem
        return PerceptionSystem()

    def initialize_navigation_system(self):
        """Initialize navigation system"""
        from navigation_system import NavigationSystem
        return NavigationSystem()

    def initialize_manipulation_system(self):
        """Initialize manipulation system"""
        from manipulation_system import ManipulationSystem
        return ManipulationSystem()

    def initialize_safety_system(self):
        """Initialize safety system"""
        from safety_system import SafetySystem
        return SafetySystem()

    def has_gpu(self):
        """Check if GPU is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
```

### Step 2: Voice Command Processing Pipeline

```python
# Example: Voice command processing pipeline
class VoiceCommandProcessor:
    def __init__(self, humanoid_system):
        self.system = humanoid_system
        self.voice_interface = humanoid_system.voice_system
        self.cognitive_planner = humanoid_system.cognitive_planner
        self.safety_checker = humanoid_system.safety_system

    def start_voice_processing(self):
        """Start continuous voice command processing"""
        self.voice_interface.start_listening()
        self.processing_thread = threading.Thread(target=self.continuous_processing)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def continuous_processing(self):
        """Continuously listen for and process voice commands"""
        while rclpy.ok():
            try:
                # Listen for voice command
                command_text = self.voice_interface.listen_for_command()

                if command_text:
                    self.process_command(command_text)

            except Exception as e:
                self.system.get_logger().error(f"Voice processing error: {e}")
                time.sleep(0.1)

    def process_command(self, command_text: str):
        """Process a voice command through the complete pipeline"""
        self.system.get_logger().info(f"Processing voice command: {command_text}")

        # Acknowledge the command
        self.acknowledge_command(command_text)

        try:
            # Get current state for planning
            current_state = self.system.current_state.copy()
            environment_state = self.system.perception_system.get_current_environment()

            # Generate action plan using cognitive planning
            plan = self.cognitive_planner.generate_plan(
                command_text,
                current_state,
                environment_state
            )

            if plan and plan['feasible']:
                # Check safety constraints
                is_safe, safety_issues = self.safety_checker.verify_plan_safety(plan, current_state)

                if is_safe:
                    # Execute the plan
                    success = self.execute_plan(plan, command_text)

                    if success:
                        self.announce_success(command_text)
                    else:
                        self.announce_failure(command_text)
                else:
                    self.handle_safety_issues(safety_issues, command_text)
            else:
                self.request_clarification(command_text, plan.get('required_info', []))

        except Exception as e:
            self.system.get_logger().error(f"Command processing error: {e}")
            self.announce_error(command_text, str(e))

    def acknowledge_command(self, command_text: str):
        """Acknowledge the received command"""
        response = f"I heard you say: '{command_text}'. Let me process that for you."
        self.speak(response)

    def execute_plan(self, plan: Dict[str, Any], original_command: str) -> bool:
        """Execute a cognitive plan"""
        try:
            for action in plan['action_sequence']:
                if not self.execute_single_action(action):
                    return False

            # Update conversation context
            self.system.current_state['conversation_context'].append({
                'command': original_command,
                'plan': plan,
                'result': 'success',
                'timestamp': time.time()
            })

            return True
        except Exception as e:
            self.system.get_logger().error(f"Plan execution error: {e}")
            return False

    def execute_single_action(self, action: Dict[str, Any]) -> bool:
        """Execute a single action from the plan"""
        action_type = action['action_type']
        parameters = action['parameters']

        if action_type == 'navigation':
            return self.system.navigation_system.navigate_to(parameters['location'])
        elif action_type == 'manipulation':
            return self.system.manipulation_system.execute_task(
                parameters['task'],
                parameters['object'],
                parameters.get('location')
            )
        elif action_type == 'perception':
            return self.system.perception_system.execute_task(
                parameters['task'],
                parameters.get('target')
            )
        elif action_type == 'interaction':
            self.speak(parameters['text'])
            return True
        else:
            self.system.get_logger().warn(f"Unknown action type: {action_type}")
            return False

    def announce_success(self, command_text: str):
        """Announce successful command execution"""
        response = f"I have completed the task: {command_text}"
        self.speak(response)

    def announce_failure(self, command_text: str):
        """Announce command execution failure"""
        response = f"I'm sorry, I couldn't complete: {command_text}. Would you like me to try something else?"
        self.speak(response)

    def announce_error(self, command_text: str, error: str):
        """Announce error during command processing"""
        response = f"I encountered an error processing your command: {command_text}. Please try again."
        self.speak(response)

    def request_clarification(self, command_text: str, required_info: List[str]):
        """Request clarification for ambiguous commands"""
        if required_info:
            info_str = " and ".join(required_info)
            response = f"I need more information to complete: {command_text}. Could you tell me {info_str}?"
        else:
            response = f"I didn't understand: {command_text}. Could you please repeat it?"

        self.speak(response)

    def handle_safety_issues(self, safety_issues: List[str], command_text: str):
        """Handle safety issues in the planned action"""
        safety_str = "; ".join(safety_issues)
        response = f"I cannot execute: {command_text} due to safety concerns: {safety_str}"
        self.speak(response)

    def speak(self, text: str):
        """Speak the given text"""
        msg = String()
        msg.data = text
        self.system.speech_publisher.publish(msg)
```

### Step 3: Humanoid Robot Model in Simulation

Create a humanoid robot URDF with all required sensors:

```xml
<?xml version="1.0"?>
<robot name="capstone_humanoid" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Humanoid robot constants -->
  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="torso_height" value="0.8" />
  <xacro:property name="torso_width" value="0.3" />
  <xacro:property name="torso_depth" value="0.2" />
  <xacro:property name="head_radius" value="0.1" />
  <xacro:property name="arm_length" value="0.6" />
  <xacro:property name="leg_length" value="0.8" />
  <xacro:property name="foot_size" value="0.2 0.1 0.05" />

  <!-- Torso -->
  <link name="torso">
    <visual>
      <origin xyz="0 0 ${torso_height/2}" rpy="0 0 0"/>
      <geometry>
        <box size="${torso_depth} ${torso_width} ${torso_height}"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 ${torso_height/2}" rpy="0 0 0"/>
      <geometry>
        <box size="${torso_depth} ${torso_width} ${torso_height}"/>
      </geometry>
    </collision>

    <inertial>
      <origin xyz="0 0 ${torso_height/2}" rpy="0 0 0"/>
      <mass value="5.0"/>
      <inertia
        ixx="0.2"
        ixy="0.0"
        ixz="0.0"
        iyy="0.3"
        iyz="0.0"
        izz="0.1"/>
    </inertial>
  </link>

  <!-- Head -->
  <joint name="torso_to_head" type="fixed">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 ${torso_height}" rpy="0 0 0"/>
  </joint>

  <link name="head">
    <visual>
      <geometry>
        <sphere radius="${head_radius}"/>
      </geometry>
      <material name="skin_color">
        <color rgba="0.9 0.8 0.6 1.0"/>
      </material>
    </visual>

    <collision>
      <geometry>
        <sphere radius="${head_radius}"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="1.0"/>
      <inertia
        ixx="0.002"
        ixy="0.0"
        ixz="0.0"
        iyy="0.002"
        iyz="0.0"
        izz="0.002"/>
    </inertial>
  </link>

  <!-- Camera in head -->
  <joint name="head_to_camera" type="fixed">
    <parent link="head"/>
    <child link="camera_link"/>
    <origin xyz="0.05 0 0" rpy="0 0 0"/>
  </joint>

  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.02"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
  </link>

  <!-- Left Arm -->
  <joint name="torso_to_left_shoulder" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="${torso_depth/2} ${torso_width/2} ${torso_height/2}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="100" velocity="1.0"/>
  </joint>

  <link name="left_upper_arm">
    <visual>
      <origin xyz="0 0 -${arm_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="${arm_length}"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -${arm_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="${arm_length}"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="0.8"/>
      <inertia
        ixx="0.002"
        ixy="0.0"
        ixz="0.0"
        iyy="0.002"
        iyz="0.0"
        izz="0.0005"/>
    </inertial>
  </link>

  <joint name="left_shoulder_to_elbow" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_lower_arm"/>
    <origin xyz="0 0 -${arm_length}" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="50" velocity="1.0"/>
  </joint>

  <link name="left_lower_arm">
    <visual>
      <origin xyz="0 0 -${arm_length/3}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="${2*arm_length/3}"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -${arm_length/3}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="${2*arm_length/3}"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="0.5"/>
      <inertia
        ixx="0.001"
        ixy="0.0"
        ixz="0.0"
        iyy="0.001"
        iyz="0.0"
        izz="0.0003"/>
    </inertial>
  </link>

  <!-- Left Hand -->
  <joint name="left_elbow_to_hand" type="fixed">
    <parent link="left_lower_arm"/>
    <child link="left_hand"/>
    <origin xyz="0 0 -${2*arm_length/3}" rpy="0 0 0"/>
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
      <inertia
        ixx="0.0001"
        ixy="0.0"
        ixz="0.0"
        iyy="0.0001"
        iyz="0.0"
        izz="0.0001"/>
    </inertial>
  </link>

  <!-- Right Arm (similar to left) -->
  <joint name="torso_to_right_shoulder" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_arm"/>
    <origin xyz="${torso_depth/2} ${-torso_width/2} ${torso_height/2}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="100" velocity="1.0"/>
  </joint>

  <link name="right_upper_arm">
    <visual>
      <origin xyz="0 0 -${arm_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="${arm_length}"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -${arm_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="${arm_length}"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="0.8"/>
      <inertia
        ixx="0.002"
        ixy="0.0"
        ixz="0.0"
        iyy="0.002"
        iyz="0.0"
        izz="0.0005"/>
    </inertial>
  </link>

  <joint name="right_shoulder_to_elbow" type="revolute">
    <parent link="right_upper_arm"/>
    <child link="right_lower_arm"/>
    <origin xyz="0 0 -${arm_length}" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="50" velocity="1.0"/>
  </joint>

  <link name="right_lower_arm">
    <visual>
      <origin xyz="0 0 -${arm_length/3}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="${2*arm_length/3}"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -${arm_length/3}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="${2*arm_length/3}"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="0.5"/>
      <inertia
        ixx="0.001"
        ixy="0.0"
        ixz="0.0"
        iyy="0.001"
        iyz="0.0"
        izz="0.0003"/>
    </inertial>
  </link>

  <joint name="right_elbow_to_hand" type="fixed">
    <parent link="right_lower_arm"/>
    <child link="right_hand"/>
    <origin xyz="0 0 -${2*arm_length/3}" rpy="0 0 0"/>
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
      <inertia
        ixx="0.0001"
        ixy="0.0"
        ixz="0.0"
        iyy="0.0001"
        iyz="0.0"
        izz="0.0001"/>
    </inertial>
  </link>

  <!-- Left Leg -->
  <joint name="torso_to_left_hip" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_leg"/>
    <origin xyz="${-torso_depth/4} ${torso_width/3} 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/3}" upper="${M_PI/3}" effort="200" velocity="1.0"/>
  </joint>

  <link name="left_upper_leg">
    <visual>
      <origin xyz="0 0 -${leg_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.06" length="${leg_length}"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -${leg_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.06" length="${leg_length}"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="1.5"/>
      <inertia
        ixx="0.02"
        ixy="0.0"
        ixz="0.0"
        iyy="0.02"
        iyz="0.0"
        izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_hip_to_knee" type="revolute">
    <parent link="left_upper_leg"/>
    <child link="left_lower_leg"/>
    <origin xyz="0 0 -${leg_length}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="150" velocity="1.0"/>
  </joint>

  <link name="left_lower_leg">
    <visual>
      <origin xyz="0 0 -${leg_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="${leg_length}"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -${leg_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="${leg_length}"/>
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
        izz="0.0008"/>
    </inertial>
  </link>

  <joint name="left_knee_to_foot" type="fixed">
    <parent link="left_lower_leg"/>
    <child link="left_foot"/>
    <origin xyz="0 0 -${leg_length}" rpy="0 0 0"/>
  </joint>

  <link name="left_foot">
    <visual>
      <origin xyz="0 0 -0.025" rpy="0 0 0"/>
      <geometry>
        <box size="${foot_size[0]} ${foot_size[1]} ${foot_size[2]}"/>
      </geometry>
      <material name="dark_grey">
        <color rgba="0.3 0.3 0.3 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -0.025" rpy="0 0 0"/>
      <geometry>
        <box size="${foot_size[0]} ${foot_size[1]} ${foot_size[2]}"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="0.5"/>
      <inertia
        ixx="0.001"
        ixy="0.0"
        ixz="0.0"
        iyy="0.002"
        iyz="0.0"
        izz="0.002"/>
    </inertial>
  </link>

  <!-- Right Leg (similar to left) -->
  <joint name="torso_to_right_hip" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_leg"/>
    <origin xyz="${-torso_depth/4} ${-torso_width/3} 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/3}" upper="${M_PI/3}" effort="200" velocity="1.0"/>
  </joint>

  <link name="right_upper_leg">
    <visual>
      <origin xyz="0 0 -${leg_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.06" length="${leg_length}"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -${leg_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.06" length="${leg_length}"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="1.5"/>
      <inertia
        ixx="0.02"
        ixy="0.0"
        ixz="0.0"
        iyy="0.02"
        iyz="0.0"
        izz="0.001"/>
    </inertial>
  </link>

  <joint name="right_hip_to_knee" type="revolute">
    <parent link="right_upper_leg"/>
    <child link="right_lower_leg"/>
    <origin xyz="0 0 -${leg_length}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="150" velocity="1.0"/>
  </joint>

  <link name="right_lower_leg">
    <visual>
      <origin xyz="0 0 -${leg_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="${leg_length}"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -${leg_length/2}" rpy="1.57 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="${leg_length}"/>
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
        izz="0.0008"/>
    </inertial>
  </link>

  <joint name="right_knee_to_foot" type="fixed">
    <parent link="right_lower_leg"/>
    <child link="right_foot"/>
    <origin xyz="0 0 -${leg_length}" rpy="0 0 0"/>
  </joint>

  <link name="right_foot">
    <visual>
      <origin xyz="0 0 -0.025" rpy="0 0 0"/>
      <geometry>
        <box size="${foot_size[0]} ${foot_size[1]} ${foot_size[2]}"/>
      </geometry>
      <material name="dark_grey">
        <color rgba="0.3 0.3 0.3 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -0.025" rpy="0 0 0"/>
      <geometry>
        <box size="${foot_size[0]} ${foot_size[1]} ${foot_size[2]}"/>
      </geometry>
    </collision>

    <inertial>
      <mass value="0.5"/>
      <inertia
        ixx="0.001"
        ixy="0.0"
        ixz="0.0"
        iyy="0.002"
        iyz="0.0"
        izz="0.002"/>
    </inertial>
  </link>

  <!-- Sensors -->
  <!-- LiDAR on torso -->
  <joint name="torso_to_lidar" type="fixed">
    <parent link="torso"/>
    <child link="lidar_link"/>
    <origin xyz="${torso_depth/2 + 0.05} 0 ${torso_height - 0.05}" rpy="0 0 0"/>
  </joint>

  <link name="lidar_link">
    <visual>
      <geometry>
        <cylinder radius="0.02" length="0.04"/>
      </geometry>
      <material name="red">
        <color rgba="0.8 0 0 1"/>
      </material>
    </visual>
  </link>

  <!-- IMU in torso -->
  <joint name="torso_to_imu" type="fixed">
    <parent link="torso"/>
    <child link="imu_link"/>
    <origin xyz="0 0 ${torso_height/2}" rpy="0 0 0"/>
  </joint>

  <link name="imu_link"/>

  <!-- Gazebo plugins -->
  <gazebo reference="torso">
    <material>Gazebo/Blue</material>
    <mu1>0.2</mu1>
    <mu2>0.2</mu2>
  </gazebo>

  <!-- Camera plugin -->
  <gazebo reference="camera_link">
    <sensor name="camera" type="camera">
      <always_on>true</always_on>
      <update_rate>30</update_rate>
      <camera name="head_camera">
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
          <namespace>/humanoid</namespace>
          <remapping>~/image_raw:=camera/image_raw</remapping>
          <remapping>~/camera_info:=camera/camera_info</remapping>
        </ros>
        <frame_name>camera_link</frame_name>
      </plugin>
    </sensor>
  </gazebo>

  <!-- LiDAR plugin -->
  <gazebo reference="lidar_link">
    <sensor name="lidar" type="ray">
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
      <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
        <ros>
          <namespace>/humanoid</namespace>
          <remapping>~/out:=scan</remapping>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
        <frame_name>lidar_link</frame_name>
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
          <namespace>/humanoid</namespace>
          <remapping>~/out:=imu</remapping>
        </ros>
        <frame_name>imu_link</frame_name>
        <body_name>torso</body_name>
        <update_rate>100</update_rate>
      </plugin>
    </sensor>
  </gazebo>

  <!-- Foot contact sensors -->
  <gazebo reference="left_foot">
    <sensor name="left_foot_contact" type="contact">
      <always_on>true</always_on>
      <update_rate>30</update_rate>
      <contact>
        <collision>left_foot_collision</collision>
      </contact>
      <plugin name="left_foot_contact_plugin" filename="libgazebo_ros_bumper.so">
        <ros>
          <namespace>/humanoid</namespace>
          <remapping>~/out:=left_foot_contact</remapping>
        </ros>
        <frame_name>left_foot</frame_name>
      </plugin>
    </sensor>
  </gazebo>

  <gazebo reference="right_foot">
    <sensor name="right_foot_contact" type="contact">
      <always_on>true</always_on>
      <update_rate>30</update_rate>
      <contact>
        <collision>right_foot_collision</collision>
      </contact>
      <plugin name="right_foot_contact_plugin" filename="libgazebo_ros_bumper.so">
        <ros>
          <namespace>/humanoid</namespace>
          <remapping>~/out:=right_foot_contact</remapping>
        </ros>
        <frame_name>right_foot</frame_name>
      </plugin>
    </sensor>
  </gazebo>

</robot>
```

### Step 4: Cognitive Planning Integration

```python
# Example: Cognitive planning system for humanoid
class CognitivePlanningSystem:
    def __init__(self):
        self.robot_capabilities = self.define_robot_capabilities()
        self.environment_map = self.load_environment_map()
        self.llm_client = self.initialize_llm_client()

    def define_robot_capabilities(self):
        """Define what the robot can do"""
        return {
            "navigation": {
                "supported_rooms": ["kitchen", "living_room", "bedroom", "office", "bathroom"],
                "max_speed": 0.3,
                "min_turn_radius": 0.2,
                "obstacle_avoidance": True
            },
            "manipulation": {
                "reachable_area": {
                    "min_x": -0.8, "max_x": 0.8,
                    "min_y": -0.6, "max_y": 0.6,
                    "min_z": 0.2, "max_z": 1.5
                },
                "gripper_types": ["parallel_jaw", "suction"],
                "max_payload": 2.0,
                "precision_tasks": ["pick", "place", "grasp"]
            },
            "interaction": {
                "speech_synthesis": True,
                "gesture": ["wave", "point", "nod"],
                "face_tracking": True
            },
            "safety_constraints": {
                "min_distance_to_human": 0.5,
                "no_go_zones": ["staircase", "construction_area", "restricted"],
                "max_operating_time": 3600  # 1 hour
            }
        }

    def load_environment_map(self):
        """Load environment layout and object locations"""
        return {
            "rooms": {
                "kitchen": {
                    "center": {"x": 2.0, "y": 3.0},
                    "objects": ["table", "chair", "fridge", "sink", "cupboard"],
                    "descriptors": ["cooking area", "food preparation"]
                },
                "living_room": {
                    "center": {"x": 0.0, "y": 0.0},
                    "objects": ["sofa", "coffee_table", "tv", "bookshelf", "lamp"],
                    "descriptors": ["relaxation area", "entertainment"]
                },
                "bedroom": {
                    "center": {"x": -2.0, "y": 1.0},
                    "objects": ["bed", "dresser", "nightstand", "wardrobe", "desk"],
                    "descriptors": ["sleeping area", "personal space"]
                },
                "office": {
                    "center": {"x": 1.0, "y": -2.0},
                    "objects": ["desk", "chair", "computer", "bookshelf", "file_cabinet"],
                    "descriptors": ["work area", "study space"]
                }
            },
            "navigable_paths": [
                {"from": "living_room", "to": "kitchen", "cost": 1.0},
                {"from": "living_room", "to": "bedroom", "cost": 1.5},
                {"from": "living_room", "to": "office", "cost": 2.0},
                {"from": "kitchen", "to": "office", "cost": 2.5}
            ]
        }

    def initialize_llm_client(self):
        """Initialize LLM client for cognitive planning"""
        # In practice, this would connect to OpenAI or other LLM API
        try:
            import openai
            return openai.OpenAI(api_key="your-api-key")
        except ImportError:
            return None

    def generate_plan(self, command: str, current_state: dict, environment_state: dict) -> dict:
        """Generate an action plan from a natural language command"""
        try:
            # Create prompt for LLM
            prompt = self.create_planning_prompt(command, current_state, environment_state)

            if self.llm_client:
                # Use LLM for complex planning
                response = self.llm_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self.get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )

                plan = self.parse_llm_response(response.choices[0].message.content)
            else:
                # Fallback to rule-based planning
                plan = self.rule_based_planning(command, current_state, environment_state)

            # Validate the plan
            validated_plan = self.validate_plan(plan, current_state)

            return validated_plan

        except Exception as e:
            self.get_logger().error(f"Planning error: {e}")
            return {
                "feasible": False,
                "action_sequence": [],
                "required_info": ["clarification needed"],
                "error": str(e)
            }

    def create_planning_prompt(self, command: str, current_state: dict, environment_state: dict) -> str:
        """Create a prompt for the LLM to generate a plan"""
        prompt = f"""
You are a cognitive planning assistant for a humanoid robot. Given the following information, create a step-by-step plan to execute the user's command.

Robot Capabilities:
{self.robot_capabilities}

Current Robot State:
{current_state}

Current Environment:
{environment_state}

User Command: "{command}"

Please provide a structured plan in JSON format with the following fields:
- "feasible": true/false
- "action_sequence": array of actions with type and parameters
- "required_info": array of information needed if command is ambiguous
- "estimated_time": estimated time to complete in seconds

Each action in action_sequence should have:
- "action_type": navigation, manipulation, interaction, perception
- "parameters": specific parameters for the action
- "description": human-readable description

Example response format:
{{
    "feasible": true,
    "action_sequence": [
        {{
            "action_type": "navigation",
            "parameters": {{"location": "kitchen"}},
            "description": "Navigate to kitchen"
        }},
        {{
            "action_type": "perception",
            "parameters": {{"task": "find_object", "object": "cup"}},
            "description": "Look for cup on table"
        }}
    ],
    "required_info": [],
    "estimated_time": 120
}}
"""

        return prompt

    def get_system_prompt(self) -> str:
        """Get system prompt for LLM"""
        return """
You are a cognitive planning assistant for a humanoid robot. Your role is to interpret natural language commands and create executable action plans. Consider the robot's capabilities, current state, and environment when creating plans. Ensure all plans are safe and feasible given the robot's limitations.
"""

    def parse_llm_response(self, response: str) -> dict:
        """Parse the LLM response into a structured plan"""
        import json
        import re

        # Extract JSON from response if it contains other text
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                plan = json.loads(json_match.group())
                return plan
            except json.JSONDecodeError:
                pass

        # If parsing fails, return a basic plan
        return {
            "feasible": False,
            "action_sequence": [],
            "required_info": ["could not parse LLM response"],
            "estimated_time": 0
        }

    def rule_based_planning(self, command: str, current_state: dict, environment_state: dict) -> dict:
        """Fallback rule-based planning for simple commands"""
        command_lower = command.lower()

        # Simple navigation commands
        if any(word in command_lower for word in ["go to", "navigate to", "move to"]):
            for room in self.environment_map["rooms"]:
                if room in command_lower:
                    return {
                        "feasible": True,
                        "action_sequence": [{
                            "action_type": "navigation",
                            "parameters": {"location": room},
                            "description": f"Navigate to {room}"
                        }],
                        "required_info": [],
                        "estimated_time": 60
                    }

        # Simple manipulation commands
        if any(word in command_lower for word in ["pick up", "get", "grab"]):
            # Extract object if possible
            import re
            obj_match = re.search(r'(?:pick up|get|grab) (?:the )?(\w+)', command_lower)
            if obj_match:
                obj = obj_match.group(1)
                return {
                    "feasible": True,
                    "action_sequence": [
                        {
                            "action_type": "perception",
                            "parameters": {"task": "find_object", "object": obj},
                            "description": f"Look for {obj}"
                        },
                        {
                            "action_type": "manipulation",
                            "parameters": {"task": "pick_up", "object": obj},
                            "description": f"Pick up {obj}"
                        }
                    ],
                    "required_info": [],
                    "estimated_time": 180
                }

        # Default response
        return {
            "feasible": False,
            "action_sequence": [],
            "required_info": ["complex command - requires clarification"],
            "estimated_time": 0
        }

    def validate_plan(self, plan: dict, current_state: dict) -> dict:
        """Validate the plan against robot capabilities and safety constraints"""
        if not plan.get("feasible", False):
            return plan

        # Check if robot has required capabilities
        for action in plan.get("action_sequence", []):
            action_type = action.get("action_type")

            if action_type == "navigation":
                location = action["parameters"]["location"]
                if location not in self.robot_capabilities["navigation"]["supported_rooms"]:
                    plan["feasible"] = False
                    plan["required_info"] = [f"Location {location} not supported"]
                    break

            elif action_type == "manipulation":
                # Check if object is within reachable area
                pass  # Add reachability checks

        return plan
```

## Testing Requirements

### 1. System Integration Tests
- [ ] All subsystems initialize correctly
- [ ] ROS 2 communication works between components
- [ ] TF tree is properly maintained
- [ ] Sensor data flows correctly through pipeline

### 2. Voice Command Tests
- [ ] Speech recognition works with various commands
- [ ] Natural language understanding is accurate
- [ ] Command-to-action mapping is correct
- [ ] Error handling for unclear commands

### 3. Navigation Tests
- [ ] Path planning works in various environments
- [ ] Obstacle avoidance functions properly
- [ ] Humanoid locomotion is stable
- [ ] Navigation is safe and collision-free

### 4. Manipulation Tests
- [ ] Object detection and localization work
- [ ] Grasping and manipulation are successful
- [ ] Task completion rate is acceptable
- [ ] Safety constraints are respected

### 5. End-to-End Tests
- [ ] Complete command processing from voice to action
- [ ] Multi-step task execution
- [ ] Error recovery and safety fallbacks
- [ ] Performance under various conditions

## Success Criteria

### Functional Requirements
- [ ] Voice commands are processed with >80% accuracy
- [ ] Navigation tasks complete with >90% success rate
- [ ] Manipulation tasks complete with >75% success rate
- [ ] System operates safely without human intervention
- [ ] All modules integrate seamlessly

### Quality Requirements
- [ ] Code follows ROS 2 and Isaac best practices
- [ ] Proper error handling and logging
- [ ] Comprehensive documentation
- [ ] Well-structured and maintainable code
- [ ] Adequate testing coverage

### Performance Requirements
- [ ] System responds to commands within 5 seconds
- [ ] Real-time operation is maintained
- [ ] Resource usage is optimized
- [ ] Battery life considerations are addressed

## Documentation Requirements

### 1. System Architecture Documentation
- Complete system diagram with all components
- Data flow and message types
- Component interfaces and APIs
- Deployment and configuration guides

### 2. User Manual
- Command reference and examples
- Safety guidelines and procedures
- Troubleshooting guide
- Maintenance instructions

### 3. Technical Documentation
- Code structure and organization
- Algorithm explanations
- Performance benchmarks
- Future enhancement possibilities

## Resources

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [NVIDIA Isaac Sim Documentation](https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html)
- [OpenAI Whisper Documentation](https://github.com/openai/whisper)
- [Large Language Model Integration Guides](https://platform.openai.com/docs/guides/gpt)

## Evaluation Rubric

| Criteria | Points | Details |
|----------|--------|---------|
| System Integration | 25 | All modules integrated cohesively |
| Voice Processing | 20 | Accurate speech recognition and understanding |
| Navigation & Locomotion | 20 | Stable and safe movement capabilities |
| Manipulation | 15 | Successful object interaction |
| Safety & Error Handling | 10 | Robust safety systems |
| Documentation & Testing | 10 | Complete documentation and validation |

## Next Steps

This capstone project represents the culmination of the Physical AI & Humanoid Robotics E-book. After completing this assessment, you will have gained comprehensive knowledge of:
- Robot Operating System 2 (ROS 2) and its applications
- Simulation and perception systems for robotics
- AI and navigation systems for autonomous robots
- Natural language processing for human-robot interaction
- System integration and validation methodologies

This foundation prepares you for advanced work in humanoid robotics, autonomous systems, and AI-driven robotics applications.

## Cross-References

- [Module 1: The Robotic Nervous System (ROS 2)](/docs/module-1/intro)
- [Module 2: The Digital Twin (Gazebo & Unity)](/docs/module-2/intro)
- [Module 3: The AI-Robot Brain (NVIDIA Isaac™)](/docs/module-3/intro)
- [Module 4: Vision-Language-Action (VLA)](/docs/module-4/intro)
- [Week 13: Conversational Robotics](/docs/weekly-breakdown/week-13)