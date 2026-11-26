import heapq




############ Etape 1: Modelisation Environnement #################################

#Classe pour Modeliser un Materiel à transporter
# (lignePos, colPos) represente la position de ce materiel sur la grille
class Materiel:

    def __init__(self, nom, poids, nature, lignePos=0, colPos=0, etat="En_STOCK"):
        
        self.nom = nom
        self.Nature = nature
        self.Poids = poids
        self.lignePos = lignePos
        self.colPos = colPos
        self.etat = etat

#Classe pour Modeliser un Obstacle sur la grille
# (lignePos, colPos) represente la position de cet Obstacle sur la grille
class Obstacle:

    def __init__(self, nom ="#",lignePos=0, colPos=0):
        
        self.nom = nom
        self.lignePos = lignePos
        self.colPos = colPos



class Depot:

    def __init__(self, nom, lignePos=0, colPos=0):
        
        self.nom = nom
        self.lignePos = lignePos
        self.colPos = colPos

#Classe pour Modeliser un Robot
# (ligne, col) represente la position de ce Robot sur la grille
# un Robot peu effectuer plusieurs action, implementer par les méthodes chargerMateriel(), dechargerMateriel()
class Robot:
    def __init__(self, capaciteMax, capaciteRestante, nom, depot: Depot,  ligne=0, col=0, charges =[]):
    
        self.nom = nom
        self.capaciteMax = capaciteMax
        self.capaciteRestante = capaciteRestante
        self.depot: Depot = depot
        self.ligne = ligne
        self.col = col
        self.charges = charges

    #Cet methode charge un materiel dans le Robot
    def chargerMateriel(self, materiel: Materiel):
        if self.capaciteRestante >= materiel.Poids:
            self.charges.append(materiel)
            self.capaciteRestante = self.capaciteRestante - materiel.Poids
            materiel.etat = "TRANSPORTE"  # lorsqu'un Materiel est chargé dans un Robot, son état passe en mode TRANSPORTE
        else:
            print("Charge maximale du robot atteinte")


    #Cet methode décharge un materiel du Robot    
    def dechargerMateriel(self, materiel: Materiel):
            if self.capaciteRestante != self.capaciteMax:
                self.charges.remove(materiel)
                self.capaciteRestante = self.capaciteRestante + materiel.Poids
                materiel.etat = "LIVRE" # lorsqu'un Materiel est déchargé du Robot, son état passe en mode LIVRE
            else:
                print("Robot déjà vide")

    # Methode pas forcement utile, juste si besoin d'afficher les caractéristiques d'un robot
    def afficherContenuRob(self):
        print("Robot ", self.nom, ": charges:")
        for c in self.charges:
            print(c.nom, end=" ")



def creer_matrice(nb_lignes, nb_colonnes, valeur='.'):
    return [[valeur for _ in range(nb_colonnes)] for _ in range(nb_lignes)]


#Classe pour Modeliser un la Grille, le Terrai sur le quel le Robot va se déplacer
# nbrLignes=6 et nbrColonnes representent la taille de la Grille
# matrice represente la matrice qui va contenir toutes les cases de la grille
# un Terrain doit etre initialiser manuellement avec initialiserTerrain() pour qu'il soit utile dans la Tournee
# Sur un Terrain, on peu effectuer plusieurs action comme: placerRobot(robot: Robot), deplacerGauche(robot: Robot),...
class Terrain:
    # Attribut de classe (partagé par toutes les instances de Terrain)
    liste_robots = []

    def __init__(self, nbrLignes=6, nbrColonnes=6):
        
        self.nbrLignes = nbrLignes
        self.nbrColonnes = nbrColonnes
        self.matrice = creer_matrice(nbrLignes, nbrColonnes)
        self.occupations = []


    #Cet methode le Robot "robot" sur la grille du Terrain
    def placerRobot(self, robot: Robot):
            if 0 <= robot.ligne < self.nbrLignes and 0 <= robot.col < self.nbrColonnes:
                self.matrice[robot.ligne][robot.col] = robot
            else:
                print(f"Le robot {robot.nom} ne peut pas être placé en dehors du terrain.")



    def initialiserTerrain(self, listeObst=[Obstacle("#",3,3), Obstacle("#",2,3), Obstacle("#",2,1)] , listeRobs= [ Robot(10, 10,"R1Def", (5,4), 2,3 ), Robot(8, 8, "R2Def", (5,5), 0,0 ) ], listeMateriels=[ Materiel("M1Def", 4, "Bois", 1, 3), Materiel("M2Def", 6, "Acier", 1, 5) ], listeDepots=None):

        self.liste_robots = listeRobs
        listeDepots = listeDepots if listeDepots is not None else []

        for d in listeDepots:
            self.matrice[ d.lignePos ][d.colPos ]= d.nom

        for ob in listeObst:
            self.matrice[ ob.lignePos ][ ob.colPos ] = ob

        for rob in listeRobs:
            self.placerRobot(rob)

        for mat in listeMateriels:
            self.matrice[mat.lignePos][mat.colPos] = mat



    #Cet methode permet de déplacer un robot du Terrain vers la Gauche, pareil pour les méthodes du mème type: Droite, Haut, Bas
    def deplacerGauche(self, robot: Robot):

        

        if robot.col > 0:

            celluleGauche = self.matrice[robot.ligne][robot.col-1]

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

        

        if robot.col < self.nbrColonnes - 1:

            celluleDroite = self.matrice[robot.ligne][robot.col+1]

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

        

        if robot.ligne > 0:
            celluleHaut = self.matrice[robot.ligne-1][robot.col]

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


        if robot.ligne < self.nbrLignes - 1:

            celluleBas = self.matrice[robot.ligne+1][robot.col]

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


