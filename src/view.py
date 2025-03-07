import curses

"""
Class for the View of the application
"""
class View:

    """
    Constructor: curses initialisation
    """
    def __init__(self):
        # Initialise the screen
        self.stdscr = curses.initscr();

        # Disable echoing of keypresses
        curses.noecho();
        
        # Enable keypad mode
        self.stdscr.keypad(True);
        
        # Disable signal interrupts
        curses.raw(); 

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
    @return: The line of user's input
    """
    def get_line_input(self):
        return self.stdscr.getstr().decode('utf-8');
          
    """
    Show a welcome form to the user
    @param welcome_message: The welcome message to display
    """
    def show_welcome_form(self, welcome_message, ask_for_name):
        self.stdscr.clear();

        # Display the welcome message
        self.stdscr.addstr(0, 0, welcome_message);

        # Ask the user for their name
        self.stdscr.addstr(1, 0, ask_for_name, curses.A_BOLD);

        self.stdscr.refresh();

    """
    Ask the user a multiple choice question
    @param question: The question to ask
    @param choices: The choices to display
    @param info_message: Optional information message to display
    """
    def show_multiple_choice(self, 
        question, 
        choices,
        info_message = None
    ):
        self.stdscr.clear();
        
        # Set the cursor to the top left corner
        self.stdscr.move(0, 0);

        # Display optional information message
        if info_message:
            self.stdscr.addstr(0, 0, info_message);

        # Display the question
        start_line = 2;
        self.stdscr.addstr(start_line, 0, question, curses.A_BOLD);
        
        # Add an extra line gap to contain overflow from the question
        start_line += 1;

        # Display the choices 
        for i, choice in enumerate(choices):
            self.stdscr.addstr(i + start_line + 1, 0, f"{i+1}. {choice}");

        self.stdscr.refresh();

    """
    Replace the first line with an error message
    @param error_message: The error message to display
    """
    def show_multiple_choice_error(self, error_message):
        # Clear previous error messages
        self.stdscr.addstr(0, 0, " " * 100);

        # Display the error message
        self.stdscr.addstr(0, 0, error_message, curses.A_BOLD);

        self.stdscr.refresh();

    """
    Update the timer
    @param time_left: The time left
    """
    def update_timer(self, time_left):
        # Clear the timer line
        self.stdscr.move(1, 0);
        self.stdscr.clrtoeol();

        # Display the time left
        self.stdscr.addstr(1, 0, f"Time left: {time_left}");

        self.stdscr.refresh();

    """
    Show a message to the user
    @param message: The message to display
    @param wait_message: Message telling user what to do next
    """
    def show_message(self, message, wait_message):
        self.stdscr.clear();

        # Display the message
        self.stdscr.addstr(0, 0, message);

        # Tell the user to press any key to continue
        self.stdscr.addstr(2, 0, wait_message);

        self.stdscr.refresh();
        
    """
    Show the leaderboard
    @param leaderboard: List of leaderboard rows
    """
    def show_leaderboard(self, leaderboard):
        self.stdscr.clear();

        # Display the leaderboard title
        self.stdscr.addstr(0, 0, "Leaderboard");
        
        self.stdscr.addstr(1, 0, "Press enter to continue...");

        # Display leaderboard rows
        start_line = 2;
        for i, row in enumerate(leaderboard):
            self.stdscr.addstr(i + start_line, 0, row);

        self.stdscr.refresh();

    """
    Exit the curses window
    """
    def exit(self):
        curses.endwin();
