import sys
hauteur_grille = int(sys.argv[1])
largeur_grille = int(sys.argv[2])

class MineSweeper ():
    def open(self, x, y):
        print("Ouvrir la case", x, y)

    def flag(self, x, y):
        print("Flagger la case", x, y)
ms = MineSweeper()
while True:
    coordinput = input("veuillez choisir 'x y' ou 'F x y' pour mettre un flag")
    coord = coordinput.rsplit(" ")
    if len(coord) == 2 and int(coord[0]) and int(coord[1]):
        ms.open(int(coord[0]), int(coord[1]))
    elif len(coord) == 3 and coord[0] == "F" and int(coord[1]) and int(coord[2]):
        ms.flag(int(coord[1]), int(coord[2]))
    else:
        raise ValueError("syntaxe invalide")

