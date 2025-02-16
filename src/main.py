from game import Game;
from view import View;

try:
    # Start the game
    view = View(stdscr);
    game = Game(view);
    
    # Ask questions until the game is over
    while game.game_over == False:
        try:
            game.play_round();
    
        # Handle keyboard interrupts (i.e the user wants to quit)
        except KeyboardInterrupt:
    
            # Try to end the game normally
            try:
                game.end_game();
    
            # If user interrupts again, force the game to end
            except KeyboardInterrupt:
                game.end_game(immediate_end = True);

finally:
    # End the game
    game.end_game(immediate_end = True);
