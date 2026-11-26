from classesUtiles import Robot, Terrain
from simulation import simuler_chemins, recuperer_positions


def creer_terrain():

    r1 = Robot(10, 10, "R1", (5, 4), 1, 1, charges=[])
    r2 = Robot(8, 8, "R2", (5, 5), 1, 2, charges=[])

    terrain = Terrain()

    terrain.initialiserTerrain(
        listeObst=[],
        listeRobs=[r1, r2],
        listeMateriels=[]
    )

    return terrain


# Test 1 : simulation réussie

terrain = creer_terrain()

chemins = {
    "R1": [(1, 2), (1, 3)],
    "R2": [(1, 3), (1, 4)]
}

assert simuler_chemins(terrain, chemins) == "CHEMINS_TERMINES"

assert recuperer_positions(terrain.liste_robots) == {
    "R1": (1, 3),
    "R2": (1, 4)
}

print("Test 1 : OK")


# Test 2 : blocage persistant

terrain = creer_terrain()

chemins = {
    "R1": [(1, 2)],
    "R2": [(1, 1)]
}

assert simuler_chemins(terrain, chemins) == "BLOCAGE"

print("Test 2 : OK")


# Test 3 : limite de tours

terrain = creer_terrain()

chemins = {
    "R1": [(1, 0)],
    "R2": [(1, 3), (1, 4)]
}

assert simuler_chemins(
    terrain, chemins, max_tours=1
) == "LIMITE_TOURS"

print("Test 3 : OK")

print("Tous les tests de simulation sont réussis !")