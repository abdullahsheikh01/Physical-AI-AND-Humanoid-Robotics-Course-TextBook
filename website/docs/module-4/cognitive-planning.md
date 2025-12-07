---
sidebar_position: 3
title: "Cognitive Planning: Using LLMs to Translate Natural Language into ROS 2 Actions"
---

# Cognitive Planning: Using LLMs to Translate Natural Language into ROS 2 Actions

## Learning Objectives

By the end of this lesson, you will be able to:
- Integrate large language models (LLMs) with robotic control systems
- Design cognitive planning architectures for natural language understanding
- Translate natural language commands into executable ROS 2 action sequences
- Implement context-aware command interpretation and planning
- Create robust error handling and recovery mechanisms for LLM-based planning
- Validate and optimize LLM-based planning performance for robotics applications

## Introduction to Cognitive Planning

Cognitive planning represents the bridge between natural language understanding and robotic action execution. It involves using large language models to interpret human commands and translate them into sequences of robot actions that achieve the requested goals while respecting safety and environmental constraints.

### The Cognitive Planning Pipeline

The cognitive planning process involves several stages:

```
Natural Language Command
         ↓
Language Understanding & Intent Recognition
         ↓
Context Integration & World Modeling
         ↓
Task Decomposition & Action Planning
         ↓
Constraint Verification & Safety Checking
         ↓
ROS 2 Action Sequence Generation
         ↓
Execution & Monitoring
```

### Challenges in LLM-Based Robotic Planning

1. **Grounding**: Connecting abstract language concepts to concrete robot capabilities
2. **Context**: Understanding the current state of the robot and environment
3. **Safety**: Ensuring planned actions are safe and appropriate
4. **Feasibility**: Verifying that planned actions are achievable by the robot
5. **Real-time Performance**: Generating plans quickly enough for interactive use
6. **Robustness**: Handling ambiguous or incorrect commands gracefully

## LLM Integration Architecture

### System Architecture Overview

The cognitive planning system architecture includes:

```python
# Example: Cognitive planning system architecture
import openai
import json
import re
from typing import Dict, List, Any, Optional
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Pose, Point
from action_msgs.msg import GoalStatus

class CognitivePlanner(Node):
    def __init__(self):
        super().__init__('cognitive_planner')

        # LLM client configuration
        self.llm_client = openai.OpenAI(api_key=self.get_llm_api_key())

        # Publishers and subscribers for ROS 2 integration
        self.command_publisher = self.create_publisher(String, 'robot_commands', 10)
        self.status_subscriber = self.create_subscription(
            String, 'robot_status', self.status_callback, 10)

        # Robot capabilities and environment information
        self.robot_capabilities = self.load_robot_capabilities()
        self.environment_map = self.load_environment_map()
        self.current_robot_state = self.get_initial_state()

        # Planning history and context
        self.conversation_history = []
        self.planning_cache = {}

    def get_llm_api_key(self):
        """Get LLM API key from configuration"""
        # In practice, use secure credential management
        return self.get_parameter_or_set_default('llm_api_key', 'your-api-key')

    def load_robot_capabilities(self):
        """Load robot capabilities and constraints"""
        return {
            "navigation": {
                "max_speed": 0.5,
                "min_turn_radius": 0.2,
                "supported_rooms": ["kitchen", "living_room", "bedroom", "office"]
            },
            "manipulation": {
                "reachable_area": {"min_x": -1.0, "max_x": 1.0, "min_y": -0.5, "max_y": 0.5},
                "gripper_types": ["suction", "parallel_jaw"],
                "max_payload": 2.0
            },
            "sensors": {
                "camera_range": 5.0,
                "lidar_range": 10.0,
                "microphone_range": 3.0
            },
            "safety_constraints": {
                "min_distance_to_human": 0.5,
                "max_operating_time": 3600,  # 1 hour
                "no_go_zones": ["staircase", "construction_area"]
            }
        }

    def load_environment_map(self):
        """Load environment layout and object locations"""
        return {
            "rooms": {
                "kitchen": {"center": {"x": 2.0, "y": 3.0}, "objects": ["table", "fridge", "sink"]},
                "living_room": {"center": {"x": 0.0, "y": 0.0}, "objects": ["sofa", "coffee_table", "tv"]},
                "bedroom": {"center": {"x": -2.0, "y": 1.0}, "objects": ["bed", "dresser", "nightstand"]},
                "office": {"center": {"x": 1.0, "y": -2.0}, "objects": ["desk", "chair", "bookshelf"]}
            },
            "navigable_paths": [
                {"from": "living_room", "to": "kitchen", "cost": 1.0},
                {"from": "living_room", "to": "bedroom", "cost": 1.5},
                {"from": "living_room", "to": "office", "cost": 2.0}
            ]
        }

    def get_initial_state(self):
        """Get initial robot state"""
        return {
            "location": {"room": "living_room", "coordinates": {"x": 0.0, "y": 0.0, "theta": 0.0}},
            "battery_level": 0.85,
            "gripper_status": "open",
            "current_task": None,
            "carrying_object": None
        }

    def status_callback(self, msg):
        """Update robot state from status messages"""
        try:
            status_data = json.loads(msg.data)
            self.current_robot_state.update(status_data)
        except json.JSONDecodeError:
            self.get_logger().warn("Invalid status message format")
```

