import bpy


def main(context, args):
    C = context
    use_self = args["use_self"]
    use_hole_tolerant = args["use_hole_tolerant"]
    material_mode = args["material_mode"]
    for obj in C.selected_objects[:]:
        for mod in obj.modifiers[:]:
            if mod.type == "BOOLEAN":
                mod.use_self = use_hole_tolerant
                mod.use_hole_tolerant = use_hole_tolerant
                mod.material_mode = material_mode


class MODIFIER_OT_set_bool_options(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "modifier.set_bool_options"
    bl_label = "Set Bool Modifier Options"
    bl_options = {"REGISTER", "UNDO"}

    use_self: bpy.props.BoolProperty(name="Use Self Intersection", default=True)
    use_hole_tolerant: bpy.props.BoolProperty(name="Use Hole Tolerant", default=True)
    material_mode: bpy.props.EnumProperty(
        name="Material Mode",
        items=[
            ("TRANSFER", "Transfer", "Transfer"),
            ("INDEX", "Index Based", "Index Based"),
        ],
        default="TRANSFER",
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context, args=self.as_keywords())
        return {"FINISHED"}
