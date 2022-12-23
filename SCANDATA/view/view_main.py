# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:43:13 2022

lunelukkio@gmail.com
main for view
"""

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import os
from matplotlib.figure import Figure
import matplotlib.patches as patches
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
        
        self.data_window = {}  # data window obj
        
        self.create_menu()
        self.create_button()
        
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
        new_window = tk.Toplevel()
        self.data_window[filename] = DataWindow(new_window, filename, self.controller)


    def create_button(self):
        self.button = tk.Button(self.master,text='Open data',command=self.open_file,width=10)
        self.button.place(x=110, y=150)
        self.button.config(fg='black', bg='skyblue')
        
    def open_file(self): 
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
        
        self.trace_ax1 = None
        self.trace_ax2 = None
        
        self.trace_y1 = []
        self.trace_y2 = []
        
        self.roi_box = []
        
        # set frames
        frame_top = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=2, bg = 'white')
        button_open = tk.Button(frame_top, text='Open',command=self.button_reopen)
        button_close = tk.Button(frame_top, text='Close')
        button_open.pack(side=tk.LEFT)
        button_close.pack(side=tk.LEFT, padx=5)
        frame_top.pack(fill=tk.X)
        
        """Bottom Buttons"""
        frame_bottom = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=0, bg = 'azure')
        button_add_roi = tk.Button(frame_bottom, text='Add ROI', command=self.add_roi, width=20)
        button_add_roi.config(fg="black", bg="pink")
        button_add_roi.pack(side=tk.LEFT, padx=5)

        button_delete_roi = tk.Button(frame_bottom, text='Delete ROI', command=self.delete_roi, width=20)
        button_delete_roi.config(fg="black", bg="pink")
        button_delete_roi.pack(side=tk.LEFT)
        
        button_delete_roi = tk.Button(frame_bottom, text='Large ROI', command=lambda: self.large_roi(1), width=20)
        button_delete_roi.pack(side=tk.LEFT)
        
        button_delete_roi = tk.Button(frame_bottom, text='Small ROI', command=self.small_roi, width=20)
        button_delete_roi.pack(side=tk.LEFT)
        
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH)



        #frame_bottom = tk.Frame(master, pady=5, padx=5, relief=tk.RAISED, bd=2)

        # tkinter image frame
        frame_left = tk.Frame(master, pady=0, padx=0)
        frame_left.pack(side=tk.LEFT)
        # matplotlib image figure
        image_fig = Figure(figsize=(5, 5), dpi=100, facecolor='azure')  #Figure
        # matplotlib image axes
        self.image_ax = image_fig.add_subplot(1, 1, 1)           #Axes
        self.image_ax.set_xticks([])
        self.image_ax.set_yticks([])
        self.canvas_image = FigureCanvasTkAgg(image_fig, frame_left)
        #canvas_image.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        self.canvas_image.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.canvas_image.mpl_connect('button_press_event', self.onclick_image)
        
        # tkinter trace frame
        frame_right = tk.Frame(master, pady=1, padx=1)
        frame_right.pack(side=tk.RIGHT,expand=True,fill=tkinter.BOTH)
        # matplotlib trace figure
        trace_fig = Figure(figsize=(5, 5), dpi=100, facecolor='azure')  #Figure
        gridspec_trace_fig = trace_fig.add_gridspec(20, 1)
        # matplotlib trace axes
        self.trace_ax1 = trace_fig.add_subplot(gridspec_trace_fig[0:15])
        self.trace_ax2 = trace_fig.add_subplot(gridspec_trace_fig[16:20], sharex=self.trace_ax1)

        self.canvas_trace = FigureCanvasTkAgg(trace_fig, frame_right)
        #canvas_trace.get_tk_widget().pack()
        
        toolbar_trace = NavigationToolbarTrace(self.canvas_trace, frame_right)
        toolbar_trace.update()
        self.canvas_trace.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.initialize()

    def initialize(self):
        self.create_image(self.image_ax, 'CellImage1')
        self.create_trace(self.trace_ax1, 'ChTrace1')
        self.create_trace(self.trace_ax1, 'ChTrace2')
        self.create_trace(self.trace_ax2, 'ElecTrace1')
        
        roi_box = RoiBox(self.image_ax)
        self.roi_box.append(roi_box)
        
    def create_image(self, ax, image_type):
        image = self.controller.get_data(self.filename, image_type)
        ax.imshow(image.image_data, cmap='gray', interpolation='none')
        
    def create_trace(self, ax, trace_type):
        trace = self.controller.get_data(self.filename, trace_type)
        line, =ax.plot(trace.time_data, trace.trace_data)  # new line object
        self.trace_y1.append(line)  # Add to the list for trace_y1 trace line objects
        
    def set_trace(self, ax, trace_num, trace_type):
        trace = self.controller.get_data(self.filename, trace_type)

        self.trace_y1[trace_num].set_ydata(trace.trace_data)
        
    def large_roi(self, roi_num):
        pass
        #self.controll.large_roi(roi_num)
    
    def small_roi(self):
        pass
        
    def add_roi(self):
        new_roi_box = RoiBox(self.image_ax)
        self.roi_box.append(new_roi_box)
        self.create_trace(self.filename, 'ChTrace1')
        self.create_trace(self.filename, 'ChTrace2')
        
        
    def delete_roi(self):
        num_box = len(self.roi_box)
        if num_box == 1:
            print('This is the last ROI')
            return
        else:
            del self.roi_box[num_box-1]
            print(num_box)
        
    def onclick_image(self, event):
        roi = self.controller.set_roi(event)
        self.set_trace(self.trace_ax1, 0, 'ChTrace1')
        self.set_trace(self.trace_ax1, 1, 'ChTrace2')
        
        self.roi_box[0].set_roi(roi)
        self.trace_ax1.relim()
        self.trace_ax1.autoscale_view()
        self.canvas_trace.draw()
        self.canvas_image.draw()
        
    def button_reopen(self):
        del self.controller.model.data_file[self.filename]
        # reopen window
        


class RoiBox():
    def __init__(self, ax):
        self.rectangle = patches.Rectangle(xy=(40, 40), width=1, height=1, ec='r', fill=False)
        ax.add_patch(self.rectangle)
        
    def set_roi(self, roi):
        self.rectangle.xy = (roi[0], roi[1])
        self.rectangle.width = roi[2]
        self.rectangle.height = roi[3]

        
        
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