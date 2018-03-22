import bpy
import sys
import addon_utils
import os

from .addon_prefs import get_addon_preferences

def update_progress_console(job_title, progress):
    length = 20 # modify this to change the length
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 2))
    if progress >= 1: msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()
    
def change_permissions_recursive(path, mode):
    if os.path.isfile(path)==True:
        os.chmod(path, mode)
    elif os.path.isdir(path)==True:
        for root, dirs, files in os.walk(path, topdown=False):
            for dir in [os.path.join(root,d) for d in dirs]:
                os.chmod(dir, mode)
        for file in [os.path.join(root, f) for f in files]:
                os.chmod(file, mode)