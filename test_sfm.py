from sfm import generate_dense_point_cloud, generate_texture, reconstruct

project_name = './projects/lab'

if __name__=="__main__":
    result = reconstruct(project_name)

    print(result)