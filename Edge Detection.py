from multiprocessing.pool import ThreadPool
from PIL import Image as Im
import threading as thr
import tkinter as tk
import os

root = tk.Tk()
root.withdraw()
## For 'askopenfilename'


def remove_extension(filepath):
    None


def find_edges(original, threshold = 50, noise = 0, mode = "grad_black",
               name = "edges.png"):
    """
    original  : str : filepath to original image
    threshold : int : minimum delta requirement for pixel to be considered
                      an 'edge'
    noise     : int : maximum delta require for pixel to be considered an
                      'edge' ; essentially removes low valued edges
    mode      : str : determines the method of displaying edges. Can be
                      'on_white' , 'overlay' , 'grad_black'
    name      : str : optional name and folder directory (note: directory
                      must exist)
    """

    orig = Im.open(original)
    orig_data = orig.load()
    
    if mode == "grad_black":
        image = Im.new("RGB", (orig.width, orig.height), (0, 0, 0))
    elif mode == "on_white":
        image = Im.new("RGB", (orig.width, orig.height), (255, 255, 255))
    elif mode == "overlay":
        image = Im.open(original)

    data = image.load()

    bot_1 = ThreadPool(1)
    bot_2 = ThreadPool(1)
    bot_3 = ThreadPool(1)
    bot_4 = ThreadPool(1)

    bounds_1 = [0, image.width // 4]
    bounds_2 = [image.width // 4, 2 * image.width // 4]
    bounds_3 = [2 * image.width // 4, int(3/2 * image.width // 4)]
    bounds_4 = [int(3/2 * image.width // 4), image.width - 1]
    ret_1 = bot_1.apply_async(compare_pixels, args = [image, orig, \
                        bounds_1, \
                        [0, image.height - 1], threshold, noise]).get()
    ret_2 = bot_2.apply_async(compare_pixels, args = [image, orig, \
                        bounds_2, \
                        [0, image.height - 1], threshold, noise]).get()
    ret_3 = bot_3.apply_async(compare_pixels, args = [image, orig, \
                        bounds_3, \
                        [0, image.height - 1], threshold, noise]).get()
    ret_4 = bot_4.apply_async(compare_pixels, args = [image, orig, \
                        bounds_4, \
                        [0, image.height - 1], threshold, noise]).get()

    image.paste(ret_1, (bounds_1[0], 0))
    image.paste(ret_2, (bounds_2[0], 0))
    image.paste(ret_3, (bounds_3[0], 0))
    image.paste(ret_4, (bounds_4[0], 0))

    original = os.path.abspath(original)
    name = original[::-1][original[::-1].find("\\"):][::-1] + name
        
    image.save(name)


def compare_pixels(image, original, x_range, y_range, threshold, noise):
    """
    image     : Image : equal to image
    original  : Image : equal to orig
    x_range   : list  : len 2 list of min and max range of x values 
    y_range   : list  : len 2 list of min and max range of y values
    threshold : int   : minimum delta requirement for pixel to be considered
                        an 'edge'
    noise     : int   : maximum delta require for pixel to be considered an
                        'edge' ; essentially removes low valued edges
    """

    data = image.load()
    orig_data = original.load()
    for x in range(x_range[0], x_range[1]):
        for y in range(y_range[0], y_range[1]):
            delta = abs(sum(orig_data[x + 1, y]) - sum(orig_data[x, y]))

            if delta > threshold:
                delta = 255 if delta > 255 else delta

                data[x, y] = (delta, delta, delta)

    for x in range(x_range[0], x_range[1]):
        for y in range(y_range[0], y_range[1]):
            delta = abs(sum(orig_data[x, y + 1]) - sum(orig_data[x, y]))

            if delta > threshold:
                delta = 255 if delta > 255 else delta

                data[x, y] = (delta, delta, delta)
                ## Mutates object directly...

    image = image.crop([x_range[0], y_range[0], x_range[1], y_range[1] + 1])
    
    return image


def remove_noise(filepath, threshold = 10):
    """ Will attempt to remove the 'noise' from an image"""
    ## input an "edge" image and remove artifacts caused by jpeg format
    image = Im.open(filepath)
    data = image.load()

    for x in range(image.width):
        for y in range(image.height):
            if data[x, y][0] < threshold:
                data[x, y] = (0, 0, 0)

    image.save(image.filename)
    
    return data


def find_importance(original, threshold = 50, noise = 0, grid_size = 100,
                    grid_sens = 3000):
    """
    Attempts to display only the important sections of an image
    original  : str : filepath to original image
    threshold : int : minimum delta requirement for pixel to be considered
                      an 'edge'
    noise     : int : maximum delta require for pixel to be considered an
                      'edge' ; essentially removes low valued edges
    grid_size : int : fraction of the total length/width which is considered
                      part of one grid space (ex. grid_size = 100 cuts the image
                      into 100 x 100 grid)
    grid_sens : int : the threshold for which a grid space must exceed to be
                      considered important
    """
    orig_image = Im.open(original)
    create_edges = False
    
    if os.path.exists("edges.png"):
        image = Im.open("edges.png")
        if not (image.width == orig_image.width and \
           image.height == orig_image.height):
            create_edges = True
    if create_edges:
        print("Finding edges...")
        find_edges(original, threshold, noise, "grad_black", "edges.png")
    image = Im.open("edges.png")
    importance = Im.new("RGB", (image.width, image.height))
    

    data = image.load()
    orig_data = orig_image.load()
    importance_data = importance.load()

    grid_space = [[0 for l in range(grid_size)] for w in range(grid_size)]

    print("Finding grid deltas...")
    for x in range(image.width - 1):
        for y in range(image.height - 1):
            x_value = x // (image.width // grid_size + 1)
            y_value = y // (image.height // grid_size + 1)
            #print(x_value, y_value)
            grid_space[x_value][y_value] += data[x,y][0]

    print("Applying grid deltas...")
    for x in range(image.width - 1):
        for y in range(image.height - 1):
            x_value = x // (image.width // grid_size + 1)
            y_value = y // (image.height // grid_size + 1)
            try:
                if grid_space[x_value][y_value] > grid_sens:
                    importance_data[x,y] = orig_data[x,y]
                
                elif grid_space[x_value-1][y_value] > grid_sens and \
                     grid_space[x_value+1][y_value] > grid_sens and \
                     grid_space[x_value][y_value-1] > grid_sens and \
                     grid_space[x_value][y_value+1] > grid_sens:
                    ## Fill in grid_space if all spaces around are filled
                    importance_data[x,y] = orig_data[x,y]
            except IndexError:
                ##x_value-1, +1, etc. out of bounds
                None

    importance.save("importance.png")

    return grid_space


def get_file():
    path = tk.filedialog.askopenfilename()
    return path
