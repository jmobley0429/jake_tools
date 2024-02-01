import bpy


class MESH_OT_separate_and_invert_edit_object(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "mesh.separate_and_invert_edit_object"
    bl_label = "Separate and Invert Active Edit Object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return "EDIT" in context.mode and context.edit_object.type == "MESH"

    def execute(self, context):
        bpy.ops.mesh.separate(type="SELECTED")
        bpy.ops.mesh.invert_active_edit_object()
        return {"FINISHED"}
