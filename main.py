import arcade
import math

import pymunk
from game_object import Archer, Target, ArrowSprite

WIDTH = 800
HEIGHT = 600
TITLE = "Archer Game"

class App(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        self.background = arcade.load_texture("assets/img/background.png")
        self.archer = Archer("assets/img/archer.png", 100, 100)
        self.target = Target("assets/img/target.png", 600, 100)
        self.arrow_group = arcade.SpriteList()  
        self.draw_line = False
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.angle = 0
        self.space = pymunk.Space()  # Crear el espacio de pymunk
        self.space.gravity = (0, -900)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background)
        self.archer.draw()
        self.target.draw()
        if self.draw_line:
            arcade.draw_line(self.start_x, self.start_y, self.end_x, self.end_y, arcade.color.BLACK)
        self.arrow_group.draw()
    
    def on_update(self, delta_time):
        self.space.step(1 / 60.0)
        self.arrow_group.update()
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.start_x = x
            self.start_y = y
            self.end_x = x
            self.end_y = y
            self.draw_line = True
            self.angle = math.atan2(y - self.archer.center_y, x - self.archer.center_x)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.draw_line:
            self.end_x = x
            self.end_y = y
    
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.draw_line:
            self.draw_line = False
            dx = self.end_x - self.start_x
            dy = self.end_y - self.start_y
            angle = math.atan2(dy, dx)
            arrow_sprite = ArrowSprite("assets/img/arrow.png", self.archer.center_x, self.archer.center_y, x, y, self.space)
            arrow_sprite.rotation = math.degrees(angle)
            arrow_speed = 2
            arrow_sprite.change_x = math.cos(self.angle) * arrow_speed
            arrow_sprite.change_y = math.sin(self.angle) * arrow_speed
            self.arrow_group.append(arrow_sprite)

def main():
    app = App()
    arcade.run()

if __name__ == "__main__":
    main()
