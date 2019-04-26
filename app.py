from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import grayscale
import os
import colored_images
import hatching
import requests
import warnings
warnings.filterwarnings("ignore")
app = Flask(__name__, static_folder='static')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_URL = ""


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/chooseModel", methods=["POST"])
def upload():
    global IMG_URL
    folder_name = 'files/images/'
    target = os.path.join(APP_ROOT, folder_name)
    if not os.path.isdir(target):
        os.mkdir(target)
    if len(request.files.getlist("file")) != 0:
        if request.form['edited-image'] != "test":
            image_url = request.form['edited-image']
            r = requests.get(image_url)
            with open("edited-image.png", "wb") as f:
                f.write(r.content)
            filename = "edited-image.png"
            IMG_URL = os.path.join(APP_ROOT, filename)
        else:
            img = request.files.getlist("file")[0]
            filename = img.filename
            IMG_URL = "/".join([target, filename])
            img.save(IMG_URL)
    else:
        flash('Drop an image in the drop area first.')
        return redirect(url_for('index'))
    return render_template('choose_model.html', image_name=filename)


@app.route("/download_grayscale", methods=["POST"])
def download_grayscale():
    global IMG_URL
    grayscale.convertGrayScaleToSTL(IMG_URL)
    if os.path.exists("edited-image.png"):
        os.remove("edited-image.png")
    return render_template("preview_stl.html")


@app.route("/download_colored", methods=["POST"])
def download_colored():
    global IMG_URL
    colored_images.convertColoredImageToSTL(IMG_URL)
    return render_template("preview_stl.html")


@app.route("/download_hatching", methods=["POST"])
def download_hatching():
    global IMG_URL
    hatching.convertHatchedImageToSTL(IMG_URL)
    return render_template("preview_stl.html")


@app.route('/static/stl_files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='static/stl_files/', filename=filename)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port= 5000)
