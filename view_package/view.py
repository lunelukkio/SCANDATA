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

        file_menu.add_command(label = 'Open', command = self.menu_open_click, accelerator = 'Ctrl+O')
        file_menu.add_separator()
        file_menu.add_command(label = 'Quit', command = self.master.destroy)
        # short cut
        menu_bar.bind_all('<Control-o>', self.menu_open_click)

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
        
        filename = self.controller.menu_open_click(fullname)
        self.window.append(tk.Toplevel())
        self.data_window.append(DataWindow(self.window[len(self.window)-1], filename, self.controller))


    def create_button(self):
        self.button = tk.Button(self.master,text='Open data',command=self.buttonClick,width=10)
        self.button.place(x=110, y=150)
        self.button.config(fg='black', bg='skyblue')
        
    def buttonClick(self): 
        self.menu_open_click()

        
class DataWindow(tk.Frame):
    def __init__(self, master=None, filename=None, controller=None):
        super().__init__(master)
        self.pack()
        self.filename = filename
        self.controller = controller
        master.geometry('1400x700')
        master.configure(background='azure')
        master.title(filename)
        
        self.trace1_ax = None
        self.trace2_ax = None
        
        # set frames
        frame_top = tk.Frame(master, pady=5, padx=5, relief=tk.RAISED, bd=2, bg = 'white')
        button_open = tk.Button(frame_top, text='Open')
        button_close = tk.Button(frame_top, text='Close')
        button_open.pack(side=tk.LEFT)
        button_close.pack(side=tk.LEFT, padx=5)
        frame_top.pack(fill=tk.X)
        
                        
        frame_bottom = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=2, bg = 'azure')
        button_roi = tk.Button(frame_bottom, text='ROI', command=self.button_roi_click,width=20)
        button_roi.place(x=1200, y=150)
        button_roi.config(fg="black", bg="pink")
        button2 = tk.Button(frame_bottom, text='Close')
        button_roi.pack(side=tk.LEFT)
        button2.pack(side=tk.LEFT, padx=5)
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH)


        #frame_bottom = tk.Frame(master, pady=5, padx=5, relief=tk.RAISED, bd=2)

        # matplotlib image
        frame_left = tk.Frame(master, pady=0, padx=0)
        frame_left.pack(side=tk.LEFT)
        image_fig = Figure(figsize=(5, 5), dpi=100, facecolor='azure')  #Figure
        image_ax = image_fig.add_subplot(1, 1, 1)           #Axes
        canvas_image = FigureCanvasTkAgg(image_fig, frame_left)
        #canvas_image.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        canvas_image.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        
        canvas_image.mpl_connect('button_press_event', self.onclick_image)
        
        # matplotlib trace
        frame_right = tk.Frame(master, pady=0, padx=0)
        frame_right.pack(side=tk.LEFT,expand = True)
        trace_fig = Figure(figsize=(5, 5), dpi=100, facecolor='azure')  #Figure
        self.trace1_ax = trace_fig.add_subplot(211)
        self.trace2_ax = trace_fig.add_subplot(212, sharex=self.trace1_ax)
        canvas_trace = FigureCanvasTkAgg(trace_fig, frame_right)
        #canvas_trace.get_tk_widget().pack()
        
        toolbar_trace = NavigationToolbarTrace(canvas_trace, frame_right)
        toolbar_trace.update()
        canvas_trace.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        #show data
        self.show_image(image_ax, 'CellImage1')
        self.show_trace(self.trace1_ax, 'ChTrace1')
        self.show_trace(self.trace1_ax, 'ChTrace2')
        self.show_trace(self.trace2_ax, 'ElecTrace1')

        
    def show_image(self, ax, image_type):
        image = self.controller.get_data(self.filename, image_type)
        ax.imshow(image.image_data, cmap='gray', interpolation='none')
        
    def show_trace(self, ax, trace_type):
        trace = self.controller.get_data(self.filename, trace_type)
        ax.plot(trace.time_data, trace.trace_data) 
        trace.plot_trace()

        
    def button_roi_click(self):
        self.controller.roi_controller()
        
    def onclick_image(self, event):
        self.controller.set_roi(event)
        self.show_trace(self.trace1_ax, 'ChTrace1')



class NavigationToolbarTrace(NavigationToolbar2Tk):
    def __init__(self, canvas=None, master=None):
        super().__init__(canvas, master)   
        self.canvas = canvas
        self.master = master

        self['bg'] = 'azure'
        for item in self.winfo_children():
           item['bg'] = 'azure'

    def get_val(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    root.title("SCANDATA")
    test = DataWindow(root)
    test.mainloop()