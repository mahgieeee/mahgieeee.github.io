import cairo
"""
Created on Wed Dec 27 19:29:20 2017

To summarize, here is how to draw a Sierpinski gasket in a square:
Determine how small the square is. If it's small enough to be a base case, 
then just fill in the square. You get to pick how small "small enough" is.
Otherwise, divide the square into upper left, upper right, lower right, and 
lower left squares. Recursively "solve" three subproblems: 
    1. Draw a Sierpinski gasket in the upper left square. 
    2. Draw a Sierpinski gasket in the upper right square. 
    3. Draw a Sierpinski gasket in the lower right square.
    You need to make not just one, but three recursive calls. 
That is why we consider drawing a Sierpinski gasket to exhibit multiple recursion.
"""

'''
draws a diagonal where vertexes represent a tuple of coordinates (x,y)
'''
def draw_diagonals(vertex_a, vertex_b, vertex_c, vertex_d, context):
    context.move_to(vertex_b)
    context.line_to(vertex_c)
    context.close_path()
    context.move_to(vertex_d)
    context.line_to(vertex_a)
    context.close_path()

#where (0,0) is the starting point        
def draw_sierpinksi(length_square, context, vertex_a, vertex_b, vertex_c, vertex_d,):
    if length_square == 1:
        context.set_source_rgb(0, 0, 0)
        context.fill()
    midpoint = length_square/2
    # move to midpoint of top line 
    context.set_source_rgba(1, 0.2, 0.2, 0.6)
    context.set_line_width(0.02)
    context.move_to(midpoint, 0)
    context.line_to(-midpoint*2, midpoint)
    context.move_to(0, -midpoint)
    context.line_to(-midpoint*2, midpoint)
    context.move_to(vertex_b)
    context.line_to(vertex_c)
    context.move_to(vertex_d)
    context.line_to(vertex_a)
    #offset = midpoint
    #starting_pt = (0, 0)
    draw_sierpinksi(length_square - 2, context, (0, 0 + midpoint), (midpoint, 0), (0, -midpoint), (midpoint, -midpoint)) # upper left
    draw_sierpinksi(length_square - 2, context, (midpoint*2, 0), (midpoint, 0), (midpoint*2, -midpoint), (midpoint, -midpoint)) # upper right share b,d from upperleft
    draw_sierpinksi(length_square - 2, context, (-midpoint*2, -midpoint*2), (midpoint*2, -midpoint),(midpoint*2, -midpoint), (midpoint, -midpoint)) #lower right share c,d upperright
    
    
if __name__ == '__main__':
    width, height = 256, 256
    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context (surface)
    width_square = 250
    context.rectangle(0, 0, width_square, width_square )
    
