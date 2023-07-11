import bpy 
import bmesh
import bmesh_utils as bmu
from custom_operator import *

def main(context):
    C = context
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmu.get_bmesh(C)
    edges = set()
    verts = set()

    for edge in bm.edges[:]:
        if edge.select:
            edges.add(edge)
            for vert in edge.verts[:]:
                verts.add(vert)

    ret = bmesh.ops.subdivide_edges(bm, edges=list(edges), cuts=1)
    inner = ret['geom_inner']
    sd_edges = [edge for edge in inner if isinstance(edge, bmesh.types.BMEdge)]
    bmesh.ops.collapse(bm, edges=sd_edges, uvs=True)
    bmesh.update_edit_mesh(C.object.data,)

class MESH_OT_collapse_edges_to_vert(CustomOperator, bpy.types.Operator):
    bl_idname = "mesh.collapse_edges_to_vert"
    bl_label = "Collapse Edges to Vert"

    @classmethod
    def poll(cls, context):
        return cls.edit_obj_poll(context)

    def execute(self, context):
        main(context)
        return {"FINISHED"}

