---
sidebar_position: 4
title: "Nav2: Path Planning for Bipedal Humanoid Movement"
---

# Nav2: Path Planning for Bipedal Humanoid Movement

## Learning Objectives

By the end of this lesson, you will be able to:
- Configure Nav2 for humanoid robot navigation with bipedal constraints
- Implement custom path planners suitable for legged locomotion
- Design footstep planners for stable bipedal navigation
- Integrate balance and stability considerations into navigation
- Validate navigation performance for humanoid-specific challenges
- Optimize navigation parameters for human-like movement patterns

## Introduction to Humanoid Navigation

Humanoid navigation presents unique challenges compared to wheeled or tracked robots. Bipedal locomotion requires careful consideration of balance, foot placement, and dynamic stability. Traditional navigation approaches must be adapted to account for the complex kinematics and dynamics of legged systems.

### Key Challenges in Humanoid Navigation

1. **Balance Maintenance**: Keeping the center of mass within the support polygon
2. **Footstep Planning**: Determining where to place feet for stable locomotion
3. **Dynamic Stability**: Managing stability during movement transitions
4. **Terrain Adaptation**: Handling uneven surfaces and obstacles
5. **Energy Efficiency**: Optimizing for battery life and operational time

### Navigation Architecture for Humanoids

The navigation system for humanoid robots typically includes:

```
High-Level Planner (Global)
├── Topological Map
├── Waypoint Generation
└── Path Optimization

Mid-Level Planner (Footstep)
├── Footstep Sequencing
├── Balance Constraint Checking
└── Stability Verification

Low-Level Controller (Motion)
├── Inverse Kinematics
├── Balance Control
└── Motor Commands
```

## Nav2 Configuration for Humanoid Robots

### Global Planner Adaptations

For humanoid robots, global planners need to consider:

```yaml
# Example: Global planner configuration for humanoid navigation
global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      width: 20
      height: 20
      resolution: 0.05  # Higher resolution for precise foot placement
      origin_x: -10.0
      origin_y: -10.0
      robot_base_frame: base_link
      global_frame: map
      rolling_window: false
      track_unknown_space: true
      footprint: [[-0.3, -0.2], [-0.3, 0.2], [0.3, 0.2], [0.3, -0.2]]
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]

      # Humanoid-specific parameters
      robot_radius: 0.3  # Radius considering arm span
      transform_tolerance: 0.2
      lethal_cost_threshold: 90
      always_send_full_costmap: true

  static_layer:
    plugin: "nav2_costmap_2d::StaticLayer"
    map_subscribe_transient_local: true

  obstacle_layer:
    plugin: "nav2_costmap_2d::ObstacleLayer"
    enabled: true
    observation_sources: scan
    scan:
      topic: /scan
      max_obstacle_height: 2.0  # Consider obstacles up to human height
      clearing: true
      marking: true
      data_type: "LaserScan"
      raytrace_max_range: 3.0
      raytrace_min_range: 0.0
      obstacle_max_range: 2.5
      obstacle_min_range: 0.0

  inflation_layer:
    plugin: "nav2_costmap_2d::InflationLayer"
    cost_scaling_factor: 3.0  # Higher inflation for humanoid safety
    inflation_radius: 0.6     # Larger safety margin
    inflate_unknown: false
    inflate_around_unknown: true
```

### Local Planner Configuration

Local planners for humanoid robots must handle dynamic balance:

