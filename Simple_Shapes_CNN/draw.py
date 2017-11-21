"""
Created on Fri Oct 27 18:41:03 2017
Draws images of shapes of circles, rectangles, squares, triangles 
@author: maggie
"""
from __future__ import print_function #python 2
import cairo
import random 
from multiprocessing import Pool
import argparse
"""
to execute this via command line:
python draw.py --draw-func draw_circle --num-images 100 --file-dir test_set_args/circle1/circle_ 
"""
def draw_objects(object, file_dir, filename):
    canvas = object(300,300)
    obj1 = canvas.background_color()
    canvas.fill_circle(obj1)
    obj2 = canvas.new_context()
    canvas.line_circle(obj2)
    obj3 = canvas.new_context()
    canvas.line_triangle(obj3)
    obj4 = canvas.new_context()
    canvas.fill_triangle(obj4)
    obj5 = canvas.new_context()
    canvas.line_rectangle(obj5)
    obj6 = canvas.new_context()
    canvas.fill_rectangle(obj6)
    obj7 = canvas.new_context()
    canvas.line_square(obj7)
    obj8 = canvas.new_context()
    canvas.fill_square(obj8)
    canvas.save_img(file_dir, filename)

def draw_rectangle(object, file_dir, filename):
    canvas = object(300,300)
    bg_obj = canvas.background_color()
    canvas.line_rectangle(bg_obj)
    context_obj = canvas.new_context()
    canvas.fill_rectangle(context_obj)
    canvas.save_img(file_dir, filename)

def draw_circle(object, file_dir, filename):
    canvas = object(300,300)
    bg_obj = canvas.background_color()
    canvas.fill_circle(bg_obj)
    context_obj = canvas.new_context()
    canvas.line_circle(context_obj)
    canvas.save_img(file_dir, filename)

def draw_square(object, file_dir, filename):
    canvas = object(300,300)
    bg_obj = canvas.background_color()
    canvas.line_square(bg_obj)
    context_obj = canvas.new_context()
    canvas.fill_square(context_obj)
    canvas.save_img(file_dir, filename)

def draw_triangle(object, file_dir, filename):
    canvas = object(300,300)
    bg_obj = canvas.background_color()
    canvas.line_triangle(bg_obj)
    context_obj = canvas.new_context()
    canvas.fill_triangle(context_obj)
    canvas.save_img(file_dir, filename)
     
