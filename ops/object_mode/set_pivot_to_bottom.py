import bpy
import bmesh
import utils
import numpy as np
from mathutils import Vector


def set_pivot_to_bottom(obj):
    mesh = obj.data
    mw = obj.matrix_world
    vert_ws = np.array([mw @ vert.co for vert in mesh.vertices])
    obj_loc = mw.translation
    new_loc = obj_loc.copy()

    z_loc = vert_ws[:, 2].min()
    new_loc.z = z_loc
    dist_vec = obj_loc.copy() - new_loc
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.translate(bm, vec=dist_vec, verts=bm.verts[:])
    bm.to_mesh(mesh)
    bm.free()
    obj.location -= dist_vec


def main(context):
    C = context
    orig_mode = C.mode
    if orig_mode == "EDIT_MESH":
        orig_mode = "EDIT"

    if C.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")
    bpy.ops.object.rotation_clear(clear_delta=False)

    for obj in context.selected_objects[:]:
        set_pivot_to_bottom(obj)
    bpy.ops.object.mode_set(mode=orig_mode)


class OBJECT_OT_set_pivot_to_bottom(bpy.types.Operator):
    """Set objects pivot to bottom"""

    bl_idname = "object.set_pivot_to_bottom"
    bl_label = "Pivot to Bottom"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        main(context)

        return {"FINISHED"}
