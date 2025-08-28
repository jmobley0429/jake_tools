import bpy


def main(context, op_type):
    C = context
    orig_mode = C.mode
    if orig_mode == "EDIT_MESH":
        orig_mode = "EDIT"

    if C.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    bpy.ops.object.origin_set(type=op_type)

    bpy.ops.object.mode_set(mode=orig_mode)


class OBJECT_custom_origin_set(bpy.types.Operator):
    """Set objects pivot to bottom"""

    bl_idname = "object.custom_origin_set"
    bl_label = "Set Object Origin"

    type: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        main(context, self.type)

        return {"FINISHED"}
