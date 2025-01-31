import bpy


def main(context):
    for obj in context.selected_objects:
        if obj.type == "MESH":
            layers = obj.data.uv_layers[:]
            while layers:
                obj.data.uv_layers.remove(layers.pop())


class MESH_OT_delete_all_uv_layers(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "mesh.delete_all_uv_layers"
    bl_label = "Delete All UV Layers"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)

    def execute(self, context):
        main(context)
        return {"FINISHED"}
