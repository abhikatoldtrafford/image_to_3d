import os
import cv2
from modelscope.models.cv.face_reconstruction.utils import write_obj
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


def save_results(result, save_root):
    os.makedirs(save_root, exist_ok=True)

    # export obj and texture
    mesh = result[OutputKeys.OUTPUT]['mesh']
    texture_map = result[OutputKeys.OUTPUT_IMG]
    mesh['texture_map'] = texture_map
    write_obj(os.path.join(save_root, 'modelscope.obj'), mesh)

    print(f'Output written to {os.path.abspath(save_root)}')

head_reconstruction = pipeline(Tasks.head_reconstruction, model='damo/cv_HRN_head-reconstruction', model_revision='v0.1')
result = head_reconstruction('abhik.jpg')

save_results(result, './head_reconstruction_results')