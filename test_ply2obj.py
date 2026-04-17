"""
Test for ply2obj_trimesh.

Usage:
    python test_ply2obj.py <project_path>

    <project_path> must be a completed reconstruction folder containing:
        dense/0/dense_texture.ply
        dense/0/dense_texture0.png

Expected output in <project_path>/model/:
    <project_name>.obj
    material.mtl          (map_Kd references dense_texture0.png)
    dense_texture0.png
"""

import os
import sys
import time

from utils.util import ply2obj_trimesh


def check_outputs(project_path, obj_path):
    project_name = os.path.basename(project_path)
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
        checks = {
            'map_Kd dense_texture0.png': 'texture reference',
            'illum 2':                   'illumination model 2',
        }
        for token, label in checks.items():
            if token in mtl_data:
                print(f"    OK       MTL {label}")
            else:
                print(f"    MISSING  MTL {label} ({token!r} not found)")
                all_ok = False

    # Warn if trimesh's auto-texture was not cleaned up
    for leftover in ['material_0.png', 'material.mtl']:
        path = os.path.join(model_dir, leftover)
        # material.mtl is expected — only warn about material_0.png
        if leftover != 'material.mtl' and os.path.exists(path):
            print(f"    WARN     Leftover trimesh file not removed: {path}")

    return all_ok


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_ply2obj.py <project_path>")
        print("Example: python test_ply2obj.py projects/1717735836742")
        sys.exit(1)

    project_path = sys.argv[1]
    dense_pc_path = os.path.join(project_path, 'dense/0')

    for required in ['dense_texture.ply', 'dense_texture0.png']:
        f = os.path.join(dense_pc_path, required)
        if not os.path.exists(f):
            print(f"ERROR: {required} not found at {f}")
            print("Make sure the project has completed the texture step first.")
            sys.exit(1)

    print(f"Project path : {project_path}")
    print(f"Dense path   : {dense_pc_path}")

    print(f"\n{'='*60}")
    print("Running: ply2obj_trimesh")
    print(f"{'='*60}")
    start = time.time()
    try:
        result = ply2obj_trimesh(project_path, dense_pc_path)
        elapsed = time.time() - start
        print(f"  Returned : {result}")
        print(f"  Time     : {elapsed:.2f}s")
        check_outputs(project_path, result)
    except Exception as e:
        import traceback
        elapsed = time.time() - start
        print(f"  FAILED after {elapsed:.2f}s: {e}")
        traceback.print_exc()
