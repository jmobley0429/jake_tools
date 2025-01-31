import bpy
import utils


def main(context, op):
    scene = context.scene
    mat = scene.jt_material
    for obj in context.selected_objects:
        if obj.type in {"MESH", "CURVE"}:
            for mod in obj.modifiers:
                if mod.type == "NODES":
                    if "LoftEdges" in mod.node_group.name:
                        _id = utils.get_node_group_input_id(mod, "Material")
                        mod[_id] = mat

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()


class OBJECT_assign_lofted_edge_mat(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.assign_lofted_edge_mat"
    bl_label = "Assign Mat to Lofted Edge"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context, self)
        return {"FINISHED"}

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row = layout.row()
        row.prop(scene, "jt_material")


def register():
    bpy.types.Scene.jt_material = bpy.props.PointerProperty(
        type=bpy.types.Material, name="Material"
    )


def unregister():
    del bpy.types.Scene.jt_materials
