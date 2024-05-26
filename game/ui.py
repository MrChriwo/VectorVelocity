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

    def show_gameover_screen(self, highscore, coins):
        # render a transparent rect (80% transparent) n center of screen
        # first line = GameOver,
        # second line = Highscore: {highscore}
        # third line = Coins: {coins}

        # render a rect
        rect = pygame.Surface((400, 200), pygame.SRCALPHA)
        rect.fill((0, 0, 0, 200))
        self.screen.blit(rect, (200, 200))

        # render text
        text = self.font.render('Game Over', True, (255, 255, 255))
        self.screen.blit(text, (300, 250))

        text = self.font.render(f'Highscore: {highscore}', True, (255, 255, 255))
        self.screen.blit(text, (300, 300))

        text = self.font.render(f'Coins: {coins}', True, (255, 255, 255))
        self.screen.blit(text, (300, 350))

        # button to restart the game

        restart = self.font.render('Restart', True, (255, 255, 255))
        self.screen.blit(restart, (300, 400))
        pygame.draw.rect(self.screen, (255, 255, 255), (300, 400, 100, 50), 1)

