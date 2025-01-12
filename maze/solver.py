import copy
from threading import Thread
from time import sleep

from maze.gui import Gui
from maze.maze import MazeCell


class Pos:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Solver(Thread):
    gui: Gui  # Reference to Gui object
    delay: float  # Delay between Maze updates in seconds

    def __init__(self, gui: Gui, delay: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gui = gui
        self.delay = delay

    def run(self) -> None:
        # Initial delay
        sleep(1.0)

        # Keep a backup so the second algorithm can start on a fresh copy
        orig_maze = copy.deepcopy(self.gui.maze)

        # Find starting position for recursive search
        pos_x = -1
        pos_y = -1
        for y in range(self.gui.maze.size_y):
            for x in range(self.gui.maze.size_x):
                if self.gui.maze.get_field(x, y) == MazeCell.START.value:
                    pos_x = x
                    pos_y = y
                    break
        if pos_x == -1:
            raise RuntimeError("No START maze cell found")

        # Run recursive search
        solved = self.solve_recursive(pos_x, pos_y)
        if not self.gui.running:
            return
        if solved:
            print("Solved")
        else:
            print("No solution found")

        # Some delay in between the two algorithms
        sleep(5.0)

        # Run the BFS
        self.gui.maze = copy.deepcopy(orig_maze)
        solved = self.solve_breadth_first(pos_x, pos_y)
        if not self.gui.running:
            return
        if solved:
            print("Solved")
        else:
            print("No solution found")

    def solve_breadth_first(self, x: int, y: int) -> bool:
        sleep(self.delay)
        if self.gui.maze.get_field(x, y) == MazeCell.END.value:
            return True
        height = self.gui.maze.size_y
        width = len(self.gui.maze.cells[0])
        start = Pos(x, y)
        heads = [start]
        parents = {(x, y): None}
        while len(heads) > 0 and self.gui.running:
            sleep(self.delay * 4)
            for h in heads:
                sleep(self.delay)
                if self.gui.maze.get_field(h.x, h.y) == MazeCell.HEAD.value:
                    self.gui.maze.set_field(h.x, h.y, MazeCell.VISITED)
                for p in [Pos(h.x - 1, h.y), Pos(h.x + 1, h.y), Pos(h.x, h.y - 1), Pos(h.x, h.y + 1)]:
                    if 0 <= p.x < width and 0 <= p.y < height:
                        if self.gui.maze.get_field(p.x, p.y) == MazeCell.END.value:
                            # Found "End", plot path
                            parents[(p.x, p.y)] = h
                            current = p
                            while parents[(current.x, current.y)] is not None:
                                current = parents[(current.x, current.y)]
                                if self.gui.maze.cells[current.y][current.x] != MazeCell.START.value:
                                    self.gui.maze.cells[current.y][current.x] = MazeCell.PATH.value
                                    sleep(self.delay)
                            return True
                        if self.gui.maze.get_field(p.x, p.y) == MazeCell.FREE.value:
                            self.gui.maze.set_field(p.x, p.y, MazeCell.HEAD)
                            heads.append(p)
                            parents[(p.x, p.y)] = h  # Track its parent
                heads.remove(h)
        return False

    def solve_recursive(self, x: int, y: int) -> bool:
        if not self.gui.running:
            return False
        sleep(self.delay)
        if self.gui.maze.get_field(x, y) == MazeCell.END.value:
            return True
        if self.gui.maze.get_field(x, y) == MazeCell.FREE.value:
            self.gui.maze.set_field(x, y, MazeCell.HEAD)
        goto = [MazeCell.FREE.value, MazeCell.END.value]
        if x > 0 and self.gui.maze.cells[y][x - 1] in goto:
            solved = self.solve_recursive(x - 1, y)
            if solved:
                if self.gui.maze.get_field(x, y) != MazeCell.START.value:
                    self.gui.maze.set_field(x, y, MazeCell.PATH)
                    sleep(self.delay)
                return solved
        if x < self.gui.maze.size_x - 1 and self.gui.maze.cells[y][x + 1] in goto:
            solved = self.solve_recursive(x + 1, y)
            if solved:
                if self.gui.maze.get_field(x, y) != MazeCell.START.value:
                    self.gui.maze.set_field(x, y, MazeCell.PATH)
                    sleep(self.delay)
                return solved
        if y > 0 and self.gui.maze.cells[y - 1][x] in goto:
            solved = self.solve_recursive(x, y - 1)
            if solved:
                if self.gui.maze.get_field(x, y) != MazeCell.START.value:
                    self.gui.maze.set_field(x, y, MazeCell.PATH)
                    sleep(self.delay)
                return solved
        if y < self.gui.maze.size_y - 1 and self.gui.maze.cells[y + 1][x] in goto:
            solved = self.solve_recursive(x, y + 1)
            if solved:
                if self.gui.maze.get_field(x, y) != MazeCell.START.value:
                    self.gui.maze.set_field(x, y, MazeCell.PATH)
                    sleep(self.delay)
                return solved
        if self.gui.maze.get_field(x, y) == MazeCell.HEAD.value:
            self.gui.maze.set_field(x, y, MazeCell.VISITED)
            sleep(self.delay)
        return False
