from game import Game;
from view import View;

view = View();
game = Game(view);

# Initialise the game
try:
    # Connects to API and gets questions
    game.init_questions();

    # Resets game state and asks for initial info
    game.reset();

# If the initial connection to the API fails, end the game immediately
except ConnectionError as e:
    print(e);
    game.immediate_end();

# If the user interrupts the initial setup, end the game immediately
except KeyboardInterrupt:
    game.immediate_end();

# Ask questions until the game is over
while not game.game_over:
    try:
        game.play_round();

    # If the user interrupts the game, attempt to end normally
    except KeyboardInterrupt:
        try:
            game.end_game();
        
        # If the user interrupts the game again, end immediately
        except KeyboardInterrupt:
            break;
    
    # If some connection to the API is attempted during the game and fails, end immediately
    except ConnectionError as e:
        print(e);
        break;
    
game.immediate_end();
