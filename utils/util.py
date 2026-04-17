import os
import pymeshlab
import shutil
import subprocess as sp
import time
from datetime import datetime


# ── Logging ──────────────────────────────────────────────────────────────────

def _log_path(project_path):
    return os.path.join(project_path, 'reconstruction.log')


def log_step(project_path, step_name, duration_sec):
    """Append a single timed step entry to the project log file."""
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {step_name}: {duration_sec:.2f}s\n"
    print(line, end='')
    with open(_log_path(project_path), 'a', encoding='utf-8') as f:
        f.write(line)


def log_header(project_path, label):
    """Write a section header to the log (e.g. start of a pipeline phase)."""
    line = f"\n{'='*60}\n{label}  —  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*60}\n"
    print(line, end='')
    with open(_log_path(project_path), 'a', encoding='utf-8') as f:
        f.write(line)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _run(project_path, step_name, cmd, **kwargs):
    """Run a subprocess, time it, and log the result."""
    start = time.time()
    result = sp.run(cmd, capture_output=False, text=True, encoding='utf-8', **kwargs)
    log_step(project_path, step_name, time.time() - start)
    return result


# ── COLMAP steps ──────────────────────────────────────────────────────────────

def feature_extraction(project_path):
    return _run(project_path, 'feature_extraction', [
        'colmap', 'feature_extractor',
        '--database', os.path.join(project_path, 'database.db'),
        '--image_path', os.path.join(project_path, 'images'),
    ])

def exhaustive_matching(project_path):
    return _run(project_path, 'exhaustive_matching', [
        'colmap', 'exhaustive_matcher',
        '--database', os.path.join(project_path, 'database.db'),
    ])

def mapping(project_path):
    return _run(project_path, 'mapping', [
        'colmap', 'mapper',
        '--database', os.path.join(project_path, 'database.db'),
        '--image_path', os.path.join(project_path, 'images'),
        '--output_path', os.path.join(project_path, 'sparse'),
    ])

def image_undistortion(project_path):
    return _run(project_path, 'image_undistortion', [
        'colmap', 'image_undistorter',
        '--image_path', os.path.join(project_path, 'images'),
        '--input_path', os.path.join(project_path, 'sparse/0'),
        '--output_path', os.path.join(project_path, 'dense/0'),
    ])

def patch_matching(project_path):
    return _run(project_path, 'patch_matching', [
        'colmap', 'patch_match_stereo',
        '--workspace_path', os.path.join(project_path, 'dense/0'),
        '--PatchMatchStereo.cache_size', '8',
        '--PatchMatchStereo.max_image_size', '1000',
    ])

def stereo_fusion(project_path):
    return _run(project_path, 'stereo_fusion', [
        'colmap', 'stereo_fusion',
        '--workspace_path', os.path.join(project_path, 'dense/0'),
        '--output_path', os.path.join(project_path, 'dense/0/fused.ply'),
        '--StereoFusion.cache_size', '8',
        '--StereoFusion.max_image_size', '1000',
    ])


# ── OpenMVS steps ─────────────────────────────────────────────────────────────

def convert_colmap_openMVS(project_path, dense_pc_path):
    return _run(project_path, 'convert_colmap_openMVS', [
        'InterfaceCOLMAP',
        '-w', dense_pc_path,
        '-i', '.',
        '-o', 'dense.mvs',
        '--image-folder', 'images',
    ])

def reconstruct_mesh(project_path, dense_pc_path):
    return _run(project_path, 'reconstruct_mesh', [
        'ReconstructMesh',
        '-w', dense_pc_path,
        '-i', 'dense.mvs',
        '--export-type', 'ply',
    ])

def refine_mesh(project_path, dense_pc_path):
    return _run(project_path, 'refine_mesh', [
        'RefineMesh',
        '-w', dense_pc_path,
        '-i', 'dense.mvs',
        '-m', 'dense_mesh.ply',
        '--cuda-device', '-2',
        '--resolution-level', '3',
        '--scales', '3',
        '--export-type', 'ply',
    ])

def texture_mesh(project_path, dense_pc_path):
    return _run(project_path, 'texture_mesh', [
        'TextureMesh',
        '-w', dense_pc_path,
        '-i', 'dense.mvs',
        '-m', 'dense_mesh.ply',
        '--resolution-level', '1',
        '--empty-color', '0',
        '--export-type', 'ply',
    ])


# ── PLY → OBJ ─────────────────────────────────────────────────────────────────

def ply2obj_meshlab(project_path, dense_pc_path):
    if not os.path.exists(os.path.join(project_path, 'model')):
        os.makedirs(os.path.join(project_path, 'model'))

    project_name = os.path.basename(project_path)
    obj_path = os.path.join(project_path, 'model', project_name + '.obj')

    start = time.time()
    sp.run([
        'meshlabserver',
        '-i', os.path.join(dense_pc_path, 'dense_texture.ply'),
        '-o', obj_path,
        '-m', 'wt',
    ], capture_output=False, text=True, encoding='utf-8')
    log_step(project_path, 'ply2obj', time.time() - start)

    shutil.copy(os.path.join(dense_pc_path, 'dense_texture0.png'), os.path.join(project_path, 'model'))

    return obj_path


def ply2obj(project_path, dense_pc_path):
    """Convert OpenMVS dense_texture.ply to OBJ using pymeshlab.
    Preserves UV coordinates and texture mapping natively.
    """

    project_path = os.path.normpath(project_path)
    project_name = os.path.basename(project_path)
    model_dir = os.path.join(project_path, 'model')
    os.makedirs(model_dir, exist_ok=True)

    ply_path = os.path.join(dense_pc_path, 'dense_texture.ply')
    obj_path = os.path.join(model_dir, project_name + '.obj')
    mtl_path = os.path.join(model_dir, obj_path + '.mtl')
    texture_name = 'dense_texture0.png'

    start = time.time()

    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(ply_path)
    ms.save_current_mesh(obj_path, save_wedge_texcoord=True)

    log_step(project_path, 'ply2obj_pymeshlab', time.time() - start)

    # Copy original texture from dense output
    shutil.copy(os.path.join(dense_pc_path, texture_name), model_dir)

    # Fix MTL: point texture at dense_texture0.png, add illum 2
    with open(mtl_path, 'r') as f:
        mtl_data = f.read()
        
    if 'illum' not in mtl_data:
        mtl_data = mtl_data.replace('map_Kd', 'illum 2\nmap_Kd')

    with open(mtl_path, 'w') as f:
        f.write(mtl_data)

    return obj_path
