# edit_mode
import bpy
import bmesh
import numpy as np
from bpy.types import Operator
from custom_operator import *


class EdgeWeightSetter(CustomBmeshOperator):
    def __init__(self, context, args):
        self.obj = context.edit_object
        self.mesh = context.edit_object.data
        self._set_args(args)
        self.bm = bmesh.from_edit_mesh(self.mesh)
        self.context = context
        self.clear = None

    def update_mesh(self):
        bmesh.update_edit_mesh(self.mesh)

    @property
    def sharp_angle(self):
        return np.radians(self.sharpness)

    def _set_args(self, args):
        for key, val in args.items():
            setattr(self, key, val)

    def _set_clear(self, event):
        if event.alt:
            self.clear = True
        elif event.ctrl:
            self.clear = False

    def verify_weight_layer(self):
        layer_names = {
            "BEVEL": "bevel_weight_edge",
            "CREASE": "crease_edge",
        }
        layer_name = layer_names[self.weight_type]
        if layer_name not in self.mesh.attributes:
            self.mesh.attributes.new(layer_name, "FLOAT", "EDGE")
        self.weight_layer = self.bm.edges.layers.float.get(layer_name)

    def set_edge_weight(self, edge):
        if self.clear is not None:
            val = self.clear
        else:
            val = not edge[self.weight_layer]
        edge[self.weight_layer] = float(val)

    def set_edges_weight(self):
        self.verify_weight_layer()
        print(self.weight_layer)
        for edge in self.sel_edges:
            self.set_edge_weight(edge)
            # try:
            #     self.set_edge_weight(edge)
            # except ReferenceError:
            #     self.bmesh(self.context)
            #     self.set_edges_weight(self)
        self.update_mesh()

    def set_sharp_to_weighted(self):
        obj = self.get_active_obj()
        stored_edges = [e for e in self.sel_edges]
        self.select_edges(self.context, self.bm.edges[:], select=False)
        self.select_sharp_edges(threshold=self.sharp_angle)
        self.verify_weight_layer()
        self.set_edges_weight()
        if stored_edges:
            self.select_edges(self.context, self.bm.edges[:], select=False)
            self.select_edges(self.context, stored_edges, select=True)
        bmesh.update_edit_mesh(self.context.edit_object.data)

    def set_boundary_to_weighted(self):
        obj = self.get_active_obj()
        stored_edges = [e for e in self.sel_edges]
        self.select_edges(
            self.context,
            self.bm.edges[:],
            select=False,
            skip_callback_func=self.is_boundary_edge,
        )
        self.verify_weight_layer()
        self.set_edges_weight()
        # # self.bmesh(self.context)
        # if stored_edges:
        #     self.select_edges(self.context, self.bm.edges[:], select=False)
        #     self.select_edges(self.context, stored_edges, select=True)
        self.update_mesh()


desc_vals = [
    "Set edge weight on selected edges. Default toggle all selected edges to opposite value.",
    "CTRL - Clear all edges.",
    "ALT - Set all edges weight to 1",
]


class MESH_OT_toggle_edge_weight(CustomBmeshOperator, Operator):
    bl_idname = "mesh.toggle_edge_weight"
    bl_label = "Set Edge Weight"

    bl_description = "\n".join(desc_vals)
    bl_options = {"REGISTER", "UNDO"}

    weight_type: bpy.props.StringProperty(name="Weight Type")

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def invoke(self, context, event):
        args = self.as_keywords()
        self.edge_weight_setter = EdgeWeightSetter(context, args)
        self.edge_weight_setter._set_clear(event)
        return self.execute(context)

    def execute(self, context):
        ews = self.edge_weight_setter
        ews.set_edges_weight()

        return {"FINISHED"}


class MESH_OT_set_sharp_to_weighted(CustomBmeshOperator, Operator):
    bl_idname = "mesh.set_sharp_to_weighted"
    bl_label = "Sharp To Weighted"
    bl_options = {"REGISTER", "UNDO"}

    weight_type: bpy.props.StringProperty(name="Weight Type", default="BEVEL")
    sharpness: bpy.props.IntProperty(name="Sharpness", default=30)

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def invoke(self, context, event):
        return self.execute(context)

    def execute(self, context):
        args = self.as_keywords()
        ews = EdgeWeightSetter(context, args)
        ews.set_sharp_to_weighted()
        return {"FINISHED"}


class MESH_OT_set_boundary_to_weighted(CustomBmeshOperator, Operator):
    bl_idname = "mesh.set_boundary_to_weighted"
    bl_label = "Boundary To Weighted"
    bl_options = {"REGISTER", "UNDO"}

    weight_type: bpy.props.StringProperty(name="Weight Type", default="BEVEL")

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        ews = EdgeWeightSetter(context, self.as_keywords())
        ews.set_boundary_to_weighted()
        return {"FINISHED"}
