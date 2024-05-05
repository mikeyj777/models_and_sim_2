import pygame
import random
import numpy

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bots_interacting.circle_bot import Circle_Bot
from consts_and_data.consts import Response_Code

# Initialize Pygame
pygame.init()

# Set up the screen
num_circles = 2001
width, height = 800, 600
circle_radius = 30
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
            if bots[i].check_for_collision_with_other_bot_and_return_response_code(bots[n]) == Response_Code.MAKE_A_NEW_BOT:
                num_circles += 1
                cb = Circle_Bot(id=i, env_width=width, env_height=height)
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
