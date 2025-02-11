from game import Game;
import signal;

# Start the game
game = Game();

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
