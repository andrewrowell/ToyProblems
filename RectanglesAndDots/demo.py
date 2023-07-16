import world

WIDTH = 5
HEIGHT = 3

bad_point = world.BadPoint(2.5, 0.5)

example_world = world.World(WIDTH, HEIGHT, [], [bad_point])
example_world.add_rectangle_for_each_good_point()

def can_merge(rectangle_a, rectangle_b, world):
    if (rectangle_a.x != rectangle_b.x and rectangle_a.y != rectangle_b.y):
        return False
    # Same x, different y. Merging on the Y axis means they need to have the same width.
    if (rectangle_a.x == rectangle_b.x):
        if (rectangle_a.width != rectangle_b.width):
            return False
        # Check if a bad point is in the way
        return True
    # Same y, different x. Merging on the X axis means they need to have the same height.
    if (rectangle_a.y == rectangle_b.y):
        if (rectangle_a.height != rectangle_b.height):
            return False
        # Check if a bad point is in the way
        return True

def merge(rectangle_a, rectangle_b, world):
    assert(can_merge(rectangle_a, rectangle_b, world))
    # Same x, different y
    if (rectangle_a.x == rectangle_b.x):
        rectangle_a.height += rectangle_b.height
        rectangle_a.good_points += rectangle_b.good_points
        world.rectangles.remove(rectangle_b)
    # Same y, different x
    if (rectangle_a.y == rectangle_b.y):
        rectangle_a.width += rectangle_b.width
        rectangle_a.good_points += rectangle_b.good_points
        world.rectangles.remove(rectangle_b)

merge(example_world.rectangles[0], example_world.rectangles[1], example_world)

print(example_world)
example_world.render()
