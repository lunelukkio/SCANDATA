# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:30:03 2022

gui layout
lunelukkio@gmail.com

"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from abc import abstractmethod
import os
import matplotlib.pyplot as plt
import numpy as np

#import tkinter.filedialog  #need this because of bug?
import abc

"""
view interface
"""
class View(tk.Frame):
    @abstractmethod
    def create_view():
        raise NotImplementedError
        
class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, message):
        pass

class MainWindow(View):
    def __init__(self, master=None):
        super().__init__(master)

        
        self.master.title("Main Window")
        self.master.geometry("1000x200")

        self.__create_menu()
        self.__create_tool_bar()
        self.__create_status_bar()
        self.__create_ROI_controller()
        self.__create_functions()
        self.move_position(1500, 500)

    def __create_menu(self):
        menu_bar = tk.Menu(self)

        #File menu
        file_menu = tk.Menu(menu_bar, tearoff = tk.OFF)
        menu_bar.add_cascade(label="File", menu = file_menu)

        file_menu.add_command(label = "Open...",
                              command = self.menu_open_click,
                              accelerator = "Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label = "Quit", command = self.master.destroy)

        menu_bar.bind_all("<Control-o>", self.menu_open_click) # shortcut

        #Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff = tk.OFF)
        menu_bar.add_cascade(label="Edit", menu = edit_menu)

        edit_menu.add_command(label = "None", )
        edit_menu.add_separator()

        # parent menu
        self.master.config(menu = menu_bar)


    def __create_tool_bar(self):

        frame_tool_bar = ttk.Frame(self.master, borderwidth = 2, relief = tk.SUNKEN)

        button1 = tk.Button(frame_tool_bar, text = "1", width = 2)
        button2 = tk.Button(frame_tool_bar, text = "2", width = 2)
        button3 = tk.Button(frame_tool_bar, text = "3", width = 2)

        button1.pack(side = tk.LEFT)
        button2.pack(side = tk.LEFT)
        button3.pack(side = tk.LEFT)

        frame_tool_bar.pack(fill = tk.X)

    def __create_status_bar(self):
        frame_status_bar = ttk.Frame(self.master, borderwidth = 2, relief = tk.SUNKEN)

        self.label1 = tk.Label(frame_status_bar, text = "filename")
        self.label2 = tk.Label(frame_status_bar, text = "status 2")

        self.label1.pack(side = tk.LEFT)
        self.label2.pack(side = tk.RIGHT)

        frame_status_bar.pack(side = tk.BOTTOM, fill = tk.X)

    def __create_ROI_controller(self):
        roi_controller_frame = ttk.Frame(
            self.master,
            borderwidth = 2,
            relief = tk.SUNKEN,
            )

        tk.Grid.rowconfigure(roi_controller_frame, index=0,weight=1)
        tk.Grid.rowconfigure(roi_controller_frame, index=1,weight=1)
        tk.Grid.rowconfigure(roi_controller_frame, index=2,weight=1)
        tk.Grid.columnconfigure(roi_controller_frame, index=0, weight=1)
        tk.Grid.columnconfigure(roi_controller_frame, index=1, weight=1)
        tk.Grid.columnconfigure(roi_controller_frame, index=2, weight=1)
        tk.Grid.columnconfigure(roi_controller_frame, index=3, weight=1,
                                pad=20)
        tk.Grid.columnconfigure(roi_controller_frame, index=4, weight=1)

        button_up = tk.Button(roi_controller_frame, text = "UP",
                              width = 5, height=5)
        button_left = tk.Button(roi_controller_frame, text = "LEFT",
                                width = 5, height=5)
        button_right = tk.Button(roi_controller_frame, text = "RIGHT",
                                 width = 5, height=5,)
        button_down = tk.Button(roi_controller_frame, text = "DOWN",
                                width = 5, height=5)
        button_LARGE = tk.Button(roi_controller_frame, text = "LARGE",
                                 width = 5, height=5)
        button_SMALL = tk.Button(roi_controller_frame, text = "SMALL",
                                 width = 5, height=5)
        button_RESET = tk.Button(roi_controller_frame, text = "RESET",
                                 width = 5, height=5)

        button_up.grid(row=0, column=1)
        button_left.grid(row=1, column=0)
        button_right.grid(row=1, column=2)
        button_down.grid(row=2, column=1)
        button_LARGE.grid(row=1, column=3)
        button_SMALL.grid(row=2, column=3)
        button_RESET.grid(row=2, column=4)

        roi_controller_frame.pack(side = tk.LEFT)

    def __create_functions(self):
        functions_frame = ttk.Frame(self.master, borderwidth = 2,
                                    relief = tk.SUNKEN)

        tk.Grid.rowconfigure(functions_frame, index=0,weight=1)
        tk.Grid.rowconfigure(functions_frame, index=1,weight=1)
        tk.Grid.rowconfigure(functions_frame, index=2,weight=1)
        tk.Grid.columnconfigure(functions_frame, index=0, weight=1)
        tk.Grid.columnconfigure(functions_frame, index=1, weight=1)
        tk.Grid.columnconfigure(functions_frame, index=2, weight=1)
        tk.Grid.columnconfigure(functions_frame, index=3, weight=1)
        tk.Grid.columnconfigure(functions_frame, index=4, weight=1)

        button_up = tk.Button(functions_frame, text = "Trace",
                              width = 15, height=10, command=self.open_trace_window)
        button_left = tk.Button(functions_frame, text = "Image",
                                width = 15, height=10)
        button_right = tk.Button(functions_frame, text = "3",
                                 width = 15, height=10, command=self.func_1)
        button_down = tk.Button(functions_frame, text = "4",
                                width = 15, height=10,  command=self.func_2)
        button_LARGE = tk.Button(functions_frame, text = "5",
                                 width = 15, height=5)
        button_SMALL = tk.Button(functions_frame, text = "6",
                                 width = 15, height=5)
        button_RESET = tk.Button(functions_frame, text = "7",
                                 width = 15, height=10)


        button_up.grid(row=0, column=0)
        button_left.grid(row=1, column=0)
        button_right.grid(row=2, column=0)
        button_down.grid(row=0, column=1)
        button_LARGE.grid(row=1, column=1)
        button_SMALL.grid(row=2, column=1)
        button_RESET.grid(row=0, column=2)

        functions_frame.pack(side = tk.LEFT)

    def open_trace_window(self):
        trace_window = TraceWindow(None)
        #trace_window.grab_set() #This is for keeping a window at top

        #move the window position
    def move_position(self, w_position, h_position):
        w = self.winfo_screenwidth()    #get display width
        h = self.winfo_screenheight()   #get display height
        w = w - w_position
        h = h - h_position
        self.master.geometry("1000x200+"+str(w)+"+"+str(h))
        
    def menu_open_click(self, event=None):
        ftypes = [("TSM Files", ".tsm"),
                  ("DA", ".da"),
                  ("All Files", ".*")]
        # file dialog
        fullname = filedialog.askopenfilename(
            initialdir = os.getcwd(), # current directory
            filetypes = ftypes
            )
        self.controller.menu_open_click(fullname)

    def func_1(self):
        """ for test"""
        print(self.controller.main_controller.filename)

    def func_2(self):
        """ not working because of no connection to model"""
        self.model.data_container.file_infor.print_filename()

class TraceWindow(tk.Toplevel, View):
    def __init__(self , parent):
        super().__init__(parent)
        self.title("Trace Window")
        self.geometry("1500x700")
        self.create_status_bar()


        frame_tool_bar = ttk.Frame(self, borderwidth = 2, relief = tk.SUNKEN)
        button1 = ttk.Button(frame_tool_bar, text='close',
                             width = 10, command=self.destroy)
        button1.pack()
        frame_tool_bar.pack(fill = tk.X)

        # Fluoresence trace window
        fluorescnece_window = tk.Canvas(self, background="#008080")
        fluorescnece_window.pack(expand=True, fill=tk.BOTH)
        fluorescnece_window.create_rectangle(50, 50, 800, 450, fill = "blue",
                                             stipple = "gray25")
        
        displayed_trace = self.controller.fluo_trace()
        a = plt.figure()
        plt.plot(displayed_trace)
        

        # Electrical trace window
        electrical_window = tk.Canvas(self, background="#008080")
        electrical_window.pack(expand=True, fill=tk.BOTH)



    def create_status_bar(self):
        frame_status_bar = ttk.Frame(self, borderwidth = 2, relief = tk.SUNKEN)

        self.label1 = tk.Label(frame_status_bar, text = "filename")
        self.label2 = tk.Label(frame_status_bar, text = "status 2")

        self.label1.pack(side = tk.LEFT)
        self.label2.pack(side = tk.RIGHT)

        frame_status_bar.pack(side = tk.BOTTOM, fill = tk.X)

        # This is for observer
    def update(self, message):
        print(f"TraceWindow: {message}")
        #write codes for updating graphs

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
        root.title("SCANDATA")
        main = MainWindow(master = root)
        main.mainloop()
