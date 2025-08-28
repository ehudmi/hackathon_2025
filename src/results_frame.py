import os
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from details_window import DetailsWindow
from PIL import Image, ImageTk
from io import BytesIO
import requests


class ResultsFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.result_font = tkfont.Font(family="Helvetica", size=14)
        self.configure(bg=self["bg"])
        self.results = []
        self.result_type = None  # 'movie' or 'person'

        # --- Scrollable area setup ---
        self.canvas = tk.Canvas(self, bg=self["bg"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.inner_frame = tk.Frame(self.canvas, bg="#2a2a2a")

        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        # --- End scrollable area setup ---

    def display_results(self, results, result_type):
        # Clear previous results
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.results = results
        self.result_type = result_type

        # --- Add column headers ---
        if result_type == "movie":
            tk.Label(
                self.inner_frame,
                text="Image",
                font=self.label_font,
                bg=self["bg"],
                fg="white",
            ).grid(row=0, column=0, padx=(10, 5), pady=(10, 2))
            tk.Label(
                self.inner_frame,
                text="",
                font=self.label_font,
                bg=self["bg"],
                fg="white",
            ).grid(row=0, column=1, padx=(10, 5), pady=(10, 2))
            tk.Label(
                self.inner_frame,
                text="Title",
                font=self.label_font,
                bg=self["bg"],
                fg="white",
            ).grid(row=0, column=2, padx=(0, 10), pady=(10, 2), sticky="w")
            tk.Label(
                self.inner_frame,
                text="Release Year",
                font=self.label_font,
                bg=self["bg"],
                fg="white",
            ).grid(row=0, column=3, padx=(0, 10), pady=(10, 2), sticky="w")
        elif result_type == "person":
            tk.Label(
                self.inner_frame,
                text="Image",
                font=self.label_font,
                bg=self["bg"],
                fg="white",
            ).grid(row=0, column=0, padx=(10, 5), pady=(10, 2))
            tk.Label(
                self.inner_frame,
                text="",
                font=self.label_font,
                bg=self["bg"],
                fg="white",
            ).grid(row=0, column=1, padx=(10, 5), pady=(10, 2))
            tk.Label(
                self.inner_frame,
                text="Name",
                font=self.label_font,
                bg=self["bg"],
                fg="white",
            ).grid(row=0, column=2, padx=(0, 10), pady=(10, 2), sticky="w")
            tk.Label(
                self.inner_frame,
                text="Role",
                font=self.label_font,
                bg=self["bg"],
                fg="white",
            ).grid(row=0, column=3, padx=(0, 10), pady=(10, 2), sticky="w")
        # --- End column headers ---

        if not results:
            tk.Label(
                self.inner_frame,
                text="No results found.",
                font=self.label_font,
                bg=self["bg"],
                fg="white",
            ).grid(row=1, column=0, padx=10, pady=10)
            return

        for idx, item in enumerate(results):
            row_idx = idx + 1  # Offset by 1 for header row

            # Get image URL (always fallback to a local image if missing)
            img_url = (
                item.get("poster_url")
                if result_type == "movie"
                else item.get("photo_url")
            )
            if not img_url:
                img_url = (
                    "assets/old_style_movie_projector.png"
                    if result_type == "movie"
                    else "assets/blank_profile_image.png"
                )
            img_obj = self.get_image_from_url(img_url)

            # Keep a reference to avoid garbage collection
            if not hasattr(self, "img_refs"):
                self.img_refs = []
            self.img_refs.append(img_obj)

            # Image label (no need for else branch, always have an image)
            tk.Label(self.inner_frame, image=img_obj, bg="#2a2a2a").grid(
                row=row_idx, column=0, padx=(10, 5), pady=5
            )

            # Button and other columns (shifted by 1)
            btn = tk.Button(
                self.inner_frame,
                text="Select",
                font=self.result_font,
                bg="#333",
                fg="white",
                relief="raised",
                command=lambda i=item: self.open_details(i, result_type),
                width=8,
            )
            btn.grid(row=row_idx, column=1, sticky="w", padx=(10, 5), pady=5)

            if result_type == "movie":
                title = item.get("title", "Unknown Title")
                year = (
                    item.get("release_date", "")[:4]
                    if item.get("release_date")
                    else "N/A"
                )
                tk.Label(
                    self.inner_frame,
                    text=title,
                    font=self.result_font,
                    bg=self["bg"],
                    fg="white",
                    anchor="w",
                ).grid(row=row_idx, column=2, sticky="w", padx=(0, 10), pady=5)
                tk.Label(
                    self.inner_frame,
                    text=year,
                    font=self.result_font,
                    bg=self["bg"],
                    fg="white",
                    anchor="w",
                ).grid(row=row_idx, column=3, sticky="w", padx=(0, 10), pady=5)
            else:
                name = item.get("name", "Unknown Name")
                department = item.get("role", "N/A")
                tk.Label(
                    self.inner_frame,
                    text=name,
                    font=self.result_font,
                    bg=self["bg"],
                    fg="white",
                    anchor="w",
                ).grid(row=row_idx, column=2, sticky="w", padx=(0, 10), pady=5)
                tk.Label(
                    self.inner_frame,
                    text=department,
                    font=self.result_font,
                    bg=self["bg"],
                    fg="white",
                    anchor="w",
                ).grid(row=row_idx, column=3, sticky="w", padx=(0, 10), pady=5)

    def open_details(self, item, result_type):
        if result_type == "movie":
            DetailsWindow(self, item, "movie")
        elif result_type == "person":
            DetailsWindow(self, item, "person")

    def get_image_from_url(self, url, size=(70, 70)):
        try:
            if url.startswith("http"):
                response = requests.get(url)
                response.raise_for_status()
                img_data = response.content
                img = Image.open(BytesIO(img_data))
            else:
                # Build absolute path relative to this file
                base_dir = os.path.dirname(os.path.abspath(__file__))
                abs_path = os.path.join(base_dir, url)
                img = Image.open(abs_path)
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print("Image load error:", e)
            return None
