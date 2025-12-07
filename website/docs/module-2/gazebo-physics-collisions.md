---
sidebar_position: 2
title: "Simulating Physics, Gravity, and Collisions in Gazebo"
---

# Simulating Physics, Gravity, and Collisions in Gazebo

## Learning Objectives

By the end of this lesson, you will be able to:
- Configure Gazebo's physics engine for realistic simulation
- Set up gravity and environmental forces for humanoid robots
- Implement collision detection and response for complex robots
- Optimize physics parameters for humanoid locomotion
- Validate physics simulation accuracy for humanoid applications

## Introduction to Gazebo Physics

Gazebo's physics engine is the core component that simulates the physical world in which robots operate. For humanoid robots, accurate physics simulation is critical for testing locomotion, manipulation, and interaction behaviors before deployment on real hardware.

### Physics Engine Options

Gazebo supports multiple physics engines:
- **ODE (Open Dynamics Engine)**: Default engine, good for most applications
- **Bullet**: Better for complex contact scenarios and articulated bodies
- **Simbody**: Advanced multibody dynamics, good for complex mechanical systems
- **DART**: Dynamic Animation and Robotics Toolkit, modern physics engine

## Configuring Physics Properties

### World Physics Configuration

Physics properties are configured in the world file:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="humanoid_world">
    <!-- Physics engine configuration -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>      <!-- Simulation time step -->
      <real_time_factor>1.0</real_time_factor>  <!-- Simulation speed -->
      <real_time_update_rate>1000.0</real_time_update_rate>
      <gravity>0 0 -9.8</gravity>               <!-- Gravity vector (m/s^2) -->

      <!-- ODE-specific parameters -->
      <ode>
        <solver>
          <type>quick</type>
          <iters>10</iters>
          <sor>1.3</sor>
        </solver>
        <constraints>
          <cfm>0.0</cfm>
          <erp>0.2</erp>
          <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
          <contact_surface_layer>0.001</contact_surface_layer>
        </constraints>
      </ode>
    </physics>

    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Sun for lighting -->
    <include>
      <uri>model://sun</uri>
    </include>
  </world>
</sdf>
```

### Time Step Considerations

For humanoid robots, physics simulation time step is critical:
- **Smaller time steps** (0.001s or smaller) provide more accurate simulation
- **Larger time steps** (0.01s) run faster but may be unstable
- **Balance** between accuracy and performance is essential

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>          <!-- 1ms time step -->
  <real_time_factor>1.0</real_time_factor>      <!-- Real-time simulation -->
  <real_time_update_rate>1000.0</real_time_update_rate>  <!-- 1000 Hz update rate -->
</physics>
```

## Gravity and Environmental Forces

### Gravity Configuration

Gravity affects all objects in the simulation:

```xml
<gravity>0 0 -9.8</gravity>  <!-- Earth gravity: 9.8 m/s^2 downward -->
```

For different environments:
- **Moon**: `<gravity>0 0 -1.62</gravity>` (1/6 Earth gravity)
- **Mars**: `<gravity>0 0 -3.71</gravity>`
- **Zero-g**: `<gravity>0 0 0</gravity>`

### Custom Forces

Additional forces can be applied to simulate wind, magnetic fields, etc.:

```xml
<model name="object_with_wind">
  <link name="link">
    <inertial>
      <mass>1.0</mass>
      <inertia>
        <ixx>0.1</ixx>
        <ixy>0</ixy>
        <ixz>0</ixz>
        <iyy>0.1</iyy>
        <iyz>0</iyz>
        <izz>0.1</izz>
      </inertia>
    </inertial>

    <!-- Apply constant force (e.g., wind) -->
    <force>1.0 0.0 0.0</force>  <!-- 1N force in X direction -->
  </link>
</model>
```

## Collision Detection and Response

### Collision Properties

Collision properties define how objects interact:

```xml
<link name="robot_link">
  <collision name="collision">
    <geometry>
      <box>
        <size>0.1 0.1 0.1</size>
      </box>
    </geometry>

    <!-- Surface properties -->
    <surface>
      <friction>
        <ode>
          <mu>0.8</mu>        <!-- Primary friction coefficient -->
          <mu2>0.8</mu2>      <!-- Secondary friction coefficient -->
          <fdir1>0 0 0</fdir1> <!-- Friction direction -->
        </ode>
      </friction>

      <bounce>
        <restitution_coefficient>0.1</restitution_coefficient> <!-- Bounciness -->
        <threshold>100000</threshold>                           <!-- Bounce threshold -->
      </bounce>

      <contact>
        <ode>
          <soft_cfm>0.000001</soft_cfm>      <!-- Constraint Force Mixing -->
          <soft_erp>0.2</soft_erp>           <!-- Error Reduction Parameter -->
          <kp>1000000000000.0</kp>          <!-- Contact stiffness -->
          <kd>1.0</kd>                      <!-- Contact damping -->
          <max_vel>100.0</max_vel>          <!-- Maximum contact penetration velocity -->
          <min_depth>0.001</min_depth>      <!-- Minimum contact depth -->
        </ode>
      </contact>
    </surface>
  </collision>
</link>
```

