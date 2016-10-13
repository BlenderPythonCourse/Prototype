# Makes plaques, as in things on walls
# Can probably make more than 2000

# Setup: import os, sys, importlib ; sys.path.append(os.path.dirname(bpy.data.filepath)) ; import plaques
# Reload: importlib.reload(plaques) ; plaques.go()

# System libraries
import csv
import sys
import bpy

# 3rd Party libraries

# Own modules

# Ensure that dependencies are up-to-date
if "move" in locals():
    print("Reloading")
    import importlib
    importlib.reload(move)
else:
    print("Importing")
    import move

# Parsed by Blender, use only strings or the world explodes
bl_info = {"name": "My Test Addon", "category": "Object"}

def register():
    pass

def unregister():
    pass

def get_backers(filename):
    with open(filename, 'r') as csvfile:
        iterable_lazy_reader = csv.reader(csvfile, quotechar="'")
        headers = next(iterable_lazy_reader) # consumes first item

        # zip into a dictionary
        for row in iterable_lazy_reader:
            backer = dict(zip(headers, row))
            yield backer # turns entire function into an iterator

def swap_material(plaque, name):
    print("Swapping material text to:", name)
    # TODO implement

def get_offset(plaque_number, columns, spacing):
    x_offset = plaque_number % columns * spacing[0]
    y_offset = plaque_number // columns * spacing[1] # // integer division
    z_offset = 0 # 2D
    return((x_offset, y_offset, z_offset))

def create_plaque(prototype, offset):
    prototype.select = True
    bpy.ops.object.duplicate_move(
        OBJECT_OT_duplicate={"linked":False},
        TRANSFORM_OT_translate={"value":offset}
    )
    new_plaque = bpy.context.selected_objects[0]
    new_plaque.select = False
    return new_plaque

def throw_invalid_selection():
    # TODO check it has a material to swap?
    if bpy.context.selected_objects == []:
        raise Exception("Nothing is selected")
    if len(bpy.context.selected_objects) > 1:
        raise Exception("Select only one prototype")

def go(filename, columns, spacing):
    throw_invalid_selection()

    prototype = bpy.context.selected_objects[0]
    for plaque_number, backer in enumerate(get_backers(filename)):
        if plaque_number == 0:
            plaque = prototype
        else:
            offset = get_offset(plaque_number, columns, spacing)
            plaque = create_plaque(prototype, offset)

        swap_material(plaque, backer['Backer Name'])

if __name__ == '__main__':
    register() # So that we can run the code from Text Editor
