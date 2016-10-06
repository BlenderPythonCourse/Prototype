import bpy

bl_info = {"name": "My Test Addon", "category": "Object"}

def register():
    print("Hello World BOOM")
def unregister():
    print("Goodbye World")

scene = bpy.context.scene
for obj in scene.objects:
    obj.location.x -= 1.0
    print("I did it, I did it")