```yaml
# Example: Local planner configuration for humanoid navigation
local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      width: 5
      height: 5
      resolution: 0.025  # Very high resolution for footstep planning
      robot_base_frame: base_footprint
      global_frame: odom
      rolling_window: true
      track_unknown_space: false
      footprint: [[-0.15, -0.1], [-0.15, 0.1], [0.15, 0.1], [0.15, -0.1]]
      plugins: ["voxel_layer", "inflation_layer"]

      # Humanoid-specific parameters
      robot_radius: 0.2
      transform_tolerance: 0.1

  voxel_layer:
    plugin: "nav2_costmap_2d::VoxelLayer"
    enabled: true
    publish_voxel_map: true
    origin_z: 0.0
    z_resolution: 0.2
    z_voxels: 10
    max_obstacle_height: 2.0
    mark_threshold: 0
    observation_sources: scan
    scan:
      topic: /scan
      max_obstacle_height: 2.0
      clearing: true
      marking: true
      data_type: "LaserScan"
      raytrace_max_range: 3.0
      raytrace_min_range: 0.0
      obstacle_max_range: 2.5
      obstacle_min_range: 0.0

  inflation_layer:
    plugin: "nav2_costmap_2d::InflationLayer"
    cost_scaling_factor: 8.0
    inflation_radius: 0.5
    inflate_unknown: false
```

## Footstep Planning for Bipedal Navigation

### Footstep Planner Fundamentals

Footstep planning is crucial for humanoid navigation. It determines where each foot should be placed to maintain balance and achieve navigation goals.

```python
# Example: Basic footstep planner implementation
import numpy as np
from geometry_msgs.msg import Point
from nav_msgs.msg import Path
from visualization_msgs.msg import Marker, MarkerArray

class FootstepPlanner:
    def __init__(self):
        self.step_width = 0.2    # Distance between feet
        self.step_length = 0.3   # Forward step length
        self.max_step_height = 0.1  # Maximum step height for obstacles

    def plan_footsteps(self, global_path, robot_pose):
        """
        Plan footstep sequence from global path
        """
        footsteps = []

        # Start with current foot positions
        left_foot, right_foot = self.get_current_foot_positions(robot_pose)

        # Plan footsteps along the path
        for i in range(len(global_path.poses) - 1):
            current_pose = global_path.poses[i]
            next_pose = global_path.poses[i + 1]

            # Calculate desired step direction
            dx = next_pose.pose.position.x - current_pose.pose.position.x
            dy = next_pose.pose.position.y - current_pose.pose.position.y
            step_direction = np.arctan2(dy, dx)

            # Determine which foot to move (alternating pattern)
            if i % 2 == 0:
                # Move right foot
                new_right_foot = self.calculate_foot_position(
                    left_foot, step_direction, self.step_length, self.step_width/2
                )
                footsteps.append(('right', new_right_foot))
            else:
                # Move left foot
                new_left_foot = self.calculate_foot_position(
                    right_foot, step_direction, self.step_length, -self.step_width/2
                )
                footsteps.append(('left', new_left_foot))

        return footsteps

    def calculate_foot_position(self, support_foot, direction, step_length, lateral_offset):
        """
        Calculate next foot position based on support foot and movement direction
        """
        new_x = support_foot.x + step_length * np.cos(direction)
        new_y = support_foot.y + step_length * np.sin(direction)

        # Add lateral offset for alternating steps
        new_x += lateral_offset * np.cos(direction + np.pi/2)
        new_y += lateral_offset * np.sin(direction + np.pi/2)

        return Point(x=new_x, y=new_y, z=0.0)

    def get_current_foot_positions(self, robot_pose):
        """
        Get current left and right foot positions based on robot pose
        """
        # Assume feet are positioned relative to robot base
        left_foot = Point()
        left_foot.x = robot_pose.position.x + 0.0
        left_foot.y = robot_pose.position.y + self.step_width/2
        left_foot.z = 0.0

        right_foot = Point()
        right_foot.x = robot_pose.position.x + 0.0
        right_foot.y = robot_pose.position.y - self.step_width/2
        right_foot.z = 0.0

        return left_foot, right_foot

# Example: Integration with Nav2
class HumanoidFootstepPlannerNode:
    def __init__(self):
        self.footstep_planner = FootstepPlanner()
        self.footstep_publisher = self.create_publisher(MarkerArray, 'footsteps', 10)

    def generate_footstep_markers(self, footsteps):
        """
        Generate visualization markers for footsteps
        """
        marker_array = MarkerArray()

        for i, (foot, position) in enumerate(footsteps):
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "footsteps"
            marker.id = i
            marker.type = Marker.CYLINDER
            marker.action = Marker.ADD

            marker.pose.position = position
            marker.pose.orientation.w = 1.0

            marker.scale.x = 0.1  # Foot size
            marker.scale.y = 0.05
            marker.scale.z = 0.01

            if foot == 'left':
                marker.color.r = 0.0
                marker.color.g = 0.0
                marker.color.b = 1.0  # Blue for left foot
            else:
                marker.color.r = 1.0
                marker.color.g = 0.0
                marker.color.b = 0.0  # Red for right foot

            marker.color.a = 1.0
            marker_array.markers.append(marker)

        return marker_array
```

