# Creation d'une classe materiau avec les attributs
# nom ex M1, M2
# poids en Kg
# position : ligne et colonne
# etat : "au_stock", "transporte" ou "livre"
# self designe l'objet lui meme


class Materiau:
    def __init__(self, nom, poids, position):
        self.nom = nom
        self.poids = poids
        self.position = position
        self.etat = "au_stock"

# Creation d'une classe robot avec les attributs
# nom ex R1
# capacite en Kg : charge maximale
# position : ligne et colonne : actuelle
# depot : case de depot
# charge : poids transporte 0 au depart
# transportes : liste des materiaux a bord
# Charge et transportes ne sont pas de parametres car tous les robots commencent pareil

class Robot:
    def __init__(self, nom, capacite, position, depot):
        self.nom = nom
        self.capacite = capacite    
        self.position = position    
        self.depot = depot          
        self.charge = 0             
        self.transportes = []

#  Creation d'une environnement avec les attributs
# lignes et colonnes 
# obstacles: liste de tuples
# robots : liste de robot
# liste de materiaux

class Environnement:
    def __init__(self, lignes, colonnes, obstacles, robots, materiaux):
        self.lignes = lignes
        self.colonnes = colonnes
        self.obstacles = obstacles     
        self.robots = robots            
        self.materiaux = materiaux

    def case_libre(self, pos):
        """Retourne True si la case est dans la grille et n'est pas un obstacle."""
        ligne = pos[0]
        colonne = pos[1]

        if ligne < 0 or ligne >= self.lignes:
            return False                # hors grille (verticalement)
        if colonne < 0 or colonne >= self.colonnes:
            return False                # hors grille (horizontalement)
        if pos in self.obstacles:
            return False                # c'est un obstacle
        return True

    def deplacer(self, robot, nouvelle_pos):
        """Déplace le robot d'une case. Retourne True si c'est accepté,
        False sinon (et alors rien ne change)."""
        ligne = robot.position[0]
        colonne = robot.position[1]
        nouvelle_ligne = nouvelle_pos[0]
        nouvelle_colonne = nouvelle_pos[1]

        # Distance en nombre de cases : doit être exactement 1
        distance = abs(ligne - nouvelle_ligne) + abs(colonne - nouvelle_colonne)
        if distance != 1:
            return False                # pas une case voisine

        if not self.case_libre(nouvelle_pos):
            return False                # obstacle ou hors grille

        robot.position = nouvelle_pos   # tout est bon : on déplace
        return True

    def charger(self, robot, materiau):
        """Le robot prend le matériau si les 3 conditions sont réunies."""
        if robot.position != materiau.position:
            return False                # le robot n'est pas sur le matériau
        if materiau.etat != "au_stock":
            return False                # matériau déjà pris ou livré
        if robot.charge + materiau.poids > robot.capacite:
            return False                # trop lourd

        materiau.etat = "transporte"
        robot.charge = robot.charge + materiau.poids
        robot.transportes.append(materiau)
        return True

    def decharger(self, robot):
        """Dépose tous les matériaux si le robot est à son dépôt."""
        if robot.position != robot.depot:
            return False                # pas au dépôt
        if len(robot.transportes) == 0:
            return False                # rien à déposer

        for materiau in robot.transportes:
            materiau.etat = "livre"
            materiau.position = robot.depot

        robot.transportes = []          # le robot est vide
        robot.charge = 0
        return True

    def afficher(self):
        """Affiche la grille. # obstacle, . case libre, R1/R2 robots,
        M1..M4 matériaux au sol, D1/D2 dépôts."""
        print("   0  1  2  3  4  5")    # en-tête des colonnes

        for ligne in range(self.lignes):
            texte = str(ligne) + "  "
            for colonne in range(self.colonnes):
                pos = (ligne, colonne)
                symbole = "."                       # par défaut : case vide

                if pos in self.obstacles:
                    symbole = "#"
                for robot in self.robots:
                    if pos == robot.depot:
                        symbole = "D" + robot.nom[1]    # "R1" -> "D1"
                for materiau in self.materiaux:
                    if pos == materiau.position and materiau.etat == "au_stock":
                        symbole = materiau.nom
                for robot in self.robots:
                    if pos == robot.position:
                        symbole = robot.nom             # robot prioritaire

                texte = texte + symbole.ljust(3)
            print(texte)
def creer_environnement():
    robots = [
        Robot("R1", 10, (1, 0), (5, 4)),
        Robot("R2", 8, (4, 0), (5, 5)),
    ]
    materiaux = [
        Materiau("M1", 4, (1, 3)),
        Materiau("M2", 6, (1, 5)),
        Materiau("M3", 3, (4, 1)),
        Materiau("M4", 5, (4, 4)),
    ]
    obstacles = [(2, 2), (3, 2), (3, 3)]
    return Environnement(6, 6, obstacles, robots, materiaux)


# Ce bloc ne s'exécute que si on lance ce fichier directement

if __name__ == "__main__":
    env = creer_environnement()
    r1 = env.robots[0]              # R1 est le premier de la liste

    env.afficher()
    print("Déplacement valide :", env.deplacer(r1, (1, 1)))     # True
    print("Hors grille       :", env.deplacer(r1, (-1, 1)))     # False
    print("Non adjacent      :", env.deplacer(r1, (1, 3)))      # False

    r1.position = (2, 1)            # on place R1 à côté de l'obstacle
    print("Vers obstacle     :", env.deplacer(r1, (2, 2)))      # False
