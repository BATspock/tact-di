import os

APP_PATH = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(APP_PATH, 'static/stl_files/')
image_path = os.path.join(APP_PATH, 'files/images/')


def get_image_path():
    return image_path


def set_image_path(path):
    global image_path
    image_path = path


def get_output_path(self):
    self.output_path = os.path.join(self.output_path, 'stl_files')
    if not os.path.isdir(self.output_path):
        os.mkdir(self.output_path)
    return output_path


def set_output_path(path):
    global output_path
    output_path = path