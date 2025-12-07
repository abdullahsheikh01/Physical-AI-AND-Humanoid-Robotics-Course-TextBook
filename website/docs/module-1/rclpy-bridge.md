---
sidebar_position: 3
title: "Bridging Python Agents to ROS Controllers using rclpy"
---

# Bridging Python Agents to ROS Controllers using rclpy

## Learning Objectives

By the end of this lesson, you will be able to:
- Use rclpy to create Python nodes that interface with ROS 2
- Design bridge systems between AI agents and robot controllers
- Implement message passing between Python agents and ROS systems
- Handle asynchronous operations in AI-ROS integration
- Create robust interfaces that maintain system stability

## Introduction to rclpy

rclpy is the Python client library for ROS 2, providing Python bindings that allow you to create ROS 2 nodes, publish and subscribe to topics, make service calls, and provide services. It serves as the essential bridge between Python-based AI agents and the ROS 2 robot control ecosystem.

### Why Python for AI Agents?

Python is the dominant language for AI and machine learning development because:
- **Rich Ecosystem**: Extensive libraries for AI, ML, computer vision, and NLP
- **Ease of Development**: Rapid prototyping and experimentation
- **Community Support**: Large community of AI researchers and practitioners
- **Integration**: Easy integration with ROS 2 through rclpy

## Setting Up rclpy Bridge

### Basic Bridge Node Structure

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time
import threading

class AgentBridge(Node):
    def __init__(self):
        super().__init__('agent_bridge')

        # Publishers for sending commands to robot
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Subscribers for receiving sensor data
        self.sensor_subscriber = self.create_subscription(
            String,
            'sensor_data',
            self.sensor_callback,
            10
        )

        # Initialize AI agent
        self.ai_agent = self.initialize_ai_agent()

        # Thread for AI processing
        self.ai_thread = threading.Thread(target=self.run_ai_processing)
        self.ai_thread.daemon = True
        self.ai_thread.start()

    def initialize_ai_agent(self):
        # Initialize your AI agent here
        # This could be a neural network, rule-based system, etc.
        return AIAgent()

    def sensor_callback(self, msg):
        # Process incoming sensor data
        self.get_logger().info(f'Received sensor data: {msg.data}')

        # Send data to AI agent for processing
        self.ai_agent.process_sensor_data(msg.data)

    def run_ai_processing(self):
        # Continuous AI processing loop
        while rclpy.ok():
            if self.ai_agent.has_decision_ready():
                decision = self.ai_agent.get_decision()
                self.execute_decision(decision)
            time.sleep(0.1)  # Small delay to prevent busy waiting

    def execute_decision(self, decision):
        # Convert AI decision to ROS message
        cmd = Twist()
        cmd.linear.x = decision.linear_velocity
        cmd.angular.z = decision.angular_velocity
        self.cmd_vel_publisher.publish(cmd)
```

## AI Agent Integration Patterns

### Pattern 1: Direct Integration

The AI agent runs within the same ROS node:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class DirectAIBridge(Node):
    def __init__(self):
        super().__init__('direct_ai_bridge')

        # Publishers and subscribers
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.scan_subscriber = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

        # Initialize AI model
        self.ai_model = self.train_navigation_model()

    def train_navigation_model(self):
        # In practice, you would load a pre-trained model
        # For this example, we'll create a simple classifier
        model = RandomForestClassifier()
        # Training code would go here
        return model

    def scan_callback(self, scan_msg):
        # Convert laser scan to features
        features = self.process_scan_for_features(scan_msg)

        # Get AI decision
        action = self.ai_model.predict([features])[0]

        # Convert action to ROS command
        cmd = self.action_to_command(action)
        self.cmd_vel_publisher.publish(cmd)

    def process_scan_for_features(self, scan_msg):
        # Extract features from laser scan
        ranges = np.array(scan_msg.ranges)
        ranges = np.nan_to_num(ranges, nan=np.inf)

        # Calculate features: min distance, front distance, left/right distances
        features = [
            np.min(ranges),  # Minimum distance to obstacle
            np.mean(ranges[300:360]),  # Front left
            np.mean(ranges[0:60]),     # Front right
            np.mean(ranges[150:210]),  # Back
        ]
        return features

    def action_to_command(self, action):
        cmd = Twist()
        if action == 0:  # Move forward
            cmd.linear.x = 0.5
        elif action == 1:  # Turn left
            cmd.angular.z = 0.5
        elif action == 2:  # Turn right
            cmd.angular.z = -0.5
        elif action == 3:  # Stop
            pass  # cmd is already zero
        return cmd
```

