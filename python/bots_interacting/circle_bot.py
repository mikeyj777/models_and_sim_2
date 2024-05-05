import random
import numpy as np

class Circle_Bot:

    def __init__(self, id, env_width, env_height, max_speed = 5, velocity = None, position = None, color = None) -> None:
        self.id = id
        self.velocity = velocity
        self.position = position
        self.env_width = env_width
        self.env_height = env_height
        self.dims = [env_width, env_height]
        self.max_speed = max_speed
        self.color = color
        self.let_me_uncollide = False
        self.radius = 30
        self.health = None
        self.damage = None

        if self.velocity is None:
            self.set_velocity()
        
        if self.position is None:
            self.set_position()
        
        if self.color is None:
            self.set_color()
        
        self.set_health_damage_and_radius()
        
    def set_velocity(self):
        self.velocity = np.random.randint(-self.max_speed, self.max_speed, 2)

    def set_position(self):
        self.position = np.array([random.randint(0, self.env_width), random.randint(0, self.env_height)])
    
    def set_color(self):
        color_np = np.random.randint(0, 255, 3)
        color_tuple = tuple(color_np)
        self.color = color_tuple
    
    def set_health_damage_and_radius(self):
        self.health = random.randint(10, 100)
        self.damage = random.randint(1, 50)
        self.update_hit_points_and_radius()
        
    def update_position(self):
        self.position += self.velocity
    
    def reverse_direction(self):
        self.velocity = -self.velocity
    
    def check_for_collision_with(self, other_bot):
        if other_bot is None:
            return
        collision_dist = self.radius + other_bot.radius
        dist = np.linalg.norm(self.position - other_bot.position)
        if self.let_me_uncollide:
            if dist > 2 * collision_dist:
                self.let_me_uncollide = False
            return
        
        if dist <= collision_dist:
            if self.let_me_uncollide:
                return
            self.react_to_collision(other_bot)
            return
            
        self.let_me_uncollide = False
        other_bot.let_me_uncollide = False
        return False
    
    def react_to_collision(self, other_bot):
        self.let_me_uncollide = True
        other_bot.let_me_uncollide = True
        self.reverse_direction()
        other_bot.reverse_direction()
        self.update_hit_points_and_radius(other_bot)

    def check_for_nearby_walls(self):

        for i in range(2):
            if self.position[i] <= 0 or self.position[i] >= self.dims[i]:
                self.velocity[i] *= -1
    
    def update_hit_points_and_radius(self, other_bot = None):
        damage_taken = 0
        if other_bot is not None:
            damage_taken = other_bot.damage
        self.health -= damage_taken
        self.health = max(0, self.health)
        self.radius = self.health
        if other_bot is not None:
            other_bot.update_hit_points_and_radius()




