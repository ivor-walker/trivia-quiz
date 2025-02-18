import time;
import threading;

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
       
        # Initialize variables
        self.reset();
        
        self.total_time = 0;
        
    """
    Start the timer
    """
    def start(self):
        # Prevent multiple threads
        if self.timing == True:
            return;
        
        # Set the start time
        self.start_time = time.time();

        # Start the timing loop
        self.timing = True;
        self.thread = threading.Thread(
            target = self.timer_loop,
            daemon = True
        );
        self.thread.start();
        
    """
    Timer loop
    @param accuracy: Time between each loop iteration
    """
    def timer_loop(self,
        accuracy = 0.01,
        decimal_places = 2
    ):
        while self.timing:
            # Avoid CPU overload
            time.sleep(accuracy);

            # Record current time
            current_time = time.time();

            # Calculate the time elapsed
            self.time_elapsed = round(current_time - self.start_time, decimal_places);

        # Reset start time
        self.start_time = None;

    """
    Stop the timer
    """
    def stop(self):
        # Update the total time
        self.total_time += self.time_elapsed;

        # Reset the timer
        self.reset();
            
    """
    Reset the timer
    @param total_time: Reset the total time as well
    """
    def reset(self,
        total_time = False
    ):
        self.thread = None;

        # Reset flags
        self.timer_exceeded = False;
        self.timing = False;

        
        # Reset time elapsed and total time
        self.time_elapsed = 0;

        if total_time:
            self.total_time = 0;

        # Reset the max time
        self.max_time = self.default_max_time;
    
    """
    Check if the timer has expired
    @return: True if the timer has expired, otherwise False
    """
    def is_expired(self):
        # Timer expires if time elapsed is greater than the max time
        return self.time_elapsed > self.max_time;
    
    """
    Check if timer view needs to be updated
    @return: Time remaining if the time elapsed is a round number, otherwise None
    """
    def get_update(self):
        # If the timer is not running, return None
        if self.timing == False:
            return None;

        # If the time elapsed is a round number
        if self.time_elapsed % 1 == 0:

            # Return the time remaining
            return int(self.max_time - self.time_elapsed);
        
        # Otherwise, return None
        else:
            return None;

    """
    Extend the timer
    @param extended_max_time: New max time
    """
    def extend_timer(self,
        extended_max_time = 60
    ):
        self.max_time = extended_max_time;

        # Update start time to reset timer to new max time
        self.start_time = time.time();

    """
    Get remaining time
    @return: Remaining time
    """
    def get_remaining_time(self):
        return self.max_time - self.time_elapsed;
