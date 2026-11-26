def creer_faits(robots, materiaux, affectation):
    """Construit la liste des faits à partir de l'environnement et du CSP."""
    faits = []
    for robot in robots:
        faits.append(("position", robot.nom, robot.position))
        faits.append(("depot", robot.nom, robot.depot))
        faits.append(("charge", robot.nom, robot.charge))
        faits.append(("capacite", robot.nom, robot.capacite))
    for materiau in materiaux:
        faits.append(("poids", materiau.nom, materiau.poids))
        faits.append(("pos_materiau", materiau.nom, materiau.position))
        faits.append(("etat", materiau.nom, materiau.etat))
        faits.append(("affecte", materiau.nom, affectation[materiau.nom]))
    return faits

def valeur(faits, relation, sujet):
    """Retourne la valeur d'un fait, ex. valeur(faits, "charge", "R1") -> 4."""
    for fait in faits:
        if fait[0] == relation and fait[1] == sujet:
            return fait[2]
    return None


def modifier(faits, relation, sujet, nouvelle_valeur):
    """Remplace la valeur d'un fait existant (actualisation des faits)."""
    for i in range(len(faits)):
        if faits[i][0] == relation and faits[i][1] == sujet:
            faits[i] = (relation, sujet, nouvelle_valeur)


def materiaux_du_robot(faits, nom_robot, etat):
    """Liste des matériaux affectés à ce robot et dans cet état."""
    resultat = []
    for fait in faits:
        if fait[0] == "affecte" and fait[2] == nom_robot:
            nom_materiau = fait[1]
            if valeur(faits, "etat", nom_materiau) == etat:
                resultat.append(nom_materiau)
    return resultat

def decider(nom_robot, faits):
    """Applique la première règle dont les conditions sont vraies.
    Retourne (action, nom_de_la_regle). Une action est un tuple :
    ("charger", "M1"), ("aller", (1, 3)), ("decharger", None), ("rien", None)."""

    position = valeur(faits, "position", nom_robot)
    depot = valeur(faits, "depot", nom_robot)
    charge = valeur(faits, "charge", nom_robot)
    capacite = valeur(faits, "capacite", nom_robot)
    au_stock = materiaux_du_robot(faits, nom_robot, "au_stock")

    # RÈGLE 1 : décharger
    # SI le robot est à son dépôt, transporte quelque chose et n'a plus rien à ramasser
    if position == depot and charge > 0 and len(au_stock) == 0:
        return ("decharger", None), "Règle 1 : décharger au dépôt"

    # RÈGLE 2 : charger
    # SI le robot est sur un matériau qui lui est affecté, au stock, et que la capacité suffit
    for nom_materiau in au_stock:
        if valeur(faits, "pos_materiau", nom_materiau) == position:
            poids = valeur(faits, "poids", nom_materiau)
            if charge + poids <= capacite:
                return ("charger", nom_materiau), "Règle 2 : charger " + nom_materiau

    # RÈGLE 3 : rejoindre le prochain matériau
    # SI il reste un matériau affecté au stock
    if len(au_stock) > 0:
        cible = valeur(faits, "pos_materiau", au_stock[0])
        return ("aller", cible), "Règle 3 : aller vers " + au_stock[0]

    # RÈGLE 4 : rejoindre le dépôt
    # SI plus rien à ramasser et le robot transporte quelque chose
    if charge > 0:
        return ("aller", depot), "Règle 4 : aller au dépôt"

    return ("rien", None), "Aucune règle : tournée terminée"

def mettre_a_jour(faits, nom_robot, action):
    """Modifie les faits après une action de chargement ou de déchargement."""
    type_action = action[0]

    if type_action == "charger":
        nom_materiau = action[1]
        modifier(faits, "etat", nom_materiau, "transporte")
        nouvelle_charge = valeur(faits, "charge", nom_robot) + valeur(faits, "poids", nom_materiau)
        modifier(faits, "charge", nom_robot, nouvelle_charge)

    elif type_action == "decharger":
        for nom_materiau in materiaux_du_robot(faits, nom_robot, "transporte"):
            modifier(faits, "etat", nom_materiau, "livre")
        modifier(faits, "charge", nom_robot, 0)


def mettre_a_jour_position(faits, nom_robot, nouvelle_position):
    """À appeler par main.py après un déplacement réellement exécuté."""
    modifier(faits, "position", nom_robot, nouvelle_position)


if __name__ == "__main__":
    from environnement import creer_environnement
    from csp import resoudre_csp

    env = creer_environnement()
    affectation = resoudre_csp(env.robots, env.materiaux)
    faits = creer_faits(env.robots, env.materiaux, affectation)

    # Simulation simplifiée : le robot "se téléporte" à sa cible
    # (dans le vrai projet, A* et le SMA géreront le déplacement)
    for etape in range(7):
        action, regle = decider("R1", faits)
        print("Étape", etape + 1, ":", regle)
        if action[0] == "aller":
            mettre_a_jour_position(faits, "R1", action[1])
        mettre_a_jour(faits, "R1", action)
