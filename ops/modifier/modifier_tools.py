#modifier

import bpy
import numpy as np
from bpy.types import Operator
from custom_operator import *

class ToggleClipping(Operator):
    bl_idname = "object.toggle_mirror_clipping"
    bl_label = "Toggle Clipping"
    bl_description = "Toggles Clipping on Any Mirror Modifiers"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        mods = [mod for mod in obj.modifiers[:] if mod.type == "MIRROR"]
        if mods:
            for mod in mods:
                clip_state = mod.use_clip
                mod.use_clip = not clip_state
        return {"FINISHED"}
    
class ToggleSubDivVisibility(Operator):
    bl_idname = "object.toggle_subdiv_vis"
    bl_label = "Toggle SubDiv Vis"
    bl_description = "Toggles Subdiv Visibility"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        self.sel_objs = context.selected_objects
        self.show_viewport = self.min_subsurf_visibility

        return self.execute(context)

    @property
    def ss_objs(self):
        objs = []
        for obj in self.sel_objs:
            mods = [mod.type for mod in obj.modifiers[:]]
            if "SUBSURF" in mods:
                objs.append(obj)
        return objs

    def is_visible(self, obj):
        for mod in obj.modifiers[:]:
            if mod.type == "SUBSURF":
                return mod.show_viewport

    @property
    def min_subsurf_visibility(self):
        status = [self.is_visible(obj) for obj in self.ss_objs]
        return min(status)

    def toggle_subsurf(self, obj):
        mods = [mod for mod in obj.modifiers[:] if mod.type == "SUBSURF"]
        if mods:
            for mod in mods:
                visible = mod.show_viewport
                mod.show_viewport = not self.show_viewport

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for obj in self.ss_objs:
            self.toggle_subsurf(obj)

        return {"FINISHED"}
    
# def menu_func(self, context):
#     layout = self.layout
#     if context.active_object:
#         if len(context.active_object.modifiers):
#             col = self.layout.column(align=True)
#             row = col.row(align=True)
#             row.operator(ToggleClipping.bl_idname, icon='MOD_MIRROR', text="Toggle Clipping")
#             row.operator(ToggleSubDivVisibility.bl_idname, icon='MOD_SUBSURF', text="Toggle SubSurf Vis")

def deselect_modifier_panel_ops(self, context):
    layout = self.layout
    col = layout.column(align=True)
    row = col.row(align=True)
    row.operator("object.toggle_subdiv_vis")
    row.operator("object.toggle_mirror_clipping")
    row = col.row(align=True)
    op = row.operator(
        "object.toggle_multires",
        text="Multires to Lowest",
    )
    op.highest = False
    op = row.operator("object.toggle_multires", text="Multires to Highest")
    op.highest = True

def register():
    bpy.types.DATA_PT_modifiers.prepend(deselect_modifier_panel_ops)            

def unregister():
    bpy.types.DATA_PT_modifiers.remove(deselect_modifier_panel_ops)            