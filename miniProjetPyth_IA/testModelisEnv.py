from modelistationEnv import Robot, Terrain, Materiel, Obstacle, ParcourHeuristiq, Depot


######################################## Fonction Utiles #######################################

def afficherGrille(terrain: Terrain):
    print("Grille du terrain :")
    print("nombre de robots presents sur le terrain : ", len(terrain.liste_robots))
    for ligne in terrain.matrice:
        for c in ligne:
            if isinstance(c, (Materiel, Robot, Depot)):
                print(c.nom, end="")
            elif isinstance(c, (Obstacle)):
                print("#", end="")
                #print("(",c.lignePos,',',c.colPos,")", end="")
            else:
                print(c, end="")
        print()


def deplacerRobot(terrain: Terrain, robot: Robot):


    print("**********************Tuto pour deplacer le robo:******************")
    print (" touches z ->Entrer pour monter")
    print (" touches s ->Entrer pour descendre")
    print (" touches d ->Entrer pour un pas à droite")
    print (" touches a ->Entrer pour un pas à gauche")
    print("**********************Tuto pour deplacer le robo:******************")

    direction = ''
    resp = True
    while (direction != 'q') and resp:
        direction = input("Appuyez sur 'q' pour quitter ou  Utilisez z, s, d ou a. pour continuer : ")

        match direction:
            case 'q':
                print("Fin du déplacement.")
                break
            case 'z':
                resp =terrain.deplacerHaut(robot)
            case 's':
                resp =terrain.deplacerBas(robot)
            case 'd':
                resp =terrain.deplacerDroite(robot)
            case 'a':
                resp =terrain.deplacerGauche(robot)
            case _:
                print("Touche non reconnue. Utilisez z, s, q, d ou a.")
        afficherGrille(terrain)

######################################## fin fonction Utiles #######################################



############ Programme Test Etape 1:Modelisation Environnement #################################
def testProg1():
    r1 = Robot(10, 10, "R1", (5,4), 2,3 )
    print (r1.nom)
    print(r1.depot)
    r1.depot=(1,1)
    print(r1.depot)

    t = Terrain()
    afficherGrille(t)
    t.initialiserTerrain()
    afficherGrille(t)

    deplacerRobot(t, r1)

############ Fin de Programme Test Etape 1: Modelisation Environnement #################################



############ Programme Test Etape 2: Recherche heuristique#################################

def testProg2Heuristique():
    
    t = Terrain()


    listeObst=[Obstacle("#",3,3), Obstacle("#",3,2), Obstacle("#",2,2)]

    dpot1= Depot("D1", 5,4)
    dpot2= Depot("D2", 5,5)
    r1 = Robot(10, 10,"R1", dpot1, 1,0 )

    listeRobs= [ r1 , Robot(8, 8, "R2", dpot2, 4,0 ) ]

    listeMateriels=[ Materiel("M1", 4, "Bois", 1, 3), Materiel("M2", 6, "Acier", 1, 5), Materiel("M3", 3, "Plastique", 4, 1), Materiel("M4", 5, "Aluminium", 4, 4) ]

    listeDepots = [dpot1, dpot2]
    t.initialiserTerrain(listeObst, listeRobs, listeMateriels, )   # pour placer les obstacles, robots et meteriel
    afficherGrille(t)

    chemin = ParcourHeuristiq(r1, t).solutionHeuristq()
    if chemin:
        print(" --> ".join(f"({n.ligne},{n.col})" for n in chemin))

############ Fin de programme test Etape 2: Recherche heuristique#################################

# Décommenter le programme que vous voulez tester:


#testProg1()
testProg2Heuristique()

    

