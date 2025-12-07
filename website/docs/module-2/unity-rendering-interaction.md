---
sidebar_position: 3
title: "High-Fidelity Rendering and Human-Robot Interaction in Unity"
---

# High-Fidelity Rendering and Human-Robot Interaction in Unity

## Learning Objectives

By the end of this lesson, you will be able to:
- Set up Unity for robotics simulation and visualization
- Create photorealistic rendering for humanoid robots
- Implement human-robot interaction systems in Unity
- Integrate Unity with ROS 2 for robot control
- Develop VR/AR interfaces for immersive robotics interaction

## Introduction to Unity for Robotics

Unity has become a powerful platform for robotics simulation and visualization, offering photorealistic rendering capabilities that complement physics-focused simulators like Gazebo. For humanoid robotics, Unity provides the visual fidelity necessary for realistic perception training and human-robot interaction studies.

### Unity Robotics Ecosystem

Unity provides several tools for robotics:
- **Unity Robotics Hub**: Collection of tools and packages for robotics development
- **Unity ML-Agents**: Framework for training intelligent agents using reinforcement learning
- **ROS#**: Unity package for ROS communication
- **Unity Perception**: Tools for generating synthetic training data

## Setting Up Unity for Robotics

### Installation and Setup

To set up Unity for robotics applications:

1. **Install Unity Hub**: Download from unity.com
2. **Install Unity Editor**: Version 2021.3 LTS or later recommended
3. **Install Robotics Packages**: Through Unity Package Manager
4. **Configure ROS Bridge**: For communication with ROS 2 systems

### Essential Unity Packages for Robotics

```json
{
  "dependencies": {
    "com.unity.robotics.ros-tcp-connector": "0.7.0",
    "com.unity.robotics.urdf-importer": "0.5.2",
    "com.unity.perception": "1.0.0",
    "com.unity.ml-agents": "2.1.0"
  }
}
```

## Photorealistic Rendering for Humanoid Robots

### Material and Shader Setup

Creating realistic humanoid materials:

```csharp
// Example: Creating a realistic humanoid skin material
using UnityEngine;

public class HumanoidMaterialSetup : MonoBehaviour
{
    [Header("Material Properties")]
    public Color skinColor = new Color(0.9f, 0.8f, 0.6f, 1.0f);
    public Texture2D skinTexture;
    public Texture2D normalMap;

    void Start()
    {
        SetupSkinMaterial();
    }

    void SetupSkinMaterial()
    {
        Renderer renderer = GetComponent<Renderer>();
        if (renderer != null)
        {
            Material material = renderer.material;

            // Set up subsurface scattering for realistic skin
            material.SetColor("_BaseColor", skinColor);
            material.SetTexture("_BaseMap", skinTexture);
            material.SetTexture("_NormalMap", normalMap);
            material.SetFloat("_Smoothness", 0.3f);
            material.SetFloat("_Metallic", 0.0f);

            // Add subsurface scattering effect for skin realism
            material.EnableKeyword("_SUBSURFACE_SCATTERING");
            material.SetFloat("_SubsurfacePower", 4.0f);
            material.SetColor("_SubsurfaceColor", Color.white);
        }
    }
}
```

### Lighting Setup for Realism

Creating realistic lighting environments:

