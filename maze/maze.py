import logging
import string
from enum import Enum
from time import sleep
from typing import List, Optional, Union, Tuple


class MazeCell(Enum):
    FREE: int = 0
    WALL: int = 1
    START: int = 2
    END: int = 3
    PATH: int = 4
    VISITED: int = 5
    HEAD: int = 6


class MazeCellColors:
    COLORS = {MazeCell.FREE: (255, 255, 255),  # White for FREE
              MazeCell.WALL: (0, 0, 0),  # Black for WALL
              MazeCell.START: (0, 255, 0),  # Green for START
              MazeCell.END: (255, 0, 0),  # Red for END
              MazeCell.PATH: (0, 205, 255),  # Blue3 for PATH
              MazeCell.VISITED: (255, 255, 197),  # Yellow for VISITED
              MazeCell.HEAD: (0, 0, 255),  # Blue for HEAD
              }

    @classmethod
    def get_color(cls, col: int):
        if 0 <= col < 7:
            if col == 0:
                return MazeCellColors.COLORS[MazeCell.FREE]
            if col == 1:
                return MazeCellColors.COLORS[MazeCell.WALL]
            if col == 2:
                return MazeCellColors.COLORS[MazeCell.START]
            if col == 3:
                return MazeCellColors.COLORS[MazeCell.END]
            if col == 4:
                return MazeCellColors.COLORS[MazeCell.PATH]
            if col == 5:
                return MazeCellColors.COLORS[MazeCell.VISITED]
            if col == 6:
                return MazeCellColors.COLORS[MazeCell.HEAD]
        raise ValueError(f"Invalid color value: {col}")


