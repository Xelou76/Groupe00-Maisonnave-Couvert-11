import pygame

class GameGUI:
    def __init__(self, game, cell_size=40):
        self.game = game
        self.cell_size = cell_size
        self.width = game.width * cell_size
        self.height = game.height * cell_size
        
        # Configuration de la fenêtre
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Démineur IA - Espace pour résoudre")
        
        # Couleurs
        self.COLORS = {
            'bg_hidden': (200, 200, 200),  # Gris clair (caché)
            'bg_revealed': (255, 255, 255), # Blanc (révélé)
            'grid': (128, 128, 128),       # Lignes de la grille
            'flag': (255, 0, 0),           # Rouge (Drapeau)
            'mine': (0, 0, 0),             # Noir (Mine BOOM)
            'text': {                      # Couleurs des chiffres (comme le vrai jeu)
                1: (0, 0, 255),    # Bleu
                2: (0, 128, 0),    # Vert
                3: (255, 0, 0),    # Rouge
                4: (0, 0, 128),    # Bleu foncé
                5: (128, 0, 0),    # Marron
                6: (0, 128, 128),  # Cyan
                7: (0, 0, 0),      # Noir
                8: (128, 128, 128) # Gris
            }
        }
        
        # Police d'écriture
        self.font = pygame.font.SysFont('Arial', 24, bold=True)

    def handle_click(self, pos):
        """Convertit le clic souris en coordonnées de grille"""
        x = pos[0] // self.cell_size
        y = pos[1] // self.cell_size
        # On ne peut cliquer que dans la grille
        if 0 <= x < self.game.width and 0 <= y < self.game.height:
            self.game.reveal(x, y)

    def draw_cell(self, x, y):
        """Dessine une case unique"""
        rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        val = self.game.get_value(x, y)
        
        # 1. Fond de la case
        if (x, y) in self.game.revealed:
            pygame.draw.rect(self.screen, self.COLORS['bg_revealed'], rect)
            
            # Si c'est une mine révélée (Perdu !)
            if (x, y) in self.game.grid:
                pygame.draw.circle(self.screen, self.COLORS['mine'], rect.center, self.cell_size // 4)
            # Sinon, on affiche le chiffre (sauf si c'est 0)
            elif val > 0:
                text = self.font.render(str(val), True, self.COLORS['text'].get(val, (0,0,0)))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
                
        else:
            # Case cachée
            pygame.draw.rect(self.screen, self.COLORS['bg_hidden'], rect)
            
            # Si c'est un drapeau posé par l'IA ou le joueur
            if (x, y) in self.game.flags:
                pygame.draw.rect(self.screen, self.COLORS['flag'], 
                                 (rect.centerx - 5, rect.centery - 5, 10, 10))

        # 2. Bordure de la grille
        pygame.draw.rect(self.screen, self.COLORS['grid'], rect, 1)
    
    def draw_probabilities(self, prob_map):
        """Affiche un calque de couleur selon la probabilité de danger"""
        for (x, y), prob in prob_map.items():
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            
            # Couleur allant du Vert (0%) au Rouge (100%)
            # On utilise ici un jaune transparent pour l'effet "scan"
            intensity = int(255 * prob) 
            s = pygame.Surface((self.cell_size, self.cell_size))
            s.set_alpha(100) # Transparence
            s.fill((intensity, 255 - intensity, 0)) # Dégradé Vert -> Rouge
            self.screen.blit(s, rect.topleft)
            
            # Affiche le % en petit
            if prob > 0.0:
                perc_text = pygame.font.SysFont('Arial', 10).render(f"{int(prob*100)}%", True, (0,0,0))
                self.screen.blit(perc_text, rect.topleft)

    def draw(self):
        """Boucle de dessin principal"""
        self.screen.fill((0, 0, 0)) # Nettoyage écran
        for x in range(self.game.width):
            for y in range(self.game.height):
                self.draw_cell(x, y)
        # Si l'IA a calculé des probabilités, on les affiche
        if hasattr(self.game, 'prob_map'):
            self.draw_probabilities(self.game.prob_map)