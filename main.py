import tkinter as tk

from src.gui import AplikacjaNSK


def main() -> None:
    root = tk.Tk()
    AplikacjaNSK(root)
    root.mainloop()


if __name__ == "__main__":
    main()
