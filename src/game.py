from questions import Questions;
from question import Question;

from view import View;
from leaderboard import Leaderboard;
from timer import Timer;

import sys;

"""
Class to represent a game
"""
class Game:
    
    """
    Constructor
    @param view: View object
    """
    def __init__(self, view):

        # Set the instance of the view 
        self.view = view;
        
        # Initialise leaderboard and best score 
        self.leaderboard = Leaderboard();
        self.best_score = 0; 

        # Get list of questions
        self.questions = Questions();
        
        # Initialise timer
        self.timer = Timer();

        # Initialise game state
        self.reset();

    """
    Restart the game
    @param immediate_end: Whether to end the game immediately or prompt the user for info
    """
    def reset(self,
        immediate_end = False
    ):
        # Reset the timer
        self.timer.reset(total_time = True);

        # Reset the game state
        self.game_over = False;

        self.correct_answers = 0;
        self.incorrect_answers = 0;
        self.score = 0;

        
        # Available chips 
        self.available_chips = ["50/50", "ask the host", "extra time", "quit"];
        
        # Ask user for information 
        self.user = "";
        self.bonus_category = "";
        
        if immediate_end == False:
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

        # Get the user's name
        return self.get_input();
    
    """
    Ask the user for their preferred bonus category
    """
    def get_bonus_category(self):
        # Get bonus categories
        bonus_categories = self.questions.get_categories();
        
        # Ask the user for their preferred bonus category 
        prompt = f"Welcome, {self.user}! Please enter your preferred bonus category";
        return self.ask_multiple_choice(prompt, bonus_categories); 

    """
    Play a round of the game
    """
    def play_round(self):
        # Ask for a difficulty level
        difficulty_level = self.ask_difficulty();

        # Get a question 
        question = self.get_question(difficulty_level);
        
        # Start the timer
        self.timer.start();

        # Show the question to the user and get their answer
        answer = self.ask_question(question);            

        # Check if user has requested a chip
        if answer == "play a chip":
            # Play a chip
            question = self.play_chip(question);

            # Ask the user for an answer again
            answer = self.ask_question(question);
        
        # Stop the timer
        self.timer.stop();

        # Check the user's answer
        if question.check_answer(answer):
            self.correct(question);
        else:
            self.incorrect(question); 
    
    """  
    Ask the user for a difficulty level     
    @param difficulty_levels: List of difficulty levels
    """
    def ask_difficulty(self,
        difficulty_levels = ["random", "easy", "medium", "hard"]
    ):
        question = "Please enter a difficulty level";
        return self.ask_multiple_choice(question, difficulty_levels);
    
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
            question = self.questions.get_filtered_question({
                "difficulty": requested_difficulty 
            });

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

        # Add "play a chip" to the list of choices
        if len(self.available_chips) > 0:
            question.choices.append("play a chip");
        
        # Show the question to the user and get their answer
        answer = self.ask_multiple_choice(
            question.question, 
            question.choices, 
            info = self.str_game_info, 
        );
        
        return answer;

    """
    Get a user's input in either line or character mode
    """
    def get_input(self,
        get_char_input = False
    ):
        # If user isn't being timed or if requested, get a simple line input
        if self.timer.timing == False or get_char_input == False:
            return self.view.get_line_input();
        
        user_input = "";
       
        # Define while loop condition
        condition = lambda: get_char_input == True or self.timer.is_expired() == False;

        # While the user has not pressed enter or not run out of time
        while condition(): 
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
            if char == 10: 
                return user_input;

            # If the user has pressed backspace, remove the last character
            elif char == 127:
                user_input = user_input[:-1];

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
        self.get_input(get_char_input = True);

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
    ):
        # Get numbers of valid answers
        str_valid_answers = self.get_choices_string(choices);
        valid_answers = self.get_valid_answers(choices); 

        # Show the question to the user along with the choices
        prompt = f"{question} ({str_valid_answers}): ";
        self.view.show_multiple_choice(prompt, choices, info_message = info);

        # Get the user's answer
        answer = self.get_input();

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

        # Check if the chip has already been played
        if chip not in self.available_chips:
            # Display an error message
            self.view.show_multiple_choice_error("You have already played this chip! Please enter a different chip.");

            # Ask the user to play a different chip
            self.play_chip(question);

        if chip == "50/50":
            # Check if the question can play 50/50
            if question.can_fifty_fifty():
                
                # Remove the chip from the list of available chips
                self.available_chips.remove("50/50");

                # Play the 50/50 chip
                question.fifty_fifty();

            else:
                self.view.show_multiple_choice_error("You cannot use the 50/50 chip on this question! Please enter a different chip."); 

                # Ask user to play a different chip
                self.play_chip(question);
       
        # Choose a weighted random answer as 'selected' by the host 
        elif chip == "ask the host":
            # Remove the chip from the list of available chips
            self.available_chips.remove(chip);

            # Play the ask the host chip
            question.ask_the_host();

        # Give the user more time 
        elif chip == "extra time":
            # Remove the chip from the list of available chips 
            self.available_chips.remove(chip);

            # Set the maximum time taken to a minute
            self.timer.extend();

        # Quit the chip menu and return to the question
        elif chip == "quit":
            ();
    
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
    @param offer_restart: Whether to offer to restart the game  
    """
    def end_game(self,
        immediate_end = False,
    ):
        self.game_over = True;
       
        # If the game is ending immediately, exit the game without displaying the user's score or offering to restart
        if immediate_end:
            self.reset(immediate_end = immediate_end);
            self.view.exit();
            sys.exit(0);
            return;
        
        # Display the user's score
        message = "Game over! Your score was {self.score}. You spent {self.total_time} seconds playing the game. Would you like to play again?";
        choices = ["Yes", "No"];
        restart = self.ask_multiple_choice(message, choices);
        
        # Add the user's score to the leaderboard 
        self.leaderboard.add_score(self.user, self.score);
        
        # Display the leaderboard
        leaderboard = self.leaderboard.get_rows();
        self.view.show_multiline_message(leaderboard);

        # Check if the user has a new high score, and display a message if they do
        if self.score > self.best_score:
            self.best_score = self.score;
            
            message = "Congratulations! You have achieved the new high score!";
            self.show_message(self.best_score, message);
        
        # Restart the game if the user has chosen to do so
        if restart == "Yes":
            self.reset();
        else:
            self.view.exit();
    
