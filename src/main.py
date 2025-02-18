from game import Game;
from view import View;

import traceback;

import signal;

view = View();
game = Game(view);

# Reset the game
try:
    game.reset();
except KeyboardInterrupt:
    game.immediate_end();

# Ask questions until the game is over
while game.game_over == False:
    try:
        game.play_round();

    # If the user interrupts the game, attempt to end normally
    except KeyboardInterrupt:
        try:
            game.end_game();

        # If the user interrupts the game again, end immediately
        except KeyboardInterrupt:
            break;

game.immediate_end();
