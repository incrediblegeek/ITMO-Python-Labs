import pygame
from pygame.locals import *
import random
from copy import deepcopy
from typing import List, Tuple

class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('Black'))
        self.clist = CellList(self.cell_height, self.cell_width, True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            self.draw_cell_list(self.clist)
            self.clist = self.clist.update()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self, clist: list) -> None:
        """ Отображение списка клеток """
        for cell in clist:
            x = cell.col * self.cell_size
            y = cell.row * self.cell_size
            a = self.cell_size
            b = self.cell_size
            if cell.is_alive() == 0:
                pygame.draw.rect(self.screen, pygame.Color('Black'), (x, y, a, b))
            else:
                pygame.draw.rect(self.screen, pygame.Color('Red'), (x, y, a, b))


class Cell:

    def __init__(self, row: int, col: int, state: bool = False) -> None:
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self) -> bool:
        return self.state


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize: bool = False, is_file: bool=False, file_clist: list=[]) -> None:
        self.nrows = nrows
        self.ncols = ncols
        self.randomize = randomize
        self.clist = []

        if randomize:
            for i in range(self.nrows):
                self.clist.append([Cell(i, j, random.randint(0, 1)) for j in range(self.ncols)])
        else:
            for i in range(self.nrows):
                self.clist.append([Cell(i, j, False) for j in range(self.ncols)])

        if is_file:
            self.clist = file_clist

    def get_neighbours(self, cell: Cell) -> List[Cell]:
        neighbours = []
        x = cell.row
        y = cell.col
        for row in range(x - 1, x + 2):
            for col in range(y - 1, y + 2):
                if (0 <= row < self.nrows) and (0 <= col < self.ncols) and (row != x or col != y):
                    neighbours.append(self.clist[row][col])
        return neighbours

    def update(self):
        new_clist = deepcopy(self)
        for row in range(self.nrows):
            for col in range(self.ncols):
                neighbours = new_clist.get_neighbours(new_clist.clist[row][col])
                sum = 0
                for i in neighbours:
                    if i.is_alive() == 1:
                        sum += 1
                if new_clist.clist[row][col].is_alive() == 0 and sum == 3:
                    self.clist[row][col] = Cell(row, col, True)
                elif new_clist.clist[row][col].is_alive() == 1 and (sum == 2 or sum == 3):
                    self.clist[row][col] = Cell(row, col, True)
                else:
                    self.clist[row][col] = Cell(row, col, False)
        return self

    def __iter__(self):
        self.row_index = 0
        self.col_index = 0
        return self

    def __next__(self):
        if self.row_index < self.nrows:
            cell = self.clist[self.row_index][self.col_index]
            self.col_index += 1
            if self.col_index == self.ncols:
                self.col_index = 0
                self.row_index += 1
            return cell
        else:
            raise StopIteration

    def __str__(self):
        str = ''
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.clist[row][col].state == 1:
                    str += '1'
                else:
                    str += '0'
            str += '\n'
        return str

    @classmethod
    def from_file(cls, filename):
        new_clist = []
        f = open(filename, 'r')
        line = f.readline()
        row = 0
        while line:
            new_clist.append([])
            col = 0
            for sym in line:
                if sym == '0' or sym == '1':
                    new_clist[row].append(Cell(row, col, bool(int(sym))))
                    col += 1
            line = f.readline()
            row += 1
        clist = cls(len(new_clist), len(new_clist[0]))
        clist.clist = new_clist
        return clist


if __name__ == '__main__':
    game = GameOfLife(640, 480, 10)
    game.run()