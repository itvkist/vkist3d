"""
Test for ply2obj_trimesh — compares output against the original meshlabserver-based ply2obj.

Usage:
    python test_ply2obj.py <project_path>

    <project_path> must be a completed reconstruction folder containing:
        dense/0/dense_texture.ply
        dense/0/dense_texture0.png

The script runs both functions and reports:
    - Whether each produced the expected output files
    - Elapsed time for each
    - File sizes for comparison
"""

import os
import sys
import time

from utils.util import ply2obj, ply2obj_trimesh


def check_outputs(label, project_path, obj_path):
    project_name = os.path.basename(project_path)
    model_dir = os.path.join(project_path, 'model')

    expected_files = {
        'OBJ':     obj_path,
        'Texture': os.path.join(model_dir, 'dense_texture0.png'),
    }

    # meshlabserver uses <name>.obj.mtl, trimesh uses <name>.mtl
    for mtl_candidate in [obj_path + '.mtl', os.path.join(model_dir, project_name + '.mtl')]:
        if os.path.exists(mtl_candidate):
            expected_files['MTL'] = mtl_candidate
            break

    print(f"\n  [{label}] Output files:")
    all_ok = True
    for name, path in expected_files.items():
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"    OK  {name}: {path}  ({size_kb:.1f} KB)")
        else:
            print(f"    MISSING  {name}: {path}")
            all_ok = False

    return all_ok


def run(label, fn, project_path, dense_pc_path):
    print(f"\n{'='*60}")
    print(f"Running: {label}")
    print(f"{'='*60}")
    start = time.time()
    try:
        result = fn(project_path, dense_pc_path)
        elapsed = time.time() - start
        print(f"  Returned: {result}")
        print(f"  Time:     {elapsed:.2f}s")
        check_outputs(label, project_path, result)
    except Exception as e:
        elapsed = time.time() - start
        print(f"  FAILED after {elapsed:.2f}s: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_ply2obj.py <project_path>")
        print("Example: python test_ply2obj.py public/images/1717735836742")
        sys.exit(1)

    project_path = sys.argv[1]
    dense_pc_path = os.path.join(project_path, 'dense/0')

    ply_file = os.path.join(dense_pc_path, 'dense_texture.ply')
    if not os.path.exists(ply_file):
        print(f"ERROR: dense_texture.ply not found at {ply_file}")
        print("Make sure the project has completed the texture step first.")
        sys.exit(1)

    print(f"Project path : {project_path}")
    print(f"Dense path   : {dense_pc_path}")
    print(f"PLY file     : {ply_file}  ({os.path.getsize(ply_file)/1024:.1f} KB)")

    # Run trimesh version
    run('ply2obj_trimesh (new)', ply2obj_trimesh, project_path, dense_pc_path)

    # Uncomment to also run the original meshlabserver version for comparison:
    # run('ply2obj (meshlabserver)', ply2obj, project_path, dense_pc_path)
