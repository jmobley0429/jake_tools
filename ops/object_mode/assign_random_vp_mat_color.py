import bpy
import numpy as np


def main(context):
    C = context
    DEFAULT_COLOR = [0.800000, 0.800000, 0.800000, 1.000000]
    done_mats = set()
    for obj in C.selected_objects:
        if obj.type == "MESH":
            mats = obj.data.materials
            for material in mats:
                if material is not None:

                    if (
                        material not in done_mats
                        or material.diffuse_color != DEFAULT_COLOR
                    ):
                        r = np.random.rand(3, 1)
                        r = np.append(r, 1.0)
                        material.diffuse_color = r
                        done_mats.add(material)


class OBJECT_OT_assign_random_vp_mat_color(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.assign_random_vp_mat_color"
    bl_label = "Assign Random Viewport Mat Color"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {"FINISHED"}


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
