"""
Class representing a leaderboard of the top scores
"""
class Leaderboard:

    """
    Constructor: initialise list of leaderboard entries
    """
    def __init__(self):
        self.entries = [];

    """
    Add a score to the leaderboard
    @param name: Name of the player
    @param score: Score achieved by the player  
    """
    def add_score(self, name, score):
        # Create and append a new entry to the leaderboard
        entry = {
            "name": name,
            "score": score
        };
        self.entries.append(entry);

        self.update_leaderboard();
        
    """
    Sort and trim the leaderboard to max size
    @param max_size: Maximum number of entries to keep in the leaderboard
    """
    def update_leaderboard(self,
        max_size = 10
    ):
        # Sort entries dictionary by score
        self.entries = sorted(self.entries, key=lambda x: x['score'], reverse=True);
        
        # While the leaderboard is larger than max size, remove lowest score
        while len(self.entries) > max_size:
            self.entries.pop();
    
    """
    Get a user friendly string representation of a single leaderboard entry
    @param entry: Dictionary representing a single entry
    @return: String representation of the entry
    """
    def str_entry(self, entry):
        return f"{entry['name']}: {entry['score']}";

    """
    Get list of string representations of all entries
    @return: List of strings representing all entries
    """
    def get_rows(self):
        return [self.str_entry(entry) for entry in self.entries];
