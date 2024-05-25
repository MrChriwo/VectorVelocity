import pygame
import sys
from player import Player
import settings
from spawn_manager import SpawnManager
from obstacle import Obstacle
from coin import Coin 

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
        self.spawnMgr = SpawnManager(self.player, self.screen, self.quit,  self.lane_positions)
        
        # Clock to control frame rate
        self.clock = pygame.time.Clock()

        self.score = 0
        self.collected_coins = 0
        self.difficulty = 1
        self.difficulty_timer = 0
        
        # Game state
        self.running = True

    def updateCoins(self, amount):
        self.collected_coins += amount
        print(f"Collected coins: {self.collected_coins}")

    def is_game_over(self):
        if not self.running:
            return True
    
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
        self.spawnMgr.check_collisions(self.player, self.spawnMgr.coins, self.updateCoins)
        self.spawnMgr.check_collisions(self.player, self.spawnMgr.obstacles)
        self.spawnMgr.update(dt)
    
    def draw(self):
        self.screen.fill((0, 0, 0))

        self.spawnMgr.draw()
   
        pygame.display.flip()
    
    def run(self):
        while not self.is_game_over():
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