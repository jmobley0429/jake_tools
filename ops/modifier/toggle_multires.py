import bpy
from bpy.types import Operator
from custom_operator import *

def toggle_multires(context, args):
    highest = args.pop("highest")
    for obj in context.selected_objects[:]:
        if obj.type == "MESH":
            for mod in obj.modifiers[:]:
                if mod.type == "MULTIRES":
                    if highest:
                        mod.levels = mod.total_levels
                    else:
                        mod.levels = 0


class OBJECT_OT_toggle_multires(Operator):
    bl_idname = "object.toggle_multires"
    bl_label = "Toggle Multires"
    bl_options = {"REGISTER", "UNDO"}

    highest: bpy.props.BoolProperty(name="All to Highest", default=False)

    def execute(self, context):
        args = self.as_keywords()
        toggle_multires(context, args)
        return {"FINISHED"}
    
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


