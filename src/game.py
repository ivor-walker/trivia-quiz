from questions import Questions;
from question import Question;

import sys;

import time;

"""
Class to represent a game
"""
class Game:
    """
    Constructor
    """
    def __init__(self):
        # Initialise game state
        self.reset();
        self.best_score = 0;

        # Get list of questions
        self.questions = Questions();
             
        # Display welcome message
        # TODO replace with real student ID
        student_id = 0;
        welcome_message = f"Quizzical, produced by {student_id} for assessment 1 of CS5003";
        print(welcome_message);

    """
    Ask a question to the user, and handle the user's answer
    """
    def ask_question(self):
        # Get a question 
        question = self.get_question();

        # Show the question to the user
        print(question.question);
   
        # Display multiple choices
        print(question.choices_string);    
    
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
        requested_difficulty_level = input("Pick a random difficulty (0), or choose the difficulty level of the question you would like to answer (1: easy, 2: medium, 3: hard) ");

        # If difficulty unspecified, ask a random question
        if requested_difficulty_level == "0":
            print("No difficulty specified. Asking a random question.");

            question = self.questions.get_random_question();
        
        # If difficulty specified, ask a question of that difficulty
        elif requested_difficulty_level in ["1", "2", "3"]:
            print(f"Difficulty level {requested_difficulty_level} specified. Asking a question of that difficulty.");

            question = self.questions.get_filtered_question(
                {"difficulty_score": int(requested_difficulty_level)}
            );

        # If difficulty is invalid, reask the question
        else:
            print("Invalid difficulty level. Must be 0, 1, 2 or 3.");
            self.get_question();
    
        return question;

    """
    Get an answer    
    @param question: Question object
    @return: User's answer
    """
    def get_answer(self, question):
        # Ask the user for an answer
        answer = input(f"Enter your answer {question.valid_answers_string} or press 'a' to play a chip: ");
        
        # Check if the user has requested a chip
        if answer == "a":

            # Play a chip
            self.play_chip(question);

            # Ask the user for an answer again
            answer = self.get_answer(question);

        # Check if the answer is valid
        if answer not in question.valid_answers:

            # Display an error message
            print(f"Invalid answer! Please enter a number between {question.min_answer} and {question.max_answer}.");

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
        chips = ["50/50", "quit"];
        chip = input(f"Enter the chip you would like to play ({', '.join(chips)}): ");

        # Check if the chip has already been played
        if chip in self.chips_played:
            print("You have already played that chip!");
            return;

        if chip == "50/50":

            # Check if the question can play 50/50
            if question.can_fifty_fifty():

                # Add the chip to the list of chips played
                self.chips_played.append("50/50");

                # Play the 50/50 chip
                question.fifty_fifty();

                # Display the question again, with the 50/50 options
                print(question.question);

                print(question.choices_string);

            else:
                print("Cannot play 50/50 on this question!");

                # Ask user to play a different chip
                play_chip(question);
       
        # Quit the chip menu and return to the question
        elif chip == "quit":
            return;

        # Invalid chip
        else:
            print("Invalid chip! ");

            # Ask user to play a different chip
            play_chip(question);

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
        print(f"Correct! You Your current score is {self.score} (best score: {self.best_score}).");
    
    """
    User answered incorrectly
    """
    def user_incorrect(self, correct_answer):
        # Increment the number of incorrect answers
        self.incorrect_answers += 1;
    
        # Display a message
        print(f"Incorrect! The correct answer is {correct_answer}. Your current score is {self.score} (best score: {self.best_score}).");
        
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
            print("Game over!");
            self.end_game(); 
    
    """
    Handle player exit via keyboard interrupt
    """
    def player_exit(self, sig, frame):
        print("Goodbye!"); 
        self.end_game(offer_restart = False);

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
        print(f"Your score was {self.score}. You spent {self.total_time} seconds playing the game.");
       
        # Check if the user has a new high score
        if self.score > self.best_score:
            # Update the high score
            self.best_score = self.score;

            # Display a message congratulating the user
            print(f"Congratulations! You have a new high score.");

        # Offer to reset the game if appropriate
        if offer_restart:
            user_restart = input("Would you like to play again? (y/n): ");

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
