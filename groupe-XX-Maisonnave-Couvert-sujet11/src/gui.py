import pygame
from game_engine import Minesweeper

CELL_SIZE = 30
COLORS = {
    'bg': (192, 192, 192),
    'hidden': (220, 220, 220),
    'text': (0, 0, 0),
    'mine': (255, 0, 0)
}

class GameGUI:
    def __init__(self, game):
        self.game = game
        pygame.init()
        self.width = game.width * CELL_SIZE
        self.height = game.height * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 24)

    def draw(self):
        self.screen.fill(COLORS['bg'])
        
        for x in range(self.game.width):
            for y in range(self.game.height):
                rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if (x, y) in self.game.revealed:
                    # Case révélée
                    val = self.game.get_value(x, y)
                    pygame.draw.rect(self.screen, COLORS['bg'], rect)
                    pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
                    if val > 0:
                        text = self.font.render(str(val), True, COLORS['text'])
                        self.screen.blit(text, (x * CELL_SIZE + 10, y * CELL_SIZE + 5))
                    elif val == -1:
                         pygame.draw.rect(self.screen, COLORS['mine'], rect)
                else:
                    # Case cachée
                    pygame.draw.rect(self.screen, COLORS['hidden'], rect)
                    pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

        pygame.display.flip()

    def handle_click(self, pos):
        x = pos[0] // CELL_SIZE
        y = pos[1] // CELL_SIZE
        if 0 <= x < self.game.width and 0 <= y < self.game.height:
            self.game.reveal(x, y)