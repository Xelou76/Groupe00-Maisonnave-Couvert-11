import pygame
import sys
from game_engine import Minesweeper
from gui import GameGUI

def main():
    # 1. Initialisation du jeu
    game = Minesweeper(width=10, height=10, num_mines=10)
    gui = GameGUI(game)
    
    running = True
    while running:
        # 2. Gestion des événements (clics, fermeture)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gui.handle_click(pygame.mouse.get_pos())

        # 3. Dessin
        gui.draw()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()