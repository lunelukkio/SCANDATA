# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:43:13 2022

lunelukkio@gmail.com
main for view
"""

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import inspect, pprint
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class View(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.model = None
        self.controller = None
        print('imported view')
        
        self.pack()
        master.geometry('400x200')
        master.title('SCANDATA')
        
        self.window = []
        self.data_window = []
        
        self.create_menu()
        self.create_button()
        
        pprint.pprint(self.window)
        pprint.pprint(self.data_window)

        
    def create_menu(self):
        menu_bar = tk.Menu(self)
 
        file_menu = tk.Menu(menu_bar, tearoff = tk.OFF)
        menu_bar.add_cascade(label='File', menu = file_menu) 

        file_menu.add_command(label = 'Open', command = self.menu_open_click, accelerator = "Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label = 'Quit', command = self.master.destroy)
        # short cut
        menu_bar.bind_all("<Control-o>", self.menu_open_click)

        # set to parent menue
        self.master.config(menu = menu_bar)

    def menu_open_click(self, event=None):
        # open file dialog
        fullname = tk.filedialog.askopenfilename(
            initialdir = os.getcwd(), # current dir
            filetypes=(('Tsm files', '*.tsm'),
                       ('Da files', '*.da'), 
                       ('Axon files', '*.abf'),
                       ('WinCP files', '*.wcp'),
                       ('All files', '*.*'))
            )
        self.window.append(tk.Toplevel())
        self.data_window.append(DataWindow(self.window[len(self.window)-1], fullname))
        self.controller.menu_open_click(fullname)

    def create_button(self):
        self.button = tk.Button(self.master,text="Make a new window",command=self.buttonClick,width=10)
        self.button.place(x=110, y=150)
        self.button.config(fg="black", bg="skyblue")
        
    def buttonClick(self):
        
        
        print(self.window)
        print(self.user)
        
class DataWindow(tk.Frame):
    def __init__(self, master, filename):
        super().__init__(master)
        self.pack()
        self.filename = filename
        master.geometry("1400x610")
        master.title(filename)

        fig = Figure(figsize=(5, 5), dpi=100)   #Figure
        ax = fig.add_subplot(1, 1, 1)           #Axes
        #cell_image = self.contoller.get_data()
        #image = ax.imshow(cell_image.image_data, cmap='gray', interpolation='none')
        
        canvas = FigureCanvasTkAgg(fig, master)
        canvas.get_tk_widget().pack()

        self.button = tk.Button(master,text="コンソール上での確認",command=self.buttonClick,width=20)
        self.button.place(x=70, y=150)
        self.button.config(fg="black", bg="pink")
        
    def buttonClick(self):
        print("こちらは"+str(self.num)+"つ目に作成されたウィンドウです。")



if __name__ == '__main__':
    start_gui()