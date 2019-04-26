import tkinter 
#from Tkinter import *
from tkinter import filedialog
from tkinter import *
#import tkFileDialog
import file_paths as file
import color_conversion_utils as color_converter
import image_properties as prop


def fetch(entries, root):
    for entry in entries:
        field = entry[0]
        text = entry[1].get()
        if text == '':
            prop.get_height_map()[field] = 0
        else:
            prop.get_height_map()[field] = int(text)
    root.destroy()


def makeform(root, colors):
    entries = []
    for color in colors:
        bgr_color = color_converter.get_bgr_from_hsv_pixel(color)
        rgb_color = tuple([bgr_color[2], bgr_color[1], bgr_color[0]])
        background_color = '#%02x%02x%02x' % rgb_color
        row = Frame(root)
        lab = Label(row, width=10, text='', bg=background_color, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT)
        entries.append((color, ent))
    return entries


def assign_height_to_colors(distinct_colors):
    root = Tk()
    root.title("Enter heights")
    instruction = Label(0, text="Please enter the height you want to assign to each color,\n"
                                "in the range 0 to 10. (Blank entries will be considered as 0)", padx=10)
    instruction.pack()
    ents = makeform(root, distinct_colors)
    root.bind('<Return>', (lambda event, e=ents: fetch(e, root)))
    b1 = Button(root, text='Submit', command=(lambda e=ents: fetch(e, root)))
    b1.pack(side=LEFT, padx=5, pady=5)
    root.mainloop()


def browse_image():
    root = Tk()
    def browsefunc():
        filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        pathlabel.config(text=filename)
        file.set_image_path(filename)
        root.destroy()

    instruction = Label(0, text="Choose the image that has to be converted", padx=10)
    instruction.pack()
    browsebutton = Button(root, text="Browse", command=browsefunc)
    browsebutton.pack()

    pathlabel = Label(root)
    pathlabel.pack()
    root.mainloop()
