import math
import arcade

class Archer(arcade.Sprite):
    def __init__(self, image: str, x: float, y: float):
        super().__init__(image, 0.2)
        self.center_x = x
        self.center_y = y

class Target(arcade.Sprite):
    def __init__(self, image: str, x: float, y: float):
        super().__init__(image, 0.07)
        self.center_x = x
        self.center_y = y

class ArrowSprite(arcade.Sprite):
    def __init__(self, image: str, start_x: float, start_y: float, end_x: float, end_y: float):
        super().__init__(image, 0.08)
        self.center_x = start_x
        self.center_y = start_y
        self.target_x = end_x
        self.target_y = end_y
        self.speed = 10
        self.angle = math.atan2(self.target_y - self.center_y, self.target_x - self.center_x)
        self.change_x = math.cos(self.angle) * self.speed
        self.change_y = math.sin(self.angle) * self.speed
        self.gravity = 0.2  
        self.dy = 0
        
    def update(self):
        self.dy -= self.gravity
        self.center_x += self.change_x
        self.center_y += self.change_y + self.dy
        self.angle = -math.degrees(math.atan2(self.change_y, self.change_x)) + 90
        
        

