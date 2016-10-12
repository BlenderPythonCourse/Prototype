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
    if bpy.context.selected_objects == []:
        print("Nothing is selected")
        return

    for count in range(1, num + 1):
        print("Creating duplicate:", count)

def print_backers():
    for backer in get_backers():
        print(backer['Backer Name'])

if __name__ == '__main__':
    register() # So that we can run the code from Text Editor
