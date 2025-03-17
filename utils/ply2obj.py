import os
import trimesh

def ply_to_obj_with_new_mtl(ply_file, obj_file):
    """
    Converts a PLY file with texture to an OBJ file, creates a new MTL file, and saves the texture.
    
    Parameters:
    ply_file (str): Path to the input PLY file.
    obj_file (str): Path to the output OBJ file.
    """
    try:
        # Load the PLY file
        mesh = trimesh.load(ply_file)
        
        # Ensure the output directory exists
        obj_dir = os.path.dirname(obj_file)
        if not os.path.exists(obj_dir):
            os.makedirs(obj_dir)

        # Define paths for MTL and texture files
        obj_basename = os.path.basename(obj_file)
        obj_name = os.path.splitext(obj_basename)[0]
        mtl_file_path = os.path.join(obj_dir, f"{obj_name}.mtl")
        texture_file_path = os.path.join(obj_dir, "texture.png")

        # Export the mesh to OBJ format
        mesh.export(obj_file)

        # Check if texture exists
        if hasattr(mesh.visual, 'material') and mesh.visual.material.image:
            # Save the texture to a PNG file
            # texture = mesh.visual.material.image
            # texture.save(texture_file_path)

            # Create a new MTL file
            with open(mtl_file_path, "w") as mtl_file:
                mtl_file.write(f"newmtl material_0\n")
                mtl_file.write(f"Ka 1.000 1.000 1.000\n")  # Ambient color
                mtl_file.write(f"Kd 1.000 1.000 1.000\n")  # Diffuse color
                mtl_file.write(f"Ks 0.000 0.000 0.000\n")  # Specular color
                mtl_file.write(f"d 1.0\n")                # Transparency
                mtl_file.write(f"illum 2\n")             # Illumination model
                mtl_file.write(f"map_Kd {os.path.basename(texture_file_path)}\n")  # Texture map

            # Update the OBJ file to reference the new MTL file
            with open(obj_file, "r") as obj:
                lines = obj.readlines()
            with open(obj_file, "w") as obj:
                obj.write(f"mtllib {os.path.basename(mtl_file_path)}\n")
                obj.writelines(lines)

            print(f"Texture saved as: {texture_file_path}")
            print(f"MTL file created at: {mtl_file_path}")
        else:
            print("No texture found in the PLY file.")

        print(f"Successfully converted {ply_file} to {obj_file} with new MTL.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
ply_file_path = "./model/dense_texture.ply"  # Replace with your PLY file path
obj_file_path = "./output/dense_texture.obj"  # Replace with the desired OBJ file path
ply_to_obj_with_new_mtl(ply_file_path, obj_file_path)
