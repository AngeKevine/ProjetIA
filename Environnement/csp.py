# Creation d'une fonction Charge affectee qui recoit en parametre:
# affectation: nom du materiau affectee
# nom_robot : nom du robot
# materiaux : dictionnaire de M et R Il est partiel pendant la recherche
# materiau.nom teste si la cle existe
# affectation[materiau.nom] : le robot associe

def charge_affectee(affectation, nom_robot, materiaux):
    """Somme des poids des matériaux déjà affectés à ce robot."""
    total = 0
    for materiau in materiaux:
        if materiau.nom in affectation:                    # déjà affecté ? bool
            if affectation[materiau.nom] == nom_robot:     # à ce robot ?
                total = total + materiau.poids
    return total


def capacites_respectees(affectation, robots, materiaux):
    """Retourne False si un robot dépasse sa capacité, True sinon."""
    for robot in robots:
        if charge_affectee(affectation, robot.nom, materiaux) > robot.capacite:
            return False
    return True

def backtracking(affectation, robots, materiaux):
    """Cherche une affectation complète. Retourne un dictionnaire ou None."""

    # CAS DE BASE : tous les matériaux sont affectés -> solution trouvée
    if len(affectation) == len(materiaux):
        return affectation

    # Choisir le prochain matériau non affecté
    materiau_courant = None
    for materiau in materiaux:
        if materiau.nom not in affectation:
            materiau_courant = materiau
            break

    # Essayer chaque robot (chaque valeur du domaine)
    for robot in robots:
        affectation[materiau_courant.nom] = robot.nom      # on essaie

        if capacites_respectees(affectation, robots, materiaux):
            resultat = backtracking(affectation, robots, materiaux)  # récursion
            if resultat is not None:
                return resultat                            # solution remontée

        del affectation[materiau_courant.nom]              # RETOUR EN ARRIÈRE

    return None 

                                           # aucun robot ne convient
def resoudre_csp(robots, materiaux):
    """Fonction appelée par main.py.
    Retourne {"M1": "R1", ...} ou None si le CSP est insoluble."""
    return backtracking({}, robots, materiaux)


if __name__ == "__main__":
    from environnement import creer_environnement

    # Poids nominaux : une solution est attendue
    env = creer_environnement()
    affectation = resoudre_csp(env.robots, env.materiaux)
    print("Nominal :", affectation)
    # {'M1': 'R1', 'M2': 'R1', 'M3': 'R2', 'M4': 'R2'}

    # M2 à 7 kg : total 4+7+3+5 = 19 > 10+8 = 18, donc échec attendu
    env2 = creer_environnement()
    env2.materiaux[1].poids = 7
    print("M2 = 7 kg :", resoudre_csp(env2.robots, env2.materiaux))   # None