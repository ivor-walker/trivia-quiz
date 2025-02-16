import curses

"""
Class for the View of the application
"""
class View:

    """
    Constructor for the View class
    """
    def __init__(self):
        # Disable echoing of keypresses
        curses.noecho();

        # Enable reading of keys instantly
        curses.cbreak();

        # Initialise the screen
        self.stdscr = curses.initscr();

        # Enable keypad mode
        self.stdscr.keypad(True);

        # Make getch non-blocking
        self.stdscr.nodelay(True);
        
        # Clear the screen
        self.stdscr.clear();
        self.stdscr.refresh();

    """
    Get a single character input
    @return: The character input
    """
    def get_char_input(self):
        return self.stdscr.getch();

    """
    Get a line of user's input
    """
    def get_line_input(self):
        return self.stdscr.getstr().decode('utf-8');
          
    """
    Show a welcome form to the user
    @param welcome_message: The welcome message to display
    """
    def show_welcome_form(self, welcome_message, ask_for_name):
        # Clear the screen
        self.stdscr.clear();

        # Display the welcome message
        self.stdscr.addstr(0, 0, welcome_message);

        # Ask the user for their name
        self.stdscr.addstr(1, 0, ask_for_name, curses.A_BOLD);

        # Refresh the screen
        self.stdscr.refresh();

    """
    Ask the user a multiple choice question
    @param question: The question to ask
    @param choices: The choices to display
    """
    def show_multiple_choice(self, question, choices):
        # Clear the screen
        self.stdscr.clear();
        
        # Display the question
        start_line = 1;
        self.stdscr.addstr(start_line, 0, question, curses.A_BOLD);

        # Display the choices 
        for i, choice in enumerate(choices):
            self.stdscr.addstr(i + start_line + 1, 0, f"{i+1}. {choice}");

        # Refresh the screen
        self.stdscr.refresh();

    """
    Replace the first line with an error message
    @param error_message: The error message to display
    """
    def show_multiple_choice_error(self, error_message):
        # Clear the first line
        self.stdscr.addstr(0, 0, " " * 100);

        # Display the error message
        self.stdscr.addstr(0, 0, error_message, curses.A_BOLD);

        # Refresh the screen
        self.stdscr.refresh();
    
    """
    Update the timer
    @param time_left: The time left
    """
    def update_timer(self, time_left):
        # TODO
        pass;

    """
    Show a message to the user
    @param message: The message to display
    """
    def show_message(self, message):
        # TODO
        pass;

    """
    Display the leaderboard
    @param leaderboard: The leaderboard to display
    """
    def display_leaderboard(self, leaderboard):
        # TODO
        pass;
    
    """
    End the application
    """
    def exit(self):
        # End the application
        curses.endwin();


