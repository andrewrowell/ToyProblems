import math
import cairo

class BadPoint:
    def __init__(self, x, y):
        assert(int(x) != x)
        assert(int(y) != y)
        self.x = x
        self.y = y


class GoodPoint:
    def __init__(self, x, y):
        assert (int(x) == x)
        assert (int(y) == y)
        self.x = x
        self.y = y
        self.rectangle = None

    def set_rectangle(self, rectangle):
        self.rectangle = rectangle


class Rectangle:
    def __init__(self, x, y, width, height, good_points):
        assert (int(x) == x)
        assert (int(y) == y)
        assert (int(width) == width)
        assert (int(height) == height)
        assert (type(good_points) == list)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.good_points = good_points

    def add_points(self, good_points):
        self.good_points.append(good_points)


class World:
    def __init__(self, width, height, rectangles, bad_points):
        assert (int(width) == width)
        assert (int(height) == height)
        assert (type(rectangles) == list)
        assert (type(bad_points) == list)
        self.width = width
        self.height = height
        self.rectangles = rectangles
        self.good_points = []
        for x in range(width):
            for y in range(height):
                self.good_points.append(GoodPoint(x, y))
        self.bad_points = bad_points

    def add_rectangle_for_each_good_point(self):
        for good_point in self.good_points:
            rectangle = Rectangle(good_point.x, good_point.y, 1, 1, [good_point])
            good_point.set_rectangle(rectangle)
            self.rectangles.append(rectangle)

    def render(self):
        WIDTH, HEIGHT = 500, 500

        x_offset = 0.05
        y_offset = 0.05
        rectangle_spacing = 0.03

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        ctx = cairo.Context(surface)
        ctx.scale(WIDTH, HEIGHT)  # Normalize the canvas

        ctx.set_source_rgb(0, 0, 1)
        for point in self.good_points:
            ctx.stroke()
            ctx.arc(point.x/self.width + x_offset, point.y/self.height + y_offset, 0.005, 0, 2 * math.pi)
            ctx.fill()

        ctx.set_source_rgb(0, 0.6, 0)
        ctx.set_line_width(0.005)
        for point in self.bad_points:
            ctx.move_to(point.x / self.width - 0.0075 + x_offset, point.y / self.height - 0.0075 + y_offset)
            ctx.line_to(point.x / self.width + 0.0075 + x_offset, point.y / self.height + 0.0075 + y_offset)
            ctx.move_to(point.x / self.width + 0.0075 + x_offset, point.y / self.height - 0.0075 + y_offset)
            ctx.line_to(point.x / self.width - 0.0075 + x_offset, point.y / self.height + 0.0075 + y_offset)
            ctx.stroke()

        ctx.set_source_rgb(1, 0, 0)
        ctx.set_line_width(0.005)
        for rectangle in self.rectangles:
            ctx.move_to(rectangle.x / self.width + (x_offset - rectangle_spacing), rectangle.y / self.height + (y_offset - rectangle_spacing)) # Top left
            ctx.line_to((rectangle.x + rectangle.width - 1) / self.width + (x_offset + rectangle_spacing), rectangle.y / self.height + (y_offset - rectangle_spacing)) # ... to top right
            ctx.line_to((rectangle.x + rectangle.width - 1) / self.width + (x_offset + rectangle_spacing), (rectangle.y + rectangle.height - 1) / self.height + (y_offset + rectangle_spacing)) # ... to bottom right
            ctx.line_to(rectangle.x / self.width + (x_offset - rectangle_spacing), (rectangle.y + rectangle.height - 1) / self.height + (y_offset + rectangle_spacing)) # ... to bottom left
            ctx.line_to(rectangle.x / self.width + (x_offset - rectangle_spacing), rectangle.y / self.height + (y_offset - rectangle_spacing)) # ... to top left
            ctx.stroke()

        surface.write_to_png("example.png")

