import bpy
from bpy import data as D
from bpy import context as C
import numpy as np


def get_axis_index(axis):
    axes = list("XYZ")
    return axes.index(axis)


def even_space_objects(context, axis):
    index = get_axis_index(axis)
    sel_objs = C.selected_objects[:]
    locs = np.array([obj.location.copy() for obj in sel_objs])
    start = locs[:, index].min()
    stop = locs[:, index].max()
    new_locs = np.linspace(start, stop, num=len(sel_objs))
    for obj, new_loc in zip(sel_objs, new_locs):
        obj.location[index] = new_loc


class OBJECT_OT_even_space_objects(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "object.even_space_objects"
    bl_label = "Even Space Objects"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(
        items=[
            ("X", "X", "X"),
            ("Y", "Y", "Y"),
            ("Z", "Z", "Z"),
        ],
        name="Axis",
        default="X",
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode == "OBJECT"

    def execute(self, context):
        even_space_objects(context, self.axis)
        return {"FINISHED"}