```csharp
// Example: Setting up realistic lighting
using UnityEngine;

public class RealisticLightingSetup : MonoBehaviour
{
    [Header("Lighting Configuration")]
    public Light mainLight;
    public Light fillLight;
    public Light rimLight;
    public ReflectionProbe reflectionProbe;

    [Header("Environment")]
    public Material skyboxMaterial;

    void Start()
    {
        ConfigureLighting();
        SetupEnvironment();
    }

    void ConfigureLighting()
    {
        // Main directional light (sun)
        if (mainLight != null)
        {
            mainLight.type = LightType.Directional;
            mainLight.color = Color.white;
            mainLight.intensity = 1.5f;
            mainLight.shadows = LightShadows.Soft;
            mainLight.shadowStrength = 0.8f;
            mainLight.transform.rotation = Quaternion.Euler(50f, -30f, 0f);
        }

        // Fill light for shadows
        if (fillLight != null)
        {
            fillLight.type = LightType.Directional;
            fillLight.color = new Color(0.4f, 0.4f, 0.5f);
            fillLight.intensity = 0.3f;
            fillLight.transform.rotation = Quaternion.Euler(-50f, 150f, 0f);
        }

        // Rim light for separation
        if (rimLight != null)
        {
            rimLight.type = LightType.Directional;
            rimLight.color = new Color(0.2f, 0.2f, 0.3f);
            rimLight.intensity = 0.2f;
            rimLight.transform.rotation = Quaternion.Euler(0f, 90f, 0f);
        }
    }

    void SetupEnvironment()
    {
        // Set up skybox for realistic environment
        if (skyboxMaterial != null)
        {
            RenderSettings.skybox = skyboxMaterial;
        }

        // Configure reflection probe for realistic reflections
        if (reflectionProbe != null)
        {
            reflectionProbe.mode = ReflectionProbeMode.Realtime;
            reflectionProbe.refreshMode = ReflectionProbeRefreshMode.OnAwake;
            reflectionProbe.timeSlicingMode = ReflectionProbeTimeSlicingMode.AllFacesAtOnce;
        }
    }
}
```

### Post-Processing Effects

Enhancing visual quality with post-processing:

```csharp
// Example: Post-processing setup for realistic rendering
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class PostProcessingSetup : MonoBehaviour
{
    [Header("Post-Processing Settings")]
    public VolumeProfile volumeProfile;

    void Start()
    {
        SetupPostProcessing();
    }

    void SetupPostProcessing()
    {
        if (volumeProfile == null)
        {
            volumeProfile = ScriptableObject.CreateInstance<VolumeProfile>();
        }

        // Add Bloom effect for realistic light scattering
        var bloom = volumeProfile.Add<UnityEngine.Rendering.Universal.Bloom>();
        bloom.threshold.value = 0.9f;
        bloom.intensity.value = 0.6f;
        bloom.scatter.value = 0.7f;

        // Add Color Adjustments
        var colorAdjust = volumeProfile.Add<UnityEngine.Rendering.Universal.ColorAdjustments>();
        colorAdjust.contrast.value = 10f;
        colorAdjust.saturation.value = 5f;

        // Add Vignette for focus
        var vignette = volumeProfile.Add<UnityEngine.Rendering.Universal.Vignette>();
        vignette.intensity.value = 0.2f;
        vignette.smoothness.value = 0.2f;
    }
}
```

## Human-Robot Interaction Systems

### Interaction Framework

Creating an interaction system for human-robot collaboration:

```csharp
// Example: Human-Robot Interaction Manager
using UnityEngine;
using System.Collections;
using UnityEngine.Events;

public class HumanRobotInteractionManager : MonoBehaviour
{
    [Header("Interaction Settings")]
    public float interactionDistance = 3.0f;
    public LayerMask interactionLayerMask;

    [Header("Interaction Events")]
    public UnityEvent onRobotApproach;
    public UnityEvent onRobotGreet;
    public UnityEvent onRobotAssist;

    private Transform humanTransform;
    private Animator robotAnimator;
    private bool isInteracting = false;

    void Start()
    {
        SetupInteractionSystem();
    }

    void Update()
    {
        CheckForHumanInteraction();
    }

    void SetupInteractionSystem()
    {
        // Find human in scene (could be player or NPC)
        GameObject human = GameObject.FindGameObjectWithTag("Player");
        if (human != null)
        {
            humanTransform = human.transform;
        }

        // Get robot animator
        robotAnimator = GetComponent<Animator>();
    }

    void CheckForHumanInteraction()
    {
        if (humanTransform != null)
        {
            float distance = Vector3.Distance(transform.position, humanTransform.position);

            if (distance <= interactionDistance && !isInteracting)
            {
                StartCoroutine(HandleInteraction());
            }
        }
    }

    IEnumerator HandleInteraction()
    {
        isInteracting = true;

        // Robot approaches human
        onRobotApproach?.Invoke();
        yield return new WaitForSeconds(1.0f);

        // Robot greets human
        onRobotGreet?.Invoke();
        if (robotAnimator != null)
        {
            robotAnimator.SetTrigger("Greet");
        }
        yield return new WaitForSeconds(2.0f);

        // Robot offers assistance
        onRobotAssist?.Invoke();
        if (robotAnimator != null)
        {
            robotAnimator.SetTrigger("Assist");
        }

        yield return new WaitForSeconds(3.0f);
        isInteracting = false;
    }
}
```

