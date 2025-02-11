from questions import Questions;
from question import Question;

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

# Get questions
questions = Questions();

# Main loop
while(True):
    ask_question();
