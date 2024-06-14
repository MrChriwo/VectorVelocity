# This project uses vector graphics designed by Vecteezy
# Vecteezy assets are used under the Free License and require attribution
# For more information, visit https://www.vecteezy.com

import pygame
from player import Player
import settings
from spawn_manager import SpawnManager
from ui import UI
from asset_manager import AssetManager

class Game:
    def __init__(self, mode='human'):
        self.mode = mode
        # Initialize Pygame with backround image variables
        pygame.init()
        
        # Set up the display
        
        if self.mode == 'human':
            self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            pygame.display.set_caption(settings.CAPTION)        
        else:    
            self.screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        self.assetMgr = AssetManager()
        self.background = self.assetMgr.get_asset('background')

        # Sound mixer initialization
        pygame.mixer.init()
        self.assetMgr.get_asset('bgmusic').play(-1)

        # Create UI instance
        self.ui = UI(self.screen)

        # Game variables
        self.score = 0
        self.score_increase_multiplier = 1

        self.collected_coins = 0
        self.speed = 4
        self.last_updated_coins = 0
        
        self.lane_positions = settings.LANE_POSITIONS
   
        #  Instances for game mechanics
        self.player = Player(self.lane_positions[1], self.lane_positions, self.assetMgr)
        self.spawnMgr = SpawnManager(self.player, self.screen, self.set_game_over,  self.lane_positions, self.speed, self.assetMgr)
        
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
        if self.last_updated_coins == self.collected_coins:
            return
        score_condition = self.score * self.score_increase_multiplier
        if (self.collected_coins % settings.COIN_SPEEDUP_FACTOR == 0 and self.collected_coins != 0) or ((int(self.score)) % score_condition == 0 and self.score != 0):          
            self.speed += amount
            self.spawnMgr.update_speed(self.speed)
            # print(f"Speed: {self.speed}")
            self.spawnMgr.update_spawn_rates()
            self.player.update_speed(amount)

            self.last_updated_coins = self.collected_coins
            self.score_increase_multiplier += amount
        
    # checking game over condition
    def is_game_over(self):
        return not self.running
    
    def set_game_over(self):
        self.running = False
    
    # handling events like game over or player input
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    self.restart()

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
        self.updateDifficulty(settings.DIFFICULTY_INCREASE_FACTOR)
        self.updateScore(2.6 * dt * self.speed)


    # main game loop
    def run(self):
        while True:
            if not self.is_game_over():
                dt = self.clock.tick(settings.FRAME_RATE) / 1000.0
                self.handle_events()
                self.update(dt)
                self.render()
            else:
                print(f"Game Over. Score: {int(self.score)}  Your Coins: {self.collected_coins}  Press R to restart")
                self.ui.show_game_over(self.collected_coins, int(self.score), self.mode )
                self.restart()


    def restart(self):
        self.score = 0
        self.collected_coins = 0
        self.speed = 4
        self.last_updated_coins = 0
        self.score_increase_multiplier = 1

        self.player = Player(self.lane_positions[1], self.lane_positions, self.assetMgr)
        self.spawnMgr = SpawnManager(self.player, self.screen, self.set_game_over, self.lane_positions, self.speed, self.assetMgr)

        self.running = True
            

    def render(self, mode='human'):
        if not self.running:
            return
        if mode == 'human':
            self.screen.blit(self.background, (0, 0))
            self.spawnMgr.draw()
            self.ui.show_coins(self.collected_coins)
            self.ui.show_highscore(int(self.score))
            self.ui.show_credits()
            pygame.display.flip()
        else:
            pass

    def quit(self):
        pygame.quit()

if __name__ == "__main__":
    game = Game("human")
    game.run()