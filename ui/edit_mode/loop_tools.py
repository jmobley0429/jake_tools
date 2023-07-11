import bpy
from bpy.types import Menu

class MESH_MT_PIE_loop_tools(Menu):
    bl_label = "Loop Tools"
    bl_idname = "MESH_MT_PIE_loop_tools"
    bl_options = {"REGISTER", "UNDO"}

    

    def draw(self, context):
        layout = self.layout
        context.window_manager.looptools.gstretch_use_guide = "Annotation"
        pie = layout.menu_pie()
        op = pie.operator("mesh.looptools_bridge")
        op = pie.operator("mesh.looptools_circle")
        op = pie.operator("mesh.looptools_curve")
        op = pie.operator("mesh.looptools_flatten")
        op = pie.operator("mesh.custom_gstretch")
        op = pie.operator("mesh.looptools_relax")
        op = pie.operator("mesh.looptools_space")

kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Mesh",
        "letter": "ONE",
        "shift": False,
        "ctrl": False,
        "alt": True,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": MESH_MT_PIE_loop_tools.bl_idname},
    }
]