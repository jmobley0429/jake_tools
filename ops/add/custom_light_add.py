import bpy
from bpy.types import Operator
from custom_operator import *
import numpy as np
from mathutils import Vector, Euler, Quaternion

def add_custom_light(context, args):
    light_type = args.pop("light_type")
    light_name = light_type.capitalize()
    cursor_loc = context.scene.cursor.location
    light_data = bpy.data.lights.new(light_name, type=light_type)
    light_data.use_contact_shadow = True
    light_obj = bpy.data.objects.new(light_name, light_data)
    context.collection.objects.link(light_obj)
    light_obj.location = cursor_loc
    context.view_layer.objects.active = light_obj
    light_obj.select_set(True)


class OBJECT_custom_light_add(bpy.types.Operator):
    bl_idname = "object.custom_light_add"
    bl_label = "Custom Add Light"
    bl_options = {"REGISTER", "UNDO"}

    light_type: bpy.props.EnumProperty(
        items={
            ("AREA", "Area", "Area"),
            ("POINT", "Point", "Point"),
            ("SPOT", "Spot", "Spot"),
            ("SUN", "Sun", "Sun"),
        },
        name="Light Type",
    )

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        args = self.as_keywords()
        add_custom_light(context, args)
        return {"FINISHED"}

