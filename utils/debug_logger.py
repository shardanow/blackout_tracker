from datetime import datetime
from config.config import config

DEBUG = config['DEBUG']
DEBUG_SAVE_FILE = config['DEBUG_SAVE_FILE']

def print_debug_message(message):
    # Check if the DEBUG flag is set to True
    if not DEBUG:
        return
    
    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #formatting the message
    full_message = f"[DEBUG] {current_datetime}: {message}"
    
    # Check if the DEBUG_SAVE_FILE flag is set to True
    if DEBUG_SAVE_FILE:
        # Save the debug message to a file
        with open("debug.log", "a") as f:
            # Write the message with the current date and time to the file
            f.write(full_message+"\n")
            
    # Print the message with the current date and time
    print(full_message)