import random
import sys
from abc import ABCMeta, abstractmethod

hauteur_grille = int(sys.argv[1])
largeur_grille = int(sys.argv[2])


class Tile(metaclass=ABCMeta):
    def __init__(self, _grid, _x, _y):
        self._grid: Grid = _grid
        self._x = _x
        self._y = _y
        self.is_open = False
        self.is_flagged = False
    @abstractmethod
    def __str__(self):
        if self.is_flagged:
            return "F"
        elif self.is_open == False:
            return '#'
        elif self.is_open:
            raise NotImplementedError("La case est déjà ouverte")


class Tilemine(Tile):
    def __str__(self):
        if self.is_open == False:
            return super().__str__()
        else :
            return "O"

class TileHint(Tile):
    def __init__(self, _grid, _x, _y):
        super().__init__(_grid, _x, _y)
        self._hint = None

    @property
    def hint(self):
        mine = 0
        if self._hint is None:
            for i in range(self._y - 1, self._y + 2):
                for j in range(self._x - 1, self._x + 2):
                    if (i > -1 and j > -1 and i < (self._grid.largeur) and j < (self._grid.hauteur)):
                        if isinstance(self._grid.get_tile(i, j), Tilemine):
                            mine += 1
            self._hint = mine
            return mine
        else:
            return self._hint

    def __str__(self):
        if not self.is_open:
           return super().__str__()
        else :
            if self.hint == 0:
                return " "
            else:
                return str(self.hint)

class Grid():
    def __init__(self, hauteur = hauteur_grille, largeur = largeur_grille):
        self._tiles =[[TileHint(self, i, j) for i in range(hauteur)] for j in range(largeur)]
        self.hauteur = hauteur
        self.largeur = largeur
        self.remaining =0
        mines_coord = self._mines_coord()
        for k in mines_coord:
            x= int(k[0])
            y= int(k[1])
            self._tiles [x][y] = Tilemine(self,x,y)
    def _mines_coord(self):
        tableau = list()
        for i in range(self.largeur):
            for j in range(self.hauteur):
                tableau.append((i, j))
        taille = int(len(tableau) * 0.1)
        self.remaining = len(tableau) - taille
        return random.sample(tableau, taille)
    def get_tile(self, x,y):
        return self._tiles[x][y]
    def open(self, x,y):
        if(self._tiles[x][y].is_open):
            raise Exception("la case est deja ouverte")
        if(self._tiles[x][y].is_flagged):
            raise Exception("la case est flaggée")
        self._tiles[x][y].is_open = True
        if isinstance(self._tiles[x][y], TileHint):
            self.remaining -= 1

    def __str__(self):
        chaine_caractere = ""
        for i in range(self.largeur):
            for j in range(self.hauteur):
                chaine_caractere += str(self._tiles[i][j])
            chaine_caractere += "\n"
        return chaine_caractere
    def toggle_flag(self, x, y):
        if self._tiles[x][y].is_open:
            raise Exception("la case est déjà ouverte")
        if self._tiles[x][y].is_flagged:
            self._tiles[x][y].is_flagged = False
        else:
            self._tiles[x][y].is_flagged = True
class MineSweeper ():
    def __init__(self):
        self.is_playing = False
        self._grid:Grid = None
    def open(self, x, y):
        if self.is_playing:
            if x >= self._grid.largeur or y >= self._grid.hauteur :
                raise Exception("Les coordonnées sont hors la grille")
            self._grid.open(x,y)
            print(self._grid)
        else:
            raise Exception("La partie n'est pas en cours")

    def flag(self, x, y):
        if self.is_playing:
            if x >= self._grid.largeur or y >= self._grid.hauteur :
                raise Exception("Les coordonnées sont hors la grille")
            self._grid.toggle_flag(x,y)
            print(self._grid)
        else:
            raise Exception("La partie n'est pas en cours")

    def newgame(self, hauteur = 0, largeur = 0):
        self.is_playing = True
        self._grid = Grid()
        print(self._grid)

ms = MineSweeper()

while True:
    coordinput = input("veuillez choisir 'x y' ou 'F x y' pour mettre un flag ou quit ou newgame")
    coord = coordinput.rsplit(" ")
    if len(coord) == 2 and isinstance(int(coord[0]), int) and isinstance(int(coord[1]), int) :
        try:
            ms.open(int(coord[0]), int(coord[1]))
        except Exception as e:
            print(str(e))

    elif len(coord) == 3 and coord[0] == "F" and isinstance(int(coord[1]), int) and isinstance(int(coord[2]), int):
        try:
            ms.flag(int(coord[1]), int(coord[2]))
        except Exception as e:
            print(str(e))
    elif (coordinput=="quit"):
        break
    elif(coordinput=="newgame"):
        ms.newgame(hauteur_grille,largeur_grille)
    else:
        print("syntaxe invalide")

