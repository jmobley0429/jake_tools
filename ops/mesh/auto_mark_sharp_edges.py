import bpy
import bmesh
import numpy as np


def main(context, args):
    print(args)
    angle_threshold = args.pop("angle")
    obj = context.edit_object
    mesh = obj.data

    mesh.use_auto_smooth = True
    mesh.auto_smooth_angle = 3.14159
    bm = bmesh.from_edit_mesh(mesh)

    for edge in bm.edges[:]:
        if edge.is_manifold:
            angle = edge.calc_face_angle()
            if np.degrees(angle) >= angle_threshold:
                edge.smooth = False
    bmesh.update_edit_mesh(mesh)


class MESH_OT_auto_mark_sharp(bpy.types.Operator):
    """Automatically select edges with edge angle greater than angle threshold and mark as sharp"""

    bl_idname = "mesh.auto_mark_sharp"
    bl_label = "Auto Mark Sharp Edges"
    bl_options = {"REGISTER", "UNDO"}

    angle: bpy.props.IntProperty(
        name="Angle", default=45, min=0, max=180, subtype="ANGLE"
    )

    @classmethod
    def poll(cls, context):
        return context.edit_object is not None

    def execute(self, context):
        main(context, self.as_keywords())
        return {"FINISHED"}
