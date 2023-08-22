import random
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
        self.background = arcade.load_texture("assets/img/background.jpg")
        self.archer = Archer("assets/img/archer.png", 100, 100)
        self.target = Target("assets/img/target.png", 600, 100)
        self.arrow_group = arcade.SpriteList()  
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.angle = 0
        self.puntaje = 0
        self.flechas_restantes = 60
        self.show_total_score = False
        self.total_score = 0
        self.total_score_timer = 0
        self.space = pymunk.Space()  # Crear el espacio de pymunk
        self.space.gravity = (0, -900)
        self.target_shapes = []
        self.create_boundaries()
        self.target_speed = 1  # Velocidad del movimiento del objetivo
        self.target_direction = random.choice([-1, 1])  # Dirección inicial del movimiento en X y Y
        self.target_x_speed = self.target_speed * self.target_direction
        self.target_y_speed = self.target_speed * self.target_direction

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background)
        self.archer.draw()
        self.target.draw()
        self.arrow_group.draw()
        arcade.draw_text(f"Puntaje = {self.puntaje}", 10, HEIGHT - 30, arcade.color.BLACK, 14)
        arcade.draw_text(f"Flechas = {self.flechas_restantes}", 10, HEIGHT - 50, arcade.color.BLACK, 14)
        
        if self.show_total_score:
            arcade.draw_text(f"Puntaje Total = {self.total_score}", WIDTH // 2, HEIGHT // 2, arcade.color.BLACK, 30, anchor_x="center")

    def on_update(self, delta_time):
        self.space.step(1 / 60)
        self.arrow_group.update()
        
        if self.target.vida <= 0:
            self.target.remove_from_sprite_lists()
            for shape in self.target.shapes:
                self.space.remove(shape)
            self.target_shapes = []
            self.puntaje += 1
                
            # Generar nuevas coordenadas aleatorias para el objetivo
            new_x = random.uniform(100, WIDTH - 100)
            new_y = random.uniform(100, HEIGHT - 100)
            self.target = Target("assets/img/target.png", new_x, new_y)
            self.target_shapes = self.target.shapes 
            self.target.vida = 10
        
         # Mover el objetivo de manera suave y controlada
        self.target.center_x += self.target_x_speed
        self.target.center_y += self.target_y_speed

        # Cambiar la dirección del movimiento cuando el objetivo se acerca a los bordes
        if self.target.center_x <= 50 or self.target.center_x >= WIDTH - 50:
            self.target_x_speed *= -1
        if self.target.center_y <= 50 or self.target.center_y >= HEIGHT - 50:
            self.target_y_speed *= -1
        
        if self.flechas_restantes == 0 and self.puntaje >= 0:
            self.show_total_score = True  # Mostrar el mensaje de Puntaje Total
            self.total_score_timer = 3  # Duración de 1 segundo
            self.total_score = self.puntaje
            self.puntaje = 0  # Reiniciar el puntaje
            self.flechas_restantes = 60
        
        if self.show_total_score:
            self.total_score_timer -= delta_time
            if self.total_score_timer <= 0:
                self.show_total_score = False
        
        for arrow_sprite in self.arrow_group:
            if not arrow_sprite.is_stuck:
                for shape in self.space.shapes:
                    if shape.body == arrow_sprite.body:
                        if shape.body.position.y < 50:  # Ajusta esta coordenada según la altura del borde inferior
                            arrow_sprite.is_stuck = True
                            arrow_sprite.stuck_timer = 1  # 1 segundo
                            break
                
                # Aplicar aceleración debida a la gravedad
                arrow_sprite.change_y -= self.space.gravity[1] * delta_time
                # Actualizar la posición y el ángulo de la flecha
                arrow_sprite.center_x = arrow_sprite.body.position.x
                arrow_sprite.center_y = arrow_sprite.body.position.y
                arrow_sprite.angle = math.degrees(arrow_sprite.body.angle)
                
            if not arrow_sprite.is_stuck and self.target.collides_with_sprite(arrow_sprite):
                arrow_sprite.is_stuck = True
                arrow_sprite.stuck_timer = 1  # 1 segundo
                self.target.vida -= arrow_sprite.damage
        
        for arrow_sprite in self.arrow_group:
            if arrow_sprite.is_stuck:  # Si la flecha está clavada
                arrow_sprite.stuck_timer -= delta_time
                if arrow_sprite.stuck_timer <= 0:
                    arrow_sprite.remove_from_space(self.space)
                    self.arrow_group.remove(arrow_sprite)
        
        
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
        if button == arcade.MOUSE_BUTTON_LEFT and self.draw_line and self.flechas_restantes > 0:
            self.draw_line = False
            dx = self.end_x - self.start_x
            dy = self.end_y - self.start_y
            angle = math.atan2(dy, dx)
            self.flechas_restantes -= 1
            arrow_sprite = ArrowSprite("assets/img/arrow.png", self.archer.center_x, self.archer.center_y, x, y, self.space)
            arrow_sprite.rotation = math.degrees(angle)
            arrow_speed = 2
            arrow_sprite.change_x = math.cos(self.angle) * arrow_speed
            arrow_sprite.change_y = math.sin(self.angle) * arrow_speed
            arrow_sprite.damage = 5
            self.arrow_group.append(arrow_sprite)
            arrow_sprite.is_stuck = False
            arrow_sprite.stuck_timer = 1  # 1 segundo
            
    def create_boundaries(self):
        # Crear los bordes de la pantalla como segmentos estáticos
        floor = pymunk.Segment(self.space.static_body, (0, 0), (WIDTH, 0), 0)
        left_wall = pymunk.Segment(self.space.static_body, (0, 0), (0, HEIGHT), 0)
        right_wall = pymunk.Segment(self.space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 0)
        ceiling = pymunk.Segment(self.space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 0)
    
        # Configurar colisiones
        floor.friction = 1
        left_wall.friction = 1
        right_wall.friction = 1
        ceiling.friction = 1
    
        self.space.add(floor, left_wall, right_wall, ceiling)

def main():
    app = App()
    arcade.run()

if __name__ == "__main__":
    main()
