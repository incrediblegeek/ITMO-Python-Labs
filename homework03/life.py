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
        self.clist = self.cell_list()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.clist)
            self.update_cell_list(self.clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True) -> List:
        """ Создание списка клеток. """
        self.clist = []
        if randomize:
            for i in range(self.cell_height):
                self.clist.append([random.randint(0, 1) for j in range(self.cell_width)])
        else:
            self.clist = [[0] * self.cell_width for i in range(self.cell_height)]
        return self.clist

    def draw_cell_list(self, clist: list) -> None:
        """ Отображение списка клеток """
        for h in range(self.cell_height):
            for w in range(self.cell_width):
                x = w * self.cell_size
                y = h * self.cell_size
                a = self.cell_size
                b = self.cell_size
                if clist[h][w] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('Black'), (x, y, a, b))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('Red'), (x, y, a, b))

    def get_neighbours(self, cell: Tuple) -> List:
        """ Вернуть список соседей для указанной ячейки """
        neighbours = []
        x = cell[0]
        y = cell[1]
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (0 <= i < self.cell_height) and (0 <= j < self.cell_width) and (i != x or j != y):
                    neighbours.append(self.clist[i][j])
        return neighbours

    def update_cell_list(self, cell_list: List) -> List:
        """ Выполнить один шаг игры. """
        new_clist = []
        new_clist = deepcopy(cell_list)
        for i in range(0, self.cell_height):
            for j in range(0, self.cell_width):
                if self.get_neighbours((i, j)).count(1) == 2:
                    continue
                elif self.get_neighbours((i, j)).count(1) == 3:
                    new_clist[i][j] = 1
                else:
                    new_clist[i][j] = 0
        self.clist = new_clist
        return self.clist

if __name__ == '__main__':
    game = GameOfLife(640, 480, 10)
    game.run()