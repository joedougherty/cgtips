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
from random import randint
import matplotlib
import matplotlib.pyplot as plt

from cgtips_helper import pairwise


matplotlib.interactive(True)


TEST_POINTS = [(3, 4), (7, 4), (2, 4), (1, 3), (5, 5), (4, 7), (0, 5), 
                       (3, 5), (8, 10), (10, 6), (9, 1)] 


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


'''
def closest_pair_planar(list_of_points, initial_call=True):
    num_of_points = len(list_of_points)

    if num_of_points < 4:
        return closest_pair_brute(list_of_points)

    # Step 1 -- sort points if not yet sorted!
    if initial_call:
        points_sorted_by_x = sorted(list_of_points, key=lambda p: p[0])
        points_sorted_by_y = sorted(list_of_points, key=lambda p: p[1])

    # Step 2 -- split points into left and right halves
    left_half, right_half = split_list(points_sorted_by_x)
        
    # Step 3 -- recurse!
    left_side_min_dist = closest_pair_planar(left_half, initial_call=False)
    right_side_min_dist = closest_pair_planar(right_half, initial_call=False)

    # Step 4 -- What about the middle "strip"?
    #
    # Find the upperbound of the distance "around" the vertical partition line
    if left_side_min_dist[0] < right_side_min_dist[0]:
        d, min_pair = left_side_min_dist
    else:
        d, min_pair = right_side_min_dist

    # Use the average of these two points to locate 
    # the midpoint x-coordinate of the partitioning vertical ray
    x_ray = (left_half[-1][0] + right_half[0][0])/2.0 

    points_around_x_ray = build_strip(points_sorted_by_y, x_ray, d)

    # Check only the first 7 points
    # 
    # In its current form, this builds a collection of (min_dist, [point_a, point_b]) tuples.
    strip_dist_collection = []
    for idx, point in enumerate(points_around_x_ray):
        strip_dist_collection.append(check_next_seven_points(points_around_x_ray, idx))

    # Easiest thing to do for now is find the min dist in this collection
    smallest_dist_in_strip = strip_dist_collection[0][0]
    for dist_tuple in strip_dist_collection:
        if dist_tuple[0] < smallest_dist_in_strip:
            smallest_dist_in_strip = dist_tuple[0]
            point_pair = dist_tuple[1]

    if d < smallest_dist_in_strip:
        return (d, min_pair)
    else:
        return (smallest_dist_in_strip, point_pair)
'''

def build_strip(list_of_points, x_ray_coord, dist_bound):
    strip = []
    left_bound = x_ray_coord - dist_bound
    right_bound = x_ray_coord + dist_bound

    for point in list_of_points:
        if point[0] > left_bound and point[1] < right_bound:
            strip.append(point)
    return strip


def check_next_seven_points(points_collection, starting_point_idx):
    # This can likely be replaced with a more salient value
    # (You ought to be able to pass in a dist value at invocation time)
    min_dist = float('inf') 

    point_in_question = points_collection[starting_point_idx]

    # Next seven points
    relevant_points = points_collection[idx+1:idx+8]
   
    for point in relevant_points:
        curr_dist = dist(point_in_question, relevant_point) 
        if curr_dist < min_dist:
            min_dist = curr_dist
            min_pair = [point_in_question, relevant_point]

    return (min_dist, min_pair)


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


def points_on_a_plane(num_of_points, min_val=None, max_val=None, unique_points=True):
    if not min_val:
        min_val = 0

    if not max_val:
        max_val = 10

    if unique_points:
        points = set()
        while len(points) < num_of_points:
            new_point = (randint(min_val, max_val), randint(min_val, max_val))
            points.add(new_point)
    else:
        points = []
        while len(points) < num_of_points:
            new_point = (randint(min_val, max_val), randint(min_val, max_val))
            points.append(new_point)

    return list(points)


def plot_points(list_of_points):
    x_coords = [i[0] for i in list_of_points]
    y_coords = [i[1] for i in list_of_points]

    plt.scatter(x_coords, y_coords)
    plt.show()
