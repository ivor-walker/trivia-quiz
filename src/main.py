from game import Game;
from view import View;

import traceback;

# Create the view and game objects
view = View();
game = Game(view);

try:
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

except Exception as e:
    traceback.print_exc();

finally:

    # End the game
    game.end_game(immediate_end = True);

    traceback.print_exc();
    print("Goodbye!");