### Pattern 2: Separate Process Bridge

The AI agent runs in a separate process and communicates via ROS:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import subprocess
import json
import threading

class ProcessBridge(Node):
    def __init__(self):
        super().__init__('process_bridge')

        # Publishers and subscribers
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.image_subscriber = self.create_subscription(
            Image,
            'camera/image_raw',
            self.image_callback,
            10
        )

        # Start AI agent process
        self.ai_process = subprocess.Popen([
            'python', 'ai_agent.py'
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        # Start thread to handle AI agent responses
        self.response_thread = threading.Thread(target=self.handle_ai_responses)
        self.response_thread.daemon = True
        self.response_thread.start()

    def image_callback(self, image_msg):
        # Convert image to format expected by AI agent
        image_data = self.convert_image_for_ai(image_msg)

        # Send to AI agent
        ai_input = {
            'type': 'image',
            'data': image_data,
            'timestamp': image_msg.header.stamp.sec
        }

        self.ai_process.stdin.write(json.dumps(ai_input) + '\n')
        self.ai_process.stdin.flush()

    def handle_ai_responses(self):
        for line in iter(self.ai_process.stdout.readline, ''):
            try:
                response = json.loads(line.strip())
                self.process_ai_response(response)
            except json.JSONDecodeError:
                self.get_logger().error('Invalid JSON from AI agent')

    def process_ai_response(self, response):
        if response['type'] == 'action':
            cmd = Twist()
            cmd.linear.x = response['linear_velocity']
            cmd.angular.z = response['angular_velocity']
            self.cmd_vel_publisher.publish(cmd)
```

### Pattern 3: Service-Based Integration

The AI agent provides services that ROS nodes can call:

```python
import rclpy
from rclpy.node import Node
from your_package.srv import PlanAction
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import threading

class ServiceBasedBridge(Node):
    def __init__(self):
        super().__init__('service_bridge')

        # Publishers and subscribers
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.scan_subscriber = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

        # Service client for AI agent
        self.ai_client = self.create_client(PlanAction, 'plan_action')
        while not self.ai_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('AI service not available, waiting...')

    def scan_callback(self, scan_msg):
        # Prepare request for AI agent
        request = PlanAction.Request()
        request.scan_data = scan_msg.ranges  # Simplified
        request.robot_pose = self.get_robot_pose()

        # Call AI agent service
        future = self.ai_client.call_async(request)
        future.add_done_callback(self.ai_response_callback)

    def ai_response_callback(self, future):
        try:
            response = future.result()
            cmd = Twist()
            cmd.linear.x = response.linear_velocity
            cmd.angular.z = response.angular_velocity
            self.cmd_vel_publisher.publish(cmd)
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
```

## Advanced Integration Techniques

### Async/Await Pattern

Using asyncio for non-blocking AI processing:

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import asyncio
import aiohttp
import threading

class AsyncBridge(Node):
    def __init__(self):
        super().__init__('async_bridge')

        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.image_subscriber = self.create_subscription(
            Image,
            'camera/image_raw',
            self.image_callback,
            QoSProfile(depth=1)
        )

        # Create asyncio event loop in separate thread
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.run_async_loop, args=(self.loop,))
        self.thread.daemon = True
        self.thread.start()

    def run_async_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def image_callback(self, image_msg):
        # Schedule async processing in the event loop
        future = asyncio.run_coroutine_threadsafe(
            self.process_image_async(image_msg),
            self.loop
        )
        future.add_done_callback(self.processing_done_callback)

    async def process_image_async(self, image_msg):
        # Convert image to bytes
        image_bytes = self.convert_image_to_bytes(image_msg)

        # Send to AI service (simulated)
        async with aiohttp.ClientSession() as session:
            async with session.post('http://ai-service:8080/predict', data=image_bytes) as response:
                result = await response.json()
                return result

    def processing_done_callback(self, future):
        try:
            result = future.result()
            cmd = self.result_to_command(result)
            self.cmd_vel_publisher.publish(cmd)
        except Exception as e:
            self.get_logger().error(f'Async processing failed: {e}')
```

### State Management for Complex Agents

Managing state between AI decisions:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import time
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class RobotState:
    position: tuple = (0.0, 0.0)
    orientation: float = 0.0
    velocity: tuple = (0.0, 0.0)
    last_scan: list = None
    goal: tuple = None
    state_timestamp: float = 0.0

class StatefulBridge(Node):
    def __init__(self):
        super().__init__('stateful_bridge')

        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.scan_subscriber = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

        # Initialize robot state
        self.robot_state = RobotState()
        self.ai_agent_state = {}  # Agent-specific state

        # Timer for periodic AI processing
        self.timer = self.create_timer(0.1, self.ai_processing_callback)

    def scan_callback(self, scan_msg):
        # Update robot state with latest scan
        self.robot_state.last_scan = list(scan_msg.ranges)
        self.robot_state.state_timestamp = time.time()

    def ai_processing_callback(self):
        # Check if we have recent sensor data
        if time.time() - self.robot_state.state_timestamp > 1.0:
            self.get_logger().warn('No recent sensor data')
            return

        # Process with AI agent
        decision = self.make_ai_decision()

        if decision is not None:
            cmd = self.decision_to_command(decision)
            self.cmd_vel_publisher.publish(cmd)

    def make_ai_decision(self):
        # Complex decision making using current state
        if self.robot_state.last_scan is None:
            return None

        # Example: Simple navigation logic
        min_distance = min(self.robot_state.last_scan)

        if min_distance < 0.5:  # Obstacle too close
            return {'linear': 0.0, 'angular': 0.5}  # Turn
        elif self.robot_state.goal:
            # Navigate to goal logic would go here
            return {'linear': 0.5, 'angular': 0.0}  # Move forward
        else:
            return {'linear': 0.3, 'angular': 0.0}  # Explore

    def decision_to_command(self, decision):
        cmd = Twist()
        cmd.linear.x = decision['linear']
        cmd.angular.z = decision['angular']
        return cmd
```

## Error Handling and Robustness

### Graceful Degradation

Handle AI agent failures gracefully:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

class RobustBridge(Node):
    def __init__(self):
        super().__init__('robust_bridge')

        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.scan_subscriber = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

        self.last_ai_command_time = time.time()
        self.fallback_active = False
        self.fallback_timer = self.create_timer(0.1, self.fallback_check)

    def scan_callback(self, scan_msg):
        try:
            # Attempt AI-based decision
            decision = self.safe_ai_decision(scan_msg)

            if decision is not None:
                self.last_ai_command_time = time.time()
                self.fallback_active = False

                cmd = self.decision_to_command(decision)
                self.cmd_vel_publisher.publish(cmd)
            else:
                self.get_logger().warn('AI agent returned no decision')

        except Exception as e:
            self.get_logger().error(f'AI agent error: {e}')
            # Continue with fallback behavior

    def safe_ai_decision(self, scan_msg):
        # Add timeout and error handling to AI processing
        try:
            # AI processing with timeout
            # This is a simplified example - in practice you'd use actual AI processing
            if min(scan_msg.ranges) < 0.3:
                return {'linear': 0.0, 'angular': 0.5}  # Turn to avoid obstacle
            else:
                return {'linear': 0.5, 'angular': 0.0}  # Move forward
        except:
            return None  # Fallback to safe behavior

    def fallback_check(self):
        # Check if AI agent has been unresponsive
        if time.time() - self.last_ai_command_time > 5.0:  # 5 seconds
            if not self.fallback_active:
                self.get_logger().warn('Activating fallback behavior')
                self.fallback_active = True

            # Simple fallback: stop if too long without AI input
            cmd = Twist()
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.cmd_vel_publisher.publish(cmd)
```

## Performance Considerations

### Threading and Concurrency

Best practices for handling concurrent AI and ROS operations:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import threading
import queue
from collections import deque
import time

class ThreadingBridge(Node):
    def __init__(self):
        super().__init__('threading_bridge')

        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.image_subscriber = self.create_subscription(
            Image,
            'camera/image_raw',
            self.image_callback,
            10
        )

        # Queue for image processing
        self.image_queue = queue.Queue(maxsize=5)

        # Thread for AI processing
        self.ai_thread = threading.Thread(target=self.ai_processing_loop)
        self.ai_thread.daemon = True
        self.ai_thread.start()

        # Buffer for results to handle timing
        self.result_buffer = deque(maxlen=10)

    def image_callback(self, image_msg):
        # Add to queue, dropping oldest if full
        try:
            self.image_queue.put_nowait(image_msg)
        except queue.Full:
            self.get_logger().warn('Image queue full, dropping frame')

    def ai_processing_loop(self):
        while rclpy.ok():
            try:
                # Get image from queue with timeout
                image_msg = self.image_queue.get(timeout=0.1)

                # Process with AI (simulated)
                result = self.process_with_ai(image_msg)

                # Add result to buffer
                self.result_buffer.append({
                    'timestamp': time.time(),
                    'result': result
                })

            except queue.Empty:
                continue  # Check again
            except Exception as e:
                self.get_logger().error(f'AI processing error: {e}')

    def process_with_ai(self, image_msg):
        # Simulate AI processing
        # In real implementation, this would run your AI model
        time.sleep(0.05)  # Simulate processing time
        return {'linear': 0.5, 'angular': 0.0}
```

## Best Practices for AI-ROS Integration

1. **Latency Management**: Balance AI processing depth with real-time requirements
2. **Resource Management**: Monitor CPU and memory usage of AI processes
3. **Data Synchronization**: Ensure AI decisions align with current sensor data
4. **Safety Fallbacks**: Implement safe behaviors when AI fails
5. **Logging and Monitoring**: Track AI performance and decision quality
6. **Modularity**: Keep AI components separate for easy replacement/upgrades

## Hands-On Exercise

Create a bridge between a simple Python-based decision tree agent and a ROS 2 robot that:
1. Subscribes to laser scan data
2. Uses the data to make navigation decisions
3. Publishes velocity commands to control the robot
4. Includes error handling and fallback behaviors

## Summary

The rclpy library provides the essential bridge between Python-based AI agents and ROS 2 robot control systems. By understanding different integration patterns, error handling strategies, and performance considerations, you can create robust systems that leverage the power of AI while maintaining the reliability of ROS 2.

## Next Steps

Continue to the next lesson on [Understanding URDF (Unified Robot Description Format) for humanoids](/docs/module-1/urdf-humanoids) to learn how to define robot structures for humanoid applications.

## Cross-References

- [Module 1 Introduction](/docs/module-1/intro)
- [ROS 2 Nodes, Topics, and Services](/docs/module-1/ros2-nodes-topics-services)
- [Understanding URDF for humanoids](/docs/module-1/urdf-humanoids)
- [Weeks 3-5: ROS 2 Fundamentals](/docs/weekly-breakdown/weeks-3-5)