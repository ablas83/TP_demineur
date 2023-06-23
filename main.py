import abc
import random
import sys
from abc import ABCMeta, abstractmethod

hauteur_grille = int(sys.argv[1])  #pylint disable: invalid-name
largeur_grille = int(sys.argv[2])  #pylint disable: invalid-name


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
        elif not self.is_open:
            return "#"
        elif self.is_open:
            raise NotImplementedError("La case est déjà ouverte")

    def open(self):
        self.is_open = True


class Tilemine(Tile):
    def __str__(self):
        if not self.is_open:
            return super().__str__()
        else:
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
                    if -1 < i < self._grid.largeur and -1 < j < self._grid.hauteur:
                        if isinstance(self._grid.get_tile(i, j), Tilemine):
                            mine += 1
            self._hint = mine
            return mine
        else:
            return self._hint

    def __str__(self):
        if not self.is_open:
            return super().__str__()
        else:
            if self.hint == 0:
                return " "
            else:
                return str(self.hint)

    def open(self):
        super().open()
        if self.hint == 0:
            for i in range(self._y - 1, self._y + 2):
                for j in range(self._x - 1, self._x + 2):
                    if -1 < i < self._grid.largeur and -1 < j < self._grid.hauteur:
                        if i != self._y or j != self._x:
                            self._grid._open_full(i, j)


class Grid:
    def __init__(self, hauteur=hauteur_grille, largeur=largeur_grille):
        self._tiles = [
            [TileHint(self, i, j) for i in range(hauteur)] for j in range(largeur)
        ]
        self.hauteur = hauteur
        self.largeur = largeur
        self.remaining = 0
        self.isMine = False  #pylint disable: invalid-name

    def _mines_coord(self, x, y):
        tableau = list()
        for i in range(self.largeur):
            for j in range(self.hauteur):
                if i != x and j != y:
                    tableau.append((i, j))
        taille = int((self.hauteur * self.largeur) * 0.1)
        self.remaining = (self.largeur * self.hauteur) - taille
        return random.sample(tableau, taille)

    def generateGrid(self, x, y):
        mines_coord = self._mines_coord(x, y)
        for k in mines_coord:
            x = int(k[0])
            y = int(k[1])
            self._tiles[x][y] = Tilemine(self, x, y)

    def get_tile(self, x, y):  #pylint disable: invalid-name
        return self._tiles[x][y]

    def open(self, x, y):  #pylint disable: invalid-name
        if self._tiles[x][y].is_open:
            raise Exception("la case est deja ouverte")
        if self._tiles[x][y].is_flagged:
            raise Exception("la case est flaggée")
        self._open_full(x, y)

    def __str__(self):
        chaine_caractere = ""
        for i in range(self.largeur):
            for j in range(self.hauteur):
                chaine_caractere += str(self._tiles[i][j])
            chaine_caractere += "\n"
        return chaine_caractere

    def toggle_flag(self, x, y):  #pylint disable: invalid-name
        if self._tiles[x][y].is_open:
            raise Exception("la case est déjà ouverte")
        if self._tiles[x][y].is_flagged:
            self._tiles[x][y].is_flagged = False
        else:
            self._tiles[x][y].is_flagged = True

    def _open_full(self, x, y):  #pylint disable: invalid-name
        if not self._tiles[x][y].is_open:
            self._tiles[x][y].open()
            if isinstance(self._tiles[x][y], TileHint):
                self.remaining -= 1
            else:
                self.isMine = True


class MineSweeper:
    def __init__(self):
        self.is_playing = False
        self.first_exec = False
        self._grid: Grid = None

    def open(self, x, y):  #pylint disable: invalid-name
        if self.is_playing:
            if not self.first_exec:
                self._grid.generateGrid(x, y)
                self.first_exec = True
            if x >= self._grid.largeur or y >= self._grid.hauteur:
                raise Exception("Les coordonnées sont hors de la grille")
            self._grid.open(x, y)
            if self.is_win():
                print("Gagné!")
            if self.is_lost():
                print("Perdu!")
            print(self._grid)
        else:
            raise Exception("La partie n'est pas en cours")
        self.is_playing = not self.is_win() and not self.is_lost()
        if not self.is_playing:
            self.first_exec = False

    def flag(self, x, y):  #pylint disable: invalid-name
        if self.is_playing:
            if x >= self._grid.largeur or y >= self._grid.hauteur:
                raise Exception("Les coordonnées sont hors de la grille")
            self._grid.toggle_flag(x, y)
            print(self._grid)
        else:
            raise Exception("La partie n'est pas en cours")

    def newgame(self, hauteur=0, largeur=0):
        self.is_playing = True
        self.first_exec = False
        self._grid = Grid()
        print(self._grid)

    def is_win(self):
        return self._grid.remaining == 0

    def is_lost(self):
        return self._grid.isMine


class PlayGame:
    def __init__(self, MineSweeper, Player):
        self.MineSweeper = MineSweeper
        self.Player = Player

    def run (self):
        while True:
            coordinput = input(
                "Veuillez choisir 'x y' ou 'F x y' pour mettre un flag, ou 'quit' ou 'newgame': "
            )
            coord = coordinput.rsplit(" ")
            if (
                    len(coord) == 2
                    and isinstance(int(coord[0]), int)
                    and isinstance(int(coord[1]), int)
            ):
                try:
                    self.MineSweeper.open(int(coord[0]), int(coord[1]))
                except Exception as e:
                    print(str(e))
            elif (
                    len(coord) == 3
                    and coord[0] == "F"
                    and isinstance(int(coord[1]), int)
                    and isinstance(int(coord[2]), int)
            ):
                try:
                    self.MineSweeper.flag(int(coord[1]), int(coord[2]))
                except Exception as e:
                    print(str(e))
            elif coordinput == "quit":
                break
            elif coordinput == "newgame":
                self.MineSweeper.newgame(hauteur_grille, largeur_grille)
            else:
                print("Syntaxe invalide")


class Player(metaclass=ABCMeta):
    def get_action(self, action, x=None, y=None):
        raise NotImplementedError


class PlayerHuman(Player):
    def get_action(self, action, x=None, y=None):
        if action == "open":
            return ActionOpen(x, y)
        elif action == "flag":
            return ActionFlag(x, y)
        elif action == "newgame":
            return ActionNewGame()
        elif action == "quit":
            return ActionQuit()

    def gameover(self, MineSweeper):
        if MineSweeper.is_lost() :
            print("Perdu !")
            print(MineSweeper._grid)
        if MineSweeper.is_win() :
            print("Gagné !")
            print(MineSweeper._grid)



class Action (metaclass=ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        pass


class ActionOpen(Action):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ActionFlag(Action):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ActionNewGame(Action):

    def __init__(self):
        pass


class ActionQuit(Action):
    def __init__(self):
        pass


ms = MineSweeper()
