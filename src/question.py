import random

"""
Question class used to store information about a single question
"""
class Question:
        
    """
    Constructor for the Question class
    """
    def __init__(self, question):
        self.question = question.get("question");
        self.category = question.get("category");
       
        # Get difficulty of question as string and score
        self.difficulty = question.get("difficulty");
        self.get_difficulty_score(); 

        # Get correct and incorrect answers
        self.correct_answer = question.get("correct_answer");
        self.incorrect_answers = question.get("incorrect_answers");

        self.type = question.get("type");
      
        # If the question is a boolean question, set the choices to True and False
        if self.type == "boolean":
            self.choices = ["True", "False"];

        # Else, set the choices to the correct and incorrect answers 
        else:

            # Combine correct and incorrect answers             
            self.choices = self.incorrect_answers;
            self.choices.append(self.correct_answer);
            
            self.type = question.get("type");

            # Shuffle the answers             
            random.shuffle(self.choices);
        
        # Store number of choices and user-friendly representation of them
        self.num_choices = len(self.choices);
        self.choices_string = self.get_choices_string();

    """
    Helper method to set the difficulty score of the question
    """
    def get_difficulty_score(self):
        # Turn string representation into a score
        if self.difficulty == "easy":
            self.difficulty_score = 1;

        elif self.difficulty == "medium":
            self.difficulty_score = 2;

        elif self.difficulty == "hard":
            self.difficulty_score = 3;
        
        else:
            self.difficulty_score = 0;

    """
    Get choices as user friendly string
    @return: Choices as a string
    """
    def get_choices_string(self):
        # Append the choices to a single string
        choices_string = "";
        for i in range(len(self.choices)):
            choices_string += str(i+1) + ". " + self.choices[i] + "\n";

        return choices_string;

    """
    Check if the answer is correct
    @param answer: The number of choice to check
    @return: True if the answer is valid and correct, False otherwise
    """
    def check_answer(self, answer):
        # Convert the answer to an index
        index = int(answer) - 1;
        
        # Check if the index is valid
        if index < 0 or index >= self.num_choices:
            return False;

        # Look up the answer in the choices list and compare it to the correct answer
        return self.choices[index] == self.correct_answer;

    """
    50/50: remove two incorrect answers
    """
    def fifty_fifty(self):
        # Shuffle the incorrect answers
        random.shuffle(self.incorrect_answers);

        # Set the choices to the correct answer and one (now random) incorrect answer
        self.choices = [self.correct_answer, self.incorrect_answers[0]];

        # Regenerate the choices string
        self.choices_string = self.get_choices_string();
        
        # Update the number of choices
        self.num_choices = len(self.choices);

    """
    Check if question can be 50/50'd
    @return: True if the question can be 50/50'd, False otherwise
    """
    def can_fifty_fifty(self):
        return self.num_choices > 2;
