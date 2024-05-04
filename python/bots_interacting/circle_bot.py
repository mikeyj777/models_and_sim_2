import random
import numpy as np

class Circle_Bot:

    def __init__(self, id, env_width, env_height, radius = 30, max_speed = 5, velocity = None, position = None) -> None:
        self.id = id
        self.radius = radius
        self.velocity = velocity
        self.position = position
        self.env_width = env_width
        self.env_height = env_height
        self.dims = [env_width, env_height]
        self.max_speed = max_speed

        if self.velocity is None:
            self.set_velocity()
        
        if self.position is None:
            self.set_position()
        
    def set_velocity(self):
        self.velocity = np.random.randint(-self.max_speed, self.max_speed, 2)

    def set_position(self):
        self.position = np.array([random.randint(0, self.env_width), random.randint(0, self.env_height)])

    def update_position(self):
        self.position += self.velocity
    
    def reverse_direction(self):
        self.velocity = -self.velocity
    
    def get_distance_to_other_bot(self, other_bot):
        return np.linalg.norm(self.position - other_bot.position)

    def check_for_nearby_walls(self):

        for i in range(2):
            if self.position[i] <= 0 or self.position[i] >= self.dims[i]:
                self.velocity[i] *= -1