### Friction Parameters

For humanoid robots, friction is critical for stable walking:

```xml
<friction>
  <ode>
    <mu>1.0</mu>    <!-- High friction for feet to prevent slipping -->
    <mu2>1.0</mu2>  <!-- Same for secondary axis -->
  </ode>
</friction>
```

### Contact Properties

Contact properties affect collision response:

```xml
<contact>
  <ode>
    <soft_cfm>0.000001</soft_cfm>  <!-- Low CFM for stiff contacts -->
    <soft_erp>0.2</soft_erp>       <!-- Moderate ERP for stability -->
    <kp>1000000000000.0</kp>      <!-- High stiffness for solid contacts -->
    <kd>1.0</kd>                  <!-- Damping to reduce oscillation -->
    <max_vel>100.0</max_vel>      <!-- Allow high velocity contacts -->
    <min_depth>0.001</min_depth>  <!-- Small minimum depth for accuracy -->
  </ode>
</contact>
```

## Humanoid-Specific Physics Considerations

### Balance and Stability

For humanoid robots, physics parameters must support balance:

```xml
<!-- Example: Foot link with high friction for stable standing -->
<link name="left_foot">
  <collision name="foot_collision">
    <geometry>
      <box size="0.2 0.1 0.05"/>
    </geometry>
    <surface>
      <friction>
        <ode>
          <mu>1.2</mu>    <!-- High friction to prevent slipping -->
          <mu2>1.2</mu2>
        </ode>
      </friction>
      <contact>
        <ode>
          <soft_cfm>0.0000001</soft_cfm>  <!-- Very stiff contact -->
          <soft_erp>0.1</soft_erp>        <!-- Low ERP for stability -->
          <kp>10000000000000.0</kp>      <!-- Very high stiffness -->
        </ode>
      </contact>
    </surface>
  </collision>
</link>
```

### Joint Dynamics

Humanoid joints need appropriate damping for natural movement:

```xml
<joint name="left_knee" type="revolute">
  <parent link="left_thigh"/>
  <child link="left_shin"/>
  <axis xyz="0 1 0">
    <dynamics damping="1.0" friction="0.1"/>  <!-- Damping for natural movement -->
  </axis>
  <limit lower="0" upper="2.356" effort="200" velocity="1.0"/>  <!-- 0 to 135 degrees -->
</joint>
```

### Center of Mass Management

Proper CoM placement is crucial for humanoid balance:

```xml
<link name="torso">
  <inertial>
    <mass>5.0</mass>
    <origin xyz="0 0 0.4" rpy="0 0 0"/>  <!-- CoM higher up in torso -->
    <inertia>
      <ixx>0.2</ixx>
      <ixy>0.0</ixy>
      <ixz>0.0</ixz>
      <iyy>0.3</iyy>
      <iyz>0.0</iyz>
      <izz>0.1</izz>
    </inertia>
  </inertial>
</link>
```

## Physics Optimization for Humanoid Robots

### Performance vs. Accuracy Trade-offs

For humanoid locomotion, balance these factors:

```xml
<!-- Optimized physics for humanoid simulation -->
<physics type="ode">
  <max_step_size>0.001</max_step_size>      <!-- Small for stability -->
  <real_time_factor>0.5</real_time_factor>  <!-- May run slower than real-time for accuracy -->
  <real_time_update_rate>1000.0</real_time_update_rate>

  <ode>
    <solver>
      <type>quick</type>    <!-- Fast solver -->
      <iters>20</iters>     <!-- More iterations for accuracy -->
      <sor>1.2</sor>        <!-- Successive over-relaxation parameter -->
    </solver>
    <constraints>
      <cfm>0.000001</cfm>   <!-- Very low CFM for stiff constraints -->
      <erp>0.1</erp>        <!-- Low ERP for stability -->
    </constraints>
  </ode>
</physics>
```

### Contact Stabilization

For stable humanoid contact with ground:

