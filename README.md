# Maze

Visualize how computers solve a maze!

# Description

This project is a small programming exercise that implements two classic search algorithms—recursive depth-first
search (DFS) and breadth-first search (BFS)—to solve a maze.

The maze is defined in a text file (`maze.txt`) using these characters in a simple `.txt` file:

- `" "` for empty spaces
- `"#"` for walls
- `"S"` for the start position
- `"E"` for the end position

The project uses the Pygame library to visualize the search algorithms in real time as they attempt to find a solution.

## Project Status & Contributions

This project is currently in a **working** state. Contributions, feedback, and code improvements are highly encouraged!

To contribute or provide feedback, please use GitHub's [Create a Ticket](https://github.com/took/maze/issues/new)
feature. Alternatively, you can reach out via [email](mailto:info@sd-gp.de).

If you'd like to contribute code, feel free to fork the repository and create a pull request with your changes.

## Installation

To install and run the project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/maze.git
    cd maze
    ```

2. **Install dependencies**:
   If you have `pip` installed, run:
    ```bash
    pip install -r requirements.txt
    ```

   You may optionally use a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Run the program**:
    ```bash
    python3 main.py
    ```

## Usage

Once the program is running, a Pygame window will display the progress of the selected search algorithm (recursive
depth-first and/or breadth-first search) as it navigates through the maze.

You can specify options via command-line
arguments, see also:

```bash
python3 main.py --help
```

```
usage: main.py [-h] [-m MAZE] [-d DELAY] [-rc RECURSION_LIMIT] [--fps FPS] [--logfile LOGFILE] [-l LOGLEVEL]
               [-v] [-vv] [-vvv]

Maze

options:
  -h, --help            show this help message and exit
  -m MAZE, --maze MAZE  Filename of maze to load (Default: mazes/maze.txt)
  -d DELAY, --delay DELAY
                        Delay for maze updates in milliseconds (Default: 200)
  -rc RECURSION_LIMIT, --recursion-limit RECURSION_LIMIT
                        Set python recursion limit (Default: Do not change)
  --fps FPS             Max frames per seconf (Default: 60)
  --logfile LOGFILE     Path to the log file (Default: app.log)
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Log level verbosity (Default: WARNING, Recommended: DEBUG, INFO, WARNING or ERROR)
  -v, --verbose         Verbose output (Default: False)
  -vv, --very-verbose   Very verbose output (Default: False)
  -vvv, --very-very-verbose
                        Very very verbose output (Default: False)
```
