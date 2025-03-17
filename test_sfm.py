from sfm import generate_dense_point_cloud, generate_texture, reconstruct

project_name = 'lab'

if __name__=="__main__":
    result = generate_texture(project_name)

    print(result)