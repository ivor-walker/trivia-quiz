from game import Game;
from view import View;

import traceback;

import signal;

# Initialise view and game objects in global scope
view = View();
game = Game(view);

"""
Handle ctrl+c signal
"""
def signal_handler(sig, frame):
    game.end_game();

# Register signal handler
signal.signal(signal.SIGINT, signal_handler);

try:
    game.reset();

    # Ask questions until the game is over
    while game.game_over == False:
        game.play_round();

# If user presses ctrl+c, end the game
except KeyboardInterrupt:
    game.end_game();

# TODO remove
except Exception as e:
    traceback.print_exc();

# If the loop stops, force the game to end
finally:
    game.immediate_end();