### Gesture Recognition System

Implementing gesture-based interaction:

```csharp
// Example: Gesture Recognition for Human-Robot Interaction
using UnityEngine;
using System.Collections.Generic;

public class GestureRecognitionSystem : MonoBehaviour
{
    [Header("Gesture Recognition")]
    public float gestureRecognitionDistance = 2.0f;
    public float gestureTimeout = 5.0f;

    [System.Serializable]
    public class Gesture
    {
        public string name;
        public Vector3[] path;
        public float tolerance = 0.1f;
    }

    public List<Gesture> recognizedGestures = new List<Gesture>();
    private List<Vector3> currentGesturePath = new List<Vector3>();
    private float gestureStartTime;

    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            StartGesture();
        }
        else if (Input.GetMouseButton(0))
        {
            AddGesturePoint();
        }
        else if (Input.GetMouseButtonUp(0))
        {
            ProcessGesture();
        }
    }

    void StartGesture()
    {
        currentGesturePath.Clear();
        gestureStartTime = Time.time;
    }

    void AddGesturePoint()
    {
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        RaycastHit hit;

        if (Physics.Raycast(ray, out hit, gestureRecognitionDistance))
        {
            currentGesturePath.Add(hit.point);
        }
    }

    void ProcessGesture()
    {
        if (currentGesturePath.Count < 3)
            return;

        if (Time.time - gestureStartTime > gestureTimeout)
        {
            currentGesturePath.Clear();
            return;
        }

        // Compare with known gestures
        foreach (Gesture gesture in recognizedGestures)
        {
            if (IsGestureMatch(currentGesturePath, gesture.path, gesture.tolerance))
            {
                ExecuteGestureCommand(gesture.name);
                break;
            }
        }

        currentGesturePath.Clear();
    }

    bool IsGestureMatch(List<Vector3> inputPath, Vector3[] referencePath, float tolerance)
    {
        if (inputPath.Count != referencePath.Length)
            return false;

        for (int i = 0; i < inputPath.Count; i++)
        {
            if (Vector3.Distance(inputPath[i], referencePath[i]) > tolerance)
                return false;
        }

        return true;
    }

    void ExecuteGestureCommand(string gestureName)
    {
        Debug.Log($"Recognized gesture: {gestureName}");

        switch (gestureName)
        {
            case "Follow":
                FollowHuman();
                break;
            case "Stop":
                StopRobot();
                break;
            case "Help":
                ProvideAssistance();
                break;
        }
    }

    void FollowHuman()
    {
        Debug.Log("Robot will follow human");
        // Implementation for following behavior
    }

    void StopRobot()
    {
        Debug.Log("Robot stopping");
        // Implementation for stopping behavior
    }

    void ProvideAssistance()
    {
        Debug.Log("Robot providing assistance");
        // Implementation for assistance behavior
    }
}
```

## VR/AR Integration for Immersive Interaction

### VR Setup for Robot Control

Creating VR interfaces for humanoid robot control:

