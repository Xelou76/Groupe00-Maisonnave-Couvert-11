import random

class CSPSolver:
    def __init__(self, game):
        self.game = game

    def solve(self):
        """
        Analyse le plateau. 
        Si des coups sûrs sont trouvés, on les retourne.
        Sinon (début de partie ou blocage), on fait un choix aléatoire.
        """
        moves = set()   # Cases sûres à cliquer
        flags = set()   # Mines trouvées à flagger
        
        # 1. Logique pure (CSP)
        # On parcourt les indices visibles
        for (x, y) in list(self.game.revealed):
            value = self.game.get_value(x, y)
            neighbors = self.game.get_neighbors(x, y)
            
            hidden_neighbors = []
            flagged_neighbors = []
            
            for nx, ny in neighbors:
                if (nx, ny) in self.game.revealed:
                    continue
                if (nx, ny) in self.game.flags:
                    flagged_neighbors.append((nx, ny))
                else:
                    hidden_neighbors.append((nx, ny))
            
            if not hidden_neighbors:
                continue

            # Règle 1 : Tout est sûr
            if len(flagged_neighbors) == value:
                for n in hidden_neighbors:
                    if n not in self.game.flags:
                        moves.add(n)

            # Règle 2 : Tout est mine
            if len(hidden_neighbors) + len(flagged_neighbors) == value:
                for n in hidden_neighbors:
                    flags.add(n)

        # 2. Le "Guessing" (Si l'IA est bloquée ou au début)
        # Si on n'a rien trouvé (ni move sûr, ni flag)
        if not moves and not flags:
            # On liste toutes les cases encore cachées et non flagguées
            all_hidden = []
            for x in range(self.game.width):
                for y in range(self.game.height):
                    if (x, y) not in self.game.revealed and (x, y) not in self.game.flags:
                        all_hidden.append((x, y))
            
            # On en choisit une au hasard pour débloquer la partie
            if all_hidden:
                guess = random.choice(all_hidden)
                print(f"🎲 L'IA doit deviner ! Tentative sur {guess}")
                moves.add(guess)

        return list(moves), list(flags)