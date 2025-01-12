from typing import Union

import pygame

from maze.maze import Maze, MazeCellColors


class Gui:
    maze: Maze
    verbose: Union[bool, int]

    running: bool
    screen: pygame.Surface
    clock: pygame.time.Clock

    def __init__(self, maze: Maze, max_fps: int = 60, verbose: Union[bool, int] = False) -> None:
        self.maze = maze
        self.max_fps = max_fps
        self.verbose = verbose

        self.running = True

        default_cell_size = 42
        max_window_size_on_start = 640
        window_width = min(max_window_size_on_start, maze.get_width() * default_cell_size)
        window_height = min(max_window_size_on_start, maze.get_height() * default_cell_size)

        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
        pygame.display.set_caption("Maze")

        self.clock = pygame.time.Clock()

    def main_loop(self) -> None:
        # Pygame Main Loop
        while self.running:
            # Check for quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Render Maze
            self.draw_maze(self.screen)
            pygame.display.update()

            # Limit FPS
            self.clock.tick(self.max_fps)
        pygame.quit()

    def draw_maze(self, screen: pygame.Surface) -> None:
        # Calculate sizes
        size_x, size_y = screen.get_size()
        min_offset = 5
        cell_size_x = (size_x - min_offset) // self.maze.size_x
        cell_size_y = (size_y - min_offset) // self.maze.size_y
        offset_x = (size_x - (cell_size_x * self.maze.size_x)) // 2
        offset_y = (size_y - (cell_size_y * self.maze.size_y)) // 2

        # Fill Background
        screen.fill(pygame.color.THECOLORS['gray'])

        # Render Maze
        for row in range(self.maze.size_y):
            for col in range(self.maze.size_x):
                val = self.maze.get_field(col, row)
                cell_color = MazeCellColors.get_color(val)
                pygame.draw.rect(screen, cell_color,
                                 (offset_x + col * cell_size_x, offset_y + row * cell_size_y, cell_size_x, cell_size_y))
