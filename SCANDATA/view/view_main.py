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
from SCANDATA.view.button_function import ButtonFn


class View(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.model = None
        self.controller = None
        self.button_fn = ButtonFn(self.controller)
        print('imported view')
        
        self.pack()
        master.geometry('500x800')
        master.title('SCANDATA')
        
               
        """
        Widgit mapping
        """
        
        "Top frame"
        frame_top = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=0, bg = 'azure')
        button_open_data = tk.Button(frame_top,text='Open data',command=self.open_file_with_list,width=10)
        button_open_data.place(x=110, y=150)
        button_open_data.config(fg='black', bg='skyblue')
        button_open_data.pack(side=tk.LEFT)
        frame_top.pack(side=tk.TOP, fill=tk.X)
        
        "Bottom frame"
        frame_bottom = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=0, bg = 'azure')
        button_open_data = tk.Button(frame_bottom,text='Open data',command=self.open_file_with_list,width=10)
        button_open_data.place(x=110, y=150)
        button_open_data.config(fg='black', bg='skyblue')
        button_exit = tk.Button(frame_bottom, text='Exit')
        
        button_open_data.pack(side=tk.LEFT)
        button_exit.pack(side=tk.RIGHT, padx=5)

        frame_bottom.pack(side=tk.BOTTOM, fill=tk.X)
        
        "Middle frame"
        frame_middle = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=2, bg = 'azure')
        frame_middle.pack(side=tk.TOP, fill=tk.BOTH)

        self.data_window = {}  # data window obj
        
        self.create_menu()
        


    def create_menu(self):
        menu_bar = tk.Menu(self)
 
        file_menu = tk.Menu(menu_bar, tearoff = tk.OFF)
        menu_bar.add_cascade(label='File', menu = file_menu) 

        file_menu.add_command(label = 'Open', command = self.open_file_with_list, accelerator = 'Ctrl+O')
        file_menu.add_separator()
        file_menu.add_command(label = 'Quit', command = self.master.destroy)
        
        # short cut
        menu_bar.bind_all('<Control-o>', self.open_file_with_list)

        # set to parent menu
        self.master.config(menu = menu_bar)
        
    """
    send to a button function class
    """
    def open_file_with_list(self, event=None):
        fullname = self.button_fn.get_fullname()
        file_list = self.button_fn.get_whole_filenames(fullname)

        tree_list = ttk.Treeview(self)
        
        # Define cuolumns   #0 is phantom column
        tree_list['columns'] = ('Main File', 'File List')
        tree_list.column('#0', width=20, minwidth=20, stretch=False)
        tree_list.column('Main File', anchor='w', width=120)
        tree_list.column('File List', anchor='w', width=120)
        
        # Headings
        tree_list.heading('#0', text='', anchor='w')
        tree_list.heading('Main File', text='File 001', anchor='w')
        tree_list.heading('File List', text='File List', anchor='w')
        
        # Add data
        tree_list.insert(parent='', index='end', iid=0, text='', values=os.path.basename(fullname))
        tree_list.insert(parent='', index='end', iid=0, text='', values=file_list)
        
        # for scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree_list.yview)
        tree_list.configure(yscroll=scrollbar.set)
        
        # Pack                 
        tree_list.pack(pady=0, fill=tk.BOTH, expand=True)  
        
    def open_file(self, event=None):
        fullname = self.button_fn.get_fullname()
        print(fullname)
        


        
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
        
        #self.initialize()

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