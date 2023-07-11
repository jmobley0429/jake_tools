#modifier
import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *


def apply_relevant_mods(obj):
    relevant_mods = [
        "SOLIDIFY",
    ]
    for mod in obj.modifiers[:]:
        if mod.type in relevant_mods:
            bpy.ops.object.modifier_apply(modifier=mod.name)


def set_angle(edge, sharpness, creases):
    try:
        angle = edge.calc_face_angle()
    except ValueError:
        angle = 0.0
    print("ANGLE: ", angle)

    delta = angle - np.radians(sharpness)
    print("DELTA: ", delta)
    if delta >= 0.001:
        edge[creases] = 1.0
    else:
        edge[creases] = 0.0
    print("CREASE_AMT: ", edge[creases])


def auto_crease_subdivide(context, args):
    sharpness = args.pop('sharpness')
    in_edit = "EDIT" in context.mode
    if in_edit:
        bpy.ops.object.mode_set(mode="OBJECT")
    for obj in context.selected_objects:
        if obj.type == "MESH":
            context.view_layer.objects.active = obj
            apply_relevant_mods(obj)
            me = obj.data
            bm = bmesh.new()
            bm.from_mesh(me)

            creases = bm.edges.layers.crease.verify()

            for edge in bm.edges[:]:
                set_angle(edge, sharpness, creases)
            bm.to_mesh(me)
            bpy.ops.object.modifier_add(type="SUBSURF")
            bm.free()
    if in_edit:
        bpy.ops.object.mode_set(mode="EDIT")


class OBJECT_OT_auto_crease_subdivide(bpy.types.Operator):
    """Automatically set sharp edges to creased and adds a subsurf mod. Will apply Solidify modifiers."""

    bl_idname = "object.auto_crease_subdivide"
    bl_label = "Simple Object Operator"

    sharpness: bpy.props.FloatProperty(name="Sharpness", description="Degree to set sharp angles at.", default=45.0)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        args = self.as_keywords()
        auto_crease_subdivide(context, args)
        return {'FINISHED'}