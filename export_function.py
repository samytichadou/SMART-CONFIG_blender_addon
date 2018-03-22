import bpy
import os
import sys
import shutil

from bpy_extras.io_utils import ExportHelper
from bpy.props import IntProperty, CollectionProperty , StringProperty , BoolProperty, EnumProperty

from .addon_prefs import get_addon_preferences
from .functions import update_progress_console, change_permissions_recursive

### Export Config Operator ###
class SmartConfig_Export(bpy.types.Operator, ExportHelper):
    bl_idname = "smartconfig.export_config"
    bl_label = "Export Configuration"
    filename_ext = ".sc"
    filter_glob = StringProperty(default="*.sc", options={'HIDDEN'})
    filepath = StringProperty(default="smart config")
    
    ##### prop #####
    include_startup_file = BoolProperty(
            name="Include Startup File",
            description="Include Blender Startup File in Export",
            default=False,
            )
    include_bookmarks = BoolProperty(
            name="Include Bookmarks File",
            description="Include Blender Bookmarks File in Export",
            default=False,
            )
    include_users_prefs = BoolProperty(
            name="Include User Preferences File",
            description="Include Blender User Preferences File in Export",
            default=False,
            )
    include_presets = BoolProperty(
            name="Include Preset Files",
            description="Include Blender Preset Files in Export",
            default=False,
            )
    include_config_folders = BoolProperty(
            name="Include Configuration Folders",
            description="Include Blender Configuration Folders in Export (some addons use these to save preferences...)",
            default=False,
            )
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label('Export Settings :', icon='SCRIPTWIN')
        box.prop(self, 'include_startup_file')
        box.prop(self, 'include_bookmarks')
        box.prop(self, 'include_users_prefs')
        box.prop(self, 'include_presets')
        box.prop(self, 'include_config_folders')
    
    def execute(self, context):
        return smartconfig_export_config(self.filepath, context, self.include_startup_file, self.include_bookmarks, self.include_users_prefs, self.include_presets, self.include_config_folders)
    

