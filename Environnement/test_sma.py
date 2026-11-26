from sma import coordonner_deplacements, mettre_a_jour_blocage
# Test 1 : même destination
positions = {"R1": (0, 1), "R2": (0, 3)}
intentions = {"R1": (0, 2), "R2": (0, 2)}
#assert : permet de vérifier automatiquement qu'une condition est vraie
assert coordonner_deplacements(positions, intentions) == {
    "R1": True, "R2": False
}

print("Test 1 : OK")


# Test 2 : case déjà occupée
positions = {"R1": (1, 1), "R2": (1, 2)}
intentions = {"R1": (1, 2), "R2": (1, 3)}

assert coordonner_deplacements(positions, intentions) == {
    "R1": False, "R2": True
}

print("Test 2 : OK")


# Test 3 : échange de positions
positions = {"R1": (1, 1), "R2": (1, 2)}
intentions = {"R1": (1, 2), "R2": (1, 1)}

assert coordonner_deplacements(positions, intentions) == {
    "R1": False, "R2": False
}

print("Test 3 : OK")


# Test 4 : aucun conflit
positions = {"R1": (0, 0), "R2": (4, 0)}
intentions = {"R1": (0, 1), "R2": (4, 1)}

assert coordonner_deplacements(positions, intentions) == {
    "R1": True, "R2": True
}

print("Test 4 : OK")

print("Tous les tests SMA sont réussis !")

# Test 5 : blocage persistant

compteur = 0

for tour in range(3):

    compteur, blocage = mettre_a_jour_blocage(
        compteur, False
    )

    print("Tour :", tour + 1,
          "| Compteur :", compteur,
          "| Blocage :", blocage)

assert blocage == True 

print("Test 5 : OK")


# Test 6 : reprise de la progression

compteur, blocage = mettre_a_jour_blocage(2, True) 

assert compteur == 0
assert blocage == False

print("Test 6 : OK")
