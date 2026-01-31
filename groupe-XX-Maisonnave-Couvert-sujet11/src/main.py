import pygame
import sys
from game_engine import Minesweeper
from gui import GameGUI
from csp_solver import CSPSolver  # <--- 1. On importe le cerveau

def main():
    # Initialisation de Pygame
    pygame.init()
    
    # 2. Initialisation du jeu et de l'IA
    game = Minesweeper(width=10, height=10, num_mines=10)
    gui = GameGUI(game)
    solver = CSPSolver(game)  # <--- On crée l'instance du solveur
    
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Clic souris (Joueur humain)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gui.handle_click(pygame.mouse.get_pos())

            # Touche Clavier (Intelligence Artificielle)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # <--- Appuie sur ESPACE
                    print("🤖 L'IA réfléchit...")
                    safe_moves, mines = solver.solve()
                    
                    print(f"Trouvé : {len(safe_moves)} cases sûres, {len(mines)} mines.")
                    
                    # On applique les découvertes de l'IA
                    for x, y in mines:
                        game.flags.add((x, y))  # On plante un drapeau
                        
                    for x, y in safe_moves:
                        game.reveal(x, y)       # On révèle la case
        
        # Dessin de l'interface
        gui.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()