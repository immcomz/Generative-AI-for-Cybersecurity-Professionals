import os
from pynput import keyboard

# Define the file where keystrokes will be stored
LOG_FILE = "live_monitored_keystrokes.txt"

# 1. Define the "unnecessary" or forbidden keywords you want to catch live
FORBIDDEN_KEYWORDS = ["pynput", "password", "secret", "admin"]

# We use a running string buffer to keep track of the last few characters typed
typed_buffer = ""

def check_for_keywords(current_text):
    """Checks if any forbidden keywords are present in the typed text."""
    for word in FORBIDDEN_KEYWORDS:
        if word in current_text.lower():
            print(f"\n🚨 ALERT: Forbidden keyword detected live: '{word}'!")
            # Optional: You could trigger an action here, like clearing the buffer,
            # alerting an admin, or shutting down the application.

def on_press(key):
    global typed_buffer
    
    try:
        # Extract the actual character typed (e.g., 'a', 'b', '1')
        char = key.char
    except AttributeError:
        # Handle special keys (Space, Enter, Backspace, etc.)
        if key == keyboard.Key.space:
            char = " "
        elif key == keyboard.Key.enter:
            char = "\n"
        elif key == keyboard.Key.backspace:
            # If user hits backspace, remove the last character from our tracker
            typed_buffer = typed_buffer[:-1]
            char = ""
        else:
            char = "" # Ignore other special keys for word tracking

    # If a valid character was processed, update our running text tracker
    if char:
        typed_buffer += char
        # Keep the buffer reasonably short (e.g., last 50 characters) to save memory
        typed_buffer = typed_buffer[-50:]
        
        # Check if the user just completed typing a bad word
        check_for_keywords(typed_buffer)

    # 2. Meanwhile, always save the raw key event into the file
    with open(LOG_FILE, "a") as f:
        f.write(f"{key} pressed\n")

def on_release(key):
    # Kill switch: press Escape to safely close the program
    if key == keyboard.Key.esc:
        print("\nStopping live monitoring script.")
        return False

# Start the live listener
print(f"Monitoring keyboard... Logging to '{LOG_FILE}'.")
print(f"Watching out for forbidden words: {FORBIDDEN_KEYWORDS}")
print("Press ESC to exit.")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()