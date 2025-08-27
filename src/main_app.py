import tkinter as tk
from tkinter import ttk as ttk
from tkinter import font as tkfont


class SearchBar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configure the grid to handle the new widgets
        for i in range(10):
            if i == 4 or i == 7 or i == 9:
                self.grid_columnconfigure(i, weight=1)
            else:
                self.grid_columnconfigure(i, weight=0)

        self.grid_rowconfigure(0, weight=0, pad=5)

        # Call a dedicated method to create all the widgets
        self.create_widgets()

    def create_widgets(self):
        # Create a font object for the labels
        self.label_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
        self.small_font = tkfont.Font(family="Helvetica", size=16)

        # Main Title Label
        title_label = tk.Label(
            self,
            text="Search by criteria",
            fg="red",
            font=self.label_font,
            bg=self["bg"],
        )
        title_label.grid(row=0, column=0, columnspan=10, pady=5, sticky="n")

        # Search Entry and Label
        tk.Label(
            self, text="Search for:", font=self.small_font, bg=self["bg"], fg="white"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.search_parameter = tk.StringVar()
        self.search_box = ttk.Entry(
            self, textvariable=self.search_parameter, width=30, justify="left"
        )
        self.search_box.grid(row=1, column=1, padx=10, pady=5, sticky="nw")
        self.search_box.configure(font=self.small_font)

        # Radio Buttons for Search Type
        style = ttk.Style()
        style.configure("Custom.TRadiobutton", font=self.small_font)

        tk.Label(
            self, text="Type:", font=self.small_font, bg=self["bg"], fg="white"
        ).grid(row=1, column=2, padx=5, pady=5, sticky="nw")
        self.search_type = tk.StringVar(value="title")
        self.title_bttn = ttk.Radiobutton(
            self,
            text="Title",
            variable=self.search_type,
            value="title",
            style="Custom.TRadiobutton",
        )
        self.person_bttn = ttk.Radiobutton(
            self,
            text="Person",
            variable=self.search_type,
            value="person",
            style="Custom.TRadiobutton",
        )
        self.title_bttn.grid(row=1, column=3, pady=5, sticky="nw")
        self.person_bttn.grid(row=1, column=4, pady=5, sticky="nw")

        # Listbox for Genre Selection
        tk.Label(
            self, text="Genre:", font=self.small_font, bg=self["bg"], fg="white"
        ).grid(row=1, column=5, padx=5, pady=5, sticky="nw")
        self.genre_list = tk.Listbox(self, exportselection=0, height=5, width=15)
        self.genre_list.grid(row=1, column=6, sticky="nw")

        # Add a scrollbar to the listbox
        scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.genre_list.yview
        )
        scrollbar.grid(row=1, column=7, sticky="nsw", padx=(0, 5))
        self.genre_list.configure(yscrollcommand=scrollbar.set, font=self.small_font)

        # Spinbox for Year
        tk.Label(
            self, text="Year:", font=self.small_font, bg=self["bg"], fg="white"
        ).grid(row=1, column=8, padx=5, pady=5, sticky="nw")
        self.spinval = tk.StringVar()
        self.spinval.set("2020")
        self.year = ttk.Spinbox(
            self, from_=1890, to=2025, textvariable=self.spinval, width=5
        )
        self.year.grid(row=1, column=9, padx=5, pady=5, sticky="nw")
        self.year.configure(font=self.small_font)

        # Search Button
        # The style configuration for a rounded button
        style = ttk.Style()
        style.configure(
            "Rounded.TButton",
            borderwidth=4,
            relief="raised",
            foreground="red",
            background="#2a2a2a",
            font=self.label_font,
        )
        style.map("Rounded.TButton", background=[("active", "#444444")])
        self.search_button = ttk.Button(
            self, text="Search", command=self.search, style="Rounded.TButton"
        )
        self.search_button.grid(row=2, column=0, columnspan=10, pady=10)

        # This is a sample list of dictionaries for genres.
        # In a real app, you would fetch this from the TMDb API.
        self.genres = [
            {"id": 28, "name": "Action"},
            {"id": 12, "name": "Adventure"},
            {"id": 16, "name": "Animation"},
            {"id": 35, "name": "Comedy"},
            {"id": 80, "name": "Crime"},
            {"id": 18, "name": "Drama"},
            {"id": 10751, "name": "Family"},
            {"id": 14, "name": "Fantasy"},
        ]

        for genre in self.genres:
            self.genre_list.insert(tk.END, genre["name"])

    def search(self):
        # This is where your search logic will go.
        search_text = self.search_parameter.get()
        search_type = self.search_type.get()
        selected_genre_id = self.get_selected_genre_id()
        selected_year = self.spinval.get()

        print(f"Search Text: {search_text}")
        print(f"Search Type: {search_type}")
        print(f"Selected Genre ID: {selected_genre_id}")
        print(f"Selected Year: {selected_year}")

    def get_selected_genre_id(self):
        # Method to get the selected genre ID
        try:
            index = self.genre_list.curselection()[0]
            genre_name = self.genre_list.get(index)
            # Find the genre ID that corresponds to the selected name
            for genre in self.genres:
                if genre["name"] == genre_name:
                    return genre["id"]
        except IndexError:
            return None  # No genre selected


class ResultsFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configure the grid to center the label
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create a font object for the label
        self.label_font = tkfont.Font(family="Helvetica", size=16, weight="bold")

        # Create and place the label
        tk.Label(
            self, text="Results", fg="blue", font=self.label_font, bg=self["bg"]
        ).grid(row=0, column=0, sticky="nsew")


class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Create Watch-List")

        # Set the window size to 75% of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.75)
        self.master.geometry(f"{window_width}x{window_height}")
        self.master.configure(bg="#2a2a2a")

        # Configure the grid to make the frames responsive
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=0, minsize=int(window_height * 0.1))
        self.master.grid_rowconfigure(1, weight=5)

        self.search_bar = SearchBar(self.master, bg="#444444")
        self.search_bar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.results_frame = ResultsFrame(self.master, bg="#444444")
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
