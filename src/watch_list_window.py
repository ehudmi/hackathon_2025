import tkinter as tk
from tkinter import font as tkfont
from db_connection import read_from_db, delete_film


class WatchlistWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("My watchlist")
        self.configure(bg="#2a2a2a")
        self.geometry("1100x700")

        self.label_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
        self.result_font = tkfont.Font(family="Helvetica", size=14)

        tk.Label(
            self, text="My watchlist", font=self.label_font, fg="red", bg="#2a2a2a"
        ).pack(pady=20)

        # Frame for the list
        list_frame = tk.Frame(self, bg="#2a2a2a")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Configure grid columns for better expansion
        list_frame.grid_columnconfigure(0, weight=0)  # Checkbox
        list_frame.grid_columnconfigure(1, weight=1)  # Title
        list_frame.grid_columnconfigure(2, weight=1)  # Release Year
        list_frame.grid_columnconfigure(3, weight=5)  # Short Summary (expands most)

        # Column headers
        tk.Label(
            list_frame,
            text="",
            bg="#2a2a2a",
            fg="white",
            font=self.result_font,
            width=3,
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            list_frame,
            text="Title",
            bg="#2a2a2a",
            fg="white",
            font=self.result_font,
            anchor="w",
        ).grid(row=0, column=1, sticky="w", padx=(0, 5))
        tk.Label(
            list_frame,
            text="Release Year",
            bg="#2a2a2a",
            fg="white",
            font=self.result_font,
            anchor="w",
        ).grid(row=0, column=2, sticky="w", padx=(0, 5))
        tk.Label(
            list_frame,
            text="Short Summary",
            bg="#2a2a2a",
            fg="white",
            font=self.result_font,
            anchor="w",
        ).grid(row=0, column=3, sticky="w")

        # Read from DB and populate list
        self.check_vars = []
        self.records = self.read_watchlist_from_db()
        for idx, record in enumerate(self.records):
            var = tk.BooleanVar()
            self.check_vars.append(var)
            tk.Checkbutton(list_frame, variable=var, bg="#2a2a2a").grid(
                row=idx + 1, column=0, sticky="w"
            )
            tk.Label(
                list_frame,
                text=record["title"],
                bg="#2a2a2a",
                fg="white",
                font=self.result_font,
                anchor="w",
            ).grid(row=idx + 1, column=1, sticky="w", padx=(0, 2))
            tk.Label(
                list_frame,
                text=record["release_date"],
                bg="#2a2a2a",
                fg="white",
                font=self.result_font,
                anchor="w",
                # No width specified, let it autosize
            ).grid(row=idx + 1, column=2, sticky="w", padx=(0, 2))

            # Frame for summary text and scrollbar
            summary_frame = tk.Frame(list_frame, bg="#2a2a2a")
            summary_frame.grid(row=idx + 1, column=3, sticky="nsew", padx=(0, 5))
            summary_text = tk.Text(
                summary_frame,
                bg="#2a2a2a",
                fg="white",
                font=self.result_font,
                wrap="word",
                height=3,
                width=60,
                borderwidth=0,
                highlightthickness=0,
            )
            summary_text.insert("1.0", record["short_summary"])
            summary_text.config(state="disabled")
            summary_text.pack(side="left", fill="both", expand=True)

            # Add vertical scrollbar to summary
            scrollbar = tk.Scrollbar(summary_frame, command=summary_text.yview)
            scrollbar.pack(side="right", fill="y")
            summary_text.config(yscrollcommand=scrollbar.set)

        # Buttons at the bottom
        btn_frame = tk.Frame(self, bg="#2a2a2a")
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Delete Selected",
            font=self.result_font,
            command=self.delete_selected,
        ).pack(side="left", padx=10)
        tk.Button(
            btn_frame,
            text="Update Selected",
            font=self.result_font,
            command=self.update_selected,
        ).pack(side="left", padx=10)
        tk.Button(
            btn_frame, text="Close", font=self.result_font, command=self.destroy
        ).pack(side="left", padx=10)

    def read_watchlist_from_db(self):
        films = read_from_db("films")
        return films

    def delete_selected(self):
        selected_indices = [i for i, var in enumerate(self.check_vars) if var.get()]
        for idx in selected_indices:
            film_id = self.records[idx]["film_id"]
            delete_film(film_id)
        self.destroy()
        self.__class__(self.master)

    def update_selected(self):
        # TODO: Implement update logic
        pass
