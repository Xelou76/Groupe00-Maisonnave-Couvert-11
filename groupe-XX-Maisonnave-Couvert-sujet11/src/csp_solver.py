import random

class CSPSolver:
    def __init__(self, game):
        self.game = game

    def solve(self):
        """
        Stratégie hybride :
        1. Tente de résoudre avec la logique pure (CSP - Satisfaction de Contraintes).
        2. Si bloqué, calcule les probabilités (Heuristique) pour jouer le coup le moins risqué.
        """
        moves = set()   # Cases sûres à cliquer
        flags = set()   # Mines identifiées
        
        # --- PHASE 1 : LOGIQUE DÉTERMINISTE (Certitudes) ---
        # On cherche des coups sûrs à 100%
        found_deterministic = False
        
        # On copie la liste des révélés pour éviter les problèmes de modification pendant la boucle
        for (x, y) in list(self.game.revealed):
            val = self.game.get_value(x, y)
            
            # Les cases 0 sont gérées par le moteur, on les ignore ici
            if val == 0: 
                continue 

            neighbors = self.game.get_neighbors(x, y)
            hidden = [n for n in neighbors if n not in self.game.revealed and n not in self.game.flags]
            flagged = [n for n in neighbors if n in self.game.flags]
            
            # S'il n'y a plus de voisins cachés, on passe
            if not hidden:
                continue

            # RÈGLE A : Si le nombre de drapeaux = le chiffre de la case
            # -> Tous les autres voisins cachés sont SÛRS.
            if len(flagged) == val:
                for n in hidden:
                    moves.add(n)
                    found_deterministic = True

            # RÈGLE B : Si (voisins cachés + drapeaux) = le chiffre de la case
            # -> Tous les voisins cachés sont des MINES.
            if len(hidden) + len(flagged) == val:
                for n in hidden:
                    flags.add(n)
                    found_deterministic = True

        # Si la logique a trouvé quelque chose, on joue ces coups immédiatement
        # Pas besoin de prendre des risques
        if found_deterministic:
            return list(moves), list(flags)

        # --- PHASE 2 : LOGIQUE PROBABILISTE (Heuristique) ---
        # Si on arrive ici, c'est que l'IA est bloquée logiquement.
        # Elle doit prendre un risque calculé.
        print("🤔 Logique épuisée. Calcul des probabilités...")
        
        best_guess = self._get_safest_guess()
        
        if best_guess:
            # On ajoute le meilleur devinette à la liste des coups à jouer
            moves.add(best_guess)
        
        return list(moves), list(flags)

    def _get_safest_guess(self):
        """
        Calcule la probabilité de danger pour chaque case frontière.
        Retourne la case avec le % de risque le plus faible.
        """
        prob_map = {} # Dictionnaire {(x,y) : probabilité_danger}
        
        # On parcourt les frontières (cases révélées avec voisins cachés)
        for (x, y) in self.game.revealed:
            val = self.game.get_value(x, y)
            neighbors = self.game.get_neighbors(x, y)
            hidden = [n for n in neighbors if n not in self.game.revealed and n not in self.game.flags]
            flagged = [n for n in neighbors if n in self.game.flags]
            
            if not hidden:
                continue
                
            # Formule : Probabilité = (Mines Restantes) / (Cases Cachées)
            mines_left = val - len(flagged)
            probability = mines_left / len(hidden)
            
            for cell in hidden:
                # Si une case est voisine de plusieurs chiffres, on garde la probabilité la plus élevée (Pessimisme)
                # Cela évite de sous-estimer le danger.
                if cell in prob_map:
                    prob_map[cell] = max(prob_map[cell], probability)
                else:
                    prob_map[cell] = probability

        # CAS 1 : Aucune information disponible (ex: tout début de partie ou zone isolée)
        if not prob_map:
            # On cherche une case au hasard parmi celles non révélées
            all_hidden = []
            for x in range(self.game.width):
                for y in range(self.game.height):
                    if (x, y) not in self.game.revealed and (x, y) not in self.game.flags:
                        all_hidden.append((x, y))
            
            if all_hidden:
                guess = random.choice(all_hidden)
                print(f"🎲 Aucune info : Tentative au hasard sur {guess}")
                return guess
            return None

        # CAS 2 : On a des probabilités, on choisit la plus faible
        # On trie le dictionnaire par probabilité croissante
        sorted_guesses = sorted(prob_map.items(), key=lambda item: item[1])
        
        best_case = sorted_guesses[0][0]     # La coordonnée (x, y)
        best_prob = sorted_guesses[0][1]     # La probabilité (0.0 à 1.0)
        
        # Affichage propre en pourcentage (ex: 14.5%)
        print(f"📊 Meilleure option : {best_case} avec {best_prob*100:.1f}% de risque de mine.")
        
        return best_case