```csharp
// Example: VR Robot Control Interface
using UnityEngine;
using UnityEngine.XR;

public class VRRobotController : MonoBehaviour
{
    [Header("VR Controllers")]
    public XRNode leftControllerNode;
    public XRNode rightControllerNode;

    [Header("Robot Control Mapping")]
    public Transform robotBody;
    public Transform robotLeftArm;
    public Transform robotRightArm;

    private InputDevice leftController;
    private InputDevice rightController;

    void Start()
    {
        SetupVRControllers();
    }

    void Update()
    {
        UpdateControllerInput();
        UpdateRobotFromVR();
    }

    void SetupVRControllers()
    {
        leftController = InputDevices.GetDeviceAtXRNode(leftControllerNode);
        rightController = InputDevices.GetDeviceAtXRNode(rightControllerNode);
    }

    void UpdateControllerInput()
    {
        leftController = InputDevices.GetDeviceAtXRNode(leftControllerNode);
        rightController = InputDevices.GetDeviceAtXRNode(rightControllerNode);
    }

    void UpdateRobotFromVR()
    {
        // Map VR controller positions to robot arm positions
        if (leftController.isValid)
        {
            Vector3 leftControllerPos;
            if (leftController.TryGetFeatureValue(CommonUsages.devicePosition, out leftControllerPos))
            {
                // Map VR controller position to robot left arm
                robotLeftArm.position = MapToRobotSpace(leftControllerPos, "left_arm");
            }
        }

        if (rightController.isValid)
        {
            Vector3 rightControllerPos;
            if (rightController.TryGetFeatureValue(CommonUsages.devicePosition, out rightControllerPos))
            {
                // Map VR controller position to robot right arm
                robotRightArm.position = MapToRobotSpace(rightControllerPos, "right_arm");
            }
        }
    }

    Vector3 MapToRobotSpace(Vector3 vrPosition, string robotPart)
    {
        // Convert VR space coordinates to robot coordinate system
        // This mapping depends on your specific robot kinematics
        Vector3 robotSpace = vrPosition;

        // Apply scaling and offset based on robot dimensions
        robotSpace.x *= 0.1f; // Scale down from VR space to robot space
        robotSpace.y *= 0.1f;
        robotSpace.z *= 0.1f;

        // Apply offset to center robot space
        robotSpace += new Vector3(0, -0.5f, 0);

        return robotSpace;
    }
}
```

## ROS Integration with Unity

### ROS TCP Connector Setup

Connecting Unity to ROS 2 systems:

```csharp
// Example: ROS TCP Connector for Unity
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROSTCPConnector.MessageTypes.Std_msgs;

public class UnityROSInterface : MonoBehaviour
{
    [Header("ROS Connection")]
    public string rosIPAddress = "127.0.0.1";
    public int rosPort = 10000;

    [Header("Robot Control Topics")]
    public string jointStateTopic = "/joint_states";
    public string cmdVelTopic = "/cmd_vel";
    public string robotDescriptionTopic = "/robot_description";

    private ROSConnection ros;
    private float publishFrequency = 10f; // 10 Hz
    private float timeSinceLastPublish = 0f;

    void Start()
    {
        ConnectToROS();
    }

    void ConnectToROS()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.Initialize(rosIPAddress, rosPort);

        Debug.Log($"Connected to ROS at {rosIPAddress}:{rosPort}");
    }

    void Update()
    {
        timeSinceLastPublish += Time.deltaTime;

        if (timeSinceLastPublish >= 1f / publishFrequency)
        {
            PublishRobotData();
            timeSinceLastPublish = 0f;
        }
    }

    void PublishRobotData()
    {
        // Publish Unity robot state to ROS
        var jointStateMsg = new Unity.Robotics.ROSTCPConnector.MessageTypes.Sensor_msgs.JointStateMsg();
        jointStateMsg.name = GetJointNames();
        jointStateMsg.position = GetJointPositions();
        jointStateMsg.velocity = GetJointVelocities();
        jointStateMsg.effort = GetJointEfforts();

        ros.Publish(jointStateTopic, jointStateMsg);
    }

    string[] GetJointNames()
    {
        // Return array of joint names for your robot
        return new string[] { "left_hip", "left_knee", "left_ankle",
                             "right_hip", "right_knee", "right_ankle",
                             "left_shoulder", "left_elbow", "left_wrist",
                             "right_shoulder", "right_elbow", "right_wrist" };
    }

    float[] GetJointPositions()
    {
        // Return current joint positions from Unity robot model
        // This would be retrieved from your robot's joint components
        return new float[] { 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f,
                            0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f };
    }

    float[] GetJointVelocities()
    {
        // Return current joint velocities
        return new float[GetJointNames().Length];
    }

    float[] GetJointEfforts()
    {
        // Return current joint efforts/torques
        return new float[GetJointNames().Length];
    }

    public void SubscribeToROSTopic(string topic, System.Action<object> callback)
    {
        ros.Subscribe<Unity.Robotics.ROSTCPConnector.MessageTypes.Std_msgs.StringMsg>(topic, callback);
    }
}
```

