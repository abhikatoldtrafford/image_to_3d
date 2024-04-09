# image_to_3d
input: image, output: 3d model + animated face

Steps for img to 3d:

conda create -n img3d python=3.10
conda activate img3d 
pip install modelscope
pip install modelscope[cv] -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html
python test_reconstruction.py

Steps for img to animated avatar:
Install blender
Add to path
pip install bpy==3.6.0
python image_to_animated.py
