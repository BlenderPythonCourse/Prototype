import bpy

def move_all(amount):
    scene = bpy.context.scene
    for obj in scene.objects:
        obj.location.x += amount