### Balance-Aware Path Planning

Incorporating balance constraints into path planning:

```python
# Example: Balance-aware costmap layer
import numpy as np
from nav2_costmap_2d.python_layers.python_layer import Layer
from geometry_msgs.msg import Point

class BalanceLayer(Layer):
    def __init__(self, name):
        super().__init__(name)
        self.foot_separation = 0.2  # Distance between feet
        self.stability_threshold = 0.1  # Minimum stability margin

    def updateBounds(self, robot_x, robot_y, robot_yaw, min_x, min_y, max_x, max_y):
        """
        Update costmap bounds considering balance constraints
        """
        # Add cost for areas that would compromise balance
        for x in range(int(min_x / self.resolution), int(max_x / self.resolution)):
            for y in range(int(min_y / self.resolution), int(max_y / self.resolution)):
                world_x = x * self.resolution + self.origin_x
                world_y = y * self.resolution + self.origin_y

                # Check if this location would create balance issues
                cost = self.calculate_balance_cost(world_x, world_y, robot_x, robot_y)

                if cost > 0:
                    self.setCost(x, y, max(self.getCost(x, y), cost))

    def calculate_balance_cost(self, point_x, point_y, robot_x, robot_y):
        """
        Calculate cost based on balance considerations
        """
        # Calculate distance from robot (for foot placement)
        dist_from_robot = np.sqrt((point_x - robot_x)**2 + (point_y - robot_y)**2)

        # High cost for positions too close to robot (can't place foot there)
        if dist_from_robot < 0.1:
            return 254  # lethal cost

        # Cost for positions too far (difficult to reach)
        if dist_from_robot > 0.5:
            return 150  # high cost

        # Check if this foot placement maintains balance with other foot
        # This is a simplified example - real implementation would be more complex
        return 0  # no additional cost in this simple example
```

## Isaac ROS Integration for Accelerated Navigation

### GPU-Accelerated Path Planning

Isaac ROS provides hardware acceleration for navigation algorithms:

```yaml
# Example: Isaac ROS accelerated navigation configuration
bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: base_link
    odom_topic: /odom
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True

    # Isaac ROS acceleration parameters
    enable_acceleration: True
    max_acceleration_factor: 5.0

    behavior_tree_xml_filename: navigate_w_replanning_and_recovery.xml
    plugin_lib_names:
    # Isaac ROS enhanced nodes
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_back_up_action_bt_node  # Accelerated with GPU
    - nav2_spin_action_bt_node     # Accelerated with GPU
    - nav2_wait_action_bt_node
    - nav2_clear_costmap_service_bt_node  # GPU accelerated
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
    - nav2_goal_updated_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_service_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node  # GPU accelerated
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_time_expired_condition_bt_node
    - nav2_path_expiring_timer_condition
    - nav2_distance_traveled_condition_bt_node
    - nav2_single_trigger_bt_node
    - nav2_is_battery_low_condition_bt_node
    - nav2_navigate_through_poses_action_bt_node
    - nav2_navigate_to_pose_action_bt_node
    - nav2_remove_passed_goals_action_bt_node
    - nav2_planner_selector_bt_node
    - nav2_controller_selector_bt_node
    - nav2_goal_checker_selector_bt_node
```

