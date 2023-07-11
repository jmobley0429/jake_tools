import bpy
from bpy.types import Operator


class SetCustomBatchName(Operator):
    bl_idname = "object.set_custom_batch_name"
    bl_label = "Set Custom Batch Name"

    name_string: bpy.props.StringProperty(name="New Name")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        active_obj = context.active_object
        objs = list(set(context.selected_objects) - set([active_obj]))
        objs.insert(0, active_obj)
        for i, obj in enumerate(objs[:]):
            if obj.name == self.name_string:
                obj.name = "__temp__"
        for i, obj in enumerate(objs):
            new_name = f"{self.name_string}_{str(i+1).zfill(2)}"
            obj.name = new_name
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        # Edit first editable button in popup
        def row_with_icon(layout, icon):
            row = layout.row()
            row.activate_init = True
            row.label(icon=icon)
            return row

        mode = context.mode
        row = row_with_icon(layout, "OBJECT_DATAMODE")
        row.prop(self, "name_string")