## Perception Simulation in Unity

### Synthetic Data Generation

Creating synthetic training data for perception systems:

```csharp
// Example: Synthetic Data Generation for Perception Training
using UnityEngine;
using System.Collections;
using UnityEngine.Rendering;
using UnityEngine.Experimental.Rendering;

public class SyntheticDataGenerator : MonoBehaviour
{
    [Header("Synthetic Data Settings")]
    public Camera rgbCamera;
    public Camera depthCamera;
    public Camera segmentationCamera;

    [Header("Dataset Configuration")]
    public string datasetPath = "SyntheticDataset/";
    public int framesPerScene = 100;
    public bool generateDepth = true;
    public bool generateSegmentation = true;
    public bool generateBBoxes = true;

    private int frameCounter = 0;
    private int sceneCounter = 0;

    void Start()
    {
        StartCoroutine(GenerateSyntheticDataset());
    }

    IEnumerator GenerateSyntheticDataset()
    {
        while (true)
        {
            for (int i = 0; i < framesPerScene; i++)
            {
                // Randomize environment
                RandomizeEnvironment();

                // Capture data
                CaptureFrameData();

                yield return new WaitForSeconds(0.1f); // 10 FPS
            }

            sceneCounter++;
            frameCounter = 0;

            // Randomize scene layout
            RandomizeSceneLayout();
        }
    }

    void RandomizeEnvironment()
    {
        // Randomize lighting
        Light mainLight = FindObjectOfType<Light>();
        if (mainLight != null)
        {
            mainLight.color = Random.ColorHSV(0.3f, 0.9f, 0.5f, 1f, 0.8f, 1.2f);
            mainLight.intensity = Random.Range(0.5f, 2.0f);
        }

        // Randomize object positions
        GameObject[] objects = GameObject.FindGameObjectsWithTag("Obstacle");
        foreach (GameObject obj in objects)
        {
            obj.transform.position = new Vector3(
                Random.Range(-5f, 5f),
                obj.transform.position.y,
                Random.Range(-5f, 5f)
            );
        }
    }

    void CaptureFrameData()
    {
        // Capture RGB image
        if (rgbCamera != null)
        {
            CaptureCameraImage(rgbCamera, $"rgb_{sceneCounter:000}_{frameCounter:000}.png");
        }

        // Capture depth image
        if (generateDepth && depthCamera != null)
        {
            CaptureDepthImage(depthCamera, $"depth_{sceneCounter:000}_{frameCounter:000}.exr");
        }

        // Capture segmentation
        if (generateSegmentation && segmentationCamera != null)
        {
            CaptureSegmentationImage(segmentationCamera, $"seg_{sceneCounter:000}_{frameCounter:000}.png");
        }

        frameCounter++;
    }

    void CaptureCameraImage(Camera cam, string filename)
    {
        RenderTexture currentRT = RenderTexture.active;
        RenderTexture.active = cam.targetTexture;

        cam.Render();

        Texture2D image = new Texture2D(cam.targetTexture.width, cam.targetTexture.height, TextureFormat.RGB24, false);
        image.ReadPixels(new Rect(0, 0, cam.targetTexture.width, cam.targetTexture.height), 0, 0);
        image.Apply();

        byte[] bytes = image.EncodeToPNG();
        string path = System.IO.Path.Combine(datasetPath, filename);
        System.IO.File.WriteAllBytes(path, bytes);

        RenderTexture.active = currentRT;
        DestroyImmediate(image);
    }

    void CaptureDepthImage(Camera cam, string filename)
    {
        // Implementation for depth image capture
        // This would involve custom depth shader and render texture
    }

    void CaptureSegmentationImage(Camera cam, string filename)
    {
        // Implementation for segmentation image capture
        // This would involve semantic segmentation shader
    }

    void RandomizeSceneLayout()
    {
        // Change the scene layout for variety
        // Move furniture, change textures, etc.
    }
}
```

