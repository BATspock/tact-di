import cv2
import numpy as np
import matplotlib


def get_hsv_from_bgr_image(bgr_image):
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    rgb_image = rgb_image.astype('float32')
    rgb_image = rgb_image/255

    hsv_image = matplotlib.colors.rgb_to_hsv(rgb_image)
    hue_values = hsv_image[:, :, 0]
    saturation_values = hsv_image[:, :, 1]
    brightness_values = hsv_image[:, :, 2]
    hsv_image[:, :, 0] = (hue_values*360).astype('int')
    hsv_image[:, :, 1] = (saturation_values*100).astype('int')
    hsv_image[:, :, 2] = (brightness_values*100).astype('int')
    return hsv_image


def get_hsv_from_bgr_pixel(pixel):
    pixel_arr = [pixel[2], pixel[1], pixel[0]]
    rgb = np.array(pixel_arr)
    rgb_normalized = rgb/255.0
    hsv_pixel_val = matplotlib.colors.rgb_to_hsv(rgb_normalized)
    hue = int(hsv_pixel_val[0]*360)
    sat = int(hsv_pixel_val[1]*100)
    brightness = int(hsv_pixel_val[2]*100)
    hsv = tuple([hue, sat, brightness])
    return hsv


def get_bgr_from_hsv_pixel(pixel):
    hue = pixel[0]/360.0
    sat = pixel[1]/100.0
    brightness = pixel[2]/100.0
    rgb_pixel_normalized = matplotlib.colors.hsv_to_rgb([hue, sat, brightness])
    rgb_pixel = np.multiply(rgb_pixel_normalized, 255).astype('int')
    bgr_pixel = [rgb_pixel[2], rgb_pixel[1], rgb_pixel[0]]
    return tuple(bgr_pixel)
