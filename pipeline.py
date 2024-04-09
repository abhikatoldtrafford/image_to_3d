import os
import bpy
import shutil
import cv2
from modelscope.models.cv.face_reconstruction.utils import write_obj
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# Function to find the first mesh child
def find_first_mesh_child(obj):
    if obj.type == 'MESH':
        return obj
    for child in obj.children:
        if child.type == 'MESH':
            return child
    return None

# Function to transfer blendshapes and generate output FBX
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

    if input_fbx.endswith(".fbx"):
        bpy.ops.import_scene.fbx(filepath=input_fbx)
    else:
        bpy.ops.import_scene.obj(filepath=input_fbx)

    object_1 = bpy.context.selected_objects[0]
    object_1.name = "input"
    
    bpy.ops.import_scene.fbx(filepath=reference_fbx)
    object_2 = bpy.context.selected_objects[0]
    object_2.name = "reference"
    
    for i in range(1, 53):  # Assuming 52 blendshapes
        bpy.data.objects['input'].active_shape_key_index = 0
        bpy.data.objects['reference'].active_shape_key_index = i
        bpy.ops.object.shape_key_transfer()

    input_mesh = find_first_mesh_child(bpy.data.objects["input"])
    input_mesh.select_set(True)
    bpy.ops.export_scene.fbx(filepath=output_fbx, use_selection=True)
    print(f"Output FBX saved at {output_fbx}")

# Function to save results from the head reconstruction model
def save_results(result, save_root):
    os.makedirs(save_root, exist_ok=True)
    mesh = result[OutputKeys.OUTPUT]['mesh']
    texture_map = result[OutputKeys.OUTPUT_IMG]
    mesh['texture_map'] = texture_map
    write_obj(os.path.join(save_root, 'modelscope.obj'), mesh)
    print(f'Output written to {os.path.abspath(save_root)}')

# Main execution function
def main():
    head_reconstruction = pipeline(Tasks.head_reconstruction, model='damo/cv_HRN_head-reconstruction', model_revision='v0.1')
    result = head_reconstruction('input.jpg')
    save_root = './head_reconstruction_output'
    save_results(result, save_root)

    input_obj_path = os.path.join(save_root, 'modelscope.obj')
    modelscope_to_blendshapes(input_fbx=input_obj_path, reference_fbx='52_blendshapes_final.fbx', output_fbx='output.fbx')

if __name__ == "__main__":
    main()
