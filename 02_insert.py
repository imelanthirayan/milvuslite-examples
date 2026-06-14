"""
02_insert.py — Insert hundreds of document chunks about Unity, Unreal and Blender

Each document is split into multiple chunks (like a RAG pipeline).
Same document title, different chunk content, unique chunk ID per row.

Run from the milvuslite-kit folder:
    python examples/02_insert.py
"""

import random
from milvuslite_kit import MilvusLiteKit

DIM = 128

def random_vector():
    return [random.uniform(0, 1) for _ in range(DIM)]

# Each entry: (doc_id_prefix, title, category, published, author, [chunks])
DOCUMENTS = [

    # ── UNITY ─────────────────────────────────────────────────────────────────
    ("unity-gs", "Getting Started with Unity", "unity", True, "Alice Morgan", [
        "Unity is a cross-platform game engine developed by Unity Technologies.",
        "Unity supports 2D and 3D game development for mobile, desktop, consoles and the web.",
        "To create a new project, open Unity Hub, click New Project and choose a template.",
        "The Unity Editor has four main panels: Scene, Game, Hierarchy and Inspector.",
        "The Scene view lets you position GameObjects in 3D space using the transform tools.",
        "The Hierarchy panel lists every GameObject in the current scene.",
        "The Inspector shows the components attached to the selected GameObject.",
        "A Component is a modular piece of behaviour you attach to a GameObject.",
        "Unity uses C# as its primary scripting language.",
        "Scripts are attached to GameObjects as components via the Inspector.",
        "The Start() method runs once when the scene begins; Update() runs every frame.",
        "Use Debug.Log() to print messages to the Unity Console.",
        "Assets like textures, models and audio are stored in the Assets folder.",
        "The Package Manager lets you add official and community packages to your project.",
        "Build Settings allow you to target different platforms such as Android, iOS or PC.",
    ]),

    ("unity-scripting", "Unity C# Scripting Guide", "unity", True, "Alice Morgan", [
        "A MonoBehaviour is the base class for all Unity scripts.",
        "Awake() is called before Start() and is used for internal initialisation.",
        "FixedUpdate() runs at a fixed time step and is best for physics calculations.",
        "LateUpdate() runs after all Update() calls, useful for camera follow logic.",
        "Use GetComponent<T>() to access another component on the same GameObject.",
        "SerializeField exposes a private field in the Inspector without making it public.",
        "Coroutines allow you to spread execution over multiple frames using IEnumerator.",
        "yield return new WaitForSeconds(t) pauses a coroutine for t seconds.",
        "ScriptableObjects store shared data as assets without needing a scene instance.",
        "Events and delegates decouple systems and reduce tight coupling between scripts.",
        "Input.GetAxis('Horizontal') returns a value between -1 and 1 for horizontal input.",
        "Rigidbody.AddForce() applies a physics force to a GameObject.",
        "Instantiate() creates a copy of a prefab at runtime.",
        "Destroy() removes a GameObject or component from the scene.",
        "PlayerPrefs stores small amounts of persistent data between sessions.",
    ]),

    ("unity-physics", "Unity Physics System", "unity", True, "Carlos Vega", [
        "Unity uses the PhysX physics engine for 3D simulations.",
        "A Rigidbody component makes a GameObject react to gravity and forces.",
        "Colliders define the physical shape used for collision detection.",
        "Box Collider, Sphere Collider and Mesh Collider are common collider types.",
        "Is Kinematic disables physics simulation so you can move objects via script.",
        "OnCollisionEnter() is called when two colliders first make contact.",
        "OnTriggerEnter() fires when a collider marked as Trigger is entered.",
        "Physics.Raycast() casts a ray and returns information about what it hits.",
        "Layers and Layer Collision Matrix control which objects can collide.",
        "Physics materials define friction and bounciness between surfaces.",
        "Joints connect two Rigidbodies, e.g. HingeJoint for doors and levers.",
        "The Physics Settings panel controls gravity, fixed timestep and solver iterations.",
        "Character Controller is a specialised collider for player movement.",
        "NavMesh enables AI agents to navigate around obstacles automatically.",
        "Continuous collision detection prevents fast-moving objects from tunnelling.",
    ]),

    ("unity-ui", "Unity UI and Canvas System", "unity", True, "Carlos Vega", [
        "Unity's UI system is built on the Canvas component.",
        "All UI elements must be children of a Canvas in the Hierarchy.",
        "Canvas Render Modes are Screen Space Overlay, Screen Space Camera and World Space.",
        "The Rect Transform replaces the regular Transform for UI elements.",
        "Text, Image, Button, Slider and Toggle are the core UI components.",
        "TextMeshPro provides high-quality text rendering with signed distance fields.",
        "Anchors pin a UI element to a part of its parent, making layouts responsive.",
        "Layout Groups (Horizontal, Vertical, Grid) arrange children automatically.",
        "The Event System handles user input such as clicks and keyboard navigation.",
        "Button.onClick is an UnityEvent you can wire up in the Inspector or via script.",
        "Panels are Image components used to group and background other UI elements.",
        "Canvas Scaler adjusts UI size for different screen resolutions.",
        "Animator can drive UI transitions just like 3D animations.",
        "UI Toolkit is a newer, CSS-like alternative to the uGUI Canvas system.",
        "UGUI and UI Toolkit can coexist in the same project.",
    ]),

    ("unity-shaders", "Unity Shader and Materials", "unity", False, "Alice Morgan", [
        "A Material defines how a surface looks by referencing a Shader.",
        "Shader Graph is a visual node-based tool for creating shaders without code.",
        "The Universal Render Pipeline (URP) is Unity's lightweight, scalable pipeline.",
        "The High Definition Render Pipeline (HDRP) targets high-end platforms.",
        "PBR shaders use albedo, metallic, smoothness and normal maps.",
        "Emission adds a glow effect independently of scene lighting.",
        "A Shader variant is generated for each combination of keywords.",
        "Shader.Find() looks up a shader by name at runtime.",
        "Surface shaders abstract lighting calculations for common use cases.",
        "Unlit shaders render without any lighting, useful for UI and effects.",
        "The Stencil Buffer enables masking and portal effects.",
        "Depth Write controls whether an object writes to the depth buffer.",
        "Transparency requires careful sorting; use Transparent render queue.",
        "GPU Instancing renders many identical objects with a single draw call.",
        "Shader compilation can be offloaded using Shader Prewarming.",
    ]),

    # ── UNREAL ENGINE ──────────────────────────────────────────────────────────
    ("unreal-gs", "Getting Started with Unreal Engine", "unreal", True, "Ben Carter", [
        "Unreal Engine is a high-end game engine developed by Epic Games.",
        "Unreal Engine 5 introduced Nanite virtualised geometry and Lumen global illumination.",
        "The Epic Games Launcher manages Unreal Engine installations and projects.",
        "The Level Editor is the main workspace for building environments.",
        "Actors are the fundamental objects placed in an Unreal level.",
        "Components are attached to Actors to add functionality, similar to Unity.",
        "The Content Browser stores all assets: meshes, textures, materials and blueprints.",
        "World Partition allows seamless open worlds without manually dividing the map.",
        "The Outliner lists all Actors in the current level.",
        "The Details panel shows properties of the selected Actor.",
        "Levels are saved as .umap files inside the Content folder.",
        "Play In Editor (PIE) lets you test the game without building.",
        "Hot Reload recompiles C++ code while the editor is running.",
        "The Marketplace provides free and paid assets for Unreal projects.",
        "Unreal supports C++ and Blueprints as development approaches.",
    ]),

    ("unreal-blueprints", "Unreal Engine Blueprints Guide", "unreal", True, "Ben Carter", [
        "Blueprints is Unreal's visual scripting system based on nodes and wires.",
        "Blueprint Classes extend existing classes such as Actor or Character.",
        "Event Graph handles events like BeginPlay, Tick and user input.",
        "BeginPlay fires once when the game starts for that Actor.",
        "Event Tick fires every frame; avoid heavy logic here for performance.",
        "Variables store data; they can be Boolean, Integer, Float, Vector and more.",
        "Functions encapsulate reusable logic within a Blueprint.",
        "Macros are like functions but can have multiple execution pins.",
        "Cast To converts a reference to a more specific type to access its properties.",
        "Get All Actors Of Class returns every Actor of a type in the level.",
        "Timers call a function after a delay or on a repeating interval.",
        "Blueprint Interfaces define a contract that multiple Blueprints can implement.",
        "Blueprint Communication allows one Blueprint to call functions on another.",
        "Data Tables store structured data, like stats or item definitions.",
        "Enumerations define a named set of values, improving readability.",
    ]),

    ("unreal-materials", "Unreal Engine Materials and Shading", "unreal", True, "Sara Lin", [
        "Materials in Unreal are created using a node-based Material Editor.",
        "The Base Color input sets the diffuse colour of the surface.",
        "Metallic controls whether a surface behaves as a metal or non-metal.",
        "Roughness determines how blurry or sharp reflections appear.",
        "Normal maps add surface detail without extra geometry.",
        "Emissive Color makes a surface glow independently of lights.",
        "Material Instances inherit from a parent material and expose parameters.",
        "Dynamic Material Instances can have their parameters changed at runtime.",
        "Texture Samples read colour or data from a texture asset.",
        "Material Functions are reusable node groups shared across materials.",
        "The Translucency blend mode enables transparent or semi-transparent surfaces.",
        "Subsurface Scattering simulates light passing through skin or wax.",
        "Vertex painting lets artists blend materials directly on a mesh in the editor.",
        "Nanite meshes support full material complexity without baking.",
        "Lumen reacts to Emissive materials to produce indirect lighting.",
    ]),

    ("unreal-physics", "Unreal Engine Physics and Collision", "unreal", True, "Sara Lin", [
        "Unreal Engine uses the Chaos physics engine since UE5.",
        "Physics Bodies define which parts of a mesh participate in simulation.",
        "Simple Collision uses primitive shapes; Complex Collision uses the mesh itself.",
        "Simulate Physics on a component enables ragdoll and rigid body dynamics.",
        "Physics Constraints act as joints connecting two physics bodies.",
        "Line Trace (Raycast) tests for intersections along a line in the world.",
        "Collision Channels determine what each Actor can block, overlap or ignore.",
        "On Component Hit fires when a simulated object strikes another collider.",
        "On Component Begin Overlap fires when two overlapping volumes intersect.",
        "Physical Materials define friction, restitution and density per surface.",
        "Destructible Meshes break apart on impact using Chaos Fracture.",
        "Cloth Simulation integrates with Chaos for realistic fabric movement.",
        "Vehicle Physics uses a WheeledVehicle class with suspension and tyre models.",
        "Fluid Simulation is available via Niagara for visual effects.",
        "Async Scene enables physics to run on a separate thread for performance.",
    ]),

    ("unreal-niagara", "Unreal Niagara Particle System", "unreal", False, "Ben Carter", [
        "Niagara is Unreal's next-generation visual effects system.",
        "A Niagara System contains one or more Emitters.",
        "Emitters define the behaviour and appearance of a particle group.",
        "Spawn Rate controls how many particles are created per second.",
        "Particle Lifetime determines how long each particle lives.",
        "Initial Velocity adds movement to newly spawned particles.",
        "Drag slows particles down over time.",
        "Colour Over Life changes the colour of a particle as it ages.",
        "Scale Mesh Size modifies particle size during its lifetime.",
        "Sprite Renderer draws particles as camera-facing billboards.",
        "Mesh Renderer spawns 3D meshes as particles instead of sprites.",
        "Ribbon Renderer connects particles into a continuous ribbon trail.",
        "GPU Simulation moves particle calculations to the GPU for large counts.",
        "Niagara Data Channels enable particles to communicate with Blueprints.",
        "Modules are reusable building blocks that can be shared across emitters.",
    ]),

    # ── BLENDER ────────────────────────────────────────────────────────────────
    ("blender-gs", "Getting Started with Blender", "blender", True, "Maya Patel", [
        "Blender is a free and open-source 3D creation suite.",
        "Blender supports modelling, sculpting, rigging, animation, rendering and compositing.",
        "The interface is divided into areas; each area can display a different editor.",
        "Right-click opens a context menu; middle-mouse orbits the 3D Viewport.",
        "Object Mode is for selecting and transforming whole objects.",
        "Edit Mode is for modifying the vertices, edges and faces of a mesh.",
        "G, R and S are the shortcuts for Grab, Rotate and Scale.",
        "X, Y or Z after a transform locks it to that axis.",
        "The Outliner lists all objects in the scene as a hierarchy.",
        "The Properties panel contains settings for rendering, materials, physics and more.",
        "Collections group objects together for organisation and visibility control.",
        "N opens the side panel with numeric transform fields.",
        "Add > Mesh adds primitive objects like cubes, spheres and cylinders.",
        "Blender uses Python for scripting and add-on development.",
        "The Asset Library stores reusable materials, objects and node groups.",
    ]),

    ("blender-modeling", "Blender Mesh Modelling Guide", "blender", True, "Maya Patel", [
        "Mesh modelling starts with a primitive and refines it into the desired shape.",
        "Loop Cut (Ctrl+R) adds an edge loop around a mesh.",
        "Extrude (E) pulls selected geometry outward to add detail.",
        "Inset (I) creates a smaller face inside a selected face.",
        "Bevel (Ctrl+B) rounds off sharp edges.",
        "Subdivision Surface adds geometry to smooth a low-poly mesh.",
        "Mirror Modifier reflects geometry across an axis for symmetrical modelling.",
        "Boolean Modifier combines or subtracts one mesh from another.",
        "The Proportional Editing tool moves nearby vertices along with the selected ones.",
        "Knife Tool (K) cuts new edges across faces.",
        "Bridge Edge Loops connects two open edge loops with faces.",
        "Merge (M) combines selected vertices into one.",
        "Vertex Groups store named selections for use in modifiers and rigging.",
        "Custom Split Normals control shading without adding extra geometry.",
        "Retopology rebuilds a clean mesh over a high-poly sculpt.",
    ]),

    ("blender-animation", "Blender Animation and Rigging", "blender", True, "James Wu", [
        "Blender's Timeline editor shows keyframes and controls playback.",
        "Insert Keyframe (I) records the current value of a property.",
        "The Dope Sheet gives an overview of all keyframes in the scene.",
        "The Graph Editor shows animation curves for fine-tuning interpolation.",
        "Armatures are skeleton objects used to deform meshes.",
        "Bones are the individual elements of an Armature.",
        "Pose Mode lets you rotate and translate bones to create poses.",
        "Automatic Weights assigns bone influences to mesh vertices on rigging.",
        "Weight Painting manually adjusts bone influence on each vertex.",
        "Inverse Kinematics (IK) solves bone chains to reach a target position.",
        "Shape Keys morph a mesh between stored vertex positions.",
        "NLA Editor stacks and blends multiple actions non-linearly.",
        "Actions store a set of keyframes that can be reused across objects.",
        "Drivers link a property to another object or variable programmatically.",
        "Motion Paths visualise the trajectory of a bone or object over time.",
    ]),

    ("blender-rendering", "Blender Rendering with Cycles and EEVEE", "blender", True, "James Wu", [
        "Blender has two main render engines: Cycles and EEVEE.",
        "Cycles is a path-tracing engine that produces physically accurate renders.",
        "EEVEE is a real-time rasterisation engine suitable for fast previews.",
        "Samples control the quality of a Cycles render; more samples reduce noise.",
        "Denoising removes render noise using AI or compositing-based filters.",
        "HDRI Environment Textures provide realistic image-based lighting.",
        "Render Layers separate the scene into passes for compositing.",
        "The Compositor combines render passes and applies post-processing effects.",
        "Bloom adds a glow to bright areas in an EEVEE render.",
        "Ambient Occlusion darkens crevices to improve depth perception.",
        "Motion Blur simulates camera shutter during fast movement.",
        "Depth of Field blurs objects outside the focal plane.",
        "Cryptomatte generates masks for objects by ID for compositing.",
        "GPU rendering in Cycles uses OptiX or CUDA on NVIDIA cards.",
        "Render Farm distributes frames across multiple machines for speed.",
    ]),

    ("blender-python", "Blender Python Scripting", "blender", False, "Maya Patel", [
        "Blender exposes its entire interface through the bpy Python module.",
        "bpy.data provides access to all data blocks: meshes, materials, objects.",
        "bpy.ops calls operators, the same actions triggered from menus or shortcuts.",
        "bpy.context gives access to the active scene, object and mode.",
        "The Scripting workspace has a text editor and Python console built in.",
        "Running a script in the text editor executes it immediately in Blender.",
        "Add-ons are Python packages registered with Blender via bl_info.",
        "Panels add custom UI to the Properties or N-panel using bpy.types.Panel.",
        "Operators define custom actions callable from menus or shortcuts.",
        "Properties registered with bpy.props store persistent add-on settings.",
        "Handlers respond to events like frame changes or scene updates.",
        "Modal Operators run over multiple events, useful for interactive tools.",
        "bmesh provides low-level mesh editing operations in Python.",
        "Geometry Nodes can be driven by Python via the node tree API.",
        "The Blender Python API documentation lists every available class and method.",
    ]),
]

def build_records():
    records = []
    for doc_prefix, title, category, published, author, chunks in DOCUMENTS:
        for i, chunk in enumerate(chunks, start=1):
            records.append({
                "id": f"{doc_prefix}-chunk-{i:02d}",
                "title": title,
                "content": chunk,
                "category": category,
                "score": round(random.uniform(0.75, 0.99), 2),
                "published": published,
                "metadata": {"author": author, "chunk": i, "total_chunks": len(chunks)},
                "embedding": random_vector(),
            })
    return records

with MilvusLiteKit.from_yaml("config.yaml") as kit:
    kit.sync_schema()
    kit.reset_collection("documents")

    records = build_records()
    print(f"Inserting {len(records)} chunks across {len(DOCUMENTS)} documents...")

    results = kit.bulk_insert("documents", records)
    print(f"Inserted: {len(results)} records")

    # Summary by category
    from collections import Counter
    counts = Counter(r["category"] for r in records)
    for cat, n in sorted(counts.items()):
        print(f"  {cat}: {n} chunks")

