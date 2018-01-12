"""

Crash Course in Computational Geometry (as sort-of applied to geospatial programming)

COORDINATE SYSTEMS:
==================

Cartesian coordinates:

    A point is described by (x, y):
    ==============================

    x => x-axis is taken to be horizontal 
    y => y-axis is taken to be vertical 


    In terms of cardinal directions:

            x => east/west
            y => north south

    Generally speaking:

            x+ => east
            x- => west
            y+ => north
            y- => south     

Q1: How do the following points relate to one another?

    a = (0,0)
    b = (3,1)

A1: b is *northeast* of a


Q2: What is the distance between a and b?

        a = (0,0)
        b = (3,1)

Before we can answer that, let's review the Pythagorean theorem!

Where a, b, c are sides of a right triangle:

        a**2 + b**2 = c**2


If I know...

        * the "bottom" of a triangle has length 3
        * the "right hand side" has length 4

... then the hypotenuse must be of length 3**2 + 4**2 == 25 [which is to say, 5**2]

Great! How does this help answer the distance question?

What if I draw a right triangle using the provided points?

Then the distance between the points is just the length of the hypotenuse of the right triangle!

Q2: dist(a,b) # 3.1622... [sqrt(10)]

"""

import math


from cgtips_helper import pairwise


def dist(point_a, point_b):
    return math.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)


def closest_pair_brute(list_of_points):
    """
    Test all pairwise combinations of points.

    If the current distance is smaller than the established min_dist:
            * set min_dist to current_dist
            * store the salient coordintate pair in min_pair
    """
    min_dist = float('inf')

    for pair in pairwise(list_of_points):
            point_a, point_b = pair
            current_dist = dist(point_a, point_b)
            
            if current_dist < min_dist:
                    min_dist = current_dist
                    min_pair = [point_a, point_b]

    return (min_dist, min_pair)


def closest_pair_planar(list_of_points):
    """
    https://en.wikipedia.org/wiki/Closest_pair_of_points_problem#Planar_case
    """
    pass


def counterclockwise(point_a, point_b, point_c):
    """
    https://www.toptal.com/python/computational-geometry-in-python-from-theory-to-implementation
    (See the section entitled "A Rigorous Definition")
    """
    a, b, c = point_a, point_b, point_c
    return (b[0] - a[0]) * (c[1] - a[1]) > (b[1] - a[1]) * (c[0] - a[0])


def clockwise(point_a, point_b, point_c):
    a, b, c = point_a, point_b, point_c
    return (b[0] - a[0]) * (c[1] - a[1]) < (b[1] - a[1]) * (c[0] - a[0])
