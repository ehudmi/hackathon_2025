import tkinter as tk

root = tk.Tk()
root.title("Frame Demo")
root.config(bg="skyblue")

# Create Frame widget
frame = tk.Frame(root, width=200, height=200)
frame.pack(padx=10, pady=10)

root.mainloop()
