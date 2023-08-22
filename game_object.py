import math
import arcade
import pymunk

class Archer(arcade.Sprite):
    def __init__(self, image: str, x: float, y: float):
        super().__init__(image, 0.1)
        self.center_x = x
        self.center_y = y

class Target(arcade.Sprite):
    def __init__(self, image: str, x: float, y: float):
        super().__init__(image, 0.04)
        self.center_x = x
        self.center_y = y
        self.vida = 10
        self.shapes = [] 

class ArrowSprite(arcade.Sprite):
    def __init__(self, image: str, start_x: float, start_y: float, end_x: float, end_y: float, space: pymunk.Space):
        super().__init__(image, 0.04)
        self.center_x = start_x
        self.center_y = start_y
        self.target_x = end_x
        self.target_y = end_y
        self.speed = 5
        self.damage = 0
        
        # Calcular el ángulo y la distancia para el lanzamiento
        dx = self.target_x - self.center_x
        dy = self.target_y - self.center_y
        self.angle = math.atan2(dy, dx)
        self.distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Configurar físicas y movimiento de Pymunk
        mass = 1
        radius = 10
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment)
        body.position = (self.center_x, self.center_y)
        power = self.distance * 2
        impulse = power * pymunk.Vec2d(1, 0)
        body.apply_impulse_at_local_point(impulse.rotated(self.angle))
        shape = pymunk.Circle(body, radius)
        shape.elasticity = 0.8
        shape.friction = 1
        
        space.add(body, shape)
        self.body = body
        self.shape = shape
        
    def update(self):
        if not self.is_stuck:
            self.center_x = self.shape.body.position.x
            self.center_y = self.shape.body.position.y
            self.angle = math.degrees(self.shape.body.angle)
    
        if self.is_stuck:
            self.angle = math.degrees(self.shape.body.angle)
        
    def remove_from_space(self, space):
        space.remove(self.body, self.shape)

        
        
        

