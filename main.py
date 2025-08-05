"""
Secret Message Decoder - Main Entry Point

This module initializes the application, sets up required directories,
creates sample files, and launches the GUI.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui.interface import SecretMessageApp
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)


def check_tkinter():
    """
    Check if tkinter is installed and available
    
    Returns:
        bool: True if tkinter is available, False otherwise
    """
    try:
        import tkinter
        return True
    except:
        return False


def create_dirs():
    """
    Create required directories for the application
    
    Creates data, decrypted, and screenshots directories if they don't exist
    """
    # List of directories to create
    dirs = ["data", "data/decrypted", "screenshots"]
    
    for d in dirs:
        try:
            os.makedirs(d, exist_ok=True)
        except:
            pass  # Not critical if directory creation fails


def create_sample_file():
    """
    Create a sample encrypted file for testing
    
    Creates an encrypted message with shift 13 if it doesn't already exist
    """
    file_path = "data/encrypted_message.txt"
    
    # Check if file already exists
    if os.path.exists(file_path):
        return  # Already exists, skip creation
    
    # Import encryption function
    from modules.cipher import encrypt_text
    
    # Sample text to encrypt
    sample = """This is a secret message from the spy. The mission is extremely important 
and must be completed before midnight. Meet me at the old warehouse near the docks. 
Bring the documents and make sure you are not followed. The password is 'Blue Moon'. 
Trust no one except Agent Seven. Good luck!"""
    
    # Encrypt with shift 13 (ROT13)
    encrypted = encrypt_text(sample, 13)
    
    # Save encrypted text to file
    with open(file_path, 'w') as f:
        f.write(encrypted)
    print(f"Created sample: {file_path}")


def main():
    """
    Main function to initialize and run the application
    
    Performs startup checks, creates necessary resources, and launches the GUI
    """
    print("Starting...")
    
    # Check if tkinter is available
    if not check_tkinter():
        print("Tkinter missing!")
        messagebox.showerror("Error", "Please install tkinter")
        return
    
    # Create required directories
    create_dirs()
    print("Directories ready")
    
    # Create sample encrypted file
    try:
        create_sample_file()
    except Exception as e:
        print(f"Sample file error: {e}")
        # Continue anyway - not critical for app functionality
    
    print("Launching GUI...")
    
    # Launch the application
    try:
        app = SecretMessageApp()
        app.run()
    except Exception as err:
        print(f"Failed: {err}")
        messagebox.showerror("Error", str(err))
        sys.exit(1)
    
    print("Done.")


if __name__ == "__main__":
    main()