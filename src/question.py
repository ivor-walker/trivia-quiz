from html import unescape;

import copy;

import random;

"""
Question class used to store information about a single question
"""
class Question:
        
    """
    Constructor for the Question class
    """
    def __init__(self, question):
        # Store information about the question from the JSON object
        self.question = question.get("question");
        self.category = question.get("category");
        self.difficulty = question.get("difficulty");
        self.correct_answer = question.get("correct_answer");
        self.incorrect_answers = question.get("incorrect_answers");
        self.type = question.get("type");
        
        # Unescape all data from JSON
        self.decode_data();

        # Get difficulty score from difficulty
        self.get_difficulty_score(); 

        # Combine correct and incorrect answers 
        self.update_choices();
    
    """
    Update the choices list     
    """
    def update_choices(self):

        # Combine correct and incorrect answers             
        # Deep copy to avoid future changes to incorrect_answers affecting choices
        self.choices = copy.deepcopy(self.incorrect_answers);
        self.choices.append(self.correct_answer);
        
        self.num_choices = len(self.choices);

        # Shuffle the answers             
        random.shuffle(self.choices);

    """
    Helper method to unescape all data from HTML encoding provided by API
    """
    def decode_data(self):
        for attr, value in self.__dict__.items():
            # If the attribute is a string, unescape it
            if isinstance(value, str):
                setattr(self, attr, unescape(value));

            # If the attribute is a list, unescape all elements
            elif isinstance(value, list):
                setattr(self, attr, [unescape(element) for element in value]);

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
    Check if the answer is correct
    @param answer: The choice to check
    @return: True if the answer is valid and correct, False otherwise
    """
    def check_answer(self, answer):
        # Check if the answer is equal to the correct answer 
        return answer == self.correct_answer;

    """
    50/50: remove two incorrect answers
    """
    def fifty_fifty(self):
        # Select one incorrect answer at random to keep
        self.incorrect_answers = random.sample(self.incorrect_answers, 1);
        
        self.update_choices();
        
    """
    Check if question can be 50/50'd
    @return: True if the question can be 50/50'd, False otherwise
    """
    def can_fifty_fifty(self):
        return self.num_choices > 2;

    """
    ask the host: label an answer as correct
    """
    def ask_the_host(self,
        easy_chance = 0.9,
        medium_chance = 0.7,
        hard_chance = 0.5    
        ):
        
        # Generate a random number between 0 and 1
        random_number = random.random();
        
        # Choose the correct answer with a probability based on the difficulty
        choose_correct_answer = False;
        
        if self.difficulty == "easy":
            choose_correct_answer = random_number < easy_chance;
        elif self.difficulty == "medium":
            choose_correct_answer = random_number < medium_chance;
        elif self.difficulty == "hard":
            choose_correct_answer = random_number < hard_chance;
        
        label_text = " (chosen by the host)";
        # If the random number is less than the threshold, choose the correct answer
        if choose_correct_answer:
            self.correct_answer += label_text;

        # Else, choose an incorrect answer
        else:
            self.incorrect_answers[0] += label_text;
        
        self.update_choices();
