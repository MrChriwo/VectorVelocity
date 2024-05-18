import pygame
import sys
from playerclass import Player
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))  # Width: 800px, Height: 600px
pygame.display.set_caption('Vector Velocity - Pygame')

# Define lane positions (left, middle, right)
lane_positions = [200, 400, 600]

# Create a player instance
player = Player(lane_positions[1], 500, 50, 50, 100, lane_positions) # start in the middle lane

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    # Fill the screen with a color (RGB: White)
    screen.fill((255, 255, 255))

    # Draw the player
    player.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
