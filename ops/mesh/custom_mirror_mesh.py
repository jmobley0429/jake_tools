import bpy
from bpy.props import EnumProperty

AXES = list("XYZ")
AXES_ITEMS = tuple(zip(AXES, AXES, AXES))


class MESH_OT_custom_mirror_mesh(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "mesh.custom_mirror_mesh"
    bl_label = "Custom Mirror Mesh"
    bl_options = {"REGISTER", "UNDO"}

    axis: EnumProperty(
        name="Axis",
        items=AXES_ITEMS,
        options={"SKIP_SAVE"},
    )

    def get_axis(self):

        AXES_VALUES = [
            (True, False, False),
            (False, True, False),
            (False, False, True),
        ]

        AXES_DICT = dict(zip(AXES, AXES_VALUES))

        return AXES_DICT[self.axis]

    @classmethod
    def poll(cls, context):
        return context.edit_object is not None and context.edit_object.type == "MESH"

    def execute(self, context):
        constraint_axis = self.get_axis()
        bpy.ops.transform.mirror(constraint_axis=constraint_axis)
        bpy.ops.mesh.flip_normals()
        return {"FINISHED"}
