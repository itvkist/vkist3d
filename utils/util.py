import os
import shutil
import subprocess as sp

def feature_extraction(project_path):
    result = sp.run(['colmap', 'feature_extractor', \
                    '--database', os.path.join(project_path, 'database.db'), \
                    '--image_path', os.path.join(project_path, 'images')], capture_output=False, text=True, encoding='utf-8')
    return result

def exhaustive_matching(project_path):
    result = sp.run(['colmap', 'exhaustive_matcher', \
                    '--database', os.path.join(project_path, 'database.db')], capture_output=False, text=True, encoding='utf-8')
    return result

def mapping(project_path):
    result = sp.run(['colmap', 'mapper', \
                    '--database', os.path.join(project_path, 'database.db'), \
                    '--image_path', os.path.join(project_path, 'images'), \
                    '--output_path', os.path.join(project_path, 'sparse')], capture_output=False, text=True, encoding='utf-8')
    return result
    
def image_undistortion(project_path):
    result = sp.run(['colmap', 'image_undistorter', \
                    '--image_path', os.path.join(project_path, 'images'), \
                    '--input_path', os.path.join(project_path, 'sparse/0'), \
                    '--output_path', os.path.join(project_path, 'dense/0')], capture_output=False, text=True, encoding='utf-8')
    return result
    
def patch_matching(project_path):
    result = sp.run(['colmap', 'patch_match_stereo', \
                    '--workspace_path', os.path.join(project_path, 'dense/0'), \
                    '--PatchMatchStereo.cache_size', '8', \
                    '--PatchMatchStereo.max_image_size', '1000'], capture_output=False, text=True, encoding='utf-8')
    return result
    
def stereo_fusion(project_path):
    result = sp.run(['colmap', 'stereo_fusion', \
                    '--workspace_path', os.path.join(project_path, 'dense/0'), \
                    '--output_path', os.path.join(project_path, 'dense/0/fused.ply'), \
                    '--StereoFusion.cache_size', '8', \
                    '--StereoFusion.max_image_size', '1000'], capture_output=False, text=True, encoding='utf-8')
    return result
    
def convert_colmap_openMVS(dense_pc_path):
    result = sp.run(['InterfaceCOLMAP', \
                    '-w', dense_pc_path, \
                    '-i', '.', \
                    '-o', 'dense.mvs', \
                    '--image-folder', 'images'], capture_output=False, text=True, encoding='utf-8')
    return result
    
def reconstruct_mesh(dense_pc_path):
    result = sp.run(['ReconstructMesh', \
                    '-w', dense_pc_path, \
                    '-i', 'dense.mvs', \
                    # '-o', 'dense_mesh.obj', \
                    '--export-type', 'ply'], capture_output=False, text=True, encoding='utf-8')
    return result
    
def refine_mesh(dense_pc_path):
    result = sp.run(['RefineMesh', \
                    '-w', dense_pc_path, \
                    '-i', 'dense.mvs', \
                    '-m', 'dense_mesh.ply', \
                    # '-o', 'dense_mesh_refined.mvs', \
                    '--cuda-device', '-2', \
                    '--resolution-level', '3', \
                    '--scales', '3', \
                    '--export-type', 'ply'], capture_output=False, text=True, encoding='utf-8')
    return result
    
def texture_mesh(dense_pc_path):
    result = sp.run(['TextureMesh', \
                    '-w', dense_pc_path, \
                    '-i', 'dense.mvs', \
                    '-m', 'dense_mesh.ply', \
                    # '-m', 'dense_refine.ply', \
                    # '-o', 'dense_mesh_texture.mvs', \
                    '--resolution-level', '1', \
                    '--empty-color', '0', \
                    '--export-type', 'ply'], capture_output=False, text=True, encoding='utf-8')
    return result

# Converting ply to obj
def ply2obj(project_path, dense_pc_path):
    if not os.path.exists(os.path.join(project_path, 'model')):
        os.makedirs(os.path.join(project_path, 'model'))

    project_name = os.path.basename(project_path)

    obj_path = os.path.join(os.path.join(project_path, 'model'), project_name + '.obj')

    sp.run(['meshlabserver', \
                    '-i', os.path.join(dense_pc_path, 'dense_texture.ply'), \
                    '-o', obj_path, \
                    '-m', 'wt'], capture_output=False, text=True, encoding='utf-8')
	
    # Fix mtl file for three.js
    with open(obj_path + '.mtl', 'r') as file:
        filedata = file.read()
        
    filedata = filedata.replace('Tr', 'd')
    
    with open(obj_path + '.mtl', 'w') as file:
        file.write(filedata)
        
    #Generate texture in model path
    shutil.copy(os.path.join(dense_pc_path, 'dense_texture0.png'), os.path.join(project_path, 'model'))

    return obj_path
