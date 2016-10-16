# Makes plaques, as in things on walls
# Can probably make more than 2000

# Setup: import os, sys ; sys.path.append(os.path.dirname(bpy.data.filepath)) ; import plaques
# Reload: import importlib ; importlib.reload(plaques) ; plaques.go('names_2.csv', 2, (10,10))


# System libraries
import csv
import sys
import bpy
import os

# 3rd Party libraries go here
sys.path.append('C:/Users/Ben/AppData/Local/Programs/Python/Python35/Lib/site-packages')
sys.path.append('C:/Users/Ben/AppData/Local/Programs/Python/Python35/Lib')
sys.path.append('C:/Users/Ben/AppData/Local/Programs/Python/Python35/DLLs')

# Own modules go here

# Ensure that dependencies are up-to-date
if "module_to_import" in locals(): # we've imported this module
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
    current_directory = os.path.dirname(bpy.data.filepath)
    full_file_path = os.path.join(current_directory, filename)
    with open(full_file_path, 'r') as csvfile:
        iterable_lazy_reader = csv.reader(csvfile, quotechar="'")
        headers = next(iterable_lazy_reader) # consumes first item

        # zip into a dictionary
        for row in iterable_lazy_reader:
            backer = dict(zip(headers, row))
            yield backer # turns entire function into an iterator

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
    materials = bpy.context.selected_objects[0].material_slots.items()
    if not 'NameMaterial' in dict(materials):
        raise Exception("Selected object has no material called 'NameMaterial'")
    if bpy.context.selected_objects == []:
        raise Exception("Nothing is selected")
    if len(bpy.context.selected_objects) > 1:
        raise Exception("Select only one prototype")

def swap_material(plaque, directory, name):
    generate_texture(name, os.path.join(directory, name + '.png'))
    bpy.context.selected_objects[0].material_slots['NameMaterial'].material.copy()
    bpy.data.materials['NameMaterial.001'].node_tree.nodes['Image Texture.001'].image.update()
    # TODO sort.001 issue and finalise

def generate_texture(name, filename):
    from PIL import Image, ImageDraw, ImageFont

    im = Image.new('RGB', (900,900), (0,0,0))

    draw = ImageDraw.Draw(im)
    fnt = ImageFont.truetype('LeelaUIb.ttf', 100)
    draw.text((200,400), name, font=fnt, fill=(255,255,255))

    im.save(filename)

def go(filename, columns, spacing):
    throw_invalid_selection()
    cache_directory = 'texture_cache'

    prototype = bpy.context.selected_objects[0]
    for plaque_number, backer in enumerate(get_backers(filename)):
        if plaque_number == 0:
            plaque = prototype
        else:
            offset = get_offset(plaque_number, columns, spacing)
            # plaque = create_plaque(prototype, offset)

        swap_material(plaque, cache_directory, backer['Backer Name'])

if __name__ == '__main__':
    register() # So that we can run the code from Text Editor
