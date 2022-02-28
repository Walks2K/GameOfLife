"""
Game of Life in Python
"""


import random
import pygame
from pygame.locals import *


class Life:

    def __init__(self, width=800, height=600, cell_size=10, speed=10):
        pygame.init()

        self.screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption('Game of Life')

        self.active = True
        self.cell_size = cell_size
        self.speed = speed

        self.height = height
        self.width = width

        self.grid = self.create_grid(width, height, cell_size)
        self.grid_copy = self.create_grid(width, height, cell_size)

        self.clock = pygame.time.Clock()

        self.run()

    def handle_input(self, event):
        """
        Handle user input

        Args:
            event (pygame.event): event to handle
        """
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == K_r:
                self.grid = self.create_grid(self.width, self.height,
                                             self.cell_size)
                self.grid_copy = self.create_grid(self.width, self.height,
                                                  self.cell_size)
                self.add_random_life(self.grid, self.width, self.height,
                                     self.cell_size)
            elif event.key == K_SPACE:
                self.active = not self.active
        elif event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = x // self.cell_size
            y = y // self.cell_size

            if event.button == 1:
                self.grid[x][y] = 1
            elif event.button == 3:
                self.grid[x][y] = 0

    def create_grid(self, width, height, cell_size):
        """
        Create a grid

        Args:
            width (int): width of the grid
            height (int): height of the grid
            cell_size (int): size of each cell

        Returns:
            grid (list): list of lists containing the grid
        """
        grid = []
        for x in range(width // cell_size):
            column = []
            for y in range(height // cell_size):
                column.append(0)
            grid.append(column)
        return grid

    def draw_grid(self, screen, grid, cell_size, width, height):
        """
        Draw the grid

        Args:
            screen (pygame.Surface): surface to draw on
            grid (list): list of lists containing the grid
            cell_size (int): size of each cell
            width (int): width of the grid
            height (int): height of the grid
        """
        for x in range(width // cell_size):
            for y in range(height // cell_size):
                if grid[x][y] == 0:
                    pygame.draw.rect(
                        screen, (0, 0, 0),
                        (x * cell_size, y * cell_size, cell_size, cell_size))
                else:
                    pygame.draw.rect(
                        screen, (255, 255, 255),
                        (x * cell_size, y * cell_size, cell_size, cell_size))
        for x in range(0, width, cell_size):
            pygame.draw.line(screen, (128, 128, 128), (x, 0), (x, height))
        for y in range(0, height, cell_size):
            pygame.draw.line(screen, (128, 128, 128), (0, y), (width, y))

    def add_random_life(self, grid, width, height, cell_size):
        """
        Add a random life to the grid

        Args:
            grid (list): list of lists containing the grid
            width (int): width of the grid
            height (int): height of the grid
            cell_size (int): size of each cell
        """
        for x in range(width // cell_size):
            for y in range(height // cell_size):
                if random.randint(0, 1) == 0:
                    grid[x][y] = 1

    def calculate_neighbours(self, grid, grid_copy, width, height):
        """
        Calculate the neighbours of each cell

        Args:
            grid (list): list of lists containing the grid
            grid_copy (list): list of lists containing the grid
            width (int): width of the grid
            height (int): height of the grid
        """
        for x in range(width // self.cell_size):
            for y in range(height // self.cell_size):
                grid_copy[x][y] = self.get_neighbours(grid, x, y)

    def get_neighbours(self, grid, x, y):
        """
        Get the neighbours of a cell

        Args:
            grid (list): list of lists containing the grid
            x (int): x coordinate of the cell
            y (int): y coordinate of the cell

        Returns:
            neighbours (int): number of neighbours
        """
        sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                sum += self.get_cell(grid, x + i, y + j)
        sum -= self.get_cell(grid, x, y)
        if sum == 3:
            return 1
        elif sum == 2:
            return self.get_cell(grid, x, y)
        else:
            return 0

    def get_cell(self, grid, x, y):
        """
        Get the value of a cell

        Args:
            grid (list): list of lists containing the grid
            x (int): x coordinate of the cell
            y (int): y coordinate of the cell

        Returns:
            value (int): value of the cell
        """
        if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
            return 0
        else:
            return grid[x][y]

    def run(self):
        """
        Run the game
        """
        self.add_random_life(self.grid, self.width, self.height,
                             self.cell_size)

        while True:
            self.clock.tick(self.speed)
            self.screen.fill((0, 0, 0))
            self.draw_grid(self.screen, self.grid, self.cell_size, self.width,
                           self.height)
            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_input(event)

            if not self.active:
                continue
            self.calculate_neighbours(self.grid, self.grid_copy, self.width,
                                      self.height)
            self.grid, self.grid_copy = self.grid_copy, self.grid


if __name__ == '__main__':
    Life()
