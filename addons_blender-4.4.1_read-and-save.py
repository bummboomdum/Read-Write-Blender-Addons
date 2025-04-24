import bpy
import csv
import os
from typing import Dict, Any

'''
Made with DeepSeek (other does not can do it)
Checked with Blender 4.4.1 ...
'''

def get_addon_info(addon) -> Dict[str, Any]:
    """Sicher bl_info-Daten extrahieren mit Fallbacks"""
    try:
        return getattr(addon, "bl_info", {})
    except Exception:
        return {}

csv_path = os.path.join(os.path.expanduser("~"), "Desktop", "blender_addons.csv")

with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Version", "Author", "Description", "Enabled", "Module"])
    
    # 1. Aktive Addons (aus Preferences)
    for addon_name, addon in bpy.context.preferences.addons.items():
        bl_info = get_addon_info(addon)
        
        writer.writerow([
            bl_info.get("name", addon_name),
            ".".join(map(str, bl_info.get("version", (0, 0, 0)))),
            bl_info.get("author", "N/A"),
            bl_info.get("description", "No description"),
            True,  # Aktiv
            addon_name
        ])
    
    # 2. Inaktive aber verfügbare Addons (über addon_utils)
    try:
        import addon_utils
        for mod in addon_utils.modules():
            if mod.__name__ not in bpy.context.preferences.addons:
                bl_info = getattr(mod, "bl_info", {})
                writer.writerow([
                    bl_info.get("name", mod.__name__),
                    ".".join(map(str, bl_info.get("version", (0, 0, 0)))),
                    bl_info.get("author", "N/A"),
                    bl_info.get("description", "No description"),
                    False,  # Inaktiv
                    mod.__name__
                ])
    except ImportError:
        pass

print(f"✅ Erfolg! Addons gespeichert unter: {csv_path}")