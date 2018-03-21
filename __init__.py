'''
Copyright (C) 2018 YOUR NAME
YOUR@MAIL.com

Created by YOUR NAME

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Smart Config",
    "description": "",
    "author": "Samy Tichadou (tonton)",
    "version": (0, 0, 2),
    "blender": (2, 79, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object" }


import bpy


# load and reload submodules
##################################

import importlib
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())

from .export_function import smart_config_menu_export_config
from .import_function import smart_config_menu_import_config    


# register
##################################

import traceback

def register():
        
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()

    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))
    
    bpy.types.INFO_MT_file_export.append(smart_config_menu_export_config)
    bpy.types.INFO_MT_file_import.append(smart_config_menu_import_config)

def unregister():
    
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()

    print("Unregistered {}".format(bl_info["name"]))

    bpy.types.INFO_MT_file_export.remove(smart_config_menu_export_config)
    bpy.types.INFO_MT_file_import.remove(smart_config_menu_import_config)