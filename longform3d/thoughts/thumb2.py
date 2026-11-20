# Ifology-PATTERN thumbnails with OUR characters (owner 2026-11-20): one dramatic idea, big character, neon dark
# backdrop, glowing thought rings/bubbles; the giant 2-word caption is added in post (tools/thumb_text.py).
#   blender -b -P thumb2.py -- A|B <out.png>
import sys, os, math, random
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, lib3d as L, sets3d as S
from mathutils import Vector
from cast import LOOKS
V, OUT = sys.argv[sys.argv.index("--") + 1:][:2]; F = 1
L.fresh(); sc = bpy.context.scene; L.world(L.hexc("120a2a"), 1.0)
# neon backdrop: big emissive plane, magenta → deep blue (mesh Generated coords work; world gradients did not)
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 7, 4), rotation=(math.pi / 2, 0, 0)); bd = bpy.context.object; m = bpy.data.materials.new("bd"); m.use_nodes = True
nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; tc = N("ShaderNodeTexCoord"); sep = N("ShaderNodeSeparateXYZ"); r = N("ShaderNodeValToRGB"); e = N("ShaderNodeEmission"); o = N("ShaderNodeOutputMaterial")
r.color_ramp.elements[0].color = (*L.hexc("3a1070"), 1); r.color_ramp.elements[0].position = 0.35; r.color_ramp.elements[1].color = (*L.hexc("0b1a4a"), 1); r.color_ramp.elements[1].position = 0.62
nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Y"], r.inputs[0]); nt.links.new(r.outputs[0], e.inputs[0]); nt.links.new(e.outputs[0], o.inputs[0]); m["toon"] = 1; bd.data.materials.append(m)
rnd = random.Random(3)
for k in range(40):     # city-light bokeh
    L.sph(rnd.uniform(0.05, 0.16), (rnd.uniform(-5, 5), rnd.uniform(4, 6.5), rnd.uniform(0.3, 4.5)), L.mat(rnd.choice(["ff5ad8", "5ae8ff", "ffd25a", "9a6aff"]), 0.3, emit=3.0), seg=12, name="bokeh")
cam = L.camera("cam", (0.0, -2.15, 1.55), (0.0, 0.0, 1.5), 35); cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = 2.8; sc.camera = cam
bpy.ops.object.empty_add(location=(0, 0, 0)); FOCUS = bpy.context.object; cam.data.dof.focus_object = FOCUS      # moved onto Leo's face below (v1: hero out of focus)
def flat(col):   # unshaded colour: bubbles must stay pure white (toon shading made them grey)
    m = bpy.data.materials.new("flat_" + col); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); e = nt.nodes.new("ShaderNodeEmission"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    e.inputs["Color"].default_value = (*L.hexc(col), 1); nt.links.new(e.outputs[0], o.inputs[0]); m["toon"] = 1; return m
def bubble(pos, text, col="e8384f"):
    nrm = (cam.location - Vector(pos)).normalized(); rgt = Vector((0, 0, 1)).cross(nrm).normalized(); up = nrm.cross(rgt)
    b = L.cyl(0.3, 0.03, pos, flat("ffffff"), name="bubble"); t = L.text3d(text, Vector(pos) + nrm * 0.03, 0.3 if len(text) < 3 else 0.14, flat(col)); t.name = "bubble_txt"
    for i, (dx, dz, rr) in enumerate(((-0.17, -0.36, 0.06), (-0.26, -0.5, 0.035))): L.cyl(rr, 0.03, Vector(pos) + rgt * dx + up * dz, flat("ffffff"), name="bubble_dot")
    for ob in [b, t] + [x for x in bpy.data.objects if x.name.startswith("bubble_dot")]:
        c = ob.constraints.new("TRACK_TO"); c.target = cam; c.track_axis = "TRACK_Z"; c.up_axis = "UP_Y"
LEO = L.character("LEO", LOOKS["LEO"]); chars = [LEO]
if V == "A":    # TOO LOUD. — everyone around him is thinking at once
    L.key_pose(LEO, F, {**L.idle(0), "head": (-6, 0, 0)}, (0.25, -0.6, 0), 0); L.key_pose(LEO, F, {**L.idle(0), "head": (-6, 0, 0), **L.hands_up(LEO, F, 0.42, 0.42, 0.05)})   # panic V-arms (ears pose failed)
    L.key_face(LEO, F, emotion="scared", look=(0, 0.2))
    for i, (n, x, y, face, txt, col) in enumerate((("NORA", -1.25, 1.2, 25, "♥", "e8384f"), ("DEX", 1.5, 1.5, -25, "?!", "e8743b"), ("THEO", -0.4, 2.3, 10, "$", "2f8f4e"), ("PRIYA", 0.9, 2.7, -10, "LIAR", "3a2a8a"))):
        ch = L.character(n, LOOKS[n]); chars.append(ch); L.key_pose(ch, F, L.idle(i), (x, y, 0), face); L.key_face(ch, F, emotion="smile" if i % 2 == 0 else "smug")
        S.thought_ring(ch, F - 8, F + 40, cam, "5ae8ff"); bubble(L.head_pos(ch, F) + Vector((0.3, 0, 0.45)), txt, col)
    S.thought_ring(LEO, F - 8, F + 40, cam, "ffd25a")
else:           # I HEAR YOU. — the power, sly and confident; Nora's crush thought behind him
    L.key_pose(LEO, F, {**L.idle(0), "head": (-4, -12, 6), "uarm.R": (60, 0, -20), "farm.R": (120, 0, 0)}, (0.45, -0.75, 0), -15)
    L.key_face(LEO, F, emotion="smug", look=(0.5, 0)); L.power_eyes(LEO, F - 2, None, "5ae8ff")
    NORA = L.character("NORA", LOOKS["NORA"]); chars.append(NORA); L.key_pose(NORA, F, L.idle(1), (-1.15, 1.4, 0), 30); L.key_face(NORA, F, emotion="happy", look=(-0.3, 0.4))
    S.thought_ring(NORA, F - 8, F + 40, cam, "ff7ad8"); bubble(L.head_pos(NORA, F) + Vector((0.25, 0, 0.5)), "♥", "e8384f")
FOCUS.location = L.head_pos(LEO, F)
L.toon_look(chars, (-0.6, -0.5, 0.6), "6ff3ff", mood="day")
for o_ in bpy.data.objects:            # the backdrop and bokeh keep their glow
    if o_.name.startswith(("bokeh",)) or o_ == bd: o_.modifiers.clear()
L.setup("final", (1280, 720), 24); sc.frame_set(F); sc.render.image_settings.file_format = "PNG"; sc.render.filepath = OUT
bpy.ops.render.render(write_still=True); print("THUMB2_DONE")
