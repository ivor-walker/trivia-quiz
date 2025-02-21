import time;

import threading;

"""
Timer class for measuring time elapsed
"""
class Timer:
    
    """
    Constructor: initialise variables   
    """
    def __init__(self):
        self.reset(reset_total_time = True);
    
    """
    Set/reset all timer variables
    @param reset_total_time: Reset the total time as well
    @param max_time: Time before the timer expires
    """
    def reset(self,
        reset_total_time = False,
        max_time = 30
    ):
        # Stop the timer loop
        self.timing = False;

        # Update the total time
        if reset_total_time:
            self.total_time = 0;
        else:
            self.total_time += self.time_elapsed;
        
        self.time_elapsed = 0;

        self.max_time = max_time;
   
    """
    Start the timer
    """
    def start(self):
        # Prevent multiple threads
        if self.timing == True:
            return;
           
        # Start the timer loop
        self.timing = True;
        self.thread = threading.Thread(
            target = self.timer_loop,
            daemon = True
        );
        self.thread.start();
        
    """
    Timer loop
    @param decimal_places: Number of decimal places to round the time elapsed to
    """
    def timer_loop(self,
        decimal_places = 0
    ):
        # To avoid CPU overload, sleep for a short time before checking the time again
        precision = 10 ** -decimal_places;
        
        # Increment time elapsed while the timer is running
        while self.timing:
            time.sleep(precision);
            self.time_elapsed = round(self.time_elapsed + precision, decimal_places); 

    """
    Check if the timer has expired
    @return: True if the timer has expired, otherwise False
    """
    def is_expired(self):
        # Timer expires if time elapsed is greater than the max time
        return self.get_remaining_time() <= 0;  

    """
    Check if timer view needs to be updated
    @param update_interval: How often to update timer view (seconds)
    @return: Time remaining if the time elapsed is a round number, otherwise None
    """
    def get_update(self,
        update_interval = 1
    ):
        # If the timer is not running, return None
        if self.timing == False:
            return None;
        
        # If the time elapsed is at the required interval, return the time remaining
        if self.time_elapsed % update_interval == 0:
            return self.get_remaining_time(); 

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
        # Reset the timer with the new max time
        self.reset(max_time = extended_max_time);

        # Start the timer again
        self.start();

    """
    Get remaining time
    @return: Remaining time
    """
    def get_remaining_time(self):
        return self.max_time - self.time_elapsed;
