"""
@description
Adds a device with the specified manufacturer part number to eagle library
Also adds to a local database for easy lookup/export later
Utilizes the octopart.com API

@author Kyle David <kbdavid15@gmail.com
"""

# from eaglepy import default_layers, eagle
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        mpn_label = tk.Label(self)
        mpn_label["text"] = "Manufacturer Part Number"
        mpn_label.pack()
        self.mpn_text = tk.Entry(self)
        self.mpn_text.pack()
        self.enter_btn = tk.Button(self)
        self.enter_btn["text"] = "Enter"
        self.enter_btn["command"] = self.add_parts
        self.enter_btn.pack(side="bottom")

    def add_parts(self):
        print(f"Now adding {self.mpn_text.get()} to database", )


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()