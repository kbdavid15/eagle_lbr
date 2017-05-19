"""
@description
Adds a device with the specified manufacturer part number to eagle library
Also adds to a local database for easy lookup/export later
Utilizes the octopart.com API

@author Kyle David <kbdavid15@gmail.com
"""

import eaglepy
import tkinter as tk
import tkinter.filedialog as fd

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.lib_file_name = ''

    def create_widgets(self):
        lib_label = tk.Label(self)
        lib_label['text'] = "Select Eagle library to add part to"
        lib_label.pack()
        self.eagle_lib = tk.Entry()
        self.eagle_lib.pack(fill=tk.X)
        self.open_eagle_lib = tk.Button()
        self.open_eagle_lib['text'] = "Open"
        self.open_eagle_lib['command'] = self.select_eagle_lib
        self.open_eagle_lib.pack(anchor='e')
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

    def select_eagle_lib(self):
        self.lib_file_name = fd.askopenfilename()
        self.eagle_lib.insert(0, self.lib_file_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()