class Draw(object):
 
    def __init__(self, canvas_width, canvas_height):
        import numpy as np
        self.canvas_width = int(canvas_width)
        self.canvas_height = int(canvas_height)
        self.data = np.zeros ((self.canvas_width, self.canvas_height, 4),
                                dtype = np.uint64)
        self.surface = cairo.ImageSurface.create_for_data(self.data, 
                                                          cairo.FORMAT_ARGB32,
                                                          self.canvas_width,
                                                          self.canvas_height)
    
    def run(self, draw_func = 'draw_circle', num_images = '100', 
            file_dir = 'test_set_args/circle1/circle_', **args):
        p = Pool(processes=4)
    
        for x in range(int(num_images)):
            # eval converts from string to function call 
            p.apply_async(eval(draw_func), (Draw, str(file_dir), str(x)) )
        p.close()
        p.join()
        
    def new_context(self):
        return cairo.Context(self.surface)
    
    # the next image drawn on background color must have the same context name as 
    # the parameter in background_color
    def background_color(self):
        r = random.uniform(0,1)
        g = random.uniform(0,1)
        b = random.uniform(0,1)
        name = self.new_context() 
        name.set_source_rgb(r,g,b)
        name.paint()
        return name
    
    def fill_circle(self, object):
        import math
        r = random.uniform(0,1)
        g = random.uniform(0,1)
        b = random.uniform(0,1)
        xc = random.randint(10,300)
        yc = random.randint(10,300)
        radius = random.randint(50,150)
        object.arc(xc, yc, radius, 0, 2*math.pi)
        object.set_source_rgb(r, g, b)
        object.fill()
    
    def line_circle(self, object):
        import math
        r = random.uniform(0,1)
        g = random.uniform(0,1)
        b = random.uniform(0,1)
        xc = random.randint(10,300)
        yc = random.randint(10,300)
        radius = random.randint(50,150)
        w = random.uniform(0,10)
        object.arc(xc, yc, radius, 0, 2*math.pi)
        object.set_line_width(w)
        object.set_source_rgb(r, g, b)
        object.stroke()
    
    def fill_rectangle(self, object):
        r = random.uniform(0,1)
        g = random.uniform(0,1)
        b = random.uniform(0,1)
        x = random.randint(50,300)
        y = random.randint(50,300)
        width = random.randint(50,250)
        height = random.randint(50,250)
        object.rectangle(x, y, width, height)
        object.set_source_rgb(r, g, b)
        object.fill()
    
    def line_rectangle(self, object):
        r = random.uniform(0,1)
        g = random.uniform(0,1)
        b = random.uniform(0,1)
        x = random.randint(10,300)
        y = random.randint(10,300)
        w = random.uniform(0,10)
        width = random.randint(50,250)
        height = random.randint(50,250)
        object.rectangle(x, y, width, height)
        object.set_line_width(w)
        object.set_source_rgb(r, g, b)
        object.stroke()
        
    def fill_square(self, object):
        r = random.uniform(0,1)
        g = random.uniform(0,1)
        b = random.uniform(0,1)
        x = random.randint(50,300)
        y = random.randint(50,300)
        width = random.randint(50,250)
        object.rectangle(x, y, width, width)
        object.set_source_rgb(r, g, b)
        object.fill()
        
    def line_square(self, object):
        r = random.uniform(0,1)
        g = random.uniform(0,1)
        b = random.uniform(0,1)
        x = random.randint(50,300)
        y = random.randint(50,300)
        w = random.uniform(0,10)
        width = random.randint(50,250)
        object.rectangle(x, y, width, width)
        object.set_line_width(w)
        object.set_source_rgb(r, g, b)
        object.stroke()
        
    def fill_triangle(self, object):
        r = random.uniform(0,1)
        g = random.uniform(0,1)
        b = random.uniform(0,1)
        x = random.randint(50,300)
        y = random.randint(50,300)
        x1 = random.randint(50,300)
        y1 = random.randint(50,300)
        y2 = random.randint(50,300)
        object.move_to(x,y)
        object.line_to(x, y1)
        object.line_to(x1, y2)
        object.line_to(x, y)
        object.set_source_rgb(r, g, b)
        object.fill()
        
    def line_triangle(self, object):
        r = random.uniform(0,1)
        g = random.uniform(0,1)
        b = random.uniform(0,1)
        x = random.randint(50,300)
        y = random.randint(50,300)
        x1 = random.randint(50,300)
        y1 = random.randint(50,300)
        y2 = random.randint(50,300)
        w = random.uniform(0,3)
        object.move_to(x,y)
        object.line_to(x, y1)
        object.line_to(x1, y2)
        object.line_to(x, y)
        object.set_line_width(w)
        object.set_source_rgb(r, g, b)
        object.stroke()
        
    def save_img(self, file_dir, filename):
        print (filename)
        # dir = "test_set/circle1/"
        # dir = "test_set_args/circle1/" 
        # intersection = "circle."
        self.surface.write_to_png(file_dir + filename + ".png")
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-dir',
                        help='directory to save the images')
    parser.add_argument('--num-images',
                        help='number of images')
    parser.add_argument('--draw-func',
                        help='draw-functions: draw_objects, draw_rectangle, draw_square, draw_circle, draw_triangle')
    args = parser.parse_args()
    arguments = args.__dict__
    d = Draw(300, 300)
    d.run(**arguments)

    
