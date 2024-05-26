import pygame
import sys
from player import Player
import settings
from spawn_manager import SpawnManager
from ui import UI
class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.background = pygame.image.load("game/assets/bg2.jpg")
        self.background = pygame.transform.scale(self.background, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        pygame.mixer.init()
        pygame.mixer.music.load("game/assets/bgmusic.wav")
        pygame.mixer.music.set_volume(0.2)  # Set the volume to 50%
        pygame.mixer.music.play(-1)  # The '-1' argument makes the music loop indefinitely

        # Set up the display
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.CAPTION)
        
        self.ui = UI(self.screen)

        self.score = 0
        self.collected_coins = 0
        self.speed = 3.5
        self.last_updated_coins = 0
        
        # Define lane positions
        self.lane_positions = settings.LANE_POSITIONS
   
        # Create a player instance
        self.player = Player(self.lane_positions[1], self.lane_positions)
        self.spawnMgr = SpawnManager(self.player, self.screen, self.quit,  self.lane_positions, self.speed)
        
        # Clock to control frame rate
        self.clock = pygame.time.Clock()
  
        # Game state
        self.running = True

    def updateCoins(self, amount):
        self.collected_coins += amount
        # print(f"Collected coins: {self.collected_coins}")

    def updateScore(self, amount):
        self.score += amount

    def updateDifficulty(self, amount):
        if self.speed == 25.75:
            return
        if self.last_updated_coins == self.collected_coins and self.collected_coins != 0:
            return
        if (self.collected_coins % 20 == 0 and self.collected_coins != 0) or (int(self.score) % 200 == 0 and self.score != 0):          
            self.speed += amount
            self.spawnMgr.update_speed(self.speed)
            print(f"Speed: {self.speed}")
            self.spawnMgr.update_spawn_rates()

            self.last_updated_coins = self.collected_coins
        
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
        self.updateDifficulty(0.375)

    
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.spawnMgr.draw()
        self.ui.show_coins(self.collected_coins)
        self.ui.show_highscore(int(self.score))

        pygame.display.flip()
    
    def run(self):
        while not self.is_game_over():
            dt = self.clock.tick(settings.FRAME_RATE) / 1000.0 
            self.handle_events()
            self.update(dt)
            self.draw()
            self.updateScore(2.6 * dt * self.speed)

                    
        self.quit()
    
    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()