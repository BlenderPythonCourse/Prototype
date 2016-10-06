# Makes plaques, as in things on walls
# Can probably make more than 2000

import sys

# Ensure that dependencies are up-to-date
if "bpy" in locals():
    print("Reloading")
    import importlib
    importlib.reload(move)
else:
    print("Importing")
    import move

import bpy

bl_info = {"name": "My Test Addon", "category": "Object"}

def register():
    print("PlaqueMaker 2000 Starting Up")
    move.move_all(0.2)

def unregister():
    print("PlaqueMaker 2000 Shutting Down")

if __name__ == '__main__':
    register() # So that we can run the code from Text Editor
