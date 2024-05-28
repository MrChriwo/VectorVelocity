# This project uses vector graphics designed by Vecteezy
# Vecteezy assets are used under the Free License and require attribution
# For more information, visit https://www.vecteezy.com

import pygame
import sys
from player import Player
import settings
from spawn_manager import SpawnManager
from ui import UI

class Game:
    def __init__(self):
        # Initialize Pygame with backround image variables
        pygame.init()
        self.background = pygame.image.load(settings.BACKGROUND_ASSET_PATH)
        self.background = pygame.transform.scale(self.background, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        # Sound mixer initialization
        pygame.mixer.init()
        pygame.mixer.music.load(settings.SOUNDS_ASSET_PATH + "bgmusic.wav")
        pygame.mixer.music.set_volume(0.2) 
        pygame.mixer.music.play(-1) 

        # Set up the display
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.CAPTION)
        
        # Create UI instance
        self.ui = UI(self.screen)

        # Game variables
        self.score = 0
        self.collected_coins = 0
        self.speed = 3.5
        self.last_updated_coins = 0
        
        self.lane_positions = settings.LANE_POSITIONS
   
        #  Instances for game mechanics
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

    # here we are updating the difficulty of the game, setting up the speed and spawn rates 
    # based on conditions like collected coins and reached score
    def updateDifficulty(self, amount):
        if self.speed == settings.MAXIMUM_SPEED:
            return
        if self.last_updated_coins == self.collected_coins and self.collected_coins != 0:
            return
        if (self.collected_coins % settings.COIN_SPEEDUP_FACTOR == 0 and self.collected_coins != 0) or (int(self.score) % int(settings.SCORE_SPEEDUP_FACTOR * 1 + amount) == 0 and self.score != 0):          
            self.speed += amount
            self.spawnMgr.update_speed(self.speed)
            # print(f"Speed: {self.speed}")
            self.spawnMgr.update_spawn_rates()
            self.player.update_speed(amount)

            self.last_updated_coins = self.collected_coins
        
    # checking game over condition
    def is_game_over(self):
        if not self.running:
            return True
    
    # handling events like game over or player input
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
    
    # updating the game state
    def update(self, dt):
        self.player.update(dt)
        self.spawnMgr.check_collisions(self.player, self.spawnMgr.coins, self.updateCoins)
        self.spawnMgr.check_collisions(self.player, self.spawnMgr.obstacles)
        self.spawnMgr.update(dt)
        self.updateDifficulty(0.375)

    # draw all the game objects
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.spawnMgr.draw()
        self.ui.show_coins(self.collected_coins)
        self.ui.show_highscore(int(self.score))
        self.ui.show_credits()

    # main game loop
    def run(self):
        while not self.is_game_over():
            dt = self.clock.tick(settings.FRAME_RATE) / 1000.0 
            self.handle_events()
            self.update(dt)
            self.draw()
            self.updateScore(2.6 * dt * self.speed)

            pygame.display.flip()


    # exit the application 
    def quit(self):
        print(f"Game Over Space Cadet!\nYour score was: {int(self.score)}\nCollect coins: {self.collected_coins}\nSpeed: {self.speed}\nSpawn rate: {self.spawnMgr.obstacle_spawn_rate}")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()