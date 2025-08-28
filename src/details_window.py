import tkinter as tk
from tkinter import font as tkfont
from db_connection import insert_film  # Make sure this import is correct


class DetailsWindow(tk.Toplevel):
    def __init__(self, master, item, result_type):
        super().__init__(master)
        self.title("Details")
        self.configure(bg="#222")
        self.geometry("600x500")  # Increased size
        font_title = tkfont.Font(family="Helvetica", size=18, weight="bold")
        font_body = tkfont.Font(family="Helvetica", size=14)
        self.item = item
        self.result_type = result_type

        if result_type == "movie":
            title = item.get("title", "Unknown Title")
            overview = item.get("overview", "No description available.")
            release = item.get("release_date", "Unknown")
            tk.Label(self, text=title, font=font_title, bg="#222", fg="red").pack(
                pady=10
            )
            tk.Label(
                self,
                text=f"Release Date: {release}",
                font=font_body,
                bg="#222",
                fg="white",
            ).pack(pady=5)
            tk.Label(
                self,
                text=overview,
                font=font_body,
                bg="#222",
                fg="white",
                wraplength=550,  # Increased wraplength for larger window
                justify="left",
            ).pack(pady=10)

            # Add to Watchlist button
            tk.Button(
                self,
                text="Add to Watchlist",
                font=font_body,
                bg="#444",
                fg="white",
                command=self.add_to_watchlist,
            ).pack(
                pady=20
            )  # Increased pady for visibility

        elif result_type == "person":
            name = item.get("name", "Unknown Name")
            known_for = ", ".join(
                [
                    m.get("title", "")
                    for m in item.get("known_for", [])
                    if m.get("title")
                ]
            )
            tk.Label(self, text=name, font=font_title, bg="#222", fg="red").pack(
                pady=10
            )
            tk.Label(
                self,
                text=f"Known for: {known_for}",
                font=font_body,
                bg="#222",
                fg="white",
                wraplength=550,
                justify="left",
            ).pack(pady=10)
        else:
            tk.Label(
                self,
                text="No details available.",
                font=font_body,
                bg="#222",
                fg="white",
            ).pack(pady=10)

    def add_to_watchlist(self):
        # Only add if it's a movie
        if self.result_type == "movie":
            film_id = str(self.item.get("id", ""))
            title = self.item.get("title", "")
            release_date = self.item.get("release_date", "")
            overview = self.item.get("overview", "")
            genre_ids = self.item.get("genre_ids", [])
            backdrop_url = self.item.get("backdrop_url", "")
            poster_url = self.item.get("poster_url", "")
            insert_film(
                film_id,
                title,
                release_date,
                overview,
                genre_ids,
                backdrop_url,
                poster_url,
            )
