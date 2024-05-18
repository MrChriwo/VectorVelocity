import pygame
import sys
from player import Player
import settings

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        # Set up the display
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.CAPTION)
        
        # Define lane positions
        self.lane_positions = settings.LANE_POSITIONS
        
        # Create a player instance
        self.player = Player(self.lane_positions[1], self.lane_positions)
        
        # Clock to control frame rate
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
    
    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
    
    def update(self, dt):
        self.player.update(dt)
    
    def draw(self):

        self.screen.fill((255, 255, 255))
        
        # Draw the player
        self.player.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FRAME_RATE) / 1000.0 

            self.handle_events()
            self.update(dt)
            self.draw()
        
        self.quit()
    
    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()