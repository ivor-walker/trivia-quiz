from game import Game;

import curses;
from curses import wrapper;

# Initialize the screen
stdscr = curses.initscr();

# Enable echoing of keys
curses.echo();

# Enable reading of keys without pressing enter
curses.cbreak();

# Enable keypad mode
stdscr.keypad(True);

"""
Main function
"""
def main(stdscr):
    # Start the game
    game = Game(stdscr);
    
    # Ask questions until the game is over
    while game.game_over == False:
        try:
            game.ask_question();
    
        # Handle keyboard interrupts
        except KeyboardInterrupt:
    
            # Try to end the game normally
            try:
                game.end_game();
    
            # If user interrupts again, force the game to end
            except KeyboardInterrupt:
                game.end_game(offer_restart=False);
                curses.endwin();
                sys.exit(0);

# Run the main function
wrapper(main);