### Export function ###
def smartconfig_export_config(filepath, context, include_startup_file, include_bookmarks, include_users_prefs, include_presets, include_config_folders):
    addon_preferences = get_addon_preferences()
    exception=['smart_config','cycles','io_scene_3ds','io_scene_fbx','io_anim_bvh','io_mesh_ply','io_scene_obj','io_scene_x3d','io_mesh_stl','io_mesh_uv_layout','io_curve_svg',
            'mesh_looptools','blender_id','io_export_after_effects','add_curve_extra_objects','add_curve_ivygen','add_curve_sapling','add_mesh_extra_objects','io_sequencer_edl',
            'io_import_images_as_planes','io_anim_nuke_chan','object_fracture_cell','object_fracture','node_wrangler','animation_animall','object_cloud_gen','development_icon_get',
            'ui_layer_manager','space_view3d_pie_menus','space_view3d_stored_views','archipack','measureit','mesh_f2','rigify','space_view3d_copy_attributes','io_import_gimp_image_to_scene',
            'netrender']
    wrong=[]
    for f in addon_preferences.exception_list.split(","):
        exception.append(f)
        
    # clean old files
    chk_p=0
    if os.path.isfile(filepath)==True:
        try:
            os.remove(filepath)
        except:
            try:
                change_permissions_recursive(filepath, 0o777)
                os.remove(filepath)
            except:
                print('Smart Config warning : Unable to delete previous file, please delete it manually')
                chk_p=1
    tempdir=os.path.join((os.path.dirname(filepath)), (os.path.basename(filepath).split(".sc")[0]+"_temp_"))
    if os.path.isdir(tempdir):
        try:
            shutil.rmtree(tempdir)
        except:
            try:
                change_permissions_recursive(tempdir, 0o777)
                shutil.rmtree(tempdir)
            except:
                print('Smart Config warning : Unable to delete previous file, please delete it manually')
                chk_p=1
                
    if chk_p==0:
        # create tempdir to copy files
        os.makedirs(tempdir)
        os.makedirs(os.path.join(tempdir, "addons"))
        addondir=os.path.join(tempdir, "addons")
        user_path=bpy.utils.resource_path('USER')
        total=len(bpy.context.user_preferences.addons.keys())
        nb=0
        job="Smart Config warning : Exporting Addons"
        print()
        #create csv file
        csvfile=os.path.join(tempdir, "to_install.txt")
        nfile = open(csvfile, "w")
        # copy addons
        for mod_name in bpy.context.user_preferences.addons.keys():
            nb+=1
            chk3=0
            for e in exception:
                if e==mod_name:
                    chk3=1
            if chk3==0:
                chk4=0
                try:
                    mod = sys.modules[mod_name]
                    chk4=1
                except KeyError:
                    wrong.append(mod_name)
                if chk4==1:
                    nfile.write(mod_name+"\n")
                    path_s=os.path.abspath(mod.__file__)
                    #single file addon
                    if os.sep not in path_s.split("addons"+os.sep)[1]:
                        path_d=os.path.join(addondir, (path_s.split("addons"+os.sep)[1]))
                        shutil.copy2(path_s, path_d)
                    #multi file addon
                    else:
                        folder_name=(path_s.split("addons"+os.sep)[1]).split(os.sep)[0]
                        path_fs=os.path.dirname(path_s)
                        path_fd=os.path.join(addondir,folder_name)
                        shutil.copytree(path_fs, path_fd)
            update_progress_console(job, nb/total)
        #close csv
        nfile.close()
        # copy startup file
        if include_startup_file==True:
            path_s=os.path.join(os.path.join(user_path, "config"),"startup.blend")
            path_d=os.path.join(tempdir, "startup.blend")
            shutil.copy2(path_s, path_d)
        # copy bookmarks file
        if include_bookmarks==True:
            path_s=os.path.join(os.path.join(user_path, "config"),"bookmarks.txt")
            path_d=os.path.join(tempdir, "bookmarks.txt")
            shutil.copy2(path_s, path_d)
        # copy userprefs file
        if include_users_prefs==True:
            path_s=os.path.join(os.path.join(user_path, "config"),"userpref.blend")
            path_d=os.path.join(tempdir, "userpref.blend")
            shutil.copy2(path_s, path_d)
        # copy presets folder
        if include_presets==True:
            path_s=os.path.join(os.path.join(user_path, "scripts"),"presets")
            path_d=os.path.join(tempdir, "presets")
            shutil.copytree(path_s, path_d)
        # copy config folders
        if include_config_folders==True:
            config=os.path.join(user_path, "config")
            config_d=os.path.join(tempdir, "config")
            for file in os.listdir(config):
                if os.path.isdir(os.path.join(config,file))==True:
                    path_s=os.path.join(config, file)
                    path_d=os.path.join(config_d, file)
                    shutil.copytree(path_s, path_d)
        # create zip and delete temp
        print("Smart Config warning : Creating Archive")
        zipfile=shutil.make_archive(filepath, 'zip', tempdir)
        try:
            shutil.rmtree(tempdir)
        except:
            try:
                change_permissions_recursive(tempdir, 0o777)
                shutil.rmtree(tempdir)
            except:
                print('Smart Config warning : Unable to delete temp folder - Please delete it manually')
        basezip = os.path.splitext(zipfile)[0]
        os.rename(zipfile, basezip)
        
        print()
        print('Smart Config warning : Export Completed')
        #error reporting
        if len(wrong)!=0:
            if addon_preferences.errors_report==True:
                error=os.path.join(os.path.dirname(filepath), (os.path.basename(filepath).split(".sc")[0]+"_export_errors.txt"))
                errorfile = open(error, "w")
                errorfile.write("PROBLEMATIC'S ADDONS :\n\n")
                for a in wrong:
                    errorfile.write(a+"\n")
                errorfile.close()
            for a in wrong:
                print('Smart Config warning : Addon Problem with - '+a)
    
    else:
        print('Smart Config warning : Unexpected Error')
            
    return {'FINISHED'} 
    
### EXPORT CONFIGURATION MENU
def smart_config_menu_export_config(self, context):
    self.layout.operator('smartconfig.export_config', text="Smart Configuration (.sc)", icon='SCRIPTWIN')