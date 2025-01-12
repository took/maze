import argparse
import logging
import os
import sys

from maze.gui import Gui
from maze.maze import Maze
from maze.solver import Solver


def type_loglevel(level):
    try:
        loglevel = getattr(logging, level.upper())
    except AttributeError:
        raise argparse.ArgumentTypeError("'%s' is not a valid log level. Please use %s" % (
            level, [x for x in logging._nameToLevel.keys() if isinstance(x, str)]))
    return loglevel


def main():
    # Initialise ArgumentParser
    parser = argparse.ArgumentParser(description="Maze")
    parser.add_argument("-m", "--maze", type=str, default="mazes/maze.txt",
                        help="Filename of maze to load (Default: mazes/maze.txt)")
    parser.add_argument("-d", "--delay", type=int, default=200,
                        help="Delay for maze updates in milliseconds (Default: 200)")
    parser.add_argument("-rc", "--recursion-limit", type=int, default=None,
                        help="Set python recursion limit (Default: Do not change)")
    parser.add_argument("--fps", type=int, default=60, help="Max frames per second (Default: 60)")
    parser.add_argument("--logfile", default="app.log", help="Path to the log file (Default: app.log)")
    parser.add_argument("-l", "--loglevel", type=type_loglevel, default="WARNING",
                        help="Log level verbosity (Default: WARNING, Recommended: DEBUG, INFO, WARNING or ERROR)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output (Default: False)")
    parser.add_argument("-vv", "--very-verbose", action="store_true", help="Very verbose output (Default: False)")
    parser.add_argument("-vvv", "--very-very-verbose", action="store_true",
                        help="Very very verbose output (Default: False)")
    args = parser.parse_args()

    # Configure the logging module
    pid = os.getpid()
    logging.basicConfig(filename=args.logfile, level=args.loglevel, datefmt="%Y-%m-%d %H:%M:%S",
                        format=f"%(asctime)s %(name)s PID {pid} %(levelname)s - %(message)s")

    # Set verbosity level
    verbose = False
    if args.very_very_verbose:
        verbose = 3
        logging.warning("Very very verbose output enabled, we might also become more pedantic with some checks now!")
    elif args.very_verbose:
        verbose = 2
    elif args.verbose:
        verbose = 1

    if verbose:
        msg = "Application started with verbosity %d." % verbose
        logging.info(msg)
        if args.loglevel != logging.DEBUG:
            msg = "%s Use --loglevel DEBUG to see even more events in logfile \"%s\"!" % (msg, args.logfile)
        else:
            msg = "%s See even more events in logfile \"%s\"!" % (msg, args.logfile)
        print(msg)
    else:
        logging.info("Application started.")

    # Set recursion limit
    try:
        if args.recursion_limit:
            sys.setrecursionlimit(args.recursion_limit)
    except Exception as err:
        msg = "A critical error has occurred: %s" % err
        logging.critical(msg, exc_info=True)
        print(msg)
        raise err

    # Run Application
    try:
        # Load Maze
        maze = Maze(file_name=args.maze, verbose=verbose)

        # Configure and initialize GUI
        gui = Gui(maze=maze, max_fps=args.fps, verbose=verbose)

        # Start Solver Thread
        solver = Solver(gui=gui, delay=args.delay/1000)
        solver.start()

        # Run the main loop
        gui.main_loop()

        # After the main loop finished, signal everyone to stop
        msg = "Shutting down."
        logging.info(msg)
        print(msg)
        gui.running = False

        # Wait for any running threads to stop
        solver.join()

    except Exception as err:
        msg = "A critical error has occurred: %s" % err
        logging.critical(msg, exc_info=True)
        print(msg)
        raise err

    # Application termination and cleanup
    logging.info("Application terminated.")
    print("Application terminated. Goodbye!")


if __name__ == "__main__":
    main()
