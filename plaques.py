# Makes plaques, as in things on walls
# Can probably make more than 2000

import bpy

bl_info = {"name": "My Test Addon", "category": "Object"}

def register():
    print("PlaqueMaker 2000 Starting Up")
    print("Work your magic")
def unregister():
    print("PlaqueMaker 2000 Shutting Down")

# scene = bpy.context.scene
# for obj in scene.objects:
#     obj.location.x -= 1.0
#     print("I did it, I did it")

if __name__ == '__main__':
    register() # So that we can run the code from Text Editor
