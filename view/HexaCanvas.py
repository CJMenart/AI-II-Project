# Hereafter 'stackoverflow' shall refer to the top answer here: http://stackoverflow.com/questions/26583602/displaying-data-in-a-hexagonal-grid-using-python

from Tkinter import *
import tkFont
import math
import random

import layout

import sys
sys.path[0] += '/../model'

import GameState
from tile import *
from point import *
from road import *
from settlement import *
#from turn import *
from resource import *
from player import Player
from simulation import skipToGoodPart, simulateTurnExplain

no_vectorize = False
no_layout_code = False
orientation_pointy = True
debug_coordinates = True
fake_roads = False
fake_settlements = False
skip_to_good_part = True

# This class and 60% of its top 3 functions are from stackoverflow.
# The remainder is original.
class HexaCanvas(Canvas):
    """ A canvas that provides a create-hexagone method """
    def __init__(self, master, hex_layout, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)

        self.hexaSize = 20
        self.hex_layout = hex_layout

    def setHexaSize(self, number):
        self.hexaSize = number


    def create_hexagone(self, center, label="", color = "black", fill="yellow", color1=None, color2=None, color3=None, color4=None, color5=None, color6=None):
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

        pix_center = center if no_layout_code else layout.hex_to_pixel(self.hex_layout, center)

        #if no_layout_code:
        #    center = (x,y)
        #else:
        #    center = layout.ScreenPoint(x,y)

        if no_layout_code:
            size = self.hexaSize
            dx = (size**2 - (size/2)**2)**0.5
            x = center[0]
            y = center[1]

            if no_vectorize:
                point1 = (x+dx, y+size/2)
                point2 = (x+dx, y-size/2)
                point3 = (x   , y-size  )
                point4 = (x-dx, y-size/2)
                point5 = (x-dx, y+size/2)
                point6 = (x   , y+size  )
            else:
                points = [(x+dx, y+size/2),
                          (x+dx, y-size/2),
                          (x   , y-size  ),
                          (x-dx, y-size/2),
                          (x-dx, y+size/2),
                          (x   , y+size  )]
        else:
            points = layout.polygon_corners(self.hex_layout, center)

        if no_vectorize:
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
        else:
            colors = [color1, color2, color3, color4, color5, color6]
            for i in range(len(colors)):
                if colors[i] == None:
                    colors[i] = color

        if no_vectorize:
            self.create_line(point1, point2, fill=color1, width=2)
            self.create_line(point2, point3, fill=color2, width=2)
            self.create_line(point3, point4, fill=color3, width=2)
            self.create_line(point4, point5, fill=color4, width=2)
            self.create_line(point5, point6, fill=color5, width=2)
            self.create_line(point6, point1, fill=color6, width=2)
        else:
	    for i in range(len(points)):
                self.create_line(points[i], points[(i+1)%6], fill=colors[i], width=2)
                #self.create_text(layout.pix_avg(points[i], points[(i+1)%6]), text="{0}".format(i))

        if fill != None:
            if no_vectorize:
                result = self.create_polygon(point1, point2, point3, point4, point5, point6, fill=fill)
            else:
              if no_layout_code:
                result = self.create_polygon(points, fill=fill)
                #self.create_polygon(points[0], points[1], points[2], points[3], points[4], points[5], fill=fill)
              else:
                result = self.create_polygon([(i.x,i.y) for i in points], fill=fill)

        self.create_text(pix_center, text=label)
        return result

    def create_edge(self, endpoints, label="", color = "black"):
        p1 = endpoints[0]
        p2 = endpoints[1]
        result = self.create_line(p1, p2, fill=color, width=4)
        
        self.create_text(layout.pix_avg(p1, p2), text=label)
        return result

    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def create_vertex(self, hex_vert, label="", radius=7, width=1, ffont=None, **kwargs):
        r = radius
        p = layout.hex_to_pixel(self.hex_layout, hex_vert)
        result = []
        result.append(self.create_circle(p.x, p.y, r, width=width, **kwargs))

        if not ffont:
            result.append(self.create_text(p, text=label, justify=CENTER))
        else:
            result.append(self.create_text(p, text=label, justify=CENTER, font=ffont))
        return result

