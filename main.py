"""
Main entry point for Video Transcriber Pro.
Launches the application.
"""

import tkinter as tk
from ui import TranscriberApp


def main():
    """Initialize and run the application."""
    root = tk.Tk()
    app = TranscriberApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
