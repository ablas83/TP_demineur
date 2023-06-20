import sys
from abc import ABCMeta
hauteur_grille = int(sys.argv[1])
largeur_grille = int(sys.argv[2])


class Tile(metaclass=ABCMeta):
    def __init__(self, _grid, _x, _y, is_open, is_flagged):
        self._grid = _grid
        self._x = _x
        self._y = _y
        self.is_open = is_open
        self.is_flagged = is_flagged
class Grid():
    pass
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
        grid = Grid()

ms = MineSweeper()

while True:
    coordinput = input("veuillez choisir 'x y' ou 'F x y' pour mettre un flag ou quit ou newgame")
    coord = coordinput.rsplit(" ")
    if len(coord) == 2 and int(coord[0]) and int(coord[1]):
        try:
            ms.open(int(coord[0]), int(coord[1]))
        except Exception as e:
            print("La partie n'est pas en cours")
    elif len(coord) == 3 and coord[0] == "F" and int(coord[1]) and int(coord[2]):
        try:
            ms.flag(int(coord[1]), int(coord[2]))
        except Exception as e:
            print("La partie n'est pas en cours")
    elif (coordinput=="quit"):
        break
    elif(coordinput=="newgame"):
        ms.newgame(hauteur_grille,largeur_grille)
    else:
        raise ValueError("syntaxe invalide")

