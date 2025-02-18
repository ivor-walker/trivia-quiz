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
    except KeyboardInterrupt:
        game.end_game();

game.immediate_end();