### Isaac ROS Path Planner

```python
# Example: Isaac ROS enhanced path planner
import rclpy
from rclpy.node import Node
from nav2_msgs.action import ComputePathToPose
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from rclpy.action import ActionServer
import numpy as np

class IsaacROSPathPlanner(Node):
    def __init__(self):
        super().__init__('isaac_ros_path_planner')

        # Initialize Isaac ROS acceleration
        self.initialize_acceleration()

        # Create action server
        self._action_server = ActionServer(
            self,
            ComputePathToPose,
            'compute_path_to_pose',
            self.execute_callback
        )

        # Isaac ROS specific parameters
        self.declare_parameters(
            namespace='',
            parameters=[
                ('acceleration_enabled', True),
                ('max_processing_time', 5.0),
                ('smoothing_iterations', 10),
                ('collision_check_density', 0.1),
            ]
        )

    def initialize_acceleration(self):
        """Initialize Isaac ROS acceleration"""
        # This would initialize the GPU-accelerated path planning
        # components in a real implementation
        self.get_logger().info('Isaac ROS path planner initialized with acceleration')

    def execute_callback(self, goal_handle):
        """Execute path planning with Isaac ROS acceleration"""
        self.get_logger().info('Received path planning request')

        start = goal_handle.request.start
        goal = goal_handle.request.goal
        planner_id = goal_handle.request.planner_id

        # Use Isaac ROS accelerated path planning
        path = self.accelerated_path_planning(start, goal)

        if path is not None:
            result = ComputePathToPose.Result()
            result.path = path
            goal_handle.succeed()
            return result
        else:
            goal_handle.abort()
            return ComputePathToPose.Result()

    def accelerated_path_planning(self, start, goal):
        """Perform GPU-accelerated path planning"""
        # In a real implementation, this would use Isaac ROS
        # accelerated algorithms for path planning
        path = Path()
        path.header.frame_id = "map"
        path.header.stamp = self.get_clock().now().to_msg()

        # Simplified path generation for example
        # Real implementation would use GPU-accelerated algorithms
        current_x, current_y = start.pose.position.x, start.pose.position.y
        target_x, target_y = goal.pose.position.x, goal.pose.position.y

        # Generate path points
        steps = max(int(abs(target_x - current_x) / 0.1),
                   int(abs(target_y - current_y) / 0.1))

        for i in range(steps + 1):
            t = i / steps if steps > 0 else 0

            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.pose.position.x = current_x + t * (target_x - current_x)
            pose.pose.position.y = current_y + t * (target_y - current_y)
            pose.pose.position.z = 0.0

            # Add orientation (simplified)
            pose.pose.orientation.w = 1.0

            path.poses.append(pose)

        return path
```

## Bipedal-Specific Navigation Behaviors

### Recovery Behaviors for Humanoid Robots

Humanoid robots need specialized recovery behaviors:

```yaml
# Example: Humanoid-specific recovery behaviors
recoveries_server:
  ros__parameters:
    costmap_topic: local_costmap/costmap_raw
    footprint_topic: local_costmap/published_footprint
    cycle_frequency: 10.0
    recovery_plugins: ["back_up", "turn_in_place", "wait", "humanoid_lean_recovery"]
    blp_plugin: "nav2_navfn_planner/NavfnPlanner"
    max_planning_retries: 5

    # Back up recovery (humanoid adapted)
    back_up:
      plugin: "nav2_recoveries/BackUp"
      backup_dist: -0.3  # Shorter backup for humanoid
      backup_speed: 0.05

    # Turn in place (humanoid adapted)
    turn_in_place:
      plugin: "nav2_recoveries/TurnInPlace"
      tolerance: 0.3
      sampling_interval: 0.1
      max_angular_accel: 0.5  # Gentle turning for balance
      max_angular_vel: 0.5
      min_angular_vel: 0.1

    # Wait recovery
    wait:
      plugin: "nav2_recoveries/Wait"
      wait_duration: 2.0

    # Humanoid-specific lean recovery
    humanoid_lean_recovery:
      plugin: "humanoid_nav2_plugins/LeanRecovery"
      lean_angle_limit: 15.0  # Maximum lean angle in degrees
      lean_recovery_time: 3.0
      stability_threshold: 0.8
```

