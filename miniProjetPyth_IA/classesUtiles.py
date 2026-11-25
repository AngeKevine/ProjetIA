
class Materiel:

    def __init__(self, nom, poids, nature, lignePos=0, colPos=0, etat="En_STOCK"):
        
        self.nom = nom
        self.Nature = nature
        self.Poids = poids
        self.lignePos = lignePos
        self.colPos = colPos
        self.etat = etat

class Obstacle:

    def __init__(self, nom ="#",lignePos=0, colPos=0):
        
        self.nom = nom
        self.lignePos = lignePos
        self.colPos = colPos



class Robot:
    def __init__(self, capaciteMax, capaciteRestante, nom, depot,  ligne=0, col=0, charges =[]):
        # Attributs d'instance
        self.nom = nom
        self.capaciteMax = capaciteMax
        self.capaciteRestante = capaciteRestante
        self.depot = depot
        self.ligne = ligne
        self.col = col
        self.charges = charges

    def chargerMateriel(self, materiel: Materiel):
        if self.capaciteRestante != 0:
            self.charges.append(materiel)
            self.capaciteRestante = self.capaciteRestante - materiel.Poids
            materiel.etat = "TRANSPORTE"
        else:
            print("Charge maximale du robot atteinte")

    def dechargerMateriel(self, materiel: Materiel):
            if self.capaciteRestante != self.capaciteMax:
                self.charges.pop(materiel)
                self.capaciteRestante = self.capaciteRestante + materiel.Poids
                materiel.etat = "LIVRE"
            else:
                print("Robot déjà vide")
    def afficherContenuRob(self):
        print("Robot ", self.nom, ": charges:")
        for c in self.charges:
            print(c.name, end=" ")



def creer_matrice(nb_lignes, nb_colonnes, valeur='.'):
    return [[valeur for _ in range(nb_colonnes)] for _ in range(nb_lignes)]


class Terrain:
    # Attribut de classe (partagé par toutes les instances)
    liste_robots = []

    def __init__(self, nbrLignes=6, nbrColonnes=6):
        
        self.nbrLignes = nbrLignes
        self.nbrColonnes = nbrColonnes
        self.matrice = creer_matrice(nbrLignes, nbrColonnes)
        self.occupations = []


    def placerRobot(self, robot: Robot):
            if 0 <= robot.ligne < self.nbrLignes and 0 <= robot.col < self.nbrColonnes:
                self.matrice[robot.ligne][robot.col] = robot
            else:
                print(f"Le robot {robot.nom} ne peut pas être placé en dehors du terrain.")



    def initialiserTerrain(self, listeObst=[Obstacle("#",3,3), Obstacle("#",2,3), Obstacle("#",2,1)] , listeRobs= [ Robot(10, 10,"R1", (5,4), 2,3 ), Robot(8, 8, "R2", (5,5), 0,0 ) ], listeMateriels=[ Materiel("M1", 4, "Bois", 1, 3), Materiel("M2", 6, "Acier", 1, 5) ]):

        self.liste_robots = listeRobs

        for ob in listeObst:
            self.matrice[ ob.lignePos ][ ob.colPos ] = ob

        for rob in listeRobs:
            self.placerRobot(rob)

        for mat in listeMateriels:
            self.matrice[mat.lignePos][mat.colPos] = mat




    def deplacerGauche(self, robot: Robot):

        celluleGauche = self.matrice[robot.ligne][robot.col-1]

        if robot.col > 0:

            if celluleGauche == '.':
                self.matrice[robot.ligne][robot.col] = '.'
                robot.col -= 1
                self.placerRobot(robot)
                return True
            elif isinstance(celluleGauche, (Obstacle)):
                print("Le robot ne peut pas se déplacer vers la gauche, obstacle détecté.")
                return False
            
            else:
                if isinstance(celluleGauche, (Materiel)):
                    print("Le robot charge, materiel détecté.")
                    robot.chargerMateriel( celluleGauche)
                    self.matrice[robot.ligne][robot.col] = '.'
                    robot.col -= 1
                    self.placerRobot(robot)
                    return True
                else: return True
            
        else:
            print("Le robot ne peut pas se déplacer vers la gauche, il est déjà à la limite.")
            return False
    
    def deplacerDroite(self, robot: Robot):

        celluleDroite = self.matrice[robot.ligne][robot.col+1]

        if robot.col < self.nbrColonnes - 1:
            if celluleDroite == '.':
                self.matrice[robot.ligne][robot.col] = '.'
                robot.col += 1
                self.placerRobot(robot)
                return True

            elif isinstance(celluleDroite, (Obstacle)):
                print("Le robot ne peut pas se déplacer vers la droite, obstacle détecté.")
                return False
            
            else:
                if isinstance(celluleDroite, (Materiel)):
                    print("Le robot charge, materiel détecté.")
                    robot.chargerMateriel( celluleDroite)
                    self.matrice[robot.ligne][robot.col] = '.'
                    robot.col += 1
                    self.placerRobot(robot)
                    return True
                else: return True
               
        else:
            print("Le robot ne peut pas se déplacer vers la droite, il est déjà à la limite.")
            return False


    def deplacerHaut(self, robot: Robot):

        celluleHaut = self.matrice[robot.ligne-1][robot.col]

        if robot.ligne > 0:
            if celluleHaut == '.':
                self.matrice[robot.ligne][robot.col] = '.'
                robot.ligne -= 1
                self.placerRobot(robot)
                return True
            elif isinstance(celluleHaut, (Obstacle)):
                print("Le robot ne peut pas se déplacer vers le Haut, obstacle détecté.")
                return False
            
            else:
                if isinstance(celluleHaut, (Materiel)):
                    print("Le robot charge, materiel détecté.")
                    robot.chargerMateriel( celluleHaut)
                    self.matrice[robot.ligne][robot.col] = '.'
                    robot.ligne -= 1
                    self.placerRobot(robot)
                    return True
                else: return True

                
        else:
            print("Le robot ne peut pas se déplacer vers le Haut, il est déjà à la limite.")
            return False

    def deplacerBas(self, robot: Robot):

        celluleBas = self.matrice[robot.ligne+1][robot.col]

        if robot.ligne < self.nbrLignes - 1:
            if celluleBas == '.':
                self.matrice[robot.ligne][robot.col] = '.'
                robot.ligne += 1
                self.placerRobot(robot)
                return True
            elif isinstance(celluleBas, (Obstacle)):
                print("Le robot ne peut pas se déplacer vers le bas, obstacle détecté.")
                return False

            else:
                if isinstance(celluleBas, (Materiel)):
                    print("Le robot charge, materiel détecté.")
                    robot.chargerMateriel( celluleBas)
                    self.matrice[robot.ligne][robot.col] = '.'
                    robot.ligne += 1
                    self.placerRobot(robot)
                    return True
                else: return True

            
        else:
            print("Le robot ne peut pas se déplacer vers le bas, il est déjà à la limite.")
            return False



class Tournee:

    def __init__(self, terrain: Terrain, listeRobots, listeMateriaux, matrAssignation = [{"R1Test":["M1Test"]}, {"R2Test":["M2kTest"]}]):

        self.terrain = terrain
        self.listeRobots = listeRobots
        self.listeMateriaux = listeMateriaux
        self.matrAssignation = matrAssignation
        