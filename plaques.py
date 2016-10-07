# Makes plaques, as in things on walls
# Can probably make more than 2000

# Setup: import os, sys, importlib ; sys.path.append(os.path.dirname(bpy.data.filepath)) ; import plaques
# Reload: importlib.reload(plaques) ; plaques.go()

# System libraries
import csv
import sys

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

def go():
    for backer in get_backers():
        print(backer['Backer Name'])

# trying idea of having a Script node as an iterator!
def sv_main(N=1000):
    verts = []
    in_sockets = [['s', 'N', N]]
    out_sockets = [['v','verts', [verts]]]

    lorenz(N, verts)
    return in_sockets, out_sockets

if __name__ == '__main__':
    register() # So that we can run the code from Text Editor
