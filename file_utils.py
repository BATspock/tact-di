import os
import file_paths as file


def save_mesh_to_file(image_path, mesh):
    # Get the file name (excluding extension) from the input image path
    filename = os.path.splitext(os.path.basename(image_path))[0]
    print(filename)
    if not os.path.isdir(file.output_path):
        os.mkdir(file.output_path)
    mesh.save(file.output_path + '/' + 'edited-image' + '.stl')