### Balance Recovery Strategies

```python
# Example: Balance recovery implementation
class BalanceRecovery:
    def __init__(self, robot_interface):
        self.robot = robot_interface
        self.stability_threshold = 0.1
        self.max_lean_angle = 15.0  # degrees

    def detect_imminent_fall(self):
        """
        Detect if the robot is about to fall based on IMU data
        """
        imu_data = self.robot.get_imu_data()

        # Check if the robot is leaning too far
        roll_angle = abs(imu_data.orientation.x) * 180 / 3.14159
        pitch_angle = abs(imu_data.orientation.y) * 180 / 3.14159

        if roll_angle > self.max_lean_angle or pitch_angle > self.max_lean_angle:
            return True

        # Check if center of mass is outside support polygon
        com = self.robot.get_center_of_mass()
        support_polygon = self.robot.get_support_polygon()

        if not self.is_point_in_polygon(com, support_polygon):
            return True

        return False

    def execute_lean_recovery(self):
        """
        Execute lean recovery to restore balance
        """
        # Move the center of mass back within the support polygon
        current_com = self.robot.get_center_of_mass()
        target_com = self.calculate_balance_point()

        # Adjust joint angles to move COM
        joint_commands = self.inverse_kinematics_to_com(target_com)
        self.robot.send_joint_commands(joint_commands)

        # Wait for balance to be restored
        timeout = 0
        while not self.is_balanced() and timeout < 3.0:
            timeout += 0.1
            time.sleep(0.1)

    def calculate_balance_point(self):
        """
        Calculate a stable center of mass position
        """
        # Find the center of the support polygon
        support_polygon = self.robot.get_support_polygon()

        # Calculate centroid of support polygon
        centroid_x = sum([p.x for p in support_polygon]) / len(support_polygon)
        centroid_y = sum([p.y for p in support_polygon]) / len(support_polygon)

        return Point(x=centroid_x, y=centroid_y, z=current_com.z)
```

## Performance Optimization for Humanoid Navigation

### Parameter Tuning

Optimize navigation parameters for humanoid robots:

```yaml
# Example: Optimized parameters for humanoid navigation
dwb_local_planner:
  ros__parameters:
    # Humanoid-specific velocity limits
    speed_limit_scaling: 0.3  # Slower speeds for stability
    min_vel_x: 0.05
    max_vel_x: 0.3   # Slower than wheeled robots
    min_vel_y: -0.1
    max_vel_y: 0.1
    max_vel_theta: 0.3  # Gentle turning

    # Acceleration limits for balance
    acc_lim_x: 0.2    # Lower acceleration for stability
    acc_lim_y: 0.1
    acc_lim_theta: 0.2

    # Humanoid-specific trajectory parameters
    decel_lim_x: -0.2
    decel_lim_y: -0.1
    decel_lim_theta: -0.2

    # Trajectory scoring
    xy_goal_tolerance: 0.15  # Larger tolerance for foot placement
    yaw_goal_tolerance: 0.2
    trans_stopped_velocity: 0.05
    rot_stopped_velocity: 0.05

    # Humanoid-specific scoring parameters
    forward_point_distance: 0.325
    stop_time_buffer: 0.2
    scaling_speed: 0.25
    max_scaling_factor: 0.2

    # Footstep-aware trajectory evaluation
    use_dwa: true
    use_simple_trajectory_generator: true
    trajectory_generator_name: dwb_plugins::LineTrajectoryGenerator

    # Humanoid-specific plugin
    critics: ["RotateToGoal", "Oscillation", "BaseObstacle",
              "GoalAlign", "PathAlign", "PreferForward",
              "FootstepStability"]

    # Footstep stability critic parameters
    FootstepStability.scale: 2.0
    FootstepStability.foot_separation: 0.2
    FootstepStability.stability_threshold: 0.1
```

