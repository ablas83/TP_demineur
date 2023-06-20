import sys
hauteur_grille = int(sys.argv[1])
largeur_grille = int(sys.argv[2])

class MineSweeper ():
    def __init__(self, is_playing = False):
        self.is_playing  = is_playing
    def open(self, x, y):
        if self.is_playing:
            print("Ouvrir la case", x, y)
        else :
            raise Exception("La partie n'est pas en cours")

    def flag(self, x, y):
        if self.is_playing:
            print("Flagger la case", x, y)
        else:
            raise Exception("La partie n'est pas en cours")

    def newgame(self, hauteur = 0, largeur = 0):
        self.is_playing = True

ms = MineSweeper()
ms.newgame()
while True:
    coordinput = input("veuillez choisir 'x y' ou 'F x y' pour mettre un flag")
    coord = coordinput.rsplit(" ")
    if len(coord) == 2 and int(coord[0]) and int(coord[1]):
        ms.open(int(coord[0]), int(coord[1]))
    elif len(coord) == 3 and coord[0] == "F" and int(coord[1]) and int(coord[2]):
        ms.flag(int(coord[1]), int(coord[2]))
    else:
        raise ValueError("syntaxe invalide")

