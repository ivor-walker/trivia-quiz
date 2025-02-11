from questions import Questions;
from question import Question;

import signal;
import sys;

"""
Ask a question to the user
"""
def ask_question():
    # Select a random question
    question = questions.get_random_question();

    # Ask the question
    print(question.question);

    # Display multiple choices
    print(question.choices_string);    

    # Get the user's answer
    answer = input("Enter your answer: ");

    # Check if the answer is correct
    if question.check_answer(answer):
        user_correct();
    else:
        user_incorrect(); 

    print("\n");

"""
User answered correctly
"""
correct_answers = 0;

def user_correct():
    # Increment the number of correct answers
    global correct_answers;
    correct_answers += 1;

    # Display a message
    print("Correct! You have answered " + str(correct_answers) + " questions correctly.");

"""
User answered incorrectly
"""
incorrect_answers = 0;

def user_incorrect():
    # Increment the number of incorrect answers
    global incorrect_answers;
    incorrect_answers += 1;

    # Display a message
    print("Incorrect! You have answered " + str(incorrect_answers) + " questions incorrectly.");

    check_game_over();

"""
Handle game over
@param max_incorrect_answers: Maximum number of incorrect answers before game over
"""

def check_game_over(
        max_incorrect_answers = 3
    ):

    # Make counter variables global
    global correct_answers;
    global incorrect_answers;

    # Check if user has reached the maximum number of incorrect answers
    if incorrect_answers == max_incorrect_answers:
        print(f"""
        Game over! You answered {correct_answers} questions correctly.
        """);
        sys.exit(0);

"""
Handle player exit
"""
def exit(sig, frame):
    print(f"""
        Goodbye! You answered {correct_answers} questions correctly and {incorrect_answers} questions incorrectly.
    """);
    sys.exit(0);

signal.signal(signal.SIGINT, exit);

# Get questions
questions = Questions();

# Main loop
while(True):
    ask_question();
