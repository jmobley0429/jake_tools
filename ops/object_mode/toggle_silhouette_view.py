import bpy 

class ShadingViewProperties(bpy.types.PropertyGroup):
    light: bpy.props.StringProperty(name="light_mode", default="STUDIO")
    color_type: bpy.props.StringProperty(name="light_mode", default="MATERIAL")
    single_color: bpy.props.FloatVectorProperty(name='single_color', default=(0,0,0))
    background_type: bpy.props.StringProperty(name="background_type", default="THEME")
    background_color: bpy.props.FloatVectorProperty(name='single_color', default=(.9,.9,.9,))


class ShadingObject:
    VIEW_ATTRS = [
        "light",
        "color_type",
        "single_color",
        "background_type",
        "background_color",
        ]
    
    SILHOUETTE_VIEW_ATTRS = [
            'FLAT',  
            'SINGLE',
            (0, 0, 0),
            "VIEWPORT",
            (1,1,1),
            ]

    def __init__(self, context):
        self.context = context
        
    def set_current_shading(self):
        for curr_attr in self.VIEW_ATTRS:
            self.current_shading.append(getattr(self.context, curr_attr))

    def toggle_silhouette_view(self, context):
        shading = context.space_data.shading
        view_properties = context.scene.shading_view_properties
        for attr, set_attr in zip(self.VIEW_ATTRS, self.SILHOUETTE_VIEW_ATTRS):
            current_attr = getattr(shading, attr)
            if current_attr != set_attr:
                setattr(view_properties, attr, current_attr)
                setattr(shading, attr, set_attr)
            else:
                reset_attr = getattr(view_properties, attr)
                try:
                    setattr(shading, attr, reset_attr)
                except AttributeError:
                    continue
        
        overlays_enabled = context.space_data.overlay.show_overlays
        context.space_data.overlay.show_overlays = not overlays_enabled



class VIEW3D_OT_toggle_silhouette_view(bpy.types.Operator):
    bl_idname = "view.toggle_silhouette_view"
    bl_label = "Toggle Silhouette View"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        ts = ShadingObject(context)
        ts.toggle_silhouette_view(context)
        return {"FINISHED"}
    
    
def register():
    bpy.types.Scene.shading_view_properties = bpy.props.PointerProperty(type=ShadingViewProperties)

def unregister():
    del bpy.types.Scene.shading_view_properties

