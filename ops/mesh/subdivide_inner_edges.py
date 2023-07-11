import bpy
import bmesh
import bmesh_utils as bmu
from bpy.types import Operator
from custom_operator import *


def subdivide_inner_edges(context):
    obj = context.edit_object
    mesh = obj.data
    bm = bmesh.from_edit_mesh(mesh)
    sel_edges = bmu.get_sel_edges(bm)
    subdiv_edges = []

    for edge in sel_edges:
        edge.select_set(False)
        if bmu.is_interior(edge) or edge.is_boundary:
            subdiv_edges.append(edge)

    ret = bmesh.ops.subdivide_edges(bm, edges=subdiv_edges, cuts=1)
    for geo in ret["geom_inner"]:
        if isinstance(geo, bmesh.types.BMEdge):
            geo.select_set(True)
    bm.select_flush(True)
    bmesh.update_edit_mesh(mesh)
    bm.free()
    del bm


class MESH_OT_subdivide_inner_edges(CustomOperator, bpy.types.Operator):
    bl_idname = "mesh.subdivide_inner_edges"
    bl_label = "Subdivide Inner Edges"

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        subdivide_inner_edges(context)
        return {"FINISHED"}
