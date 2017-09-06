#!/usr/bin/env python3

import math
import svgwrite
from collections import deque

class BikeChain:

    def __init__(self, length=80, r=30, roller_r=12, bend_deg=45):
        self.length     = length
        self.r          = r
        self.roller_r   = roller_r
        self.bend_rad   = math.radians(bend_deg)
        self.R          = self.length/(2.0*math.cos(self.bend_rad))-self.r
        self.H          = self.length/2.0*math.tan(self.bend_rad)
        self.rc         = self.r*math.cos(self.bend_rad)
        self.rs         = self.r*math.sin(self.bend_rad)
        self.dx         = self.length - 2*self.rc
        self.dy         = 2*self.rs
        if not( self.r<=self.length/2 and self.R<self.H):
            print("The parameters of BikeChain link are out of bounds")


    def min_angle_deg(self):
        "Report the minimal angle constained by the parameters of the chain"
        return math.degrees( 2*math.asin(self.r/self.length) )


    def add_horizontal_link(self, dwg, target_group, top=True):
        "Draw one horizontal link of the chain on a rotated and translated group element"
        if top:
            target_group.add( dwg.path( d="M %f,%f a %f,%f 0 1,0 %f,%f a %f,%f 0 0,1 %f,%f a %f,%f 0 1,0 %f,%f a %f,%f 0 0,1 %f,%f Z"
                % (self.rc, -self.rs,
                   self.r, self.r, 0, self.dy,
                   self.R, self.R, self.dx, 0,
                   self.r, self.r, 0, -self.dy,
                   self.R, self.R, -self.dx, 0),
                fill='none' ) )
            target_group.add( dwg.circle( center=(0,0),           r=self.roller_r, fill='none' ) )
            target_group.add( dwg.circle( center=(self.length,0), r=self.roller_r, fill='none' ) )
        else:
            target_group.add( dwg.path( d="M %f,%f a %f,%f 0 0,1 %f,%f m %f,%f a %f,%f 0 0,1 %f,%f"
                        % (self.rc,  self.dy-self.rs,  self.R, self.R,  self.dx, 0,
                           0,       -self.dy,          self.R, self.R, -self.dx, 0),
                        fill='none' ) )


    def draw_chain_loop(self, filename='chain_loop.svg', turns=[90], colours=['red', 'blue'], canvas_size=(900,900)):
        "Given a sequence of turn angles iterate drawing links on rotated+translated groups until one full turn is accumulated"
        dwg         = svgwrite.Drawing(filename=filename, debug=True, size=canvas_size)
        turn_q      = deque(turns)
        colour_q    = deque(colours)
        (sx, sy, abs_tilt_deg, curr_top)  = (canvas_size[0]/2, canvas_size[1]/4, 0, True)
        while abs_tilt_deg!=360:
            curr_turn       = turn_q.popleft()
            curr_colour     = colour_q.popleft()

            target_group    = dwg.g( transform='translate(%f,%f),rotate(%f,0,0)' % (sx,sy,abs_tilt_deg), stroke=curr_colour, stroke_width='2' )
            self.add_horizontal_link(dwg, target_group, top=curr_top)
            dwg.add( target_group )

            turn_rad        = math.radians(abs_tilt_deg)
            sx             += self.length*math.cos(turn_rad)
            sy             += self.length*math.sin(turn_rad)

            abs_tilt_deg   += curr_turn
            turn_q.append(curr_turn)
            colour_q.append(curr_colour)
            curr_top        = not curr_top

        dwg.save()


def draw_regular_ring(n=8, filename='ring.svg', colours=['red', 'blue']):
    "Draw a regular ring out of a given number of links"
    chain           = BikeChain()
    convex_deg      = 360.0/n
    chain.draw_chain_loop(filename=filename, turns=[convex_deg])


def draw_regular_star(n=8, filename='star.svg', colours=['red', 'blue'], safe_gap=5):
    "Draw a regular star with given number of points; avoid links bumping into each other for v.acute angles by pulling the star apart a bit"
    chain           = BikeChain()
    min_angle_deg   = chain.min_angle_deg()
    concave_deg     = 360.0/n
    convex_deg      = 720.0/n
    if 180-convex_deg < min_angle_deg+safe_gap:
        delta           = safe_gap+min_angle_deg+convex_deg-180
        convex_deg     -= delta
        concave_deg    -= delta
    chain.draw_chain_loop(filename=filename, turns=[-concave_deg, convex_deg])


if __name__ == '__main__':
    draw_regular_ring(n=6,  filename="ring_6.svg")
    draw_regular_ring(n=16, filename="ring_16.svg")
    draw_regular_star(n=3,  filename="star_3.svg")
    draw_regular_star(n=5,  filename="star_5.svg")
    draw_regular_star(n=6,  filename="star_6.svg")
    draw_regular_star(n=8,  filename="star_8.svg")
