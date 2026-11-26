from environnement import Robot, Environnement
from simulation import executer_deplacements, recuperer_positions, simuler_chemins


def creer_terrain():

    r1 = Robot("R1", 10, (1, 1), (5, 4))
    r2 = Robot("R2", 8, (1, 2), (5, 5))

    return Environnement(6, 6, [], [r1, r2], [])


# Test 1 : simulation réussie

terrain = creer_terrain()

chemins = {
    "R1": [(1, 2), (1, 3)],
    "R2": [(1, 3), (1, 4)]
}

assert simuler_chemins(terrain, chemins) == "CHEMINS_TERMINES"

assert recuperer_positions(terrain.robots) == {
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