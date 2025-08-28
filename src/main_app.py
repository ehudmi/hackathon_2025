import tkinter as tk
from tkinter import font as tkfont
from search_tmdb import SearchTMDBWindow
from watch_list_window import WatchlistWindow


class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Create Watch-List")
        self.master.configure(bg="#2a2a2a")

        # Set window size
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.5)
        self.master.geometry(f"{window_width}x{window_height}")

        # Configure grid
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Fonts
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=16)

        # Welcome label
        tk.Label(
            self.master,
            text="Welcome to your watchlist!",
            font=self.title_font,
            fg="red",
            bg="#2a2a2a",
        ).grid(row=0, column=0, pady=(40, 10), sticky="n")

        # Buttons Frame
        btn_frame = tk.Frame(self.master, bg="#2a2a2a")
        btn_frame.grid(row=1, column=0, pady=20, sticky="n")

        tk.Button(
            btn_frame,
            text="Open Watchlist",
            font=self.button_font,
            width=20,
            command=self.open_watchlist,
        ).grid(row=0, column=0, pady=10, sticky="ew")

        tk.Button(
            btn_frame,
            text="Search TMDB",
            font=self.button_font,
            width=20,
            command=self.open_search_tmdb,
        ).grid(row=1, column=0, pady=10, sticky="ew")

        # Make buttons expand horizontally in btn_frame
        btn_frame.grid_columnconfigure(0, weight=1)

        # Result font for labels
        self.result_font = tkfont.Font(family="Helvetica", size=12)

    def open_watchlist(self):
        WatchlistWindow(self.master)

    def open_search_tmdb(self):
        SearchTMDBWindow(self.master)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
