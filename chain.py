#!/usr/bin/env python3

import math
import svgwrite
from collections import deque

dwg = svgwrite.Drawing(filename="chain.svg", debug=True, size=(900,900))

def draw_link(length=80, end_r=30, roller_r=12, bend_deg=45, tilt_deg=0, start=(100,200), colour='black', top=True):
    bend_rad    = math.radians(bend_deg)
    tilt_rad    = math.radians(tilt_deg)
    (sx,sy)     = start
    (rc,rs)     = (end_r*math.cos(bend_rad), end_r*math.sin(bend_rad))
    R           = length/(2.0*math.cos(bend_rad))-end_r
    H           = length/2.0*math.tan(bend_rad)
    if end_r<=length/2 and R<H:
        dx          = length - 2*rc
        dy          = 2*rs

        group   = dwg.g( transform='rotate(%d,%d,%d)' % (-tilt_deg,sx,sy), stroke=colour, stroke_width='2' )

        if top:
            group.add( dwg.path( d="M %d,%d m %d,%d a %d,%d 0 1,0 %d,%d a %d,%d 0 0,1 %d,%d a %d,%d 0 1,0 %d,%d a %d,%d 0 0,1 %d,%d Z"
                        % (sx, sy,  rc, -rs,  end_r, end_r, 0, dy,  R, R, dx, 0,  end_r, end_r, 0, -dy,  R, R, -dx, 0),
                         fill='none' ) )
            group.add( dwg.circle( center=(sx,sy),        r=roller_r, fill='none' ) )
            group.add( dwg.circle( center=(sx+length,sy), r=roller_r, fill='none' ) )
        else:
            group.add( dwg.path( d="M %d,%d m %d,%d a %d,%d 0 0,1 %d,%d m %d,%d a %d,%d 0 0,1 %d,%d"
                        % (sx, sy,  rc, dy-rs,  R, R, dx, 0,  0, -dy,  R, R, -dx, 0),
                        fill='none' ) )

        dwg.add( group )

        return (sx+length*math.cos(tilt_rad), sy-length*math.sin(tilt_rad))

colour_q    = deque(['red', 'blue'])
(sx, sy, abs_tilt, curr_top)  = (400, 100, 0, True)
for i in range(0,16):
    curr_colour = colour_q.popleft()
    (sx, sy)    = draw_link(start=(sx, sy), tilt_deg=abs_tilt, colour=curr_colour, top=curr_top)
    colour_q.append(curr_colour)
    abs_tilt   -= 22.5
    curr_top    = not curr_top

dwg.save()

