"""
Class representing a leaderboard
"""
class Leaderboard:

    """
    Constructor
    """
    def __init__(self):
        self.entries = [];
        self.max_size = 10;

    """
    Add a score to the leaderboard
    """
    def add_score(self, name, score):
        # Create a new entry for the score
        entry = {
            "name": name,
            "score": score
        };

        # Add the entry to the list of entries
        self.entries.append(entry);
        
        # Sort entries dictionary by score
        self.entries = sorted(self.entries, key=lambda x: x['score'], reverse=True);
        
        # If there are too many entries, remove the lowest score
        if len(self.entries) > self.max_size:
            self.entries.pop();

    """
    Get a user friendly string representation of a single leaderboard entry
    """
    def str_entry(self, entry):
        return f"{entry['name']}: {entry['score']}";

    """
    Get string representation of the all entries
    """
    def get_rows(self):
        return [self.str_entry(entry) for entry in self.entries];