### LLM Prompt Engineering for Robotics

```python
# Example: LLM prompt templates for robotic planning
class PromptTemplates:
    def __init__(self):
        self.command_analysis_prompt = """
You are a cognitive planning assistant for a humanoid robot. Your task is to analyze natural language commands and translate them into robot action plans.

Robot Capabilities:
{robot_capabilities}

Current Environment:
{environment_map}

Current Robot State:
{current_state}

Natural Language Command: "{command}"

Please analyze this command and provide a structured response in JSON format:

1. Intent: What the user wants to achieve
2. Entities: Specific objects, locations, or parameters mentioned
3. Action Sequence: Step-by-step plan to achieve the goal
4. Feasibility: Whether the task is achievable with current capabilities
5. Safety Check: Whether the plan is safe to execute
6. Required Information: Any missing information needed to complete the task

Response format:
{{
    "intent": "...",
    "entities": {{...}},
    "action_sequence": [
        {{
            "action_type": "...",
            "parameters": {{...}},
            "description": "..."
        }}
    ],
    "feasibility": true/false,
    "safety_check": true/false,
    "required_information": ["..."]
}}
"""

        self.action_mapping_prompt = """
Map the following natural language action to specific ROS 2 commands for a humanoid robot:

Command: "{natural_language_command}"
Context: {context}

Available ROS 2 Actions:
- navigation: Navigate to a specific location
- manipulation: Pick up, place, or manipulate an object
- interaction: Greet, wave, or interact with humans
- perception: Look for objects, scan environment
- communication: Speak or provide information

Provide the mapping in JSON format:
{{
    "action_type": "...",
    "ros_command": "...",
    "parameters": {{...}},
    "safety_constraints": [...]
}}
"""

    def format_command_analysis_prompt(self, command, robot_capabilities, environment_map, current_state):
        """Format the command analysis prompt"""
        return self.command_analysis_prompt.format(
            command=command,
            robot_capabilities=json.dumps(robot_capabilities, indent=2),
            environment_map=json.dumps(environment_map, indent=2),
            current_state=json.dumps(current_state, indent=2)
        )
```

## Natural Language Understanding and Intent Recognition

### Intent Classification System

