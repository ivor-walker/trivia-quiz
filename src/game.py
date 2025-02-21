from questions import Questions;
from question import Question;

from view import View;
from leaderboard import Leaderboard;
from timer import Timer;

import copy;

import sys;

"""
Class to represent a game
"""
class Game:
    
    """
    Constructor: set view and create a leaderboard and timer
    @param view: View object
    """
    def __init__(self, view):

        # Set the instance of the view 
        self.view = view;
        
        # Initialise leaderboard and best score 
        self.leaderboard = Leaderboard();
        self.best_score = 0; 

        # Initialise timer
        self.timer = Timer();
        
        # Fetch initial questions
        self.init_questions();

        # Initialise game state and ask user for info
        self.reset();

    """
    Get and initialise a list of Question objects
    """
    def init_questions(self):
        # Try to get a list of questions
        try:
            self.questions = Questions();

        # If there is a network error, display an error message and immediately end the game
        except ConnectionError as e:
            return self.handle_error(e);

    """
    Handle an error
    @param e: Exception object
    """
    def handle_error(self, e):
        # Display error message and immediately end the game
        self.show_message(str(e));
        self.immediate_end();

        return;

    """
    Reset the game and ask for user info 
    """
    def reset(self):
        # Reset the timer
        self.timer.reset(total_time = True);

        # Reset the game state
        self.game_over = False;

        self.correct_answers = 0;
        self.incorrect_answers = 0;
        self.score = 0;

        # Available chips 
        self.available_chips = ["50/50", "ask the host", "extra time", "quit"];
        
        # Ask for user info
        self.user = self.ask_for_user(); 
        self.bonus_category = self.get_bonus_category();
            
    """
    Display a welcome message and ask user for info (i.e their name)
    """
    def ask_for_user(self):
        # Display welcome message and ask for user's name
        # TODO replace with real student ID
        student_id = 0;
        welcome_message = f"Quizzical, produced by {student_id} for assessment 1 of CS5003";
        ask_for_name = "Welcome to Quizzical! Please enter your name: ";
        self.view.show_welcome_form(welcome_message, ask_for_name);
        
        # Try getting the user's name
        try:
            return self.get_input();

        # If the user interrupts this prompt, immediately end the game
        except KeyboardInterrupt:
            return self.immediate_end();
    
    """
    Ask the user for their preferred bonus category
    """
    def get_bonus_category(self):
        # Get bonus categories
        bonus_categories = self.questions.get_categories();
        
        # Ask the user for their preferred bonus category 
        prompt = f"Welcome, {self.user}! Please enter your preferred bonus category";
        return self.ask_multiple_choice(prompt, bonus_categories, exception_immediate_end = True); 
    
    """
    Start the game loop
    """
    def start(self):
        # Ask questions until the game is over
        while not self.game_over:
            self.play_round();

    """
    Play a round of the game
    """
    def play_round(self):
        
        # Try asking for a difficulty level
        try:
            difficulty_level = self.ask_difficulty();

        except KeyboardInterrupt:
            return self.try_end_game();

        # Try getting a question 
        try:
            question = self.get_question(difficulty_level);

        # Handle potential network error as fetching new questions from API could be needed
        except ConnectionError as e:
            return self.handle_error(e);
            
        self.timer.start();
        
        # Try asking an appropriate question and getting the user's answer 
        try:
            answer = self.ask_question(question);            
        
        # If the user throws a keyboard interrupt, try to end normally 
        except KeyboardInterrupt:
            return self.try_end_game(); 

        # Stop the timer
        self.timer.stop();

        # Check the user's answer
        if question.check_answer(answer):
            self.correct(question);
        else:
            self.incorrect(question); 
    
    """
    Try to end the game gracefully
    """
    def try_end_game(self):
        # If the user interrupts the game, try to end the game gracefully
        try:
            return self.end_game();

        # If the user interrupts the game again, end the game immediately
        except KeyboardInterrupt:
            return self.immediate_end();

    """  
    Ask the user for a difficulty level     
    @param difficulty_levels: List of difficulty levels
    """
    def ask_difficulty(self,
        difficulty_levels = ["random", "easy", "medium", "hard"]
    ):
        question = "Please enter a difficulty level";
        return self.ask_multiple_choice(
            question, difficulty_levels, 
            # Bubble exception to play_round
            bubble_exception = True
        );

    """
    Get a question based on requested difficulty
    """
    def get_question(self,
        requested_difficulty
    ):
        # If difficulty unspecified, ask a random question
        if requested_difficulty == "random":
            question = self.questions.get_random_question();
        
        # If difficulty specified, ask a question of that difficulty
        else:
            search_dict = {
                "difficulty": requested_difficulty
            };

            question = self.questions.get_filtered_question(search_dict);
        
        return question;
    
    """
    Ask the user a question
    @param question: Question object
    """
    def ask_question(self,
        question,
    ):
        answer = "";

        # Get game information 
        self.str_game_info = f"Name: {self.user} | Incorrect answers: {self.incorrect_answers} | Score: {self.score} | High score: {self.best_score}"; 
        
        # Deep copy of the question's choices to avoid modifying the original question
        choices = copy.deepcopy(question.choices);

        # Add "play a chip" to the list of choices
        if len(self.available_chips) > 1: 
            choices.append("play a chip");
        
        # Show the question to the user and get their answer
        answer = self.ask_multiple_choice(
            question.question, 
            choices,
            info = self.str_game_info, 
            # Bubble exception to play_round
            bubble_exception = True
        );
        
        # Check if user has requested a chip
        if answer == "play a chip":
            # Play a chip
            question = self.play_chip(question);

            # Ask the user for an answer again
            return self.ask_question(question);

        return answer;

    """
    Get a user's input in character mode, with a timer
    """
    def get_input(self):

        user_input = "";
        
        # Continue to get user's input until the timer has expired
        while self.timer.timing == False or self.timer.is_expired() == False: 
            # Update the timer view if necessary
            update_time = self.timer.get_update();
            if update_time is not None:
                self.view.update_timer(update_time);

            # Get a user's input by character
            char = self.view.get_char_input();
            
            # If user has pressed nothing, continue
            if char is None or char == -1:
                continue;

            # If the user has pressed enter, return the entire input
            if char in (10, 13): 
                return user_input;

            # If the user has pressed backspace, remove the last character
            elif char in (8, 127):
                user_input = user_input[:-1];
            
            # If the user presses ctrl+c, exit the game
            elif char in (3, 26):
                raise KeyboardInterrupt; 
                return;

            # If the user has pressed a valid character, add it to the input
            elif char >= 32 and char <= 126:
                user_input += chr(char);

        # If the user has run out of time, return None
        return None;
    
    """
    Display a message to the user and ask user to press enter to continue
    """
    def show_message(self, message):
        # Show the message to the user
        enter_prompt = "Press enter to continue...";
        self.view.show_message(message, enter_prompt);

        # Wait for user to press enter
        self.get_input();

    """
    Helper function to get user-friendly string of choices
    @param choices: List of choices
    """
    def get_choices_string(self, choices):
        str_choices = "";
        
        # Append each choice to the string
        for i, choice in enumerate(choices): 
            str_choices += f"{i+1}";

            # Add a comma if not the last choice
            if i < len(choices) - 1:
                str_choices += ", ";

        return str_choices

    """
    Helper function to get valid answers
    @param choices: List of choices
    """
    def get_valid_answers(self, choices):
        return [str(i+1) for i in range(len(choices))];

    """
    Ask the user a multiple choice question
    """
    def ask_multiple_choice(self, 
        question, 
        choices,
        info = None,
        exception_immediate_end = False,
        bubble_exception = False
    ):
        # Get numbers of valid answers
        str_valid_answers = self.get_choices_string(choices);
        valid_answers = self.get_valid_answers(choices); 

        # Show the question to the user along with the choices
        prompt = f"{question} ({str_valid_answers}): ";
        self.view.show_multiple_choice(prompt, choices, info_message = info);
        
        # Try getting the user's answer
        answer = "";
        try:
            answer = self.get_input();
        
        # If the user interrupts the game, end the game
        except KeyboardInterrupt:
            # Let parent function handle the exception
            if bubble_exception:
                raise KeyboardInterrupt;

            # End the game gracefully
            if exception_immediate_end:
                return self.end_game();

            # End the game immediately
            else:
                return self.immediate_end();
        
        # Check if the user has entered a valid answer (or None has been returned in case of error)
        while answer not in valid_answers and answer is not None:
            # Display an error message
            self.view.show_multiple_choice_error(f"Invalid answer! Please enter a valid answer ({str_valid_answers}).");

            # Ask the user for an answer again
            answer = self.get_input();
            
        
        # Return the user's answer
        if answer is not None:
            return choices[int(answer) - 1];

        # Return None if the user has run out of time
        else:
            return None;

    """
    Play a chip
    @param question: Question object
    """
    def play_chip(self, question):
        # Ask the user for the name of the chip they would like to play
        prompt = "Please enter the name of the chip you would like to play, or 'quit' to return to the question";
        choices = self.available_chips;
        chip = self.ask_multiple_choice(prompt, choices);
        
        # Return to unmodified question 
        if chip == "quit":
            return question;

        # Display one correct and one incorrect answer
        if chip == "50/50":

            # Check if the question can play 50/50
            if question.can_fifty_fifty():
                question.fifty_fifty();

            else:
                # Ask user to play a different chip
                self.view.show_multiple_choice_error("You cannot use the 50/50 chip on this question! Please enter a different chip."); 

                return self.play_chip(question);
       
        # Choose a weighted random answer as 'selected' by the host 
        elif chip == "ask the host":
            question.ask_the_host();

        # Set the maximum time taken to a minute
        elif chip == "extra time":
            self.timer.extend_timer();

        # Remove the played chip from the list of available chips 
        self.available_chips.remove(chip);

        # Return question modified by chip
        return question;
    
    """
    User answered correctly
    @param question: Question object
    """
    def correct(self, question):
        # Increment the number of correct answers
        self.correct_answers += 1;
        
        # If the user answered a question in their bonus category, double the score 
        points_scored = question.difficulty_score;

        if self.bonus_category == question.category:
            points_scored *= 2;

        # Increment the user's score
        self.score += question.difficulty_score;
       
        # Show the user that they answered correctly
        self.show_message(f"Correct! You have earned {points_scored} points.");

    """
    User answered incorrectly
    @param question: Question object
    """
    def incorrect(self, question):
        # Increment the number of incorrect answers
        self.incorrect_answers += 1;
        
        # Show the user that they answered incorrectly
        message = f"Incorrect! The correct answer was {question.correct_answer}.";
        self.show_message(message);

        # Check if the game is over
        self.check_game_over();
    
    """
    Check for and handle game over
    @param max_incorrect_answers: Maximum number of incorrect answers before game over
    """
    def check_game_over(self, 
            max_incorrect_answers = 3
        ):
    
        # Check if user has reached the maximum number of incorrect answers
        if self.incorrect_answers == max_incorrect_answers:
            # End the game 
            self.end_game(); 
    
    """
    End the game
    """
    def end_game(self):
        # Stop the timer
        self.timer.stop();

        # Display the user's score
        message = f"Game over! Your score was {self.score}. You spent {self.timer.total_time} seconds playing the game. Would you like to play again?";
        choices = ["Yes", "No"];

        restart = self.ask_multiple_choice(message, choices, exception_immediate_end = True);
        
        # Add the user's score to the leaderboard 
        self.leaderboard.add_score(self.user, self.score);
        
        # Display the leaderboard
        leaderboard = self.leaderboard.get_rows();
        self.view.show_leaderboard(leaderboard);

        # Wait for user to press enter
        self.get_input();

        # Check if the user has a new high score, and display a message if they do
        if self.score > self.best_score:
            self.best_score = self.score;
            
            message = "Congratulations! You have achieved the new high score!";
            self.show_message(message);
        
        # Restart the game if the user has chosen to do so
        if restart == "Yes":
            return self.reset();

        # Stops the loop in main.py if user chooses not to restart
        else:
            self.game_over = True;
            return;
   
    """
    Immediately end the game
    """
    def immediate_end(self):
        # Close view
        self.view.exit();

        # Exit application
        sys.exit(0);

        return;
