import numpy as np
from skimage import measure
import cv2
from stl import mesh
from skimage.filters import threshold_otsu
import PIL.Image, PIL.ImageTk
import tkinter


import file_utils
import file_paths as file
import image_properties as prop
from preprocess import preprocess

import color_conversion_utils as color_converter
import color_extraction_utils as color_extractor
import ui_utils_hatching as ui
import file_utils
import file_paths as file
import image_properties as prop
from texton_color_utils import Textons

def get_gray_value_from_color(pixel, distinct_colors):
    gray_value = 0
    matching_color = color_extractor.get_matching_color(pixel, distinct_colors)
    if matching_color is not None:
        gray_value = prop.get_height_map()[matching_color]*0.1
    return gray_value

def convert_from_colored_to_gray(image, distinct_colors):
    rows = image.shape[0]
    cols = image.shape[1]
    gray_image = np.zeros((rows, cols)).astype('float32')
    for i in range(0, rows):
        for j in range(0, cols):
            pixel_val = tuple(image[i, j, :].astype('int'))
            gray_image[i][j] = get_gray_value_from_color(pixel_val, distinct_colors)
    return gray_image

    

def convertHatchedImageToSTL(imageurl):
    image = cv2.imread(imageurl)

    ''''
    # generate copy of original image
    im1 = image.copy()
    # decrease contrast to emboss lines
    ob = preprocess(im1)
    # decrease contrast to emboss lines
    im1 = ob.ChangeContrast(0.5)
    # blur to emboss edges
    im1 = ob.Blur()
    # define kernel for dilate
    kernel = np.ones((5, 5), np.uint8)
    # morphology operations for separating outer lines
    opening = cv2.morphologyEx(im1, cv2.MORPH_OPEN, kernel)
    # detect edges for dilation
    edges = cv2.Canny(opening, 100, 150)

    # img = np.array(image, dtype=np.uint8)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform 'closing' morphological operation on the image
    kernel = np.ones((1, 1), np.uint8)
    gray_image = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)

    # Figure out the scaling parameter according to original size and then scale
    scale = prop.get_scaling_factor()
    gray_image = cv2.resize(gray_image, (0, 0), fx=scale, fy=scale)

    # Normalize all pixels to assume values from 0 to 1
    gray_image = gray_image / 255.0
    gray_image = np.subtract(1.0, gray_image)

    # Find the threshold to separate foreground from background using OTSU's thresholding method
    threshold = threshold_otsu(gray_image)
    (rows, cols) = gray_image.shape
    '''
    textons = Textons(image, 3, 10, 1)
    tex = textons.textons()
    show = np.zeros_like(image)
    colors = np.unique(tex)
    show[tex == colors[1]] = [0,0,255]
    show[tex == colors[2]] = [0,255,255]
    show = cv2.medianBlur(show,5)

    cv2.imwrite('temp.jpg', show)

    distinct_colors = color_extractor.get_top_colors_hsv(show, 10)

    ui.assign_height_to_colors(distinct_colors, 'temp.jpg')

    hsv_image = color_converter.get_hsv_from_bgr_image(show)
    gray_image = convert_from_colored_to_gray(hsv_image, distinct_colors)

    gray_image = cv2.medianBlur(gray_image, 3)

    # Perform 'closing' morphological operation on the image
    kernel = np.ones((1, 1), np.uint8)
    gray_image = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)

    # Figure out the scaling parameter according to original size and then scale
    scale = prop.get_scaling_factor()
    gray_image = cv2.resize(gray_image, (0, 0), fx=scale, fy=scale)

    # Find the threshold to separate foreground from background using OTSU's thresholding method
    threshold = threshold_otsu(gray_image)
    (rows, cols) = gray_image.shape

    '''
    Create a 3D voxel data from the image
    The top-most (#1) and bottom-most (#13) layer will contain all zeros
    The middle 10 layers (#3 to #12) contain the same pixel values as the gray scale image
    There is an additional layer(#2) for the base of the model 
    '''
    layers = 13
    rows += 2
    cols += 2
    voxel = np.zeros((rows, cols, layers))
    voxel[:, :, 1] = np.ones((rows, cols)).astype('float32')

    # making the boundary voxel values to be zero, for the marching cubes algorithm to work correctly
    voxel[0, :, :] = np.zeros((cols, layers)).astype('float32')
    voxel[(rows - 1), :, :] = np.zeros((cols, layers)).astype('float32')

    voxel[:, 0, :] = np.zeros((rows, layers)).astype('float32')
    voxel[:, (cols - 1), :] = np.zeros((rows, layers)).astype('float32')

    '''
    Create the middle 10 layers from the image
    Based on the pixel values the layers are created to assign different heights to different regions in the image
    '''
    for level in range(1, 10):
        level_threshold = level * 0.1
        for j in range(0, rows - 2):
            for k in range(0, cols - 2):
                pixel_value = gray_image[j][k]
                if pixel_value > level_threshold:
                    voxel[j + 1][k + 1][level + 1] = pixel_value

    '''
    Run the marching cubes algorithm to extract surface mesh from 3D volume. Params:
        volume : (M, N, P) array of doubles
            Input data volume to find isosurfaces. Will be cast to `np.float64`.
        level : float
            Contour value to search for isosurfaces in `volume`. If not
            given or None, the average of the min and max of vol is used.
        spacing : length-3 tuple of floats
            Voxel spacing in spatial dimensions corresponding to numpy array
            indexing dimensions (M, N, P) as in `volume`.
        gradient_direction : string
            Controls if the mesh was generated from an isosurface with gradient
            descent toward objects of interest (the default), or the opposite.
            The two options are:
            * descent : Object was greater than exterior
            * ascent : Exterior was greater than object
    '''
    verts, faces, normals, values = measure.marching_cubes_lewiner(volume=voxel, level=threshold,
                                                                   spacing=(1., 1., 1.), gradient_direction='descent')

    # Export the mesh as stl
    mymesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

    for i, f in enumerate(faces):
        for j in range(3):
            mymesh.vectors[i][j] = verts[f[j], :]

    file_utils.save_mesh_to_file(imageurl, mymesh)


def ChangeContrast(self, gamma=1.0):
    """
    change contrast of an image
    gamma value 1 for same image
    gamma value greater than 1 to increase brightness
    gamma value less than 1 to make image darker
    """
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(self.im, table)


if __name__ == "__main__":
    convertHatchedImageToSTL(file.get_image_path())


