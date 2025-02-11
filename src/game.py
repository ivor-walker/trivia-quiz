from questions import Questions;
from question import Question;

import sys;

"""
Class to represent a game
"""
class Game:
    """
    Constructor
    """
    def __init__(self):
        self.questions = Questions();
        self.correct_answers = 0;
        self.incorrect_answers = 0;
        self.game_over = False;
      
        # TODO replace with real student ID
        student_id = 0;
        message = f"Quizzical, produced by {student_id} for assessment 1 of CS5003";
        print(message);

    """
    Ask a question to the user
    """
    def ask_question(self):
        # Select a random question
        question = self.questions.get_random_question();
    
        # Ask the question
        print(question.question);
    
        # Display multiple choices
        print(question.choices_string);    
    
        # Get the user's answer
        answer = input("Enter your answer: ");
    
        # Check if the answer is correct
        if question.check_answer(answer):
            self.user_correct();
        else:
            self.user_incorrect(); 
    
        print("\n");
    
    """
    User answered correctly
    """
    def user_correct(self):
        # Increment the number of correct answers
        self.correct_answers += 1;
    
        # Display a message
        print(f"Correct! You have answered {self.correct_answers} questions correctly.");
    
    """
    User answered incorrectly
    """
    def user_incorrect(self):
        # Increment the number of incorrect answers
        self.incorrect_answers += 1;
    
        # Display a message
        print(f"Incorrect! You have answered {self.incorrect_answers} questions incorrectly.");
        
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
        print(f"You answered {self.correct_answers} questions correctly and {self.incorrect_answers} questions incorrectly.");
        self.game_over = True;
    
        # Offer to restart the game if appropriate
        if offer_restart:

            # Ask user if they want to play again
            user_restart = input("Would you like to play again? (y/n): ");

            if user_restart == "y":
                self.restart_game();

    """
    Restart the game
    """
    def restart_game(self):
        # Reset the game
        self.correct_answers = 0;
        self.incorrect_answers = 0;
        self.game_over = False;
