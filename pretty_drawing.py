"""
This simple animation example shows how to move an item with the mouse, and
handle mouse clicks.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.move_mouse
"""
from random import randint

import arcade
from scipy.spatial.distance import euclidean

from kristofedes import kristofedes

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALLS_RADIUS = 20


class Vertex:
    def __init__(self, id, position_x, position_y, radius=BALLS_RADIUS, color=arcade.color.BLACK):
        # Take the parameters of the init function above, and create instance variables out of them.
        self.x = position_x
        self.y = position_y
        self.radius = radius
        self.color = color
        self.id = id

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)
        arcade.draw_text(str(self.id), self.x - self.radius, self.y + self.radius, self.color)


class Edge:
    def __init__(self, v1, v2, line_width=4):
        self.x1, self.y1, self.x2, self.y2 = v1.x, v1.y, v2.x, v2.y
        self.line_width = line_width

        self.len = euclidean((v1.x, v1.y), (v2.x, v2.y))
        self.label_x = (v1.x + v2.x) / 2 + 10
        self.label_y = (v1.y + v2.y) / 2 - 10

    def draw(self):
        arcade.draw_line(self.x1, self.y1, self.x2, self.y2, color=arcade.color.BLACK, border_width=self.line_width)
        arcade.draw_text(str(int(self.len)), self.label_x, self.label_y, color=arcade.color.RED)

class MyAutomat(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)
        self.vertices = []
        self.edges = []
        self.picked_vertex = None

        for i in range(3):
            self.add_vertex()
        self.solve_tsp()


    def solve_tsp(self):
        pos = [(pos.x, pos.y) for pos in self.vertices]
        a = [[euclidean(u, v) for v in pos] for u in pos]
        edges = kristofedes(a)
        self.edges = [Edge(self.vertices[e[0]], self.vertices[e[1]]) for e in edges]

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        for e in self.edges:
            e.draw()
        for v in self.vertices:
          v.draw()


    def add_vertex(self):
        self.vertices.append(Vertex(len(self.vertices), randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.A:
            self.add_vertex()
        self.solve_tsp()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        if self.picked_vertex:
            self.picked_vertex.x = x
            self.picked_vertex.y = y
            self.solve_tsp()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        for v in self.vertices:
            if euclidean((v.x, v.y), (x, y)) <= BALLS_RADIUS:
                self.picked_vertex = v

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        self.picked_vertex = None

def main():
    window = MyAutomat(SCREEN_WIDTH, SCREEN_HEIGHT, "TSP Example")
    arcade.run()


if __name__ == "__main__":
    main()
