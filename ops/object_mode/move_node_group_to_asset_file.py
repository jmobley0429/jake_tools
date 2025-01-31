import bpy
import os

ASSET_BLENDFILE = os.path.expandvars(
    r"%PON_ARTSOURCE_DIR%\Scripts\TemplateFiles\Assets\NodeGroups.blend"
)


def get_node_group(scene):
    ng_prop = scene.make_node_asset_ng
    ng_index = scene.make_node_asset_ng_active_index
    ng_name = ng_prop[ng_index].node_group_name
    return bpy.data.node_groups[ng_name]


def main(context):
    scene = context.scene
    ng = get_node_group(scene)
    with bpy.data.libraries.load(ASSET_BLENDFILE) as (data_from, data_to):
        data_to.node_groups.append(ng)


class JAKETOOLS_send_node_group_to_asset_file(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "jake_tools.send_node_group_to_asset_file"
    bl_label = "Make Asset Node Group"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        main(context)
        return {"FINISHED"}
