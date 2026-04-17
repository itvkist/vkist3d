"""
Test for ply2obj conversion functions.

Usage:
    python test_ply2obj.py <project_path> [trimesh|pymeshlab|both]

    <project_path> must be a completed reconstruction folder containing:
        dense/0/dense_texture.ply
        dense/0/dense_texture0.png

Expected output in <project_path>/model/:
    <project_name>.obj
    material.mtl          (map_Kd references dense_texture0.png, illum 2)
    dense_texture0.png
"""

import os
import shutil
import sys
import time
import traceback

from utils.util import ply2obj_trimesh, ply2obj_pymeshlab


def check_outputs(project_path, obj_path):
    model_dir = os.path.join(project_path, 'model')

    expected = {
        'OBJ':     obj_path,
        'MTL':     os.path.join(model_dir, 'material.mtl'),
        'Texture': os.path.join(model_dir, 'dense_texture0.png'),
    }

    print("\n  Output files:")
    all_ok = True
    for name, path in expected.items():
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"    OK       {name}: {path}  ({size_kb:.1f} KB)")
        else:
            print(f"    MISSING  {name}: {path}")
            all_ok = False

    # Verify MTL content
    mtl_path = expected['MTL']
    if os.path.exists(mtl_path):
        with open(mtl_path) as f:
            mtl_data = f.read()
        for token, label in [
            ('map_Kd dense_texture0.png', 'texture reference'),
            ('illum 2',                   'illumination model 2'),
        ]:
            if token in mtl_data:
                print(f"    OK       MTL {label}")
            else:
                print(f"    MISSING  MTL {label} ({token!r} not found)")
                all_ok = False

    # Check OBJ has UV coordinates
    if os.path.exists(obj_path):
        with open(obj_path) as f:
            obj_data = f.read()
        has_vt = '\nvt ' in obj_data or obj_data.startswith('vt ')
        if has_vt:
            vt_count = obj_data.count('\nvt ')
            print(f"    OK       OBJ has UV coordinates ({vt_count} vt entries)")
        else:
            print("    MISSING  OBJ has no vt (UV) entries — texture will not map")
            all_ok = False

    return all_ok


def run(label, fn, project_path, dense_pc_path):
    # Clean model dir before each run for a fair test
    model_dir = os.path.join(project_path, 'model')
    if os.path.exists(model_dir):
        shutil.rmtree(model_dir)

    print(f"\n{'='*60}")
    print(f"Running: {label}")
    print(f"{'='*60}")
    start = time.time()
    try:
        result = fn(project_path, dense_pc_path)
        elapsed = time.time() - start
        print(f"  Returned : {result}")
        print(f"  Time     : {elapsed:.2f}s")
        check_outputs(project_path, result)
    except Exception as e:
        elapsed = time.time() - start
        print(f"  FAILED after {elapsed:.2f}s: {e}")
        traceback.print_exc()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_ply2obj.py <project_path> [trimesh|pymeshlab|both]")
        print("Example: python test_ply2obj.py projects/1717735836742 pymeshlab")
        sys.exit(1)

    project_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'both'
    dense_pc_path = os.path.join(project_path, 'dense/0')

    for required in ['dense_texture.ply', 'dense_texture0.png']:
        f = os.path.join(dense_pc_path, required)
        if not os.path.exists(f):
            print(f"ERROR: {required} not found at {f}")
            print("Make sure the project has completed the texture step first.")
            sys.exit(1)

    print(f"Project path : {project_path}")
    print(f"Dense path   : {dense_pc_path}")
    print(f"Mode         : {mode}")

    if mode in ('trimesh', 'both'):
        run('ply2obj_trimesh', ply2obj_trimesh, project_path, dense_pc_path)

    if mode in ('pymeshlab', 'both'):
        run('ply2obj_pymeshlab', ply2obj_pymeshlab, project_path, dense_pc_path)
