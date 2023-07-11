import bpy

class MyPieMenuProps(bpy.types.PropertyGroup):
    custom_vertex_color: bpy.props.FloatVectorProperty(name="Custom Vertex Color", size=4, min=0.0, max=1.0, subtype="COLOR")



def register():
    bpy.types.Scene.mpm_props = bpy.props.PointerProperty(type=MyPieMenuProps)

def unregister():
    del bpy.types.Scene.mpm_props


