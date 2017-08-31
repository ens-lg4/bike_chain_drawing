#!/usr/bin/env python3

import math
import svgwrite
from collections import deque


def draw_link(dwg, length=80, end_r=30, roller_r=12, bend_deg=45, tilt_deg=0, start=(100,200), colour='black', top=True):
    bend_rad    = math.radians(bend_deg)
    tilt_rad    = math.radians(tilt_deg)
    (sx,sy)     = start
    (rc,rs)     = (end_r*math.cos(bend_rad), end_r*math.sin(bend_rad))
    R           = length/(2.0*math.cos(bend_rad))-end_r
    H           = length/2.0*math.tan(bend_rad)
    if end_r<=length/2 and R<H:
        dx          = length - 2*rc
        dy          = 2*rs

        group   = dwg.g( transform='rotate(%f,%f,%f)' % (-tilt_deg,sx,sy), stroke=colour, stroke_width='2' )

        if top:
            group.add( dwg.path( d="M %f,%f m %f,%f a %f,%f 0 1,0 %f,%f a %f,%f 0 0,1 %f,%f a %f,%f 0 1,0 %f,%f a %f,%f 0 0,1 %f,%f Z"
                        % (sx, sy,  rc, -rs,  end_r, end_r, 0, dy,  R, R, dx, 0,  end_r, end_r, 0, -dy,  R, R, -dx, 0),
                         fill='none' ) )
            group.add( dwg.circle( center=(sx,sy),        r=roller_r, fill='none' ) )
            group.add( dwg.circle( center=(sx+length,sy), r=roller_r, fill='none' ) )
        else:
            group.add( dwg.path( d="M %f,%f m %f,%f a %f,%f 0 0,1 %f,%f m %f,%f a %f,%f 0 0,1 %f,%f"
                        % (sx, sy,  rc, dy-rs,  R, R, dx, 0,  0, -dy,  R, R, -dx, 0),
                        fill='none' ) )

        dwg.add( group )

        return (sx+length*math.cos(tilt_rad), sy-length*math.sin(tilt_rad))

def even_links_ring(n=8, ring_filename='ring.svg', colours=['red', 'blue']):
    dwg = svgwrite.Drawing(filename=ring_filename, debug=True, size=(900,900))
    rel_tilt_deg    = 360.0/n
    colour_q        = deque(colours)
    (sx, sy, abs_tilt_deg, curr_top)  = (450, 100, 0, True)
    for i in range(0,n):
        curr_colour     = colour_q.popleft()
        (sx, sy)        = draw_link(dwg, start=(sx, sy), tilt_deg=abs_tilt_deg, colour=curr_colour, top=curr_top)
        colour_q.append(curr_colour)
        abs_tilt_deg   -= rel_tilt_deg
        curr_top        = not curr_top

    dwg.save()

def regular_star(n=8, star_filename='star.svg', colours=['red', 'blue']):
    dwg = svgwrite.Drawing(filename=star_filename, debug=True, size=(900,900))
    concave_deg     = 360.0/n
    convex_deg      = -720.0/n
    colour_q        = deque(colours)
    (sx, sy, abs_tilt_deg, curr_top)  = (450, 200, 0, True)
    for i in range(0,2*n):
        curr_colour     = colour_q.popleft()
        (sx, sy)        = draw_link(dwg, start=(sx, sy), tilt_deg=abs_tilt_deg, colour=curr_colour, top=curr_top)
        colour_q.append(curr_colour)
        abs_tilt_deg   += convex_deg if curr_top else concave_deg
        curr_top        = not curr_top

    dwg.save()

even_links_ring(n=6, ring_filename="six_links_ring.svg")
even_links_ring(n=16, ring_filename="sixteen_links_ring.svg")
regular_star(n=6, star_filename="six_pointed_star.svg")
regular_star(n=8, star_filename="eight_pointed_star.svg")
