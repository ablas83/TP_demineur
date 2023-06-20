import sys
hauteur_grille = int(sys.argv[1])
largeur_grille = int(sys.argv[2])
while True:
    coordinput = input("veuillez choisir x et y")
    coord = coordinput.rsplit(" ")
    if len(coord) == 2 and int(coord[0]) and int(coord[1]):
        print("Ouvrir la case", coord[0], coord[1])
    elif len(coord) == 3 and coord[0] == "F" and int(coord[1]) and int(coord[2]):
        print("Flagger la case", coord[1], coord[2])
    else:
        raise ValueError("syntaxe invalide")
