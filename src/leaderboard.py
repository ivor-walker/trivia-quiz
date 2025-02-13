"""
Class representing a leaderboard
"""
class Leaderboard:

    """
    Constructor
    """
    def __init__(self):
        self.scores = [];
        self.max_size = 10;

    """
    Add a score to the leaderboard
    """
    def add_score(self, score):
        # Add the score to the list of scores
        self.scores.append(score);

        # Sort scores by score property
        self.scores.sort(key=lambda x: x.score, reverse=True);
        
        # If there are too many scores, remove the lowest score
        if len(self.scores) > self.max_size:
            self.scores.pop();

    """
    Get a user friendly string representation of the leaderboard
    """
    def __str__(self):
        # Create a string representation of the leaderboard
        leaderboard_str = "Leaderboard:\n";

        # Append each score to the string
        for i in range(len(self.scores)):
            leaderboard_str += str(i+1) + ". " + str(self.scores[i]) + "\n";

        return leaderboard_str;
