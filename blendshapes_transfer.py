import bpy
import shutil

def find_first_mesh_child(obj):
    """
    Finds the first child object of the given object that is of type 'MESH'.

    Args:
        obj: The parent object to search children in.

    Returns:
        The first mesh child object or None if no mesh child is found.
    """
    if obj.type == 'MESH':
        return obj
    for child in obj.children:
        if child.type == 'MESH':
            return child
    return None

def modelscope_to_blendshapes(input_fbx='modelscope.obj', reference_fbx='52_blendshapes_final.fbx', output_fbx='output.fbx'):
    blender_bin = shutil.which("blender")
    if blender_bin:
        print("Found:", blender_bin)
        bpy.app.binary_path = blender_bin
    else:
        print("Unable to find blender!")
        return

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import input FBX or OBJ
    if input_fbx.endswith(".fbx"):
        bpy.ops.import_scene.fbx(filepath=input_fbx)
    else:
        bpy.ops.import_scene.obj(filepath=input_fbx)

    object_1 = bpy.context.selected_objects[0]
    if object_1:
        object_1.name = "input"
        print(f"Object1 created with name: {object_1.name}")
    else:
        print(f"Error importing {input_fbx}")
        return

    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]

    before_vertices = sum(len(m.data.vertices) for m in bpy.context.selected_objects if m.type == 'MESH')

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()

    after_vertices = sum(len(m.data.vertices) for m in bpy.context.selected_objects if m.type == 'MESH')

    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    print("Number of vertices before removal:", before_vertices)
    print("Number of vertices after removal:", after_vertices)

    bpy.data.objects["input"].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["input"]
    bpy.ops.object.shape_key_add(from_mix=False)
    print("Shape key 'Basis' added!")

    bpy.ops.import_scene.fbx(filepath=reference_fbx)

    object_2 = bpy.context.selected_objects[0]
    if object_2:
        object_2.name = "reference"
        print(f"Object2 created with name: {object_2.name}")
    else:
        print(f"Error importing {reference_fbx}")
        return

    # Transfer blendshapes from reference to input
    input_obj = bpy.data.objects['input']
    ref_obj = bpy.data.objects['reference']
    for i in range(1, 53):  # Assuming 52 blendshapes
        input_obj.active_shape_key_index = 0
        ref_obj.active_shape_key_index = i
        bpy.ops.object.shape_key_transfer()

        # print(f"Shape key {i} transferred!")

    # Export the modified input object
    input_mesh = find_first_mesh_child(input_obj)
    if not input_mesh:
        print("Error: Could not find mesh with blendshapes in input object!")
        return

    input_mesh.select_set(True)
    bpy.ops.export_scene.fbx(filepath=output_fbx, use_selection=True)

if __name__ == "__main__":
    modelscope_to_blendshapes()