```python
# Example: Intent classification and entity extraction
class IntentClassifier:
    def __init__(self):
        self.intent_patterns = {
            "navigation": [
                r"go to (the )?(?P<location>\w+)",
                r"navigate to (the )?(?P<location>\w+)",
                r"move to (the )?(?P<location>\w+)",
                r"bring me to (the )?(?P<location>\w+)"
            ],
            "manipulation": [
                r"pick up (the )?(?P<object>\w+)",
                r"grab (the )?(?P<object>\w+)",
                r"get (the )?(?P<object>\w+)",
                r"bring me (the )?(?P<object>\w+)",
                r"place (the )?(?P<object>\w+) on (the )?(?P<destination>\w+)"
            ],
            "interaction": [
                r"say hello",
                r"wave",
                r"greet",
                r"introduce yourself",
                r"tell me about yourself"
            ],
            "information": [
                r"what is",
                r"tell me about",
                r"describe",
                r"where is",
                r"find"
            ]
        }

    def classify_intent(self, command):
        """Classify the intent of a command using pattern matching and LLM"""
        command_lower = command.lower()

        # Try pattern matching first
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, command_lower)
                if match:
                    return intent, match.groupdict()

        # If no pattern matches, use LLM for more complex understanding
        return self.llm_classify_intent(command)

    def llm_classify_intent(self, command):
        """Use LLM to classify intent for complex commands"""
        prompt = f"""
Classify the intent of this command and extract entities:

Command: "{command}"

Available intents: navigation, manipulation, interaction, information

Response format:
{{
    "intent": "...",
    "entities": {{"...": "..."}}
}}
"""

        # In practice, call your LLM here
        # For demo purposes, return a simple classification
        return "information", {"command": command}
```

### Context Integration

```python
# Example: Context-aware command processing
class ContextIntegrator:
    def __init__(self):
        self.context_window = 10  # Number of previous interactions to remember

    def build_context(self, command, current_state, environment, conversation_history):
        """Build context for LLM planning"""
        context = {
            "current_command": command,
            "robot_state": current_state,
            "environment": environment,
            "recent_interactions": conversation_history[-self.context_window:],
            "time_of_day": self.get_current_time(),
            "user_preferences": self.get_user_preferences(),
            "safety_constraints": self.get_safety_constraints()
        }

        return context

    def get_current_time(self):
        """Get current time for context"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S %A")

    def get_user_preferences(self):
        """Get known user preferences"""
        # In practice, this would come from user profile or previous interactions
        return {
            "preferred_rooms": ["kitchen", "living_room"],
            "avoid_rooms": ["basement"],
            "preferred_interaction_style": "polite"
        }

    def get_safety_constraints(self):
        """Get current safety constraints"""
        return {
            "time_limits": True,
            "speed_limits": True,
            "no_go_zones": ["staircase"],
            "human_proximity": 0.5
        }

    def update_context_after_execution(self, command, result, context):
        """Update context after command execution"""
        # Log the interaction for future context
        interaction_log = {
            "command": command,
            "result": result,
            "timestamp": self.get_current_time(),
            "environment_state": context["environment"]
        }

        context["recent_interactions"].append(interaction_log)

        # Keep context window size manageable
        if len(context["recent_interactions"]) > self.context_window:
            context["recent_interactions"] = context["recent_interactions"][-self.context_window:]

        return context
```

## Task Decomposition and Action Planning

### Hierarchical Task Planner

