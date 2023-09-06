#node_editor
import bpy

class NODE_OT_directional_node_align(bpy.types.Operator):
    bl_idname = "node.directional_align"
    bl_label = "Align Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    direction: bpy.props.EnumProperty(
        items=(
            ("TOP", "Top", "Top"),
            ("BOTTOM", "Bottom", "Bottom"),
            ("LEFT", "Left", "Left"),
            ("RIGHT", "Right", "Right"),
        ),
        name='Direction',
        description='Direction to align on.',
        default=None,
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == "NODE_EDITOR" and bool(context.selected_nodes)

    def execute(self, context):
        sel_nodes = context.selected_nodes
        axis = "y" if self.direction in {"TOP", "BOTTOM"} else "x"
        min_max_func = min if self.direction in {"LEFT", "BOTTOM"} else max
        loc = min_max_func([getattr(node.location, axis) for node in sel_nodes])
        for node in sel_nodes:
            setattr(node.location, axis, loc)
        return {'FINISHED'}
    
kms = [
    {
        "keymap_operator": "node.directional_align",
        "name": "Node Editor",
        "letter": "W",
        "shift": 1,
        "ctrl": 0,
        "alt": 1,
        "space_type": "NODE_EDITOR",
        "region_type": "WINDOW",
        "keywords": {"direction": "TOP"},
    },
    {
        "keymap_operator": "node.directional_align",
        "name": "Node Editor",
        "letter": "S",
        "shift": 1,
        "ctrl": 0,
        "alt": 1,
        "space_type": "NODE_EDITOR",
        "region_type": "WINDOW",
        "keywords": {"direction": "BOTTOM"},
    },
    {
        "keymap_operator": "node.directional_align",
        "name": "Node Editor",
        "letter": "D",
        "shift": 1,
        "ctrl": 0,
        "alt": 1,
        "space_type": "NODE_EDITOR",
        "region_type": "WINDOW",
        "keywords": {"direction": "RIGHT"},
    },
    {
        "keymap_operator": "node.directional_align",
        "name": "Node Editor",
        "letter": "A",
        "shift": 1,
        "ctrl": 0,
        "alt": 1,
        "space_type": "NODE_EDITOR",
        "region_type": "WINDOW",
        "keywords": {"direction": "LEFT"},
    },
]
