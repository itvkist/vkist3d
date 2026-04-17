import os
import shutil
import time
from utils.util import (
    feature_extraction, exhaustive_matching, mapping,
    image_undistortion, patch_matching, stereo_fusion,
    convert_colmap_openMVS, reconstruct_mesh, refine_mesh,
    texture_mesh, ply2obj, log_header, log_step,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_MODELS_DIR = os.path.join(BASE_DIR, 'public', 'models')

####################################################################################################

def generate_dense_point_cloud(project_path):
    if not os.path.exists(os.path.join(project_path, 'sparse')):
        os.makedirs(os.path.join(project_path, 'sparse'))

    if not os.path.exists(os.path.join(project_path, 'dense')):
        os.makedirs(os.path.join(project_path, 'dense'))

    log_header(project_path, 'Phase 1: Dense Point Cloud')
    start = time.time()

    feature_extraction(project_path)
    exhaustive_matching(project_path)
    mapping(project_path)
    image_undistortion(project_path)
    patch_matching(project_path)
    stereo_fusion(project_path)

    log_step(project_path, 'TOTAL dense point cloud', time.time() - start)
    return 'Finished generating dense point cloud'


def generate_texture(project_path):
    dense_pc_path = os.path.join(project_path, 'dense/0')

    log_header(project_path, 'Phase 2: Mesh & Texture')
    start = time.time()

    convert_colmap_openMVS(project_path, dense_pc_path)
    reconstruct_mesh(project_path, dense_pc_path)
    # refine_mesh(project_path, dense_pc_path)
    texture_mesh(project_path, dense_pc_path)
    obj_path = ply2obj(project_path, dense_pc_path)

    log_step(project_path, 'TOTAL mesh & texture', time.time() - start)

    # Copy finished model to public/models/<project_id>/
    project_id = os.path.basename(project_path)
    public_model_dir = os.path.join(PUBLIC_MODELS_DIR, project_id)
    if os.path.exists(public_model_dir):
        shutil.rmtree(public_model_dir)
    shutil.copytree(os.path.join(project_path, 'model'), public_model_dir)
    log_step(project_path, 'copy model to public', 0)

    return obj_path


def reconstruct(project_path):
    result1 = generate_dense_point_cloud(project_path)
    result2 = generate_texture(project_path)
    return result1 + ' and ' + result2


if __name__ == '__main__':
    project_path = 'test'
    print(reconstruct(project_path))