```python
# Example: Hierarchical task decomposition
class HierarchicalTaskPlanner:
    def __init__(self):
        self.atomic_actions = {
            "move_to_location": self.execute_move_to_location,
            "pick_up_object": self.execute_pick_up_object,
            "place_object": self.execute_place_object,
            "speak": self.execute_speak,
            "look_for_object": self.execute_look_for_object,
            "wait": self.execute_wait
        }

    def decompose_task(self, high_level_goal, context):
        """Decompose high-level goals into atomic actions"""
        if high_level_goal["intent"] == "navigation":
            return self.decompose_navigation_task(high_level_goal, context)
        elif high_level_goal["intent"] == "manipulation":
            return self.decompose_manipulation_task(high_level_goal, context)
        elif high_level_goal["intent"] == "interaction":
            return self.decompose_interaction_task(high_level_goal, context)
        else:
            return self.decompose_generic_task(high_level_goal, context)

    def decompose_navigation_task(self, goal, context):
        """Decompose navigation tasks"""
        actions = []

        # Find path to destination
        destination = goal["entities"].get("location")
        if not destination:
            return [{"action_type": "request_clarification", "parameter": "destination"}]

        # Check if destination is valid
        if destination not in context["environment"]["rooms"]:
            return [{"action_type": "speak", "parameter": f"Sorry, I don't know where {destination} is."}]

        # Generate navigation sequence
        actions.extend([
            {
                "action_type": "speak",
                "parameter": f"Okay, I'm going to {destination} now.",
                "description": "Acknowledge the navigation request"
            },
            {
                "action_type": "navigate_to",
                "parameter": destination,
                "description": f"Navigate to {destination}"
            },
            {
                "action_type": "speak",
                "parameter": f"I have arrived at {destination}.",
                "description": "Confirm arrival"
            }
        ])

        return actions

    def decompose_manipulation_task(self, goal, context):
        """Decompose manipulation tasks"""
        actions = []

        # Extract object and destination
        obj = goal["entities"].get("object")
        destination = goal["entities"].get("destination", "current_location")

        if not obj:
            return [{"action_type": "request_clarification", "parameter": "object"}]

        actions.extend([
            {
                "action_type": "look_for_object",
                "parameter": obj,
                "description": f"Look for {obj}"
            },
            {
                "action_type": "navigate_to",
                "parameter": f"near_{obj}",
                "description": f"Navigate close to {obj}"
            },
            {
                "action_type": "pick_up_object",
                "parameter": obj,
                "description": f"Pick up {obj}"
            }
        ])

        if destination != "current_location":
            actions.extend([
                {
                    "action_type": "navigate_to",
                    "parameter": destination,
                    "description": f"Navigate to {destination}"
                },
                {
                    "action_type": "place_object",
                    "parameter": {"object": obj, "location": destination},
                    "description": f"Place {obj} at {destination}"
                }
            ])

        actions.append({
            "action_type": "speak",
            "parameter": f"I have {self.get_action_verb(goal['intent'])} the {obj}.",
            "description": "Confirm task completion"
        })

        return actions

    def get_action_verb(self, intent):
        """Get appropriate verb for the intent"""
        verb_map = {
            "manipulation": "retrieved",
            "navigation": "taken you to",
            "interaction": "performed"
        }
        return verb_map.get(intent, "completed")

    def execute_move_to_location(self, location, context):
        """Execute move to location action"""
        # In practice, this would call ROS 2 navigation services
        self.get_logger().info(f"Moving to {location}")
        return {"status": "success", "location": location}

    def execute_pick_up_object(self, obj, context):
        """Execute pick up object action"""
        # In practice, this would call ROS 2 manipulation services
        self.get_logger().info(f"Picking up {obj}")
        return {"status": "success", "object": obj}

    def execute_place_object(self, obj, location, context):
        """Execute place object action"""
        # In practice, this would call ROS 2 manipulation services
        self.get_logger().info(f"Placing {obj} at {location}")
        return {"status": "success", "object": obj, "location": location}

    def execute_speak(self, text, context):
        """Execute speak action"""
        # Publish to speech synthesis topic
        speech_msg = String()
        speech_msg.data = text
        self.speech_publisher.publish(speech_msg)
        return {"status": "success", "text": text}

    def execute_look_for_object(self, obj, context):
        """Execute look for object action"""
        # In practice, this would use perception services
        self.get_logger().info(f"Looking for {obj}")
        # Return whether object was found
        return {"status": "success", "object_found": True, "location": "table"}
```

## Safety and Constraint Verification

### Safety Checker System

