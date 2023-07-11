import bpy
from bpy.types import Operator
import utils
from custom_operator import *
import numpy as np

class OBJECT_OT_quick_transforms(CustomOperator, Operator):
    bl_idname = "object.quick_transform"
    bl_label = "Quick Transform"
    bl_options = {"REGISTER", "UNDO"}
    desc_lines = [
        "Quick transform an object by set amount",
        "CTRL - Multiply transform amount by -1.",
        "ALT - Transform amount = 1 / transform amount",
    ]
    bl_description = "\n".join(desc_lines)

    axis: bpy.props.EnumProperty(
        items=(
            ("X", "X", "X Axis"),
            ("Y", "Y", "Y Axis"),
            ("Z", "Z", "Z Axis"),
            ("ALL", "All", "All Axes"),
        ),
        name="Axis",
        description="Transform Axis",
        default=None,
    )
    transform_type: bpy.props.EnumProperty(
        items=(
            ("Scale", "Scale", "Scale"),
            ("Rotation", "Rotation", "Rotation"),
        ),
        name="Transform Type",
        description="Type of Transform",
        default=None,
    )
    transform_amt: bpy.props.FloatProperty(name="Transform Amount")

    @property
    def axis_as_vector(self):
        if self.axis == "ALL":
            return [1, 1, 1]
        vector = [0, 0, 0]
        i = list("XYZ").index(self.axis)
        vector[i] = 1
        return vector

    def rotate_object(self):
        deg = np.radians(self.transform_amt)
        setattr(self, "transform_amt", deg)
        mat_func = getattr(self.mx, self.transform_type)
        transform_matrix = mat_func(self.transform_amt, 4, self.axis_as_vector)
        self.obj.matrix_world = transform_matrix

    def scale_object(self):
        if self.axis == "ALL":
            scale_attr = getattr(self.obj, "scale")
            scale_attr *= self.transform_amt
        else:
            scale_attr = getattr(self.obj.scale, self.axis.lower())
            new_val = scale_attr * self.transform_amt
            setattr(self.obj.scale, self.axis.lower(), new_val)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def invoke(self, context, event):
        if event.ctrl:
            self.transform_amt *= -1
        if event.alt:
            self.transform_amt = 1 / self.transform_amt
        return self.execute(context)

    def execute(self, context):
        self.obj = self.get_active_obj()
        self.mx = self.obj.matrix_world
        scale_apply = False
        rotation_apply = False
        if self.transform_type == "Rotation":
            rotation_apply = True
            self.rotate_object()
        else:
            scale_apply = True
            self.scale_object()
        bpy.ops.object.transform_apply(
            location=False, rotation=rotation_apply, scale=scale_apply
        )
        return {"FINISHED"}
