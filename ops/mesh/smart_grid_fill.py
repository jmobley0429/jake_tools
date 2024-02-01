# edit_mode

import bpy
import bmesh
from bpy.types import Operator
from custom_operator import *


def get_bm(context):
    obj = context.edit_object
    mesh = obj.data
    bm = bmesh.from_edit_mesh(mesh)
    return bm


def has_sel_faces(context):
    bm = get_bm(context)
    sel_faces = bool(get_selected(bm, "faces"))
    bm.free()
    del bm
    return sel_faces


def get_selected(mesh, elem_type):
    return [elem for elem in getattr(mesh, elem_type)[:] if elem.select]


def get_face_edges(bm, face):
    edges = [edge.index for edge in face.edges[:]]
    ret = [edge for edge in bm.edges[:] if edge.index in edges]
    return ret


# def dissolve_faces(bm, faces):

#     return ret["faces"]


def smart_grid_fill(context, args):
    span = args.pop("span")
    offset = args.pop("offset")
    obj = context.edit_object
    bm = get_bm(context)
    sel_faces = get_selected(bm, "faces")
    if sel_faces:
        if len(sel_faces) > 1:
            ret = bmesh.ops.dissolve_faces(bm, faces=sel_faces)
            print(bm)
            print(ret)
            face = ret["region"][0]
        else:
            face = sel_faces[0]
        face_edges = get_face_edges(bm, face)
        bm.faces.remove(face)
        for edge in face_edges[:]:
            edge.select_set(True)
        bm.select_flush(True)
        bmesh.update_edit_mesh(obj.data)
    bpy.ops.mesh.fill_grid("INVOKE_DEFAULT", span=span, offset=offset)


class MESH_OT_smart_grid_fill(Operator):
    bl_idname = "mesh.smart_grid_fill"
    bl_label = "Grid Fill"
    bl_options = {"REGISTER", "UNDO"}

    span: bpy.props.IntProperty(default=1, name="Span")
    offset: bpy.props.IntProperty(default=0, name="Offset")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and "EDIT" in context.mode

    def execute(self, context):
        args = self.as_keywords()
        smart_grid_fill(context, args)
        return {"FINISHED"}