class Maze:
    file_name: Optional[str]
    verbose: Union[bool, int]

    size_x: int
    size_y: int
    cells: List[List[int]]

    def __init__(self, file_name: Optional[str] = None, verbose: Union[bool, int] = False) -> None:
        self.file_name = file_name
        self.verbose = verbose
        self.size_x, self.size_y = 1, 1
        self.cells = [[MazeCell.WALL.value]]
        if not file_name is None:
            pedantic = (True if self.verbose == 3 else False)
            self.read_maze_from_file(self.file_name, pedantic)

    def init_empty_maze(self, file_name: Optional[str] = None) -> None:
        # Warning: self.cells[0] will not be set!
        if self.verbose > 1:
            msg = "Initializing empty maze"
            logging.debug(msg)
            if self.verbose > 2:
                print(msg)
        self.file_name = file_name
        self.size_x, self.size_y = 0, 0
        self.cells = []

    def read_maze_from_file(self, file_name: str, pedantic: bool = False) -> None:
        self.init_empty_maze(file_name)
        with open(file_name, "r") as file:
            r = 0
            for line in file:
                c = 0
                row = []
                for char in line.rstrip("\n"):
                    if not char in string.printable:
                        continue
                    if char == " ":
                        row.append(MazeCell.FREE.value)
                    elif char in ["#", "-", "+", "|"]:
                        row.append(MazeCell.WALL.value)
                    elif char == "S":
                        row.append(MazeCell.START.value)
                    elif char == "E":
                        row.append(MazeCell.END.value)
                    else:
                        msg = f"Unknown maze character: \"{char}\"; Use Space, #, S or E." + self._add_log_info(c, r)
                        if pedantic:
                            logging.error(msg, exc_info=True)
                            raise ValueError(msg)
                        else:
                            logging.warning(msg)
                            row.append(MazeCell.FREE.value)
                self.cells.append(row)

        # Validate data and calculate size
        self.size_y = len(self.cells)
        if self.size_y == 0:
            msg = f"No maze cells found." + self._add_log_info(0, 0)
            logging.error(msg, exc_info=True)
            raise ValueError(msg)
        self.size_x = len(self.cells[0])

        # Ensure equal length of rows (Pad shorter rows with walls)
        max_length = max(len(row) for row in self.cells)
        for row in self.cells:
            while len(row) < max_length:
                row.append(MazeCell.WALL.value)

        # Validate that there is exact one starting position and at least one end position
        # For compatibility with https://pypi.org/project/labyrinth-py/ add a start and end position
        # in the upper left and lower right corner (with one wall tile to the edge of the world).
        start_count = sum(row.count(MazeCell.START.value) for row in self.cells)
        end_count = sum(row.count(MazeCell.END.value) for row in self.cells)
        if pedantic:
            if start_count != 1:
                msg = f"Invalid number of start points: {start_count}. There must be exactly one start point." + self._add_log_info()
                logging.error(msg, exc_info=True)
                raise ValueError(msg)
            if end_count < 1:
                msg = f"Invalid number of end points: {end_count}. There must be at least one end point." + self._add_log_info()
                logging.error(msg, exc_info=True)
                raise ValueError(msg)
        else:
            if start_count == 0 and end_count == 0:
                if self.size_x >= 3 and self.size_y >= 3 and self.size_x + self.size_y > 3 + 4:
                    if self.cells[1][1] == MazeCell.FREE.value and self.cells[self.size_y - 2][self.size_x - 2] == MazeCell.FREE.value:
                        msg = "Adding START and END." + self._add_log_info()
                        logging.info(msg)
                        self.cells[1][1] = MazeCell.START.value
                        self.cells[self.size_y - 2][self.size_x - 2] = MazeCell.END.value


    def set_field(self, col: int, row: int, value: Union[MazeCell, int], delay: int = 10) -> None:
        self._check_bounds(col, row)  # Raises IndexError() on Out-of-Bounds error
        if not isinstance(value, MazeCell) and not isinstance(value, int):
            msg = f"Value {value} is not a valid MazeCell or int at row {row}, column {col}."
            logging.error(msg, exc_info=True)
            raise TypeError(msg)

        if isinstance(value, MazeCell):
            val = value.value
            name = value.name
        else:
            val = value
            try:
                name = MazeCell(value).name
            except ValueError as err:
                msg = f"Value (int){value} is not a valid MazeCell ENUM (0-6) at row {row}, column {col}: {err}"
                logging.error(msg, exc_info=True)
                print(msg)
                raise err

        # Set the field in the maze
        sleep(delay / 3000)
        if self.verbose > 0:
            logging.debug(f"Set field at ({row=}, {col=}) to {name} ({val=}).")
        self.cells[row][col] = val
        sleep(delay / 7000)

    def get_field(self, col: int, row: int) -> int:
        self._check_bounds(col, row)  # Raises IndexError() on Out-of-Bounds error
        try:
            return self.cells[row][col]
        except Exception as err:
            msg = f"A critical error has occurred at get_field(row={row}, col={col}): {err}"
            logging.error(msg, exc_info=True)
            print(msg)
            raise err

    def get_width(self) -> int:
        return self.size_x

    def get_height(self) -> int:
        return self.size_y

    def get_size(self) -> Tuple[int, int]:
        return self.get_width(), self.get_height()

    def _check_bounds(self, col: int, row: int) -> None:
        if not (0 <= row < self.size_y):
            msg = f"Row index {row} is out of bounds (0 <= row < {self.size_y})."
            logging.error(msg, exc_info=True)
            raise IndexError(msg)
        if not (0 <= col < self.size_x):
            msg = f"Column index {col} is out of bounds (0 <= col < {self.size_x})."
            logging.error(msg, exc_info=True)
            raise IndexError(msg)

    def _add_log_info(self, c: Optional[int] = None, r: Optional[int] = None) -> str:
        log_info = f" (In {self.file_name if self.file_name is not None else 'N/A'}"
        if r is not None or c is not None:
            log_info += f", row={r if r is not None else 'N/A'}, column={c if c is not None else 'N/A'}"
        log_info += ")"
        return log_info
