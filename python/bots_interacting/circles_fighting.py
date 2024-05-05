import pygame
import random
import numpy as np

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bots_interacting.circle_bot import Circle_Bot
from consts_and_data.consts import RESPONSE_CODE

# Initialize Pygame
pygame.init()

# Set up the screen
num_circles = 7
width, height = 1500, 800
circle_radius = 30
max_bot_count = 50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Circles")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 25)
bot_colors = [RED, GREEN, BLUE]

# Circles rule
bots = []
for i in range(num_circles):
    bot_color_id = i % len(bot_colors)
    cb = Circle_Bot(id=i, env_width=width, env_height=height)
    bots.append(cb)

# Main loop
running = True
# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update circle positions
    i = 0
    while i < len(bots):
        bots[i].update_position()

        # Check for collisions
        n = i + 1
        while n < len(bots):
            resp_code = bots[i].check_for_collision_with_other_bot_and_return_response_code(bots[n])
            if resp_code == RESPONSE_CODE.MAKE_A_NEW_BOT and len(bots) < max_bot_count:
                num_circles += 1
                new_pos = bots[i].position
                new_pos += bots[i].radius * np.array([1,1])
                cb = Circle_Bot(id=i, env_width=width, env_height=height, position=bots[i].position)
                bots.append(cb)
            if bots[n].radius <= 0:
                bots.pop(n)
            if bots[i].radius <= 0:
                bots.pop(i)
            n += 1
        # Bounce off the walls
        bots[i].check_for_nearby_walls()

        # Draw circles
        pygame.draw.circle(screen, bots[i].color, bots[i].position, bots[i].radius)

        i += 1

    pygame.display.flip()

    # Control FPS


    # Control FPS
    pygame.time.Clock().tick(60)

pygame.quit()
