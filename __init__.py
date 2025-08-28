bl_info = {
    "name": "Jake Tools (MPM Refactor)",
    "author": "Jake Mobley",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Object Mode",
    "description": "Collection of tools for my Workflow",
    "warning": "",
    "doc_url": "",
    "category": "Tools",
}

import bpy
import utils
from pathlib import Path
from import_utils import Importer


ROOT_DIR = Path(__file__).parent

importer = Importer(ROOT_DIR)
imported_modules = importer.import_modules()
classes = list(importer.get_classes(imported_modules))

addon_keymaps = []


def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            print(f"Error registering: {cls}")
    for mod in imported_modules:
        if hasattr(mod, "register"):
            mod.register()
        if hasattr(mod, "kms"):
            utils.register_keymaps(mod.kms, addon_keymaps)


def unregister():
    utils.unregister_keymaps(addon_keymaps)
    for mod in reversed(list(imported_modules)):
        if hasattr(mod, "register"):
            mod.unregister()
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            print(cls)