# This class (originally HexagonalGrid) and 50% of its setCell method are from stackoverflow.
# The remainder is original.
class CatanBoard(HexaCanvas):
    """ A grid whose each cell is hexagonal """
    def __init__(self, master, hex_layout, scale, radius_mult = 2, *args, **kwargs):

        #dx     = (scale**2 - (scale/2.0)**2)**0.5
        #width  = 2 * dx * grid_width + dx
        #height = 1.5 * scale * grid_height + 0.5 * scale
        self.hex_layout = hex_layout
        M = hex_layout.orientation
        self.width = (M.f0 * 2 + M.f1 * 2) * scale * radius_mult
        #self.height = (M.f2 * 2 + M.f3 * 2) * scale * radius_mult
        self.height = self.width
        self.robber = []

        HexaCanvas.__init__(self, master, hex_layout, background='white', width=self.width, height=self.height, *args, **kwargs)
        self.setHexaSize(scale)

    def setCell(self, cell, *args, **kwargs ):
        """ Create a content in the cell of coordinates x and y. Could specify options throught keywords : color, fill, color1, color2, color3, color4; color5, color6"""

        #compute pixel coordinate of the center of the cell:
        if False:
            size = self.hexaSize
            dx = (size**2 - (size/2)**2)**0.5

            pix_x = dx + 2*dx*cell[0]
            if yCell%2 ==1 :
                pix_x += dx

            pix_y = size + 1.5*size*cell[1]
            pix_center = (pix_x, pix_y)
        else:
            if not hasattr(cell, 'y'):
                cell = layout.ScreenPoint(cell[0], cell[1])
            if no_layout_code:
                pix_center = layout.hex_to_pixel(self.hex_layout, cell)
            else:
                pix_center = cell
        self.create_hexagone(pix_center, *args, **kwargs)

    def setEdge(self, cell1, cell2, *args, **kwargs):
        endpoints = layout.pix_shared_edge(self.hex_layout, cell1, cell2)
        if debug_coordinates:
            label="({0},{1})->({2},{3})".format(cell1.x, cell1.y, cell2.x, cell2.y)
            self.create_edge(endpoints, label=label, *args, **kwargs)
        else:
            self.create_edge(endpoints, *args, **kwargs)

    def setRobber(self, pos, radius=10, label="R", **kwargs):
        self.robberPos = pos
        for ele in self.robber:
            self.delete(ele)
        pos += Point(0, 0.35)
        if debug_coordinates:
            label = "\n" + label + "\n({0},{1})".format(pos.x, pos.y)
        self.robber = self.create_vertex(pos, label=label, radius=radius, width=2, ffont=tkFont.Font(weight='bold'), **kwargs)

    def setVertex(self, cell1, cell2, cell3, radius=7, label="", **kwargs):
        vertex = layout.ScreenPoint((cell1.x+cell2.x+cell3.x)/3.0, (cell1.y+cell2.y+cell3.y)/3.0)
        if debug_coordinates and label=="":
            label="({0},{1})\n({2},{3})\n({4},{5})".format(cell1.x, cell1.y, cell2.x, cell2.y, cell3.x, cell3.y)
        self.create_vertex(vertex, label=label, radius=radius, **kwargs)

    def setSettlement(self, cell1, cell2, cell3, isCity, **kwargs):
        if isCity:
            self.setVertex(cell1, cell2, cell3, radius = 10, outline="white", width=2, **kwargs)
        else:
            self.setVertex(cell1, cell2, cell3, **kwargs)

# This class contains the remainder of the code from stackoverflow as well as a lot of original code.
class View:
  def __init__(self, game):
    self.game = game
    #game.players.append(Player(len(game.players)))
    nPlayers = len(game.players)
    self.hand_positions = [None] * nPlayers
    self.hand_text = [None] * nPlayers
    self.explain_position = (5, 5)
    self.explain_text = None

    tk = Tk()
    self.tk = tk

    gw = 9.5
    gh = 10
    
    scale = 50
    size = 50
    orientation = layout.orientation_pointy if orientation_pointy else layout.orientation_flat
    origin = layout.ScreenPoint(-scale*orientation.f0/2, -scale*orientation.f2/2)
    hex_layout = layout.Layout(orientation, layout.ScreenPoint(size, size), origin)
    self.board = CatanBoard(tk, hex_layout, scale, radius_mult=3)
    self.board.grid(row=0, column=0, padx=5, pady=5, columnspan=3)

    bw = self.board.width#cget("width")
    bh = self.board.height#cget("height")
    center = Point(bw/2, bh/2)
    for i in range(nPlayers):
        angle = 2.0 * math.pi * i / nPlayers
        pt = center - Point(0.4*bw * math.cos(angle), 0.4*bh * math.sin(angle))
        self.hand_positions[i] = (pt.x, pt.y)

    #origin = layout.ScreenPoint(origin.x * 3, origin.y * 3)
    origin = layout.ScreenPoint(bw/2 - scale*(orientation.f0+orientation.f1)*2, bh/2 - scale*(orientation.f2+orientation.f3)*2)
    self.board.hex_layout = layout.Layout(orientation, layout.ScreenPoint(size, size), origin)

    def correct_quit(tk):
        tk.destroy()
        tk.quit()

    mvRob = Button(tk, text = "Move Robber",command= lambda :self.move_robber())
    mvRob.grid(row=1, column=0)

    nextTurn = Button(tk, text = "Next Turn",command= lambda :self.next_turn())
    nextTurn.grid(row=1, column=1)

    quit = Button(tk, text = "Quit",command= lambda :correct_quit(tk))
    quit.grid(row=1, column=2)

    self.tile_fills = {}
    self.tile_fills[TileType.FIELDS] = "gold"
    self.tile_fills[TileType.FOREST] = "saddle brown"
    self.tile_fills[TileType.MOUNTAINS] = "gray"
    self.tile_fills[TileType.HILLS] = "firebrick"
    self.tile_fills[TileType.PASTURE] = "lawn green"
    self.tile_fills[TileType.DESERT] = "white"

    self.playerColors = ["red", "yellow", "green", "blue", "brown"]

    self.first_time_view(self.game)
    self.tk.mainloop()

  def move_robber(self):
      pts = self.game.robberPos.allAdjacentPoints()
      random.shuffle(pts)
      #print "robberPos:",self.game.robberPos,", pts:",pts
      for p in pts:
          if p.isOnBoard():
              self.board.setRobber(p)
              break

  def next_turn(self):
      gameExplain = simulateTurnExplain(self.game)

      self.game = gameExplain[0]
      self.first_time_view(*gameExplain)

  def first_time_view(self, game, *args):
    for w in self.board.children.values():
        w.destroy()

    randomColors = ['blue', 'red', 'green', 'yellow', 'cyan', 'teal', 'silver', 'white', 'gray']

    if False:
        cells = [(0,0), (1,0), (0,1), (1,1), (2,0), (0,2), (2,1), (1,2), (2,2)]
        for i in xrange(len(cells)):
            self.board.setCell(cells[i], fill=randomColors[i])
        # ex. grid.setCell(0,0, fill='blue')
    else:
        for x in range(0,5):
            for y in range(0,5):
                p = Point(x,y)
                if p.isOnBoard():
                    dNum = game.spaces[x][y].dieNumber
                    label = "{0}".format(dNum) if dNum > 0 else ""
                    if debug_coordinates:
                        label += "\n({0}, {1})".format(x, y)
                    #label = game.spaces[x][y].dieNumber
                    fill = self.tile_fills[game.spaces[x][y].tileType]
                    self.board.setCell(p, label, fill=fill)

        self.board.setRobber(game.robberPos)

        self.view(game, *args)

  def view(self, game, explain=None):
        nPlayers = len(game.players)

        # Just as a test, display fake roads when there aren't any            
        roads = game.roads
        if fake_roads and len(roads) <= 0:
            center = Point(2,2)
            for i in xrange(len(point_directions)):
                h1 = center + point_directions[i]
                h2 = h1 + point_directions[i]
                assert h1 != h2
                #print h1, h2
                roads.append(Road(h1, h2, i%nPlayers))

        for road in roads:
            self.board.setEdge(road.adjHex1, road.adjHex2, color=self.playerColors[road.owner])

        settlements = game.settlements
        if fake_settlements and len(settlements) <= 0:
            s1 = Settlement(Point(1,2), Point(2,2), Point(2,1), 1)
            c1 = Settlement(Point(3,3), Point(3,2), Point(2,3), 2)
            c1.isCity = True
            settlements.append(s1)
            settlements.append(c1)

        for s in settlements:
            self.board.setSettlement(s.adjHex1, s.adjHex2, s.adjHex3, s.isCity, fill=self.playerColors[s.owner])

        for i in range(nPlayers):
            if self.hand_text[i]:
                self.board.delete(self.hand_text[i])

            p = game.players[i]
            text = "id {0}\nWOOL: {1}\nBRICK: {2}\nORE: {3}\nLUMBER: {4}\nGRAIN: {5}".format(p.playerId, p.resources[ResourceType.WOOL], p.resources[ResourceType.BRICK], p.resources[ResourceType.ORE], p.resources[ResourceType.LUMBER], p.resources[ResourceType.GRAIN])
            self.hand_text[i] = self.board.create_text(self.hand_positions[i], text=text)

        if self.explain_text:
            self.board.delete(self.explain_text)
        if explain:
            if isinstance(explain, tuple):
                explain = "Roll: {0}, {1}".format(*explain)
            else:
                explain = str(explain)
            self.explain_text = self.board.create_text(self.explain_position, text=explain, anchor=NW)

if __name__ == "__main__":
    args = map(int, sys.argv[1:])
    if skip_to_good_part:
        View(skipToGoodPart(*args))
    else:
        View(GameState.newGame(*args))
