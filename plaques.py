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

def get_backers():
    with open('names.csv', 'r') as csvfile:
        iterable_lazy_reader = csv.reader(csvfile, quotechar="'")
        headers = next(iterable_lazy_reader) # consumes first item

        # zip into a dictionary
        for row in iterable_lazy_reader:
            backer = dict(zip(headers, row))
            yield backer # turns entire function into an iterator

def duplicate(num, spacing):
    (num_x, num_y, num_z) = num
    (sp_x, sp_y, sp_z) = spacing

    if bpy.context.selected_objects == []:
        print("Nothing is selected")
        return

    # keep a reference to the originally selected object
    old_column_prototype = None

    for count in range(0, num[0]):
        if old_column_prototype:
            bpy.ops.object.select_all(action='DESELECT')
            old_column_prototype.select = True
            bpy.ops.object.duplicate_move(
                OBJECT_OT_duplicate={"linked":False},
                TRANSFORM_OT_translate={"value":[sp_x, 0, 0]}
            )
        new_column_prototype = bpy.context.selected_objects[0]


        for count in range(0, num[1]):
            print('boo')
            print(bpy.context.scene.objects.active)
            bpy.ops.object.duplicate_move(
                OBJECT_OT_duplicate={"linked":False},
                TRANSFORM_OT_translate={"value":[0, sp_y, 0]}
            )

        old_column_prototype = new_column_prototype


def print_csv():
    for backer in get_backers():
        print(backer['Backer Name'])

if __name__ == '__main__':
    register() # So that we can run the code from Text Editor
