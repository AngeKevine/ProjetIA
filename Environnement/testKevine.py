# Partie test


if __name__ == "__main__":
    from environnement import creer_environnement

    # Test 1 : poids nominaux, une solution est attendue
    env = creer_environnement()
  

    affectation = resoudre_csp(env.robots, env.materiaux)
    print("Nominal   :", affectation)

    # Test 2 : M2 à 7 kg, échec attendu (4+7+3+5 = 19 > 18)
    env2 = creer_environnement()
    env2.materiaux[1].poids = 7
    print("M2 = 7 kg :", resoudre_csp(env2.robots, env2.materiaux))

    # Test 3 : vérification des charges de la solution nominale
    for robot in env.robots:
        total = charge_affectee(affectation, robot.nom, env.materiaux)
        print(robot.nom, ":", total, "/", robot.capacite, "kg")