```python
# Example: Safety and constraint verification
class SafetyChecker:
    def __init__(self):
        self.safety_rules = {
            "collision_avoidance": True,
            "human_safety": True,
            "environmental_safety": True,
            "robot_safety": True
        }

    def verify_plan_safety(self, action_sequence, current_state, environment):
        """Verify that an action sequence is safe to execute"""
        violations = []

        for i, action in enumerate(action_sequence):
            action_violations = self.check_action_safety(action, current_state, environment)
            violations.extend([(i, v) for v in action_violations])

        return len(violations) == 0, violations

    def check_action_safety(self, action, current_state, environment):
        """Check if a single action is safe"""
        violations = []

        action_type = action["action_type"]

        if action_type == "navigate_to":
            violations.extend(self.check_navigation_safety(action, current_state, environment))
        elif action_type == "manipulation":
            violations.extend(self.check_manipulation_safety(action, current_state, environment))
        elif action_type == "speak":
            violations.extend(self.check_communication_safety(action, current_state, environment))

        return violations

    def check_navigation_safety(self, action, current_state, environment):
        """Check navigation safety constraints"""
        violations = []

        # Check if destination is in no-go zone
        destination = action.get("parameter")
        if destination in environment.get("no_go_zones", []):
            violations.append(f"Destination {destination} is in no-go zone")

        # Check if path is clear
        current_pos = current_state["location"]["coordinates"]
        dest_pos = self.get_location_coordinates(destination, environment)

        if dest_pos:
            path_clear = self.check_path_clear(current_pos, dest_pos, environment)
            if not path_clear:
                violations.append(f"Path to {destination} is not clear")

        return violations

    def check_manipulation_safety(self, action, current_state, environment):
        """Check manipulation safety constraints"""
        violations = []

        # Check if object is safe to manipulate
        obj = action.get("parameter", {}).get("object")
        if obj:
            obj_properties = environment.get("objects", {}).get(obj, {})
            if obj_properties.get("fragile", False):
                violations.append(f"Object {obj} is fragile and may be damaged")

            # Check if object is too heavy
            weight = obj_properties.get("weight", 0)
            max_payload = current_state.get("robot_capabilities", {}).get("max_payload", 2.0)
            if weight > max_payload:
                violations.append(f"Object {obj} is too heavy to lift")

        return violations

    def check_path_clear(self, start, end, environment):
        """Check if path between two points is clear of obstacles"""
        # In practice, this would use path planning and collision checking
        # For now, return True (in practice, implement proper collision checking)
        return True

    def get_location_coordinates(self, location, environment):
        """Get coordinates for a named location"""
        room = environment.get("rooms", {}).get(location)
        if room:
            return room.get("center")
        return None
```

## ROS 2 Action Integration

### Action Server Implementation

