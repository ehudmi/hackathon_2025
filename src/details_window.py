import tkinter as tk
from tkinter import font as tkfont


class DetailsWindow(tk.Toplevel):
    def __init__(self, master, item, result_type):
        super().__init__(master)
        self.title("Details")
        self.configure(bg="#222")
        self.geometry("400x350")
        font_title = tkfont.Font(family="Helvetica", size=18, weight="bold")
        font_body = tkfont.Font(family="Helvetica", size=14)

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
                wraplength=350,
                justify="left",
            ).pack(pady=10)
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
                wraplength=350,
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
