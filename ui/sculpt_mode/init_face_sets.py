
from bpy.types import Menu

class PIE_MT_init_face_sets(Menu):
    bl_label = "Init Face Sets"
    bl_idname = "PIE_MT_init_face_sets"
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        op = pie.operator("sculpt.face_sets_init", text='Loose Parts', icon="OUTLINER_DATA_POINTCLOUD")
        op.mode = 'LOOSE_PARTS'
        op = pie.operator("sculpt.face_sets_init", text='Face Set Boundaries', icon="PIVOT_BOUNDBOX")
        op.mode = 'FACE_SET_BOUNDARIES'
        op = pie.operator("sculpt.face_sets_init", text='Materials', icon="MATERIAL")
        op.mode = 'MATERIALS'
        op = pie.operator("sculpt.face_sets_init", text='Normals', icon="NORMALS_VERTEX_FACE")
        op.mode = 'NORMALS'
        op = pie.operator("sculpt.face_sets_init", text='UV Seams', icon="UV_EDGESEL")
        op.mode = 'UV_SEAMS'
        op = pie.operator("sculpt.face_sets_init", text='Edge Creases', icon="EDGESEL")
        op.mode = 'CREASES'
        op = pie.operator("sculpt.face_sets_init", text='Edge Bevel Weight', icon="MOD_BEVEL")
        op.mode = 'BEVEL_WEIGHT'
        op = pie.operator("sculpt.face_sets_init", text='Sharp Edges', icon="SHARPCURVE")
        op.mode = 'SHARP_EDGES'

kms = [
     {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Sculpt",
        "letter": "ONE",
        "shift": 0,
        "ctrl": 0,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_init_face_sets.bl_idname},
    },
]