```xml
<!-- Ground plane with optimal properties -->
<link name="ground_plane_collision">
  <collision name="collision">
    <geometry>
      <plane>
        <normal>0 0 1</normal>
        <size>100 100</size>
      </plane>
    </geometry>
    <surface>
      <friction>
        <ode>
          <mu>1.0</mu>    <!-- High friction -->
          <mu2>1.0</mu2>
        </ode>
      </friction>
      <contact>
        <ode>
          <soft_cfm>0.0</soft_cfm>      <!-- Rigid contact -->
          <soft_erp>0.9</soft_erp>      <!-- High ERP for immediate error correction -->
          <kp>1e12</kp>                <!-- Very high stiffness -->
          <kd>1.0</kd>                 <!-- Moderate damping -->
          <max_vel>100.0</max_vel>
          <min_depth>0.001</min_depth>
        </ode>
      </contact>
    </surface>
  </collision>
</link>
```

## Advanced Physics Features

### Multi-Body Dynamics

For complex humanoid structures:

```xml
<!-- Example: Complex articulated robot -->
<model name="humanoid_robot" canonical_link="torso">
  <!-- All links and joints defined here -->

  <!-- Enable self-collision detection -->
  <self_collide>true</self_collide>

  <!-- Enable kinematic loops if needed -->
  <kinematic>false</kinematic>
</model>
```

### Custom Physics Plugins

For specialized physics behavior:

```xml
<gazebo>
  <plugin name="custom_physics_controller" filename="libCustomPhysicsController.so">
    <robot_namespace>/humanoid</robot_namespace>
    <update_rate>100</update_rate>
    <!-- Custom parameters -->
  </plugin>
</gazebo>
```

## Validation and Tuning

### Physics Validation Techniques

1. **Static Balance Test**: Ensure robot stands stably
2. **Simple Motion Test**: Verify basic movement is realistic
3. **Contact Test**: Check collision responses are appropriate
4. **Inertial Test**: Validate mass and inertia properties

### Common Physics Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Robot falls through ground | Insufficient contact stiffness | Increase kp value |
| Robot bounces unrealistically | High restitution | Set restitution to low value |
| Robot slides when it should grip | Low friction | Increase mu values |
| Simulation is unstable | Large time step | Reduce max_step_size |
| Robot parts interpenetrate | Insufficient constraint parameters | Adjust CFM/ERP values |

## Performance Considerations

### Optimizing for Real-time Simulation

```xml
<!-- For real-time humanoid simulation -->
<physics type="ode">
  <max_step_size>0.002</max_step_size>      <!-- Larger step for performance -->
  <real_time_factor>1.0</real_time_factor>  <!-- Real-time execution -->

  <ode>
    <solver>
      <iters>10</iters>     <!-- Fewer iterations for speed -->
      <sor>1.3</sor>
    </solver>
  </ode>
</physics>
```

### Parallel Processing

Enable multi-threaded physics (if supported):

```xml
<physics type="ode">
  <!-- Multi-threading settings -->
  <thread_count>4</thread_count>  <!-- Use multiple CPU cores -->
</physics>
```

## Best Practices for Humanoid Physics

1. **Start Conservative**: Begin with stable parameters and optimize gradually
2. **Validate with Real Data**: Compare simulation results with physical robot data
3. **Use Appropriate Units**: Maintain consistent units throughout (SI units recommended)
4. **Consider Computational Cost**: Balance accuracy with simulation speed
5. **Test Edge Cases**: Validate behavior under extreme conditions
6. **Document Parameters**: Keep records of physics settings for reproducibility

## Hands-On Exercise

Create a simple humanoid model in Gazebo with:
1. Proper physics configuration for stable standing
2. Appropriate friction values for feet
3. Realistic gravity and inertial properties
4. Validation of basic physics behavior

## Summary

Physics simulation in Gazebo is fundamental for humanoid robotics development. Proper configuration of gravity, friction, and collision properties is essential for realistic simulation of humanoid behaviors, particularly locomotion and manipulation tasks. The balance between simulation accuracy and performance is crucial for effective development workflows.

## Next Steps

Continue to the next lesson on [High-fidelity rendering and human-robot interaction in Unity](/docs/module-2/unity-rendering-interaction) to learn about visual simulation and interaction capabilities.

## Cross-References

- [Module 2 Introduction](/docs/module-2/intro)
- [High-fidelity rendering and human-robot interaction in Unity](/docs/module-2/unity-rendering-interaction)
- [Weeks 6-7: Robot Simulation with Gazebo](/docs/weekly-breakdown/weeks-6-7)