### Real-time Performance Monitoring

```python
# Example: Performance monitoring for humanoid navigation
class NavigationPerformanceMonitor:
    def __init__(self):
        self.path_execution_times = []
        self.balance_margins = []
        self.footstep_success_rates = []

    def monitor_navigation_performance(self):
        """
        Monitor and log navigation performance metrics
        """
        # Track path execution time
        start_time = time.time()

        # Execute navigation
        success = self.execute_navigation_task()

        execution_time = time.time() - start_time
        self.path_execution_times.append(execution_time)

        # Monitor balance during navigation
        balance_margin = self.get_balance_margin()
        self.balance_margins.append(balance_margin)

        # Track footstep success
        footstep_success = self.get_footstep_success_rate()
        self.footstep_success_rates.append(footstep_success)

        # Log performance metrics
        self.log_performance_metrics()

    def get_balance_margin(self):
        """
        Get current balance margin from IMU data
        """
        imu_data = self.robot.get_imu_data()
        com = self.robot.get_center_of_mass()
        support_polygon = self.robot.get_support_polygon()

        # Calculate distance from COM to edge of support polygon
        min_distance = float('inf')
        for edge in self.get_polygon_edges(support_polygon):
            distance = self.distance_point_to_line(com, edge)
            min_distance = min(min_distance, distance)

        return min_distance

    def log_performance_metrics(self):
        """
        Log performance metrics for analysis
        """
        avg_execution_time = np.mean(self.path_execution_times[-10:]) if self.path_execution_times else 0
        avg_balance_margin = np.mean(self.balance_margins[-10:]) if self.balance_margins else 0
        avg_footstep_success = np.mean(self.footstep_success_rates[-10:]) if self.footstep_success_rates else 0

        self.get_logger().info(
            f"Navigation Performance - "
            f"Time: {avg_execution_time:.2f}s, "
            f"Balance: {avg_balance_margin:.3f}m, "
            f"Footstep Success: {avg_footstep_success:.1f}%"
        )
```

## Best Practices for Humanoid Navigation

### Safety Considerations

1. **Conservative Parameters**: Use lower speeds and accelerations
2. **Balance Monitoring**: Continuously monitor stability margins
3. **Recovery Behaviors**: Implement robust recovery strategies
4. **Emergency Stops**: Have immediate stop capabilities
5. **Terrain Assessment**: Evaluate terrain before navigation

### Testing and Validation

1. **Simulation Testing**: Extensive testing in simulation first
2. **Gradual Complexity**: Start with simple environments
3. **Edge Case Testing**: Test balance limits and recovery
4. **Real-World Validation**: Validate in controlled real environments
5. **Performance Monitoring**: Track metrics during operation

## Hands-On Exercise

Implement a complete humanoid navigation system with:
1. Nav2 configuration adapted for bipedal constraints
2. Footstep planning integration
3. Balance-aware path planning
4. Isaac ROS acceleration where applicable
5. Performance monitoring and validation

## Summary

Nav2 provides a robust foundation for humanoid robot navigation, but requires specific adaptations for bipedal locomotion. By incorporating footstep planning, balance constraints, and stability considerations, we can create navigation systems that enable safe and effective humanoid robot mobility. The integration of Isaac ROS provides additional performance benefits through hardware acceleration.

## Next Steps

Continue to the next module on [Vision-Language-Action (VLA)](/docs/module-4/intro) to learn about integrating perception, language understanding, and action execution.

## Cross-References

- [Module 3 Introduction](/docs/module-3/intro)
- [Module 4: Vision-Language-Action (VLA)](/docs/module-4/intro)
- [Weeks 8-10: NVIDIA Isaac Platform](/docs/weekly-breakdown/weeks-8-10)