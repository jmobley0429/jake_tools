# edit_mode

import bmesh
from bpy.types import Operator
from custom_operator import *


class SmartVertsJoiner(EditModeOperatorBaseClass):
    def __init__(self, context, args, op):
        super().__init__(context, args, op)
        self.bmesh(context)
        self.sel_verts = []
        self.active_vert = None

    def _set_verts_selection(self):
        for v in self.bm.verts[:]:
            if v.select and v not in self.sel_verts:
                self.sel_verts.append(v)
        self.active_vert = self.bm.select_history.active

    @property
    def _non_active(self):
        return [vert for vert in self.sel_verts if vert != self.active_vert]

    @property
    def _one_edge(self):
        return len(self.sel_verts) == 2

    def join_verts(self):
        self._set_verts_selection()
        if not self.active_vert and not self._one_edge:
            self.op.report({"ERROR"}, "At least one vert must be active.")
            return {"CANCELLED"}
        if self._one_edge:
            bmesh.ops.connect_vert_pair(self.bm, verts=self.sel_verts)
        else:
            for vert in self._non_active[:]:
                pair = [vert, self.active_vert]
                bmesh.ops.connect_vert_pair(self.bm, verts=pair)
        bmesh.update_edit_mesh(self.mesh)
        self.bm.free()
        return {"FINISHED"}


class MESH_OT_smart_join_verts(CustomBmeshOperator, Operator):
    bl_idname = "mesh.smart_join_verts"
    bl_label = "Smart Join Verts"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        active_obj = context.active_object
        tools = context.scene.tool_settings.mesh_select_mode[:]
        in_vert_select = tools[0] == True and not all(tools[1:])
        return (
            active_obj is not None
            and "EDIT" in context.mode
            and active_obj.type == "MESH"
            and in_vert_select
        )

    def execute(self, context):
        svj = SmartVertsJoiner(context, self.as_keywords(), self)
        return svj.join_verts()
