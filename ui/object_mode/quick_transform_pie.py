import bpy
from bpy.types import Menu


class OBJECT_MT_quick_transform_pie(Menu):
    bl_idname = "OBJECT_MT_quick_transform_pie"
    bl_label = "Quick Transform"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        box = pie.box()
        val = 90
        box.label(text=f"Rotate {val}")
        spl = box.split()
        op = spl.operator("object.quick_transform", text="X")
        op.axis = "X"
        op.transform_type = "Rotation"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Y")
        op.axis = "Y"
        op.transform_type = "Rotation"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Z")
        op.axis = "Z"
        op.transform_type = "Rotation"
        op.transform_amt = val

        box = pie.box()
        val = 22.5
        box.label(text=f"Rotate {val}")
        spl = box.split()
        op = spl.operator("object.quick_transform", text="X")
        op.axis = "X"
        op.transform_type = "Rotation"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Y")
        op.axis = "Y"
        op.transform_type = "Rotation"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Z")
        op.axis = "Z"
        op.transform_type = "Rotation"
        op.transform_amt = val

        box = pie.box()
        val = 45
        box.label(text=f"Rotate {val}")
        spl = box.split()
        op = spl.operator("object.quick_transform", text="X")
        op.axis = "X"
        op.transform_type = "Rotation"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Y")
        op.axis = "Y"
        op.transform_type = "Rotation"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Z")
        op.axis = "Z"
        op.transform_type = "Rotation"
        op.transform_amt = val

        box = pie.box()
        val = 180
        box.label(text=f"Rotate {val}")
        spl = box.split()
        op = spl.operator("object.quick_transform", text="X")
        op.axis = "X"
        op.transform_type = "Rotation"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Y")
        op.axis = "Y"
        op.transform_type = "Rotation"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Z")
        op.axis = "Z"
        op.transform_type = "Rotation"
        op.transform_amt = val

        # SCALE
        box = pie.box()
        val = 2
        box.label(text=f"Scale {val}x")
        row = box.row()
        op = row.operator("object.quick_transform", text="All")
        op.transform_amt = val
        op.axis = "ALL"
        op.transform_type = "Scale"
        row = box.row()
        spl = row.split()
        op = spl.operator("object.quick_transform", text="X")
        op.axis = "X"
        op.transform_type = "Scale"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Y")
        op.axis = "Y"
        op.transform_type = "Scale"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Z")
        op.axis = "Z"
        op.transform_type = "Scale"
        op.transform_amt = val

        # SCALE
        box = pie.box()
        val = 10
        box.label(text=f"Scale {val}x")
        row = box.row()
        op = row.operator("object.quick_transform", text="All")
        op.transform_amt = val
        op.axis = "ALL"
        op.transform_type = "Scale"
        row = box.row()
        spl = row.split()
        op = spl.operator("object.quick_transform", text="X")
        op.axis = "X"
        op.transform_type = "Scale"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Y")
        op.axis = "Y"
        op.transform_type = "Scale"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Z")
        op.axis = "Z"
        op.transform_type = "Scale"
        op.transform_amt = val
        # SCALE
        box = pie.box()
        val = 5
        box.label(text=f"Scale {val}x")
        box.scale_y *= 0.9
        row = box.row()
        op = row.operator("object.quick_transform", text="All")
        op.transform_amt = val
        op.axis = "ALL"
        op.transform_type = "Scale"
        row = box.row()
        spl = row.split()
        op = spl.operator("object.quick_transform", text="X")
        op.axis = "X"
        op.transform_type = "Scale"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Y")
        op.axis = "Y"
        op.transform_type = "Scale"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Z")
        op.axis = "Z"
        op.transform_type = "Scale"
        op.transform_amt = val
        box = pie.box()
        val = 4
        box.label(text=f"Scale {val}x")
        row = box.row()
        op = row.operator("object.quick_transform", text="All")
        op.transform_amt = val
        op.axis = "ALL"
        op.transform_type = "Scale"
        row = box.row()
        spl = row.split()
        op = spl.operator("object.quick_transform", text="X")
        op.axis = "X"
        op.transform_type = "Scale"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Y")
        op.axis = "Y"
        op.transform_type = "Scale"
        op.transform_amt = val
        op = spl.operator("object.quick_transform", text="Z")
        op.axis = "Z"
        op.transform_type = "Scale"
        op.transform_amt = val




kms = [
    
]