# Most code from http://www.redblobgames.com/grids/hexagons/codegen/output/lib.py
# Editted to match our Point structure (known as "Hex" by the library) by Michael Zoller on 3/25/2016

import collections
import math
import bisect

import sys
sys.path[0] += '/../model'

from point import *

LAYOUT_DRAWING_FUNCS = False
ScreenPoint = collections.namedtuple("ScreenPoint", ["x", "y"])

def pix_add(a, b):
    return ScreenPoint(a.x + b.x, a.y + b.y)

def pix_subtract(a, b):
    return ScreenPoint(a.x - b.x, a.y - b.y)

def pix_scale(a, k):
    return ScreenPoint(a.x * k, a.y * k)

def pix_avg(a, b):
    return ScreenPoint((a.x+b.x)/2, (a.y+b.y)/2)

def hex_round(h):
    hs = -h.x-h.y
    q = int(round(h.x))
    r = int(round(h.y))
    s = int(round(hs))
    q_diff = abs(q - h.x)
    r_diff = abs(r - h.y)
    s_diff = abs(s - hs)
    if q_diff > r_diff and q_diff > s_diff:
        q = -r - s
    else:
       if r_diff > s_diff:
           r = -q - s
       #else: s = -q - r
    return Point(q, r)

if LAYOUT_DRAWING_FUNCS:
    def hex_subtract(a, b):
        return Point(a.x - b.x, a.y - b.y)

    def hex_length(hex):
        return (abs(hex.x) + abs(hex.y) + abs(-hex.x-hex.y)) // 2

    def hex_distance(a, b):
        return hex_length(hex_subtract(a, b))

    def hex_lerp(a, b, t):
        return Point(a.x + (b.x-a.x)*t, a.y + (b.y-a.y)*t)

    def hex_linedraw(a, b):
        N = hex_distance(a, b)
        results = []
        step = 1.0 / max(N, 1)
        for i in range(0, N + 1):
            results.append(hex_round(hex_lerp(a, b, step * i)))
        return results

Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])

Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])

orientation_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, -0.5)
orientation_flat = Orientation(3.0 / 2.0, 0.0, math.sqrt(3.0) / 2.0, math.sqrt(3.0), 2.0 / 3.0, 0.0, -1.0 / 3.0, math.sqrt(3.0) / 3.0, 0.0)

def hex_to_pixel(layout, h):
    M = layout.orientation
    size = layout.size
    origin = layout.origin
    x = (M.f0 * h.x + M.f1 * h.y) * size.x
    y = (M.f2 * h.x + M.f3 * h.y) * size.y
    return ScreenPoint(x + origin.x, y + origin.y)

def pixel_to_hex(layout, p):
    M = layout.orientation
    size = layout.size
    origin = layout.origin
    pt = ScreenPoint((p.x - origin.x) / size.x, (p.y - origin.y) / size.y)
    q = M.b0 * pt.x + M.b1 * pt.y
    r = M.b2 * pt.x + M.b3 * pt.y
    return Point(q, r)

def hex_corner_offset(layout, corner):
    M = layout.orientation
    size = layout.size
    angle = 2.0 * math.pi * (corner + M.start_angle) / 6
#    print "hex_corner_offset: corner=",corner,", angle=",180*angle/math.pi
    return ScreenPoint(size.x * math.cos(angle), size.y * math.sin(angle))

def hex_corner(layout, h, corner):
    return pix_add(hex_to_pixel(layout, h), hex_corner_offset(layout, corner))

def polygon_corners(layout, h):
    corners = []
    center = hex_to_pixel(layout, h)
    for i in range(0, 6):
        offset = hex_corner_offset(layout, i)
        corners.append(ScreenPoint(center.x + offset.x, center.y + offset.y))
    return corners

def pixel_angle(p):
    return math.atan2(p.y, p.x)

hex_angles = [pixel_angle(d) for d in point_directions]
#print hex_angles
assert all(hex_angles[i] < hex_angles[i+1] for i in xrange(len(hex_angles)-1))
#for i in range(6):
#    print point_directions[i], 180*hex_angles[i]/math.pi

# returns the pixel endpoints of the edge the hexagons share
def pix_shared_edge(layout, h1, h2):
    endpoints = [-1, -1]
    center = hex_to_pixel(layout, h1)
    #diff = h1-h2 #wonky solution
    diff = h2-h1 #correct solution
    angle = pixel_angle(diff)
    start_corner = bisect.bisect_left(hex_angles, angle)
    start_corner = (start_corner+4)%6
    end_corner = (start_corner+1)%6
    endpoints[0] = pix_add(center, hex_corner_offset(layout, start_corner))
    endpoints[1] = pix_add(center, hex_corner_offset(layout, end_corner))
#    print "h1:",h1,", h2:",h2,", diff:",diff,", angle:",180*angle/math.pi,", start_corner:",start_corner,", center:",center
    return endpoints
