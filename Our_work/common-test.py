"""import importlib
common = input('common:')
importlib.import_module(common)

uboot_overlay_enabled()
"""
import common as common
common.uboot_overlay_enabled()
common.load_device_tree("P9_31")
print(common.device_tree_loaded("P9_31"))
common.unload_device_tree("P9_31")
print(common.device_tree_loaded("P9_31"))
