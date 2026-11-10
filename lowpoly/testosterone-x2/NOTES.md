# testosterone-x2 (3D low-poly, smooth, 30 s, 900 frames)
New look: a sunset loft gym (Gym.tsx) and a detailed procedural man (Man.tsx: muscle, beard, acne, hairline, flush, chest, ripping shirt).
Inside-body scenes (Inside.tsx): a vessel clogging with biconcave RBCs, a racing heart, and aromatase turning T into E.
Facts:
- Supraphysiological testosterone raises muscle mass (Bhasin 1996), facial and body hair, acne, and androgenic hair loss (DHT).
- It causes erythrocytosis: haematocrit above ~54% is the TRT threshold.
- Aromatase converts excess T into estradiol, which causes gynecomastia.
- HPG suppression shuts down the body's own production and causes testicular atrophy.
On-screen: "EFFECTS SPED UP FOR THE VIDEO". The caption also says it takes weeks.
Bug to remember: never pass `new Geometry/Material` inline in `<instancedMesh args>`. A new object every render recreates the mesh, all instances collapse to the origin, and you get a glowing box. Memoize them and set matrices in an effect without deps.

## v2: real rigged character
- The hero is now Quaternius "BaseHuman" (CC0, poly.pizza; public/man.glb) driven by Hero.tsx: Idle clip + aimed bones for curl, double-biceps, look-down and hunch.
- Muscles, beard, acne, pecs and abs are meshes attached to bones through `attach()`, which cancels the armature's world scale.
- Lessons:
  - Never scale bones non-uniformly. The parent scale shears the child limbs and ruins the poses.
  - Reset the bones to their rest quaternions every frame. Bones the clip doesn't animate otherwise accumulate rotateX.
  - Preload GLBs outside ThreeCanvas (glb.ts useGLBs). Otherwise Remotion captures frames before the model loads.
- The vertex "inflate" deformer (rig.bulk) is disabled: it broke the mesh in the browser. Reason unknown, TODO.
