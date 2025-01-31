import bpy


def main(context):
    for ob in context.scene.objects:
        print(ob)


class OUTLINER_OT_set_sub_component_coll(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "collection.set_sub_component_coll"
    bl_label = "Set as Sub-Component Collection"

    is_subcomponent_coll: bpy.props.BoolProperty(
        name="Is Sub-Component Collection", default=True
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == "OUTLINER" and context.collection

    def execute(self, context):
        coll = context.collection
        try:
            is_sub_coll = coll["is_sub_coll"]
            coll["is_sub_coll"] = not is_sub_coll
        except KeyError:
            coll["is_sub_coll"] = self.is_subcomponent_coll

        if coll["is_sub_coll"]:
            self.report(
                {"INFO"}, f"Set collection: {context.collection.name} to Sub-Component!"
            )
            coll.color_tag = "COLOR_04"
        else:
            self.report(
                {"INFO"}, f"Set collection: {context.collection.name} to Component!"
            )
            coll.color_tag = "NONE"

        return {"FINISHED"}


kms = [
    {
        "keymap_operator": OUTLINER_OT_set_sub_component_coll.bl_idname,
        "name": "Outliner",
        "letter": "S",
        "shift": 0,
        "ctrl": 0,
        "alt": 1,
        "space_type": "OUTLINER",
        "region_type": "WINDOW",
        "keywords": {},
    }
]
