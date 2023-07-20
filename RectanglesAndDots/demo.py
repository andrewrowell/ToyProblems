import world

WIDTH = 5
HEIGHT = 3

bad_point = world.BadPoint(2.5, 0.5)

example_world = world.World(WIDTH, HEIGHT, [], [bad_point])
example_world.add_rectangle_for_each_good_point()


def rectangles_contain_bad_point(rectangle_a, rectangle_b, bad_points):
    for bad_point in bad_points:
        if min(rectangle_a.x, rectangle_b.x) < bad_point.x < max(rectangle_a.x + rectangle_a.width,
                                                                 rectangle_b.x + rectangle_b.height):
            if min(rectangle_a.y, rectangle_b.y) < bad_point.y < max(rectangle_a.y + rectangle_a.height,
                                                                     rectangle_b.y + rectangle_b.height):
                return False
    return True


def can_merge(rectangle_a, rectangle_b, world):
    if rectangle_a == rectangle_b:
        return False
    if (rectangle_a.x != rectangle_b.x and rectangle_a.y != rectangle_b.y):
        return False
    # Same x, different y. Merging on the Y axis means they need to have the same width.
    if rectangle_a.x == rectangle_b.x:
        if (rectangle_a.width != rectangle_b.width):
            return False
        # Check if b starts at the end of a
        if (rectangle_a.y < rectangle_b.y):
            if (rectangle_a.y + rectangle_a.height != rectangle_b.y):
                return False
        else:
            if (rectangle_b.y + rectangle_b.height != rectangle_a.y):
                return False
        # Check if a bad point is in the way
        return rectangles_contain_bad_point(rectangle_a, rectangle_b, world.bad_points)
    # Same y, different x. Merging on the X axis means they need to have the same height.
    if (rectangle_a.y == rectangle_b.y):
        if (rectangle_a.height != rectangle_b.height):
            return False
        # Check if a starts at the end of b
        if (rectangle_a.x < rectangle_b.x):
            if rectangle_a.x + rectangle_a.width != rectangle_b.x:
                return False
        else:
            if rectangle_b.x + rectangle_b.width != rectangle_a.x:
                return False

        # Check if a bad point is in the way
        return rectangles_contain_bad_point(rectangle_a, rectangle_b, world.bad_points)

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


merge(example_world.rectangles[1], example_world.rectangles[0], example_world)
merge(example_world.rectangles[1], example_world.rectangles[0], example_world)

for _ in range(2):
    for i in range(len(example_world.rectangles)):
        for j in range(len(example_world.rectangles)):
            if i == j:
                continue
            if j >= len(example_world.rectangles):
                break
            if i >= len(example_world.rectangles):
                break
            if can_merge(example_world.rectangles[i], example_world.rectangles[j], example_world):
                merge(example_world.rectangles[i], example_world.rectangles[j], example_world)

print(example_world)
example_world.render()
