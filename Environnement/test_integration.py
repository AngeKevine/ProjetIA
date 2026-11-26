from environnement import creer_environnement
from simulation import initialiser_simulation, recuperer_decisions

env = creer_environnement()

affectation, faits = initialiser_simulation(env)

assert affectation is not None

print("Affectation :", affectation)

decisions = recuperer_decisions(env, faits)

print("Décisions :", decisions)

assert decisions == {
    "R1": ("aller", (1, 3)),
    "R2": ("aller", (4, 1))
}

print("Test integration CSP et logique : OK")

# Test CSP insoluble

env2 = creer_environnement()
env2.materiaux[1].poids = 7

affectation, faits = initialiser_simulation(env2)

assert affectation is None
assert faits is None

print("Test CSP insoluble : OK")
