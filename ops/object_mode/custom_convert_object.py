import bpy
from bpy.types import Operator


class OBJECT_OT_CustomConvertObject(Operator):
    """Convert object to another object type. CTRL > Keep Original"""

    bl_idname = "object.custom_convert_object"
    bl_label = "Custom Convert Object"
    bl_description = """Convert object to another object type. CTRL > Keep Original."""
    bl_options = {"REGISTER", "UNDO"}

    target: bpy.props.StringProperty(default="MESH", name="Target")
    keep_original: bpy.props.BoolProperty(default=False, name="Keep Original")

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def invoke(self, context, event):
        self.keep_original = False
        if event.ctrl:
            self.keep_original = True
        return self.execute(context)

    def execute(self, context):
        objs = sorted(context.selected_objects[:], key=lambda obj: obj.name)
        obj_types = {"MESH", "CURVE", "METABALL", "GPENCIL", "FONT"}
        objs = [obj for obj in objs if obj.type in obj_types]
        bpy.ops.object.select_all(action="DESELECT")
        for obj in objs:
            obj.select_set(True)
        bpy.ops.object.convert(
            target=self.target, keep_original=self.keep_original
        )
        return {"FINISHED"}