```python
# Example: ROS 2 action server for cognitive planning
import rclpy
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from std_msgs.msg import String
from geometry_msgs.msg import Pose
from cognitive_planning_interfaces.action import ExecuteCommand

class CognitivePlanningActionServer:
    def __init__(self, node):
        self.node = node
        self.goal_handle = None

        # Create action server
        self._action_server = ActionServer(
            node,
            ExecuteCommand,
            'execute_command',
            self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=ReentrantCallbackGroup()
        )

        # Initialize cognitive planning components
        self.planner = HierarchicalTaskPlanner()
        self.safety_checker = SafetyChecker()
        self.intent_classifier = IntentClassifier()
        self.context_integrator = ContextIntegrator()

    def goal_callback(self, goal_request):
        """Handle goal request"""
        self.node.get_logger().info(f'Received command: {goal_request.command}')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Handle cancel request"""
        self.node.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """Execute the planning and action sequence"""
        self.node.get_logger().info('Executing cognitive planning')

        feedback_msg = ExecuteCommand.Feedback()
        result = ExecuteCommand.Result()

        command = goal_handle.request.command
        current_state = self.node.current_robot_state
        environment = self.node.environment_map

        try:
            # Classify intent
            intent, entities = self.intent_classifier.classify_intent(command)
            feedback_msg.status = f"Classified intent: {intent}"
            goal_handle.publish_feedback(feedback_msg)

            # Build context
            context = self.context_integrator.build_context(
                command, current_state, environment, self.node.conversation_history
            )

            # Decompose task into actions
            action_sequence = self.planner.decompose_task(
                {"intent": intent, "entities": entities}, context
            )
            feedback_msg.status = f"Generated action sequence with {len(action_sequence)} steps"
            goal_handle.publish_feedback(feedback_msg)

            # Verify safety
            is_safe, violations = self.safety_checker.verify_plan_safety(
                action_sequence, current_state, environment
            )

            if not is_safe:
                result.success = False
                result.message = f"Safety violations found: {violations}"
                goal_handle.succeed()
                return result

            # Execute action sequence
            execution_results = []
            for i, action in enumerate(action_sequence):
                if goal_handle.is_cancel_requested:
                    result.success = False
                    result.message = "Goal canceled"
                    goal_handle.canceled()
                    return result

                feedback_msg.status = f"Executing action {i+1}/{len(action_sequence)}: {action['description']}"
                goal_handle.publish_feedback(feedback_msg)

                # Execute the action
                action_result = self.execute_atomic_action(action, context)
                execution_results.append(action_result)

                if action_result.get("status") != "success":
                    result.success = False
                    result.message = f"Action failed at step {i}: {action_result.get('error', 'Unknown error')}"
                    goal_handle.succeed()
                    return result

            # Update context after successful execution
            self.context_integrator.update_context_after_execution(
                command, execution_results, context
            )

            # Update conversation history
            self.node.conversation_history.append({
                "command": command,
                "result": "success",
                "actions": len(action_sequence)
            })

            result.success = True
            result.message = f"Successfully executed {len(action_sequence)} actions"
            result.execution_log = execution_results

        except Exception as e:
            self.node.get_logger().error(f'Planning execution failed: {str(e)}')
            result.success = False
            result.message = f"Planning failed: {str(e)}"

        goal_handle.succeed()
        return result

    def execute_atomic_action(self, action, context):
        """Execute a single atomic action"""
        action_type = action["action_type"]
        parameter = action.get("parameter")

        if action_type in self.planner.atomic_actions:
            try:
                result = self.planner.atomic_actions[action_type](parameter, context)
                return {"status": "success", "result": result}
            except Exception as e:
                return {"status": "error", "error": str(e)}
        else:
            return {"status": "error", "error": f"Unknown action type: {action_type}"}
```

## Error Handling and Recovery

### Error Handling System

```python
# Example: Comprehensive error handling
class ErrorHandlingSystem:
    def __init__(self):
        self.error_types = {
            "communication_error": self.handle_communication_error,
            "navigation_error": self.handle_navigation_error,
            "manipulation_error": self.handle_manipulation_error,
            "perception_error": self.handle_perception_error,
            "safety_violation": self.handle_safety_violation
        }

    def handle_planning_error(self, error, context):
        """Handle errors during planning phase"""
        error_type = self.classify_error(error)

        if error_type in self.error_types:
            return self.error_types[error_type](error, context)
        else:
            return self.handle_generic_error(error, context)

    def classify_error(self, error):
        """Classify error type based on error message"""
        error_msg = str(error).lower()

        if any(keyword in error_msg for keyword in ["navigation", "path", "move", "go"]):
            return "navigation_error"
        elif any(keyword in error_msg for keyword in ["pick", "place", "grasp", "manipul"]):
            return "manipulation_error"
        elif any(keyword in error_msg for keyword in ["see", "find", "detect", "percept"]):
            return "perception_error"
        elif any(keyword in error_msg for keyword in ["safe", "danger", "risk"]):
            return "safety_violation"
        else:
            return "generic_error"

    def handle_navigation_error(self, error, context):
        """Handle navigation-related errors"""
        return {
            "action": "report_error",
            "message": "I encountered an issue while navigating. Let me try an alternative route.",
            "recovery": "use_alternative_navigation"
        }

    def handle_manipulation_error(self, error, context):
        """Handle manipulation-related errors"""
        return {
            "action": "report_error",
            "message": "I had trouble manipulating the object. The object might be too heavy or in an inaccessible location.",
            "recovery": "request_assistance"
        }

    def handle_perception_error(self, error, context):
        """Handle perception-related errors"""
        return {
            "action": "report_error",
            "message": "I couldn't find the object you mentioned. Could you please describe it differently or guide me to it?",
            "recovery": "request_clarification"
        }

    def handle_safety_violation(self, error, context):
        """Handle safety-related errors"""
        return {
            "action": "abort_task",
            "message": "I cannot perform this task as it would violate safety constraints.",
            "recovery": "suggest_alternative"
        }

    def handle_generic_error(self, error, context):
        """Handle generic errors"""
        return {
            "action": "report_error",
            "message": f"I encountered an unexpected error: {str(error)}. I'll need to abort this task.",
            "recovery": "return_to_safe_state"
        }
```

