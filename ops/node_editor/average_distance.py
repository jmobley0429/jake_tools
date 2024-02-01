import bpy
from mathutils import Vector
import numpy as np


class NODE_OT_node_average_distance(bpy.types.Operator):
    bl_idname = "node.average_distance"
    bl_label = "Average Node Distance"
    bl_options = {"REGISTER", "UNDO"}

    @property
    def _num_nodes(self):
        return len(self.nodes)

    @property
    def _avg_node_dim(self):
        real_avg = np.mean(self.dims)
        return np.mean([real_avg * 1.1, max(self.dims)])

    @property
    def _avg_node_loc(self):
        return Vector((np.mean(self.x_locs), np.mean(self.y_locs)))

    @property
    def _space_between(self):
        return self._avg_node_dim * self.spacing_mult

    def _set_start_point(self):
        total_length = (self._avg_node_dim * self.spacing_mult) * (self._num_nodes + 1)
        self.start = self._avg_node_loc.x - total_length / 2
        self.end = self._avg_node_loc.x + total_length / 2

    def _set_new_locs(self):
        mult = 1
        current_loc = self._avg_node_loc
        y_avg = self._avg_node_loc.y
        range_locs = np.arange(
            self.start + self._avg_node_dim, self.end, self._space_between
        )

        locs = [Vector((loc, y_avg)) for loc in range_locs]
        i = 0
        for node, loc in zip(self.nodes, locs):
            node.location = loc

    @classmethod
    def poll(cls, context):
        print("Checking context")
        return context.area.type == "NODE_EDITOR"

    def invoke(self, context, event):
        self.spacing_mult = 1.2
        self.nodes = sorted(context.selected_nodes, key=lambda node: node.location.x)

        self.dims = np.array([node.dimensions.x for node in self.nodes])
        self.locs = np.array([node.location for node in self.nodes])
        self.x_locs, self.y_locs = zip(*self.locs)
        self._set_start_point()
        return self.execute(context)

    def execute(self, context):
        self._set_new_locs()
        return {"FINISHED"}


kms = [
    {
        "keymap_operator": "node.average_distance",
        "name": "Node Editor",
        "letter": "Q",
        "shift": 1,
        "ctrl": 0,
        "alt": 1,
        "space_type": "NODE_EDITOR",
        "region_type": "WINDOW",
        "keywords": {},
    },
]
