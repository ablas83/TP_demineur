import random
import sys
from abc import ABCMeta, abstractmethod

hauteur_grille = int(sys.argv[1])
largeur_grille = int(sys.argv[2])


class Tile(metaclass=ABCMeta):
    def __init__(self, _grid, _x, _y):
        self._grid = _grid
        self._x = _x
        self._y = _y
        self.is_open = False
        self.is_flagged = False
    @abstractmethod
    def __str__(self):
        if self.is_flagged:
            return "F"
        if self.is_open == False:
            return "#"
        if self.is_open:
            raise NotImplementedError("La case est déjà ouverte")

class Tilemine(Tile):
    def __str__(self):
        if self.is_open == False:
            super().__str__()
        else :
            return "O"

class TileHint(Tile):
    def __init__(self, _grid, _x, _y):
        super().__init__(_grid, _x, _y)
        self.hint = 0
    def __str__(self):
        if self.is_open == False:
            super().__str__()
        else :
            if self.hint == 0:
                return " "
            else:
                return chr(self.hint)

class Grid():
    def __init__(self, hauteur = hauteur_grille, largeur = largeur_grille):
        self._tiles = [[]]
        self.hauteur = hauteur
        self.largeur = largeur
        for i in range(hauteur):
            for j in range(largeur):
                self._tiles[i][j] = TileHint(self, i, j)
        mines_coord = self._mines_coord()
        for k in mines_coord:
            x= int(k[0])
            y= int(k[1])
            self._tiles [x][y] = Tilemine(self,x,y)
    def _mines_coord(self):
        tableau = list()
        for i in range(self.hauteur):
            for j in range(self.largeur):
                tableau.append((i, j))
        taille = int(len(tableau) * 0.1)
        return random.sample(tableau, taille)

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

