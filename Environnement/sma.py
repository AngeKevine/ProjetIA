def coordonner_deplacements(positions, intentions):

    autorisations = {} # crée un dictionnaire vide qui contiendra les décisions finales du SMA.
    cases_occupees = set(positions.values()) #mémoriser toutes les cases occupées au début du tour.
    cases_reservees = set() #crée un ensemble contenant les destinations déjà autorisées pour ce tour.

    for robot in sorted(intentions): #R1 est traité avant R2

        destination = intentions[robot]

        if destination is None: #Attendre 
            autorisations[robot] = False

        elif destination in cases_occupees:
            autorisations[robot] = False

        elif destination in cases_reservees:
            autorisations[robot] = False

        else:
            autorisations[robot] = True #Aucun conflit
            cases_reservees.add(destination)

    return autorisations
#Tester :
if __name__ == "__main__":

    positions = {
        "R1": (0, 1),
        "R2": (0, 3)
    }

    intentions = {
        "R1": (0, 2),
        "R2": (0, 2)
    }

    resultat = coordonner_deplacements(positions, intentions)

    print(resultat)

def mettre_a_jour_blocage(compteur, progression, limite=3):
    if progression:
        compteur = 0
    else:
        compteur += 1

    blocage = compteur >= limite #indiquant si la simulation doit s'arrêter
    return compteur, blocage
