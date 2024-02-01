# modifier

import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *
from mathutils import Vector
import utils


def add_lattice_object(context, location=None):
    lat_data = bpy.data.lattices.new("Lattice")
    lat_obj = bpy.data.objects.new("Lattice", lat_data)
    context.collection.objects.link(lat_obj)
    if location is None:
        location = context.scene.cursor.location
    lat_obj.location = location
    return lat_obj


def add_lattice_mod_to_obj(obj, lattice, generate_lat=True):
    if obj.type in {"MESH", "CURVE"}:
        lat_mod = obj.modifiers.new("Lattice", type="LATTICE")
        lat_mod.object = lattice
        if generate_lat:
            dims = obj.dimensions
            ldims = lattice.dimensions
            scale_fac = Vector([d / l for l, d in zip(ldims, dims)])
            mx = obj.matrix_world
            center = utils.get_bbox_center(obj, mx)
            lattice.name = f"lattice_{obj.name}"
            lattice.location = center
            lattice.rotation_euler = obj.rotation_euler
            lattice.scale *= scale_fac
            lattice.data.points_u = 3
            lattice.data.points_v = 3
            lattice.data.points_w = 3


def remove_lattices(context, lattice_object):
    for obj in context.selected_objects[:]:
        for mod in obj.modifiers[:]:
            if mod.type == "LATTICE" and mod.object == lattice_object:
                obj.modifiers.remove(mod)


class CustomLattice(CustomModalOperator, Operator):
    bl_idname = "object.custom_lattice"
    bl_label = "Add Smart Lattice"
    bl_options = {"REGISTER", "UNDO"}

    @property
    def current_lattice_axis_val(self):
        return getattr(self.lattice.data, f"points_{self.current_axis}")

    def cycle_interp_types(self):
        curr_type = self.interpolation_type
        num_types = len(self.interpolation_types)
        curr_index = self.interpolation_types.index(curr_type)
        new_index = (curr_index + 1) % num_types
        self.interpolation_type = self.interpolation_types[new_index]
        for ax in list("uvw"):
            attrib_str = f"interpolation_type_{ax}"
            setattr(self.lattice.data, attrib_str, self.interpolation_type)

    def invoke(self, context, event):
        self.interpolation_types = [
            "KEY_CARDINAL",
            "KEY_BSPLINE",
            "KEY_LINEAR",
            "KEY_CATMULL_ROM",
        ]

        self.current_axis = "u"
        self.axes_dict = dict(zip(list("xyz"), list("uvw")))
        self.interpolation_type = self.interpolation_types[0]
        active_obj = context.view_layer.objects.active
        generate_lat = active_obj.type != "LATTICE"
        if generate_lat:
            self.lattice = add_lattice_object(context)
        else:
            self.lattice = active_obj
        if len(context.selected_objects) == 0:
            self.lattice.select_set(True)
            context.view_layer.objects.active = self.lattice
        else:
            for obj in context.selected_objects[:]:
                if obj != self.lattice:
                    add_lattice_mod_to_obj(obj, self.lattice, generate_lat=generate_lat)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    @property
    def get_info_msg(self):
        lines = [f"CURRENT AXIS: {self.current_axis.upper()}"]
        for ax in list("uvw"):
            letter = ax.upper()
            val = getattr(self.lattice.data, f"points_{ax}")
            lines.append(f"{letter}: {val}")

        lines.append(f"INTERPOLATION TYPE (I): {self.interpolation_type}")
        return ", ".join(lines)

    def modal(self, context, event):
        e = event
        et = e.type
        self.display_modal_info(self.get_info_msg, context)
        if et in list("UVW"):
            self.current_axis = et.lower()
        elif et in list("XYZ"):
            self.current_axis = self.axes_dict[et.lower()]
        elif et in {"WHEELUPMOUSE", "WHEELDOWNMOUSE"}:
            curr_val = self.current_lattice_axis_val
            if "DOWN" in et:
                setattr(self.lattice.data, f"points_{self.current_axis}", curr_val - 1)
            else:
                setattr(self.lattice.data, f"points_{self.current_axis}", curr_val + 1)
        elif et == "I" and e.value == "PRESS":
            self.cycle_interp_types()

        elif event.type == "LEFTMOUSE":
            self._clear_info(context)
            return {"FINISHED"}
        elif event.type in {"RIGHTMOUSE", "ESC"}:
            self._clear_info(context)
            remove_lattices(context, self.lattice)
            bpy.data.objects.remove(self.lattice)
            return {"CANCELLED"}
        return {"RUNNING_MODAL"}