# Une Tournee, pour le moment pas utile, passer à une autre Classe
class Tournee:

    def __init__(self, terrain: Terrain, listeRobots, listeMateriaux, matrAssignation = [{"R1Test":["M1Test"]}, {"R2Test":["M2kTest"]}]):

        self.terrain = terrain
        self.listeRobots = listeRobots
        self.listeMateriaux = listeMateriaux
        self.matrAssignation = matrAssignation






############ Etape 2: Recherche heuristique#################################



# une classe Noeud pour modiliser les états possibles du domaine de recherche
# un noeud correspond à un état (actuel ou pas), il a un parent noeudParent (état précédent)
#   et la distance déjà parcourue en arrivant à ce noeud: gDistParc
#   et la distance Heuristique restant à parcourir en arrivant à ce noeud: heurustq




class NoeudHeuristique:
    def __init__(self, ligne=0, col=0, noeudParent=None, gDistParc=0, heurustq=0):
        self.ligne = ligne
        self.col = col
        self.noeudParent = noeudParent
        self.gDistParc = gDistParc
        self.heurustq = heurustq
        self.fonctionHeur = gDistParc + heurustq   # f = g + h


class ParcourHeuristiq:

    def __init__(self, robot: Robot, terrain):
        self.noeudCourant = NoeudHeuristique(robot.ligne, robot.col, None, 0)
        self.butHeuristq = (robot.depot.lignePos , robot.depot.colPos )
        self.terrain = terrain
        self.noeudsOuverts = []     # tas (heap)
        self.noeudsFermes = set()   # ensemble de (ligne, col)
        self.noeudsChemin = []
        self.distanceParc = 0
        self._compteur = 0          # départage les égalités dans le tas

    def approximHeuristq(self, noeud):
        return abs(noeud.ligne - self.butHeuristq[0]) + abs(noeud.col - self.butHeuristq[1])

    def insererNoeudHeur(self, noeud):
        self._compteur += 1
        heapq.heappush(self.noeudsOuverts, (noeud.fonctionHeur, self._compteur, noeud))

    def successeursNoeud(self, noeud):
        succ = []
        for dl, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            l, c = noeud.ligne + dl, noeud.col + dc
            if 0 <= l < self.terrain.nbrLignes and 0 <= c < self.terrain.nbrColonnes:
                if not isinstance(self.terrain.matrice[l][c], Obstacle):
                    n = NoeudHeuristique(l, c, noeud, noeud.gDistParc + 1)
                    n.heurustq = self.approximHeuristq(n)
                    n.fonctionHeur = n.gDistParc + n.heurustq
                    succ.append(n)
        return succ

    def solutionHeuristq(self):
        self.insererNoeudHeur(self.noeudCourant)

        while self.noeudsOuverts:
            _, _, courant = heapq.heappop(self.noeudsOuverts)
            pos = (courant.ligne, courant.col)

            if pos in self.noeudsFermes:
                continue
            self.noeudsFermes.add(pos)

            if pos == tuple(self.butHeuristq):
                # reconstruire le chemin depuis les parents
                chemin = []
                n = courant
                while n is not None:
                    chemin.append(n)
                    n = n.noeudParent
                chemin.reverse()
                self.noeudsChemin = chemin
                self.distanceParc = courant.gDistParc
                return chemin

            for s in self.successeursNoeud(courant):
                if (s.ligne, s.col) not in self.noeudsFermes:
                    self.insererNoeudHeur(s)

        print("Echec Recherche Heuristique, aucun chemin")
        return None