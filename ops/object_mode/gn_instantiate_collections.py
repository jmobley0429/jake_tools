from bpy.types import Operator
from custom_operator import *
import utils


ASSET_BLEND_FILE = r"G:\PONLocal\blender\blender_assets\Assets.blend"

D = bpy.data
gn_name = "InstanceCollection"


def get_node_group():
    if gn_name not in bpy.data.node_groups:
        return utils.append_node_group(ASSET_BLEND_FILE, gn_name)
    return bpy.data.node_groups[gn_name]

def get_existing_inst_colls(dest_coll):
    colls = set()
    for obj in dest_coll.objects[:]:
        for mod in obj.modifiers[:]:
            if mod.type == "NODES":
                if mod.node_group.name == "InstanceCollection":
                    coll = mod['Input_2']
                    colls.add(coll)
                    break
    return colls

   

def instantiate_child_collections(context, update=True):
    to_coll = context.scene.instantiate_colls_dest
    existing_colls = get_existing_inst_colls(to_coll)
    from_coll = context.collection
    node_group = get_node_group()

    for coll in from_coll.children[:]:
        if coll not in existing_colls and update:
            mesh = bpy.data.meshes.new(coll.name)
            obj = bpy.data.objects.new(coll.name, mesh)
            to_coll.objects.link(obj)
            gn = obj.modifiers.new("Instance", type="NODES")
            gn.node_group = node_group
            gn["Input_2"] = coll



class OBJECT_OT_gn_instantiate_collections(CustomOperator, Operator):
    bl_idname = "object.gn_instantiate_collections"
    bl_label = "Instantiate Child Collections"
    bl_options = {"REGISTER", "UNDO"}

    update: bpy.props.BoolProperty(name="Update Only", default=True)


    @classmethod
    def poll(cls, context):
        return context.collection is not None
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        instantiate_child_collections(context, update=self.update)
        return {"FINISHED"}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Destination Collection")
        row = col.row()
        row.prop(context.scene, 'instantiate_colls_dest')



def gn_instantiate_collections_menu_func(self, context):
    layout = self.layout
    layout.operator("object.gn_instantiate_collections")


def register():
    bpy.types.Scene.instantiate_colls_dest = bpy.props.PointerProperty(
        type=bpy.types.Collection,
        name="To Coll",
    )


def unregister():
    del bpy.types.Scene.instantiate_colls_dest
