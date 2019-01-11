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
BALLS_RADIUS = 25


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


class MyAutomat(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)
        self.vertices = []
        self.path = []
        self.picked_vertex = None

        for i in range(3):
            self.add_vertex()
        self.solve_tsp()


    def solve_tsp(self):
        pos = [(pos.x, pos.y) for pos in self.vertices]
        a = [[euclidean(u, v) for v in pos] for u in pos]
        edges = kristofedes(a)
        self.path = [pos[e[0]] for e in edges] + [pos[edges[-1][1]]]

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        for v in self.vertices:
          v.draw()
        arcade.draw_line_strip(self.path, arcade.color.BLACK)
        arcade.finish_render()

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
