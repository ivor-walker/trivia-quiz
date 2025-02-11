from questions import Questions;
from question import Question;

import sys;

import time;

import curses;

"""
Class to represent a game
"""
class Game:
    """
    Constructor
    @param stdscr: Instance of curses stdscr
    """
    def __init__(self, stdscr):
        # Set the instance of curses stdscr
        self.stdscr = stdscr;
        
        # Initialise high score
        self.best_score = 0;
        self.best_score_name = "";

        # Initialise game state
        self.reset();
        
        # Get list of questions
        self.questions = Questions();

    """
    Display a welcome message and ask user for info (i.e their name)
    """
    def show_welcome_form(self):
        # Display welcome message
        # TODO replace with real student ID
        student_id = 0;
        welcome_message = f"Quizzical, produced by {student_id} for assessment 1 of CS5003";
        self.stdscr.addstr(0, 0, welcome_message, curses.A_BOLD);
        
        # Ask the user for their name
        self.stdscr.addstr(1, 0, "Welcome to Quizzical! Please enter your name: ");

        self.stdscr.refresh();

        # Get the user's name
        self.user_name = self.stdscr.getstr().decode('utf-8');

    """
    Ask a question to the user, and handle the user's answer
    """
    def ask_question(self):
        # Wipe the screen
        self.stdscr.clear();
        
        # Get a question 
        question = self.get_question();
        
        # Show the question to the user
        self.show_question(question);

        # Start the timer
        self.start_timer();

        # Wait for the user's answer
        answer = self.get_answer(question);            
        
        # Check the user's answer
        if question.check_answer(answer):
            self.user_correct(question.difficulty_score);
        else:
            self.user_incorrect(question.correct_answer); 
        
        # Stop the timer
        self.stop_timer();

    
    """  
    Ask the user for a difficulty level and get a question
    """
    def get_question(self):
        # Ask user for a difficulty 
        self.stdscr.addstr(0, 0, "Please enter a difficulty level (0 for random, 1 for easy, 2 for medium, 3 for hard): ");
        self.stdscr.refresh();
        requested_difficulty_level = self.stdscr.getstr().decode('utf-8');

        # If difficulty unspecified, ask a random question
        if requested_difficulty_level == "0":
            question = self.questions.get_random_question();
        
        # If difficulty specified, ask a question of that difficulty
        elif requested_difficulty_level in ["1", "2", "3"]:
            question = self.questions.get_filtered_question({
                "difficulty_score": int(requested_difficulty_level)
            });

        # If difficulty is invalid, reask the question
        else:
            # Display an error message
            self.stdscr.addstr(1, 0, "Invalid difficulty level! Please enter a number between 0 and 3.");
            self.stdscr.refresh();
            
            # Ask the user for a difficulty level again
            self.get_question();
    
        return question;
    
    """
    Show a question to the user
    @param question: Question object
    """
    def show_question(self, question):
        # Show the user's name and score, and the best score and name
        self.game_info = f"Name: {self.user_name} | Incorrect answers: {self.incorrect_answers} | Total time elapsed: {self.total_time}s | Score: {self.score} | High score: {self.best_score} (held by {self.best_score_name})"; 

        self.stdscr.addstr(0, 0, self.game_info, curses.A_BOLD);
        
        # Display the question
        self.stdscr.addstr(1, 0, question.question, curses.A_BOLD);
   
        # Display multiple choices
        self.stdscr.addstr(2, 0, question.choices_string);

    """
    Get an answer    
    @param question: Question object
    @return: User's answer
    """
    def get_answer(self, question):
        # Ask the user for an answer
        self.stdscr.addstr(3, 0, f"Enter your answer {question.valid_answers_string} or press 'a' to play a chip: ");
        self.stdscr.refresh(); 

        # Get the user's answer
        answer = self.stdscr.getstr().decode('utf-8');

        # Check if the user has requested a chip
        if answer == "a":
            # Play a chip
            self.play_chip(question);

            # Ask the user for an answer again
            answer = self.get_answer(question);

        # Check if the answer is valid
        if answer not in question.valid_answers:

            # Display an error message
            self.stdscr.addstr(4, 0, "Invalid answer! Please enter a valid answer.");
            self.stdscr.refresh();

            # Ask the user for an answer again
            answer = self.get_answer(question);

        return answer;
    
    """
    Start the timer
    """
    def start_timer(self):
        # Record current time as start
        self.start_time = time.time();

    """
    Stop the timer
    """
    def stop_timer(self):
        # Record current time as end
        self.end_time = time.time();
        
        # Calculate time taken
        self.time_taken = self.end_time - self.start_time;

        # Add time taken to total time
        self.total_time += self.time_taken;

    """
    Play a chip
    @param question: Question object
    """
    def play_chip(self, question):
        # Ask the user for the name of the chip they would like to play
        stdscr.move(4, 0);
        stdscr.clrtoeol();
        self.stdscr.addstr(4, 0, "Please enter the name of the chip you would like to play (50/50, quit): ");
        self.stdscr.refresh();

        # Get the name of the chip the user would like to play
        chip = self.stdscr.getstr().decode('utf-8');

        # Check if the chip has already been played
        if chip in self.chips_played:

            # Display an error message
            self.stdscr.addstr(5, 0, "You have already played this chip during this game! Please enter a different chip."); 
            self.stdscr.refresh();

            return;

        if chip == "50/50":
            # Check if the question can play 50/50
            if question.can_fifty_fifty():

                # Add the chip to the list of chips played
                self.chips_played.append("50/50");

                # Play the 50/50 chip
                question.fifty_fifty();

                # Display the question again, with the 50/50 options
                self.show_question(question);

            else:
                # Display an error message
                self.stdscr.addstr(5, 0, "You cannot use the 50/50 chip on this question! Please enter a different chip.");
                self.stdscr.refresh();

                # Ask user to play a different chip
                play_chip(question);
       
        # Quit the chip menu and return to the question
        elif chip == "quit":
            ();

        # Invalid chip
        else:
            # Display an error message
            self.stdscr.addstr(5, 0, "Invalid chip! Please enter a valid chip.");
            self.stdscr.refresh();

            # Ask user to play a different chip
            play_chip(question);
        
        # Clear chip messages after playing a chip
        self.clear_chip_messages(); 

    """
    Clear chip messages
    """
    def clear_chip_messages(self):
        # Clear chip prompt
        self.stdscr.move(4, 0);
        self.stdscr.clrtoeol();

        # Clear any error messages
        self.stdscr.move(5, 0);
        self.stdscr.clrtoeol();
        
        self.stdscr.refresh();

    """
    User answered correctly
    @param difficulty_score 1-3 score of difficulty, scale defined in question.py
    """
    def user_correct(self, difficulty_score):
        # Increment the number of correct answers
        self.correct_answers += 1;
        
        # Increment score
        self.score += difficulty_score

        # Display a message
        self.stdscr.addstr(4, 0, f"Correct!");
        self.stdscr.refresh();

    """
    User answered incorrectly
    """
    def user_incorrect(self, correct_answer):
        # Increment the number of incorrect answers
        self.incorrect_answers += 1;
    
        # Display a message
        self.stdscr.addstr(4, 0, f"Incorrect! The correct answer was {correct_answer}."); 
        self.stdscr.refresh();

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
        offer_restart = True
    ):
        self.game_over = True;
        
        # Stop timer
        self.stop_timer();

        # Display the user's score
        self.stdscr.clear();

        self.stdscr.addstr(0, 0, "Game over!", curses.A_BOLD);
        self.stdscr.addstr(1, 0, f"Your score was {self.score}. You spent {self.total_time} seconds playing the game.");

        # Check if the user has a new high score
        if self.score > self.best_score:
            # Update the high score
            self.best_score = self.score;
            self.best_score_name = self.user_name

            # Display a message congratulating the user
            self.stdscr.addstr(3, 0, f"Congratulations! You have achieved the new high score!", curses.A_BOLD);

        # Offer to reset the game if appropriate
        if offer_restart:
            self.stdscr.addstr(2, 0, "Would you like to play again? (y/n): ");
            self.stdscr.refresh();
            user_restart = self.stdscr.getstr().decode('utf-8');

            if user_restart == "y":
                self.reset();

    """
    Restart the game
    """
    def reset(self):
        # Reset the game
        self.game_over = False;

        self.correct_answers = 0;
        self.incorrect_answers = 0;
        self.score = 0;

        self.chips_played = [];

        self.start_time = 0;
        self.end_time = 0;
        self.time_taken = 0;
        self.total_time = 0;

        # Show the welcome form to the user
        self.show_welcome_form(); 

