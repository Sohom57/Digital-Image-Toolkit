import tkinter as tk
from gui.main_window import DigitalImageToolkit

def main():
    """
    Initializes and runs the Digital Image Processing Toolkit application.
    """
    root = tk.Tk()
    app = DigitalImageToolkit(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# pyinstaller --onefile --windowed --add-data "assets;assets" main.py