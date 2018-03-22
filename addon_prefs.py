import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

class SmartConfig_AddonPrefs(bpy.types.AddonPreferences):
    bl_idname = addon_name
    
    exception_list = bpy.props.StringProperty(name='Addons to exclude', default='', description='Addon Modules to exclude separated with a comma')
    errors_report = bpy.props.BoolProperty(name='Create Error Report on export', default=True, description='Create a text file with problematic addons in case of error on the export')
        
    def draw(self, context):
        layout = self.layout
        row=layout.row()
        row.prop(self, "exception_list")
        row=layout.row()
        row.prop(self, "errors_report")

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.user_preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)