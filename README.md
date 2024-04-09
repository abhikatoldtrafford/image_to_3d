
input: image, output: 3d model + animated face

Steps for img to 3d:

a)conda create -n img3d python=3.10

b)conda activate img3d 

c) pip install modelscope face_alignment

d) pip install modelscope[cv] -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html

e) python test_reconstruction.py


Steps for img to animated avatar:

a) Install blender

b) Add to path

c)pip install bpy==3.6.0

d) python pipeline.py
