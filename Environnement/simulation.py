from environnement import Robot, Environnement, creer_environnement
from sma import coordonner_deplacements, mettre_a_jour_blocage
from csp import resoudre_csp
from logique import creer_faits, decider
# Cette fonction transforme automatiquement les objets Robot en un dictionnaire que notre SMA sait utiliser.

def recuperer_positions(robots):
    positions = {}

    for robot in robots:
        positions[robot.nom] = robot.position

    return positions
#On calcule la différence entre la position actuelle et la destination:
def deplacer_vers(terrain, robot, destination):
    return terrain.deplacer(robot, destination)
#Relier le SMA aux déplacements
#exécuter_deplacements : prend les destinations souhaités par les robots ,demande quels déplacements sont autorisés.
def executer_deplacements(terrain, intentions):
# donne la liste des robots:
    robots = terrain.robots

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
            terrain.robots
        ))

        if blocage:
            print("Blocage persistant détecté !")
            return "BLOCAGE"

        if not any(chemins_restants.values()):
            return "CHEMINS_TERMINES"

    return "LIMITE_TOURS" #S"	Le nombre maximal de tours a été atteint et il reste des étapes à parcourir.
# Initialisation de la simulation avec le CSP et la logique
def initialiser_simulation(env):

    affectation = resoudre_csp(
        env.robots, env.materiaux
    )

    if affectation is None:
        print("CSP insoluble")
        return None, None

    faits = creer_faits(
        env.robots, env.materiaux, affectation
    )

    return affectation, faits

def recuperer_decisions(env, faits):

    decisions = {}

    for robot in env.robots:

        action, regle = decider(robot.nom, faits)

        decisions[robot.nom] = action

        print(robot.nom, ":", regle)

    return decisions
# Tester la simulation avec deux robots et des chemins prédéfinis
if __name__ == "__main__":

    r1 = Robot("R1", 10, (1, 1), (5, 4))
    r2 = Robot("R2", 8, (1, 2), (5, 5))

    terrain = Environnement(6, 6, [], [r1, r2], [])

    chemins = {
        "R1": [(1, 2), (1, 3)],
        "R2": [(1, 3), (1, 4)]
    }

    resultat = simuler_chemins(terrain, chemins)

    print("\nRésultat final :", resultat)

