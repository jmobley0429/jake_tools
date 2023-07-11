import bpy
from custom_operator import *


class SMObjectNamer(OperatorBaseClass):
    def __init__(self, context, args=None, op=None, index=None, root_obj=None):
        super().__init__(context, args=args, op=op)
        self.index = index
        self.parent = root_obj
        self.current_object = None

    def _get_num_suffix(self, index):
        if len(self.context.selected_objects[:]) < 2:
            if self.current_object is None:
                return ''
        return str(index + 1).zfill(2)

    @property
    def _child_objects(self):
        return [obj for obj in self.parent.children_recursive]

    def get_name(self, obj, index):
        if obj == self.parent:
            name = self.name_str
        else:
            name = f"{self.name_str}_{self._get_num_suffix(self.index)}"
        return index, name

    def format_name(self, i, name):
        prefix = "SM"
        if "SM_" in name:
            name = name.replace("SM_", '')
        suffix = self._get_num_suffix(i)
        new_name = "_".join([prefix, name, suffix]).rstrip("_")
        return new_name

    @staticmethod
    def _is_collision_mesh(obj):
        coll = obj.users_collection[0].name.lower()
        name = obj.name 
        dt = obj.display_type
        return any(
            [
               'collision' in coll,
               "UCX" in name,
               dt == "WIRE" 
            ]
        )

    def rename_objs(self):
        i, name = self.get_name(self.parent, self.index)
        self.parent.name = self.format_name(i, name)
        for i, obj in enumerate(self._child_objects[:]):
            self.current_object = obj
            if self._is_collision_mesh(obj):
                continue
            _, name = self.get_name(obj, i)
            obj.name = self.format_name(i, name)


class OBJECT_OT_NameStaticMeshGrouping(bpy.types.Operator):
    bl_idname = "object.name_static_mesh_grouping"
    bl_label = "Name Static Mesh Grouping"
    bl_options = {"REGISTER", "UNDO"}

    name_str: bpy.props.StringProperty(name="")
    orig_name = ""

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        objs = context.selected_objects[:]
        for obj in objs:
            obj.name == "__TEMP__rename"
        for i, obj in enumerate(objs):
            args = self.as_keywords()
            SMNamer = SMObjectNamer(context, args=args, op=self, index=i, root_obj=obj)
            SMNamer.rename_objs()
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        icon = "OBJECT_DATAMODE"
        box = layout
        row = box.row()
        row.label(text='Static Mesh Name')
        row = box.row()
        row.activate_init = True
        prop = row.prop(self, "name_str",  icon=icon, )