import pygame
import random
import numpy

from python.bots_interacting.circle_bot import Circle_Bot

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
num_circles = 2
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
    cb = Circle_Bot(id=i, env_width=width, env_height=height, radius=circle_radius)
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
    for i in range(len(bots)):
        bots[i].update_position()

        # Check for collisions
        for n in range(i+1, len(bots)):
            dist = bots[i].get_distance_to_other_bot(bots[n])
            if dist <= (2 * circle_radius)**2:
                # Reverse circle trajectories
                bots[i].reverse_direction()
                bots[n].reverse_direction()
        
        # Bounce off the walls
        bots[i].check_for_nearby_walls()

        # Draw circles
        bot_color_id = i % len(bots)
        bot_color = bot_colors[bot_color_id]
        pygame.draw.circle(screen, bot_color, bots[i].position, bots[i].radius)

    pygame.display.flip()

    # Control FPS


    # Control FPS
    pygame.time.Clock().tick(60)

pygame.quit()
