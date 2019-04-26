from collections import defaultdict

import color_conversion_utils as color_converter


def get_matching_color(color_to_be_matched, color_list):
    hue = color_to_be_matched[0]
    sat = color_to_be_matched[1]
    brightness = color_to_be_matched[2]
    if sat < 10 and brightness > 90:
        return tuple([0, 0, 100])
    if sat < 10 and brightness < 10:
        return tuple([0, 0, 0])
    for color in color_list:
        color_hue = color[0]
        color_sat = color[1]
        color_brightness = color[2]
        if hue in range(color_hue - 5, color_hue + 5) and sat in range(color_sat - 10, color_sat + 10)\
                and brightness in range(color_brightness - 10, color_brightness + 10):
            return color
    return None


def deduplicate_entries(colors_map, top_colors_limit, total_number_of_pixels):
    top_colors = {}
    top_colors[(0, 0, 100)] = 0
    top_colors[(0, 0, 0)] = 0
    for color in colors_map:
        matching_color = get_matching_color(color, top_colors.keys())
        print(matching_color)
        if matching_color is None:
            top_colors[color] = colors_map[color]
        else:
            top_colors[matching_color] += colors_map[color]
    top_colors_filtered = {k: v for k, v in top_colors.items() if v/float(total_number_of_pixels)*100 > 0.1}
    top_colors_sorted = sorted(top_colors_filtered, key=top_colors_filtered.get, reverse=True)
    return top_colors_sorted[0:top_colors_limit]


def get_top_colors_hsv(image, no_of_colors):
    # map storing the frequency of each pixel color (in bgr) present in the image
    color_freq_map = defaultdict(int)
    (rows, cols, levels) = image.shape
    for i in range(0, rows):
        for j in range(0, cols):
            pixel_color = tuple(image[i, j, :].astype('int'))
            color_freq_map[pixel_color] += 1
    sorted_colors = sorted(color_freq_map, key=color_freq_map.get, reverse=True)
    top_colors = sorted_colors[0:100]
    top_colors_map = {}
    for color in top_colors:
        hsv_color = color_converter.get_hsv_from_bgr_pixel(color)
        if hsv_color in top_colors_map:
            top_colors_map[hsv_color] += color_freq_map[color]
        else:
            top_colors_map[hsv_color] = color_freq_map[color]
    top_colors_hsv = deduplicate_entries(top_colors_map, no_of_colors, rows*cols)
    return top_colors_hsv

