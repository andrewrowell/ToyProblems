import world
from random import *

DEBUG_MERGING = False

WIDTH = 12
HEIGHT = 12

def rectangles_contain_bad_point(rectangle_a, rectangle_b, world):
    for bad_point in world.bad_points:
        if min(rectangle_a.x, rectangle_b.x) < bad_point.x < max(rectangle_a.x + rectangle_a.width - 1,
                                                                 rectangle_b.x + rectangle_b.width - 1):
            if min(rectangle_a.y, rectangle_b.y) < bad_point.y < max(rectangle_a.y + rectangle_a.height - 1,
                                                                     rectangle_b.y + rectangle_b.height - 1):
                print_debug_merging("Can't merge " + str(world.rectangles.index(rectangle_a)) + " with " + str(world.rectangles.index(
                    rectangle_b)) + " because they have a bad point in the way")
                return False
    return True


def can_merge(rectangle_a, rectangle_b, world):
    if rectangle_a == rectangle_b:
        print_debug_merging("Can't merge " + str(world.rectangles.index(rectangle_a)) + " with itself")
        return False
    if (rectangle_a.x != rectangle_b.x and rectangle_a.y != rectangle_b.y):
        print_debug_merging("Can't merge " + str(world.rectangles.index(rectangle_a)) + " with " + str(world.rectangles.index(rectangle_b)) + " because they do not share an axis")
        return False
    # Same x, different y. Merging on the Y axis means they need to have the same width.
    if rectangle_a.x == rectangle_b.x:
        if (rectangle_a.width != rectangle_b.width):
            print_debug_merging("Can't merge " + str(world.rectangles.index(rectangle_a)) + " with " + str(world.rectangles.index(
                rectangle_b)) + " because they have mismatching widths")
            return False
        # Check if b starts at the end of a
        if (rectangle_a.y < rectangle_b.y):
            if (rectangle_a.y + rectangle_a.height != rectangle_b.y):
                print_debug_merging("Can't merge " + str(world.rectangles.index(rectangle_a)) + " with " + str(world.rectangles.index(
                    rectangle_b)) + " because a's y + height does not equal b's y")
                return False
        else:
            if (rectangle_b.y + rectangle_b.height != rectangle_a.y):
                print_debug_merging("Can't merge " + str(world.rectangles.index(rectangle_a)) + " with " + str(world.rectangles.index(
                    rectangle_b)) + " because b's y + height does not equal a's y ")
                return False
        # Check if a bad point is in the way
        return rectangles_contain_bad_point(rectangle_a, rectangle_b, world)
    # Same y, different x. Merging on the X axis means they need to have the same height.
    if (rectangle_a.y == rectangle_b.y):
        if (rectangle_a.height != rectangle_b.height):
            print_debug_merging("Can't merge " + str(world.rectangles.index(rectangle_a)) + " with " + str(world.rectangles.index(
                rectangle_b)) + " because they do not have the same height")
            return False
        # Check if a starts at the end of b
        if (rectangle_a.x < rectangle_b.x):
            if rectangle_a.x + rectangle_a.width != rectangle_b.x:
                print_debug_merging("Can't merge " + str(world.rectangles.index(rectangle_a)) + " with " + str(world.rectangles.index(
                    rectangle_b)) + " because a's x + width does not equal b's x")
                return False
        else:
            if rectangle_b.x + rectangle_b.width != rectangle_a.x:
                print_debug_merging("Can't merge " + str(world.rectangles.index(rectangle_a)) + " with " + str(world.rectangles.index(
                    rectangle_b)) + " because b's x + width does not equal a's x")
                return False

        # Check if a bad point is in the way
        return rectangles_contain_bad_point(rectangle_a, rectangle_b, world)

def merge(rectangle_a, rectangle_b, world):
    assert (can_merge(rectangle_a, rectangle_b, world))
    # Same x, different y
    if (rectangle_a.x == rectangle_b.x):
        if (rectangle_a.y < rectangle_b.y):
            rectangle_a.height += rectangle_b.height
            rectangle_a.good_points += rectangle_b.good_points
            world.rectangles.remove(rectangle_b)
            return
        else:
            rectangle_b.height += rectangle_a.height
            rectangle_b.good_points += rectangle_a.good_points
            world.rectangles.remove(rectangle_a)
            return
    # Same y, different x
    if (rectangle_a.y == rectangle_b.y):
        if (rectangle_a.x < rectangle_b.x):
            rectangle_a.width += rectangle_b.width
            rectangle_a.good_points += rectangle_b.good_points
            world.rectangles.remove(rectangle_b)
            return
        else:
            rectangle_b.width += rectangle_a.width
            rectangle_b.good_points += rectangle_a.good_points
            world.rectangles.remove(rectangle_a)
            return


def bad_points_contains_point(bad_points, point_a):
    for point_b in bad_points:
        if point_a.x == point_b.x and point_a.y == point_b.y:
            return True
    return False


def print_debug_merging(i):
    if DEBUG_MERGING:
        print(i)

best_world = None

for run_count in range(100):
    print(run_count)
    bad_points = []
    for _ in range(10):
        bad_point = world.BadPoint(randint(0, WIDTH - 2) + 0.5, randint(0, HEIGHT - 2) + 0.5)
        while (bad_points_contains_point(bad_points, bad_point)):
            bad_point = world.BadPoint(randint(0, WIDTH - 2) + 0.5, randint(0, HEIGHT - 2) + 0.5)
        bad_points.append(bad_point)

    example_world = world.World(WIDTH, HEIGHT, [], bad_points)
    example_world.add_rectangle_for_each_good_point()

    for _ in range(len(example_world.rectangles) * 10):
        rectangle_count = len(example_world.rectangles)
        chosen_rectangle_index = randint(0, rectangle_count - 1)
        rectangle_a = example_world.rectangles[randint(0, rectangle_count - 1)]
        for rectangle_b in example_world.rectangles:
            if (can_merge(rectangle_a, rectangle_b, example_world)):
                print_debug_merging("Merging " + str(example_world.rectangles.index(rectangle_a)) + " and " + str(example_world.rectangles.index(rectangle_b)))
                merge(rectangle_a, rectangle_b, example_world)
                break

    print("Found solution with " + str(len(example_world.rectangles)) + " rectangles")

    if (best_world == None or len(example_world.rectangles) < len(best_world.rectangles)):
        print("New best solution with " + str(len(example_world.rectangles)) + " rectangles!")
        best_world = example_world

best_world.render()
