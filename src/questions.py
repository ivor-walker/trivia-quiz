from question import Question

import requests
import time
from html import unescape

import random


"""
Class used to store multiple questions and fetch new ones from the API
"""
class Questions:

    """
    Constructor: fetch a token and initial questions
    """
    def __init__(self):
        # Set error messages
        self.connection_error = "Error fetching questions from API: connection error";

        # Set initial token
        self.get_new_token();

        # Fetch initial questions
        self.questions = [];
        self.fetch_new_questions();

        
    """
    Ask for a token from the API 
    """
    def get_new_token(self):
        try:
            response = requests.get("https://opentdb.com/api_token.php?command=request");
        
        # Catch connection errors
        except requests.exceptions.RequestException:
            raise ConnectionError(self.connection_error);

        # Parse JSON response
        data = response.json();

        # Set token
        self.token = data["token"];

    """
    Fetch new questions from the API
    @param n_to_fetch: number of questions to fetch (max 50 questions per call)
    @param rate_limit: number of seconds to wait if rate limit is exceeded (5 according to API)
    """
    def fetch_new_questions(self, 
        n_to_fetch = 50,
        rate_limit = 5,
    ):

        # Fetch questions from API
        try:
            response = requests.get(f"https://opentdb.com/api.php?amount={n_to_fetch}&token={self.token}");

        # Catch connection errors
        except requests.exceptions.RequestException:
            raise ConnectionError(self.connection_error);

        # Parse JSON response
        data = response.json();

        # Check if response contains error
        response_code = data["response_code"];

        # Code 4: no more questions left
        if response_code == 4:

            # Get new token (to wipe 'memory' of old questions)
            self.get_new_token(); 

            # Try fetching questions again
            return self.fetch_new_questions();

        # Code 5: rate limit exceeded
        if response_code == 5:
            # Wait and try again
            time.sleep(rate_limit);
            return self.fetch_new_questions();

        # Other codes: error
        if response_code != 0:
            raise ConnectionError(f"Error fetching questions from API: error code {response_code}");

        # Get questions from response
        data = data["results"];

        # Construct Question objects from API response
        data = [Question(x) for x in data];

        # Add questions to the list
        self.add_questions(data);

    """
    Add questions to the list
    @param questions: questions to add
    """
    def add_questions(self, questions):
        self.questions.extend(questions);

    """
    Delete questions from the list
    @param questions: list of questions to delete
    """
    def delete_questions(self, questions):
        self.questions = [x for x in self.questions if x not in questions];

    """
    Delete single question from the list
    @param question: single question to delete
    """
    def delete_question(self, question):
        self.questions.remove(question);

    """
    Get a random question   
    @param questions: list of questions to choose from
    @return: random question
    """
    def get_random_question(self, questions = None):
        # Get a random question from either the list of questions or a provided list
        if questions:
            question = random.choice(questions);
        else:
            question = random.choice(self.questions);

        # Remove from list of questions
        self.delete_question(question);

        # Fetch replacement questions if no questions left
        if len(self.questions) == 0:
            self.fetch_new_questions();

        return question;

    """
    Get a random question by attribute
    @param search dict: dictionary of attributes to search for
    @return: question
    """
    def get_filtered_question(self, search_dict):
        # Get all questions that match the search criteria
        search_dict = search_dict.items();
        questions = [x for x in self.questions if all(getattr(x, key) == value for key, value in search_dict)];

        # If no questions match, fetch new questions and try again
        if len(questions) == 0:
            self.fetch_new_questions();
            return self.get_filtered_question(search_dict);
       
        # Return a random question from the list of matching questions
        return self.get_random_question(questions);

    """
    Get a random category
    @param number: number of categories to return
    @return: list of categories
    """
    def get_categories(self, 
        number = 4
    ):
        # Get all categories
        categories = list(set([x.category for x in self.questions]));

        # Return a random sample of categories
        return random.sample(categories, number);
