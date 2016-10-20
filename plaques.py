# Makes plaques, as in things on walls
# Can probably make more than 2000

# Setup: import os, sys ; sys.path.append(os.path.dirname(bpy.data.filepath)) ; import plaques
# Reload: import importlib ; importlib.reload(plaques) ; plaques.go('backers_10.csv', 4, (1.5,2), True)


# System libraries
import csv
import sys
import bpy
import os
import codecs # to ensure correct text file handling cross-platform

# 3rd Party libraries go here
## Windows (comment next 3 lines on Mac)
sys.path.append('C:/Users/Ben/AppData/Local/Programs/Python/Python35/Lib/site-packages')
sys.path.append('C:/Users/Ben/AppData/Local/Programs/Python/Python35/Lib')
sys.path.append('C:/Users/Ben/AppData/Local/Programs/Python/Python35/DLLs')

## Mac (comment next 2 lines on Windows)
# sys.path.append('/venv/lib/python3.5/site-packages')
# sys.path.append('/venv/lib/python3.5/lib')

# Own modules go here

# Ensure that dependencies are up-to-date
if "module_to_import" in locals(): # we've imported this module
    print("Reloading")
    import importlib
    # importlib.reload(module_to_import)
else:
    print("Importing")
    # import module_to_import

# Parsed by Blender, use only strings or the world explodes
bl_info = {"name": "My Test Addon", "category": "Object"}

def register():
    pass

def unregister():
    pass

def get_backers(csv_filename):
    current_directory = os.path.dirname(bpy.data.filepath)
    full_file_path = os.path.join(current_directory, csv_filename)
    with codecs.open(full_file_path, 'r', 'utf-8-sig') as csvfile:
        iterable_lazy_reader = csv.reader(csvfile, quotechar='"')
        headers = next(iterable_lazy_reader) # consumes first item
        for row in iterable_lazy_reader:
            backer = dict(zip(headers, row))
            yield backer # turns entire function into an iterator

def get_offset(plaque_number, columns, spacing):
    x_offset = plaque_number % columns * spacing[0]
    y_offset = plaque_number // columns * spacing[1] # // integer division
    z_offset = 0
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
    if bpy.context.selected_objects == []:
        raise Exception("Nothing is selected")
    if len(bpy.context.selected_objects) > 1:
        raise Exception("Select only one prototype")

def swap_cycles_material(plaque, image_filename):
    new_material = plaque.material_slots[0].material.copy()
    plaque.material_slots[0].material = new_material
    new_image = bpy.data.images.load(image_filename)
    new_material.node_tree.nodes['Image Texture'].image = new_image # if first

def swap_blender_texture(plaque, image_filename):
    print("Using Blender Render method")
    print("Or at least I will when the code's written!")
    pass

def render_texture_to_file(text_to_render, to_filename):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new('RGB', (512,64), (0,0,0))
    draw = ImageDraw.Draw(im)
    fnt = ImageFont.truetype('arial.ttf', 50)
    draw.text((0, 0), text_to_render, font=fnt, fill=(255,255,255))
    im.save(to_filename)

def swap_text(plaque, backer, render_mode):
    cwd = os.path.dirname(bpy.data.filepath)
    image_filename = cwd + '\\texture_cache\\' + backer['Number'] + '.png'
    text_to_render = backer['Name'] + ', ' + backer['Country']
    render_texture_to_file(text_to_render, image_filename)
    if render_mode == 'cycles':
        swap_cycles_material(plaque, image_filename)
    elif render_mode == 'br':
        swap_blender_texture(plaque, image_filename)
    else:
        raise Exception("Invalid render mode selected")

def go(csv_filename, columns, spacing, render_mode):
    throw_invalid_selection()
    prototype = bpy.context.selected_objects[0]
    for plaque_number, backer in enumerate(get_backers(csv_filename)):
        if plaque_number == 0:
            plaque = prototype
        else:
            offset = get_offset(plaque_number, columns, spacing)
            plaque = create_plaque(prototype, offset)
        swap_text(plaque, backer, render_mode)

if __name__ == '__main__':
    register() # So that we can run the code from Text Editor
