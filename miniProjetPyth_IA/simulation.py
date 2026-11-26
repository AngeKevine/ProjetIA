from classesUtiles import Robot, Terrain
from sma import coordonner_deplacements, mettre_a_jour_blocage
# Cette fonction transforme automatiquement les objets Robot en un dictionnaire que notre SMA sait utiliser.

def recuperer_positions(robots):

    positions = {}

    for robot in robots:
        positions[robot.nom] = (robot.ligne, robot.col)

    return positions
#On calcule la différence entre la position actuelle et la destination:
def deplacer_vers(terrain, robot, destination): #déplacer le robot d’une seule case vers destination.

    ligne, col = destination

    if not (0 <= ligne < terrain.nbrLignes
            and 0 <= col < terrain.nbrColonnes):
        return False

    if terrain.matrice[ligne][col] != ".":
        return False
#Calculer la direction:
    delta_ligne = ligne - robot.ligne
    delta_col = col - robot.col
# verifier Mouvement : Droite, Gauche, Haut, Bas
    if (delta_ligne, delta_col) == (0, 1):
        terrain.deplacerDroite(robot)

    elif (delta_ligne, delta_col) == (0, -1):
        terrain.deplacerGauche(robot)

    elif (delta_ligne, delta_col) == (-1, 0):
        terrain.deplacerHaut(robot)

    elif (delta_ligne, delta_col) == (1, 0):
        terrain.deplacerBas(robot)

    else:
        return False
#Vérifier le résultat:
    return (robot.ligne, robot.col) == destination
#Relier le SMA aux déplacements
#exécuter_deplacements : prend les destinations souhaités par les robots ,demande quels déplacements sont autorisés.
def executer_deplacements(terrain, intentions):
# donne la liste des robots:
    robots = terrain.liste_robots

    positions = recuperer_positions(robots)
#reçoit les positions actuelles et les destinations souhaitées.
    autorisations = coordonner_deplacements(
        positions, intentions
    )
#crée un dictionnaire vide pour chaque robot.
    resultats = {}

    for robot in robots:

        if autorisations.get(robot.nom, False):

            resultats[robot.nom] = deplacer_vers(
                terrain, robot, intentions[robot.nom]
            )

        else:
            resultats[robot.nom] = False

    return resultats
#Programmer la boucle:
def simuler_chemins(terrain, chemins, max_tours=50):

    chemins_restants = {
        nom: list(chemin)
        for nom, chemin in chemins.items()
    }

    compteur = 0
#Numérote les tours de 1 à max_tours, qui vaut 50 par défaut.
    for tour in range(1, max_tours + 1):

        if not any(chemins_restants.values()):
            return "CHEMINS_TERMINES"

        print("\nTour", tour)

        intentions = {}

        for nom, chemin in chemins_restants.items():

            if chemin:
                intentions[nom] = chemin[0]
            else:
                intentions[nom] = None

        resultats = executer_deplacements(
            terrain, intentions
        )

        for nom, deplacement in resultats.items():

            if deplacement:
                chemins_restants[nom].pop(0) # Si le déplacement a été effectué, on supprime la première destination du chemin restant du robot.

        progression = any(resultats.values())

        compteur, blocage = mettre_a_jour_blocage(
            compteur, progression
        )

        print("Intentions :", intentions)
        print("Déplacements :", resultats)
        print("Positions :", recuperer_positions(
            terrain.liste_robots
        ))

        if blocage:
            print("Blocage persistant détecté !")
            return "BLOCAGE"

        if not any(chemins_restants.values()):
            return "CHEMINS_TERMINES"

    return "LIMITE_TOURS" #S"	Le nombre maximal de tours a été atteint et il reste des étapes à parcourir.
# Tester la simulation avec deux robots et des chemins prédéfinis
if __name__ == "__main__":

    r1 = Robot(10, 10, "R1", (5, 4), 1, 1, charges=[])
    r2 = Robot(8, 8, "R2", (5, 5), 1, 2, charges=[])

    terrain = Terrain()

    terrain.initialiserTerrain(
        listeObst=[],
        listeRobs=[r1, r2],
        listeMateriels=[]
    )

    chemins = {
        "R1": [(1, 2), (1, 3)],
        "R2": [(1, 3), (1, 4)]
    }

    resultat = simuler_chemins(terrain, chemins)

    print("\nRésultat final :", resultat)

#Tester avec deux véritables robots: 
if __name__ == "__main__":
#5,4 : son déôpt, 0,1 : sa position de départ, charges = [] : il transport rien au départ.
    r1 = Robot(10, 10, "R1", (5, 4), 0, 1, charges=[])
    r2 = Robot(8, 8, "R2", (5, 5), 0, 3, charges=[])

    terrain = Terrain()

    terrain.initialiserTerrain(
        listeObst=[],
        listeRobs=[r1, r2],
        listeMateriels=[]
    )

    intentions = {
        "R1": (0, 2),
        "R2": (0, 2)
    }

    print("Avant :", recuperer_positions([r1, r2]))

    resultats = executer_deplacements(terrain, intentions)

    print("Déplacements :", resultats)
    print("Après :", recuperer_positions([r1, r2]))

