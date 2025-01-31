import bpy
import numpy as np


def missing_node_group():
    return "Smooth by Angle" not in bpy.data.node_groups


def has_ss_mod(obj):
    for mod in obj.modifiers:
        if "ShadeSmooth" in mod.name:
            return mod.name
    return False


def handle_existing_mod(obj, context, ss_mod_name):

    if ss_mod_name:
        num_mods = len(obj.modifiers)
        context.view_layer.objects.active = obj
        bpy.ops.object.modifier_move_to_index(modifier=ss_mod_name, index=num_mods - 1)
        return True


def set_mod_vals(mod):
    mod["Socket_1"] = True
    mod["Input_1"] = np.radians(22.5)


def add_shade_smooth_ng(obj, context):
    ss_mod_name = has_ss_mod(obj)
    if missing_node_group():
        bpy.ops.object.modifier_add_node_group(
            asset_library_type="ESSENTIALS",
            asset_library_identifier="",
            relative_asset_identifier=(
                "geometry_nodes\\smooth_by_angle.blend\\NodeTree\\Smooth by Angle"
            ),
        )
        mod = obj.modifiers[-1]
        set_mod_vals(mod)
    elif ss_mod_name:
        handle_existing_mod(obj, context, ss_mod_name)
    else:
        mod = obj.modifiers.new(name="ShadeSmooth", type="NODES")
        mod.node_group = bpy.data.node_groups["Smooth by Angle"]
        set_mod_vals(mod)


class OBJECT_OT_shade_smooth_modifier_add(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.shade_smooth_modifier_add"
    bl_label = "Add Shade Smooth Modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        for obj in context.selected_objects[:]:
            if obj.type in {"MESH", "CURVE"}:
                context.view_layer.objects.active = obj
                add_shade_smooth_ng(obj, context)
        return {"FINISHED"}


kms = [
    {
        "keymap_operator": OBJECT_OT_shade_smooth_modifier_add.bl_idname,
        "name": "Object Mode",
        "letter": "H",
        "shift": 0,
        "ctrl": 1,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {},
    }
]
