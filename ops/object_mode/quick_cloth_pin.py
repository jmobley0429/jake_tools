from bpy.types import Operator
from custom_operator import *


class PinCreator:

    def __init__(self, context):
        self.obj = context.view_layer.objects.active
        self.mesh = self.obj.data
        self.verts = self.mesh.vertices

    def get_pin_group(self):
        if "pin" not in [group.name for group in self.obj.vertex_groups[:]]:
            self.group = self.obj.vertex_groups.new(name="pin")
        else:
            self.group = self.obj.vertex_groups["pin"]

    def execute(self):
        self.get_pin_group()
        sel_verts = [vert.index for vert in self.verts if vert.select]
        self.add_to_group(sel_verts)
        self.add_cloth_modifier()

    def add_to_group(self, verts):
        self.group.add(verts, 1.0, "ADD")

    def add_cloth_modifier(self):
        mods = [mod for mod in self.obj.modifiers[:]]
        mod_types = [mod.type for mod in mods]
        if "CLOTH" not in mod_types:
            mod = self.obj.modifiers.new("CLOTH", type="CLOTH")
        else:
            mod = mods[mod_types.index("CLOTH")]
        mod.settings.vertex_group_mass = "pin"


class OBJECT_OT_quick_cloth_pin(Operator):
    bl_idname = "object.quick_cloth_pin"
    bl_label = "Quick Cloth Pin"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        orig_type = context.mode
        if orig_type != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        pc = PinCreator(context)
        pc.execute()
        if "EDIT" in orig_type:
            bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}
