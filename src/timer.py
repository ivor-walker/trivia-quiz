"""
Class for a timer that can be started, stopped, and reset
"""
class Timer:
    
    """
    Constructor for the Timer class
    """
    def __init__(self):
        # Set defaults
        self.default_max_time = 30;
        
        self.start_time = None;
        self.stop_time = None;
        self.time_elapsed = 0;
        self.total_time = 0;

        self.max_time = self.default_max_time;

        self.timing = False;
        self.timer_exceeded = False;

    """
    Start the timer
    """
    def start(self):
        self.timing = True;

        # Set the start time
        self.start_time = time.time();

        while self.timing:
            # Record current time
            current_time = time.time();

            # Calculate the time elapsed
            self.time_elapsed = current_time - self.start_time;

    """
    Stop the timer
    """
    def stop(self):
        # Stop the timing loop
        self.timing = False;
        
        # Record the stop time
        self.stop_time = time.time()
        
        # Update the total time
        self.total_time += self.time_elapsed;

        # Reset the timer
        self.reset();
    
    """
    Reset the timer
    """
    def reset(self):
        # Reset start and stop times
        self.start_time = None
        self.stop_time = None

        # Reset time elapsed and total time
        self.time_elapsed = 0;
        self.total_time = 0;

        # Reset flags
        self.timer_exceeded = False;
        self.timing = False;

        # Reset the max time
        self.max_time = self.default_max_time;
    
    """
    Check if the timer has expired
    @return: True if the timer has expired, otherwise False
    """
    def expired(self):
        # Timer expires if time elapsed is greater than the max time
        return self.time_elapsed > self.max_time;
    
    """
    Check if timer view needs to be updated
    @return: Time remaining if the time elapsed is a round number, otherwise None
    """
    def update(self):
        # If the time elapsed is a round number
        if self.time_elapsed % 1 == 0:

            # Return the time remaining
            return self.max_time - self.time_elapsed;
        
        # Otherwise, return None
        else:
            return None;

    """
    Extend the timer
    @param extended_max_time: New max time for the timer
    """
    def extend(self,
        extended_max_time = 60
    ):
        self.max_time = extended_max_time; 

    """
    Get remaining time
    @return: Remaining time
    """
    def remaining_time(self):
        return self.max_time - self.time_elapsed;
    