## Best Practices for Unity Robotics

### Performance Optimization

1. **LOD (Level of Detail) Systems**: Use lower-poly models at distance
2. **Occlusion Culling**: Don't render objects not visible to cameras
3. **Texture Streaming**: Load textures as needed
4. **Object Pooling**: Reuse objects instead of instantiating/destroying

### Realism vs. Performance

Balance visual fidelity with simulation performance:

```csharp
public class QualityManager : MonoBehaviour
{
    public enum QualityLevel
    {
        Performance,    // Lower quality, higher FPS
        Balanced,       // Balanced quality and performance
        Realistic       // Higher quality, lower FPS
    }

    public QualityLevel currentQualityLevel = QualityLevel.Balanced;

    void UpdateQualitySettings()
    {
        switch (currentQualityLevel)
        {
            case QualityLevel.Performance:
                QualitySettings.SetQualityLevel(2); // Lower preset
                break;
            case QualityLevel.Balanced:
                QualitySettings.SetQualityLevel(3); // Medium preset
                break;
            case QualityLevel.Realistic:
                QualitySettings.SetQualityLevel(5); // Higher preset
                break;
        }
    }
}
```

## Integration with Gazebo

### Hybrid Simulation Approach

Combine Gazebo physics with Unity rendering:

```
Gazebo (Physics) ←→ ROS Bridge ←→ Unity (Rendering)
     ↓                    ↓              ↓
  Accurate        Standardized    Photorealistic
  Dynamics        Communication    Visualization
```

### Synchronization Considerations

- **Timing**: Keep physics and rendering synchronized
- **State**: Ensure robot state consistency between systems
- **Performance**: Balance update rates for both systems

## Hands-On Exercise

Create a Unity scene with:
1. A humanoid robot model with realistic materials
2. Basic interaction system responding to user input
3. ROS connection for state synchronization
4. Simple perception simulation capabilities

## Summary

Unity provides powerful capabilities for high-fidelity rendering and human-robot interaction in robotics applications. By combining Unity's visual capabilities with ROS integration, you can create immersive environments for testing humanoid robots, training perception systems, and developing human-robot interaction paradigms.

## Next Steps

Continue to the next lesson on [Simulating sensors: LiDAR, Depth Cameras, and IMUs](/docs/module-2/sensor-simulation) to learn about sensor simulation for perception systems.

## Cross-References

- [Module 2 Introduction](/docs/module-2/intro)
- [Simulating sensors: LiDAR, Depth Cameras, and IMUs](/docs/module-2/sensor-simulation)
- [Weeks 6-7: Robot Simulation with Gazebo](/docs/weekly-breakdown/weeks-6-7)