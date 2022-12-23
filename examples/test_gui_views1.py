# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:30:03 2022

lunelukkio@gmail.com

gui layout
"""

import tkinter as tk
from tkinter import ttk
from abc import abstractmethod
import os
import tkinter.filedialog



class View(tk.Frame):
    @abstractmethod
    def create_view():
        raise NotImplementedError


class MainWindow(View):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Main Window")
        self.master.geometry("500x500") 

        self.create_menu()
        self.create_tool_bar()
        self.create_status_bar()
        self.create_side_panel()

    def create_menu(self):
        menu_bar = tk.Menu(self)
 
        file_menu = tk.Menu(menu_bar, tearoff = tk.OFF)
        menu_bar.add_cascade(label="File", menu = file_menu) 

        file_menu.add_command(label = "Open...", command = self.menu_open_click, accelerator = "Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label = "Quit", command = self.master.destroy)
        
        menu_bar.bind_all("<Control-o>", self.menu_open_click) # shortcut

        # parent menu
        self.master.config(menu = menu_bar)

    def menu_open_click(self, event=None):

        # file dialog
        filename = tk.filedialog.askopenfilename(
            filetypes = "py",
            initialdir = os.getcwd() # current directory
            )
        print(filename)
        #trace_window = TraceWindow(self)

    def create_tool_bar(self):

        frame_tool_bar = tk.Frame(self.master, borderwidth = 2, relief = tk.SUNKEN)

        button1 = tk.Button(frame_tool_bar, text = "1", width = 2)
        button2 = tk.Button(frame_tool_bar, text = "2", width = 2)
        button3 = tk.Button(frame_tool_bar, text = "3", width = 2)

        button1.pack(side = tk.LEFT)
        button2.pack(side = tk.LEFT)
        button3.pack(side = tk.LEFT)

        frame_tool_bar.pack(fill = tk.X)

    def create_status_bar(self):
        frame_status_bar = tk.Frame(self.master, borderwidth = 2, relief = tk.SUNKEN)

        self.label1 = tk.Label(frame_status_bar, text = "status 1")
        self.label2 = tk.Label(frame_status_bar, text = "status 2")

        self.label1.pack(side = tk.LEFT)
        self.label2.pack(side = tk.RIGHT)

        frame_status_bar.pack(side = tk.BOTTOM, fill = tk.X)

    def create_side_panel(self):
        side_panel = tk.Frame(self.master, borderwidth = 2, relief = tk.SUNKEN)

        button1 = tk.Button(side_panel, text = "button 1", width = 15, command=self.open_window)
        button2 = tk.Button(side_panel, text = "button 2", width = 15)

        button1.pack()
        button2.pack()
        
        side_panel.pack(side = tk.RIGHT, fill = tk.Y)
        
    def open_window(self): 
        trace_window = TraceWindow(self)
        #trace_window.grab_set() #This is for keeping a window at top
        
        # This is for observer
    def update(self, message):
        print(f"MainWindow: {message}")
        #write codes for updating graphs


class TraceWindow(tk.Toplevel, View):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Trace Window")
        self.geometry("1500x700") 

        frame_tool_bar = tk.Frame(self, borderwidth = 2, relief = tk.SUNKEN)
        button1 = ttk.Button(frame_tool_bar, text='close', width = 10, command=self.destroy)
        button1.pack()
        frame_tool_bar.pack(fill = tk.X)
        
        # draw canvas to left space
        canvas = tk.Canvas(self, background="#008080")
        canvas.pack(expand=True, fill=tk.BOTH)
        canvas.create_rectangle(50, 50, 800, 450, fill = "blue", stipple = "gray25")
        



class ImageWindow(View):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Image Window")
        self.master.geometry("700x700") 

        self.create_menu()
        self.create_tool_bar()
        self.create_status_bar()
        self.create_side_panel()
    

class BaselineWindow(View):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Baseline Window")
        self.master.geometry("700x700") 

        self.create_menu()
        self.create_tool_bar()
        self.create_status_bar()
        self.create_side_panel()


class DifferenceWindow(View):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Difference Window")
        self.master.geometry("700x700") 

        self.create_menu()
        self.create_tool_bar()
        self.create_status_bar()
        self.create_side_panel()



if __name__ == "__main__":
    
        root = tk.Tk()
        main = MainWindow(master = root)
        main.mainloop()
