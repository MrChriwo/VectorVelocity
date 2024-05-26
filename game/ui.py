import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()  # Initialize the font module
        self.font = pygame.font.Font(None, 36)  # Create a default pygame font object

    def show_coins(self, highscore):
        text = self.font.render(f'Coins: {highscore}', True, (128, 0, 120))  # White color
        self.screen.blit(text, (10, 10)) 

    def show_highscore(self, coins):
        text = self.font.render(f'High Score: {coins}', True, (184, 0, 184))
        self.screen.blit(text, (10, 50))