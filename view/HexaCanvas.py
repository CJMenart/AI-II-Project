# Most code from top answer here: http://stackoverflow.com/questions/26583602/displaying-data-in-a-hexagonal-grid-using-python
# Editted to play with layout.py by Michael Zoller on 3/25/2016

from Tkinter import *
#from layout import *
import layout

class HexaCanvas(Canvas):
    """ A canvas that provides a create-hexagone method """
    def __init__(self, master, hex_layout, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)

        self.hexaSize = 20
        self.hex_layout = hex_layout

    def setHexaSize(self, number):
        self.hexaSize = number


    def create_hexagone(self, x, y, label="0", color = "black", fill="yellow", color1=None, color2=None, color3=None, color4=None, color5=None, color6=None):
        """ 
        Compute coordinates of 6 points relative to a center position.
        Point are numbered following this schema :

        Points in euclidiean grid:  
                    6

                5       1
                    .
                4       2

                    3

        Each color is applied to the side that link the vertex with same number to its following.
        Ex : color 1 is applied on side (vertex1, vertex2)

        Take care that tkinter ordinate axes is inverted to the standard euclidian ones.
        Point on the screen will be horizontally mirrored.
        Displayed points:

                    3
              color3/      \color2      
                4       2
            color4|     |color1
                5       1
              color6\      /color6
                    6

        """
        size = self.hexaSize
        dx = (size**2 - (size/2)**2)**0.5

        point1 = (x+dx, y+size/2)
        point2 = (x+dx, y-size/2)
        point3 = (x   , y-size  )
        point4 = (x-dx, y-size/2)
        point5 = (x-dx, y+size/2)
        point6 = (x   , y+size  )
        point0 = (x,y)

        #this setting allow to specify a different color for each side.
        if color1 == None:
            color1 = color
        if color2 == None:
            color2 = color
        if color3 == None:
            color3 = color
        if color4 == None:
            color4 = color
        if color5 == None:
            color5 = color
        if color6 == None:
            color6 = color

        self.create_line(point1, point2, fill=color1, width=2)
        self.create_line(point2, point3, fill=color2, width=2)
        self.create_line(point3, point4, fill=color3, width=2)
        self.create_line(point4, point5, fill=color4, width=2)
        self.create_line(point5, point6, fill=color5, width=2)
        self.create_line(point6, point1, fill=color6, width=2)

        if fill != None:
            self.create_polygon(point1, point2, point3, point4, point5, point6, fill=fill)

        self.create_text(point0, text=label)

class HexagonalGrid(HexaCanvas):
    """ A grid whose each cell is hexagonal """
    def __init__(self, master, scale, grid_width, grid_height, hex_layout, *args, **kwargs):

        dx     = (scale**2 - (scale/2.0)**2)**0.5
        width  = 2 * dx * grid_width + dx
        height = 1.5 * scale * grid_height + 0.5 * scale
        self.hex_layout = hex_layout

        HexaCanvas.__init__(self, master, hex_layout, background='white', width=width, height=height, *args, **kwargs)
        self.setHexaSize(scale)

    def setCell(self, xCell, yCell, *args, **kwargs ):
        """ Create a content in the cell of coordinates x and y. Could specify options throught keywords : color, fill, color1, color2, color3, color4; color5, color6"""

        #compute pixel coordinate of the center of the cell:
        if False:
            size = self.hexaSize
            dx = (size**2 - (size/2)**2)**0.5

            pix_x = dx + 2*dx*xCell
            if yCell%2 ==1 :
                pix_x += dx

            pix_y = size + yCell*1.5*size
        else:
            pix = layout.hex_to_pixel(hex_layout, layout.ScreenPoint(xCell, yCell))
            pix_x = pix.x
            pix_y = pix.y
        self.create_hexagone(pix_x, pix_y, *args, **kwargs)



if __name__ == "__main__":
    tk = Tk()

    scale = 50
    size = 50
    hex_layout = layout.Layout(layout.orientation_pointy, layout.ScreenPoint(size, size), layout.ScreenPoint(0, size*layout.orientation_pointy.f0))
    grid = HexagonalGrid(tk, scale = scale, grid_width=6, grid_height=6, hex_layout=hex_layout)
    grid.grid(row=0, column=0, padx=5, pady=5)

    def correct_quit(tk):
        tk.destroy()
        tk.quit()

    quit = Button(tk, text = "Quit", command = lambda :correct_quit(tk))
    quit.grid(row=1, column=0)

    if False:
        grid.setCell(0,0, fill='blue')
        grid.setCell(1,0, fill='red')
        grid.setCell(0,1, fill='green')
        grid.setCell(1,1, fill='yellow')
        grid.setCell(2,0, fill='cyan')
        grid.setCell(0,2, fill='teal')
        grid.setCell(2,1, fill='silver')
        grid.setCell(1,2, fill='white')
        grid.setCell(2,2, fill='gray')
    else:
        for x in range(0,5):
            for y in range(0,5):
                if (x+y) in range(2,7):
                    label = "({0}, {1})".format(x, y)
                    grid.setCell(x,y, label)

    tk.mainloop()
