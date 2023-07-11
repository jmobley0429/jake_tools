from bpy.types import Menu


class PIE_MT_parent_object_pie(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Parent Objects"
    bl_idname = "PIE_MT_parent_object_pie"


    def draw(self, context):
        ao = context.active_object
        layout = self.layout
        pie = layout.menu_pie()
        op = pie.operator("object.parent_set",)
        op.type = 'OBJECT'
        op = pie.operator("object.parent_set", text="Make Parent (Keep Transforms)")
        op.type = 'OBJECT'
        op.keep_transform = True 
        op = pie.operator("object.parent_clear", text="Clear Parent (Keep Transforms)")
        op.type = 'CLEAR_KEEP_TRANSFORM'
        op = pie.operator("object.parent_clear", text="Clear Parent")
        op.type = 'CLEAR'
        op = pie.operator("object.parent_clear", text="Clear Parent (Inverse)")
        op.type = 'CLEAR_INVERSE'
        if ao.type == "CURVE":
            op = pie.operator("object.parent_set", text="Curve Deform")
            op.type = 'CURVE'
        if ao.type == "LATTICE":
            op = pie.operator("object.parent_set", text="Lattice Deform")
            op.type = 'LATTICE'

kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Object Mode",
        "letter": "TWO",
        "shift": 0,
        "ctrl": 1,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": PIE_MT_parent_object_pie.bl_idname},
    }
]