import bpy


def main(context, operator):
    args = operator.as_keywords()
    invert = args["invert"]
    operator_to_call = args["operator_to_call"]
    del_type = args["del_type"]
    mod, operator_str = operator_to_call.split(".")
    if invert:
        bpy.ops.mesh.select_all(action="INVERT")

    module = getattr(bpy.ops, mod)
    op = getattr(module, operator_str)
    if del_type:
        op("INVOKE_DEFAULT", type=del_type)
    else:
        op("INVOKE_DEFAULT")


class MESH_OT_custom_delete_elements(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "mesh.delete_elements"
    bl_label = "Delete Mesh Elements"
    bl_options = {"REGISTER", "UNDO"}

    invert: bpy.props.BoolProperty(
        name="Invert Delete", default=False, options={"SKIP_SAVE"}
    )
    operator_to_call: bpy.props.StringProperty(
        name="Delete Operator", default="", options={"SKIP_SAVE"}
    )
    del_type: bpy.props.StringProperty(
        name="Delete Type", default="", options={"SKIP_SAVE"}
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and "EDIT" in context.mode

    def invoke(self, context, event):
        if event.alt:
            self.invert = True
        return self.execute(context)

    def execute(self, context):
        main(context, self)
        return {"FINISHED"}
