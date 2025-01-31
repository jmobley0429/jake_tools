import bpy
from bpy.types import Menu


class OBJECT_MT_instance_collection_tools(Menu):
    bl_label = "Instance Tools"
    bl_idname = "OBJECT_MT_instance_collection_tools"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # Naming tools
        col = pie.column()
        row = col.row()
        row.operator("object.transfer_instance_name_to_object")
        row = col.row()
        row.operator("object.camel_caseify_names")
        row = col.row()
        row.operator("object.assign_lofted_edge_mat")

        # bool tools
        col = pie.column()
        row = col.row()
        row.operator("object.move_bool_objects_to_coll")
        row = col.row()
        row.operator("modifier.set_bool_obj_visibility")
        row = col.row()
        row.operator("modifier.set_bool_options")
        row = col.row()

        # disable child
        pie.operator("object.disable_child_instances", text="Disable Child Instances")

        pie.operator(
            "object.show_gn_instance_root_collection",
            text="Show Root Collection",
        )

        pie.operator(
            "object.move_parent_groups_to_component_collection",
            text="Bundles to Component",
        )

        ##

        pie.operator(
            "object.move_selected_to_active_object_coll",
            text="Move Selected to Active's Coll",
        )
        ##


kms = [
    {
        "keymap_operator": "wm.call_menu_pie",
        "name": "Object Mode",
        "letter": "FOUR",
        "shift": 0,
        "ctrl": 1,
        "alt": 1,
        "space_type": "VIEW_3D",
        "region_type": "WINDOW",
        "keywords": {"name": OBJECT_MT_instance_collection_tools.bl_idname},
    }
]