## Performance Optimization

### Caching and Optimization

```python
# Example: Performance optimization with caching
import functools
import time
from typing import Callable

class PerformanceOptimizer:
    def __init__(self):
        self.response_cache = {}
        self.cache_ttl = 300  # 5 minutes

    def cached_planning(self, ttl=300):
        """Decorator for caching planning results"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key from arguments
                cache_key = self.create_cache_key(args, kwargs)

                # Check if result is in cache
                if cache_key in self.response_cache:
                    cached_result, timestamp = self.response_cache[cache_key]
                    if time.time() - timestamp < ttl:
                        return cached_result

                # Execute function and cache result
                result = func(*args, **kwargs)
                self.response_cache[cache_key] = (result, time.time())

                # Clean up old cache entries
                self.cleanup_cache()

                return result
            return wrapper
        return decorator

    def create_cache_key(self, args, kwargs):
        """Create a cache key from function arguments"""
        import hashlib
        import json

        # Convert args and kwargs to a consistent string
        cache_input = {
            "args": [str(arg) for arg in args],
            "kwargs": {k: str(v) for k, v in kwargs.items()}
        }

        cache_string = json.dumps(cache_input, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()

    def cleanup_cache(self):
        """Remove expired cache entries"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.response_cache.items()
            if current_time - timestamp > self.cache_ttl
        ]

        for key in expired_keys:
            del self.response_cache[key]

# Usage example
optimizer = PerformanceOptimizer()

@optimizer.cached_planning(ttl=300)
def plan_for_command(command, context):
    """Plan for a command with caching"""
    # Expensive planning computation here
    pass
```

## Best Practices for LLM-Based Planning

### 1. Prompt Engineering Best Practices

- **Be Specific**: Provide detailed context about robot capabilities and environment
- **Use Examples**: Include few-shot examples in prompts for better performance
- **Structure Output**: Use JSON format for structured output that's easy to parse
- **Include Constraints**: Explicitly mention safety and feasibility constraints

### 2. Error Handling Best Practices

- **Graceful Degradation**: Have fallback plans when LLM responses are unclear
- **Safety First**: Always verify safety before executing actions
- **User Feedback**: Provide clear feedback when commands can't be executed
- **Logging**: Log all interactions for debugging and improvement

### 3. Performance Best Practices

- **Caching**: Cache common command interpretations
- **Pre-filtering**: Use rule-based systems for common commands before LLM
- **Asynchronous Processing**: Process LLM requests asynchronously
- **Resource Management**: Monitor and limit resource usage

## Hands-On Exercise

Implement a complete cognitive planning system with:
1. LLM integration for natural language understanding
2. Context-aware planning with environment and state information
3. Task decomposition into executable ROS 2 actions
4. Safety checking and constraint verification
5. Error handling and recovery mechanisms
6. Performance optimization techniques

## Summary

Cognitive planning using LLMs enables robots to understand and execute complex natural language commands by translating them into sequences of executable actions. The key components include intent recognition, context integration, task decomposition, safety verification, and ROS 2 action execution. Proper implementation requires careful attention to safety, error handling, and performance optimization.

## Next Steps

Continue to the next lesson on [Capstone Project: The Autonomous Humanoid](/docs/module-4/capstone-project) to integrate all components into a complete autonomous humanoid system.

## Cross-References

- [Module 4 Introduction](/docs/module-4/intro)
- [Voice-to-Action: Using OpenAI Whisper for voice commands](/docs/module-4/voice-to-action)
- [Capstone Project: The Autonomous Humanoid](/docs/module-4/capstone-project)
- [Week 13: Conversational Robotics](/docs/weekly-breakdown/week-13)