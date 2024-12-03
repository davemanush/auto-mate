# Shared events and flags
import threading

from pyautogui import sleep

stop_event = threading.Event()  # To stop the process
process_running = threading.Event()  # To track if the process is running

def long_running_process():
    """Simulate a long-running process that can be stopped."""
    print("Process started. Press 'q' to stop.")
    while not stop_event.is_set():
        print("Processing...")
        sleep(1)  # Simulate work
    print("Process stopped.")
    stop_event.clear()  # Reset the stop_event for future starts
    process_running.clear()  # Mark the process as stopped

def on_press(key):
    """Callback function for key press."""

    if key.char == 'a':  # Start the process on 'a'
        if not process_running.is_set():
            print("Start signal received.")
            process_running.set()
            stop_event.clear()
            process_thread = threading.Thread(target=long_running_process)
            process_thread.start()
    elif key.char == 'q':  # Stop the process on 'q'
        if process_running.is_set():
            print("Stop signal received.")
            stop_event.set()