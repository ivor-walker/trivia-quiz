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
        self.difficulty = question.get("difficulty");
        
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

        self.num_choices = len(self.choices);
        self.choices_string = self.get_choices_string();

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
    @return: True if the answer is correct, False otherwise
    """
    def check_answer(self, answer):
        # Convert the answer to an index
        index = int(answer) - 1;
        
        # Look up the answer in the choices list and compare it to the correct answer
        return self.choices[index] == self.correct_answer;
