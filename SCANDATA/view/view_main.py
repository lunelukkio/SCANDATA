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
from cycler import cycler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from SCANDATA.controller.controller_main import ImagingController


class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = None
        
        self.__filename_obj_list = []
        self.window = []
        self.data_window = []  # data window obj
        
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
        filename_obj = self.controller.create_filename_obj(fullname)
        self.__filename_obj_list.append(filename_obj)
        
        "make a tree_list"
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
        #tree_list.insert(parent='Main File', index='end', iid=0, text='', values=filename_obj.filename_list)
        
        # for scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree_list.yview)
        tree_list.configure(yscroll=scrollbar.set)
        
        # Pack                 
        tree_list.pack(pady=0, fill=tk.BOTH, expand=True)  
        
        self.window.append(tk.Toplevel())
        self.data_window.append(DataWindow(self.window[len(self.window)-1], filename_obj, self.controller))

    def open_file(self, event=None):
        fullname = self.button_fn.get_fullname()
        print('Open ' + str(fullname))
        

class DataWindow(tk.Frame):
    def __init__(self, master=None, filename_obj=None):
        super().__init__(master)
        self.pack()
        self.__filename = filename_obj
        self.model = None
        self.controller = None
        
        master.geometry('1400x700')
        master.configure(background='azure')
        master.title(self.__filename.name)
        
        self.trace_ax_list = []  # [0] = fluoresent trace ax, [1] = elec trace ax
        self.image_ax_list = []  # [0] = main cell image ax

        # set frames
        frame_top = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=2, bg = 'white')
        button_open = tk.Button(frame_top, text='Open',command=self.file_open)
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
        
        #button_large_roi = tk.Button(frame_bottom, text='Large ROI', command=lambda: self.large_roi(1), width=20)  #need lambda for a fuction with aguments
        button_large_roi = tk.Button(frame_bottom, text='Large ROI', command=self.large_roi, width=20)
        button_large_roi.pack(side=tk.LEFT)
        
        button_small_roi = tk.Button(frame_bottom, text='Small ROI', command=self.small_roi, width=20)
        button_small_roi.pack(side=tk.LEFT)
        
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH)

        #frame_bottom = tk.Frame(master, pady=5, padx=5, relief=tk.RAISED, bd=2)

        # tkinter image frame
        frame_left = tk.Frame(master, pady=0, padx=0)
        frame_left.pack(side=tk.LEFT)
        # matplotlib image figure
        image_fig = Figure(figsize=(5, 5), dpi=100, facecolor='azure')  #Figure
        # matplotlib image axes
        image_ax = image_fig.add_subplot(1, 1, 1)           #Axes
        
        self.canvas_image = FigureCanvasTkAgg(image_fig, frame_left)
        #canvas_image.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        
        self.image_ax_list.append(ImageAx(self.canvas_image, image_ax))
        
        self.image_ax_list[0].image_ax.set_xticks([])
        self.image_ax_list[0].image_ax.set_yticks([])

        self.canvas_image.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.canvas_image.mpl_connect('button_press_event', self.onclick_image)
        
        # tkinter trace frame
        frame_right = tk.Frame(master, pady=1, padx=1)
        frame_right.pack(side=tk.RIGHT,expand=True,fill=tkinter.BOTH)
        # matplotlib trace figure
        trace_fig = Figure(figsize=(5, 5), dpi=100, facecolor='azure')  #Figure
        gridspec_trace_fig = trace_fig.add_gridspec(20, 1)
        
        self.canvas_trace = FigureCanvasTkAgg(trace_fig, frame_right)
        #canvas_trace.get_tk_widget().pack()
        
        # matplotlib trace axes
        trace_ax1 = trace_fig.add_subplot(gridspec_trace_fig[0:15])
        self.trace_ax_list.append(TraceAx(self.canvas_trace, trace_ax1))
        
        trace_ax2 = trace_fig.add_subplot(gridspec_trace_fig[16:20], sharex=self.trace_ax_list[0].trace_ax)
        self.trace_ax_list.append(TraceAx(self.canvas_trace, trace_ax2))
        
        toolbar_trace = NavigationToolbarTrace(self.canvas_trace, frame_right)
        toolbar_trace.update()
        self.canvas_trace.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.current_roi_num = 1

        # make a contoller and model.
        self.controller = ImagingController(self, self.__filename)
        self.model = self.controller.model
        
        # This is the main stream from the main controller.
        if self.__filename != None:
            self.model = self.controller.create_model(self.__filename)
            for i in range(2):
                self.trace_ax_list[i].model = self.model
            self.image_ax_list[0].model = self.model
            
    def file_open(self):
        fullname = FileService.get_fullname()
        self.model = self.controller.file_open(fullname)

    def onclick_image(self, event):
        if event.button == 1:  # left click
            self.controller.set_roi_position(event, self.current_roi_num)
            
        elif event.button == 2:
            pass
        elif event.button == 3:
            num = len(self.roi_box)
            self.current_roi_num += 1
            if self.current_roi_num > num:
                self.current_roi_num = 1
            else:
                pass
            self.set_trace(self.trace_ax1, 0, 'ChTrace' + str(2*self.current_roi_num-1))
            self.set_trace(self.trace_ax1, 1, 'ChTrace' + str(2*self.current_roi_num))
            
            self.draw_ax()
        
        
        
        
        
        
    def large_roi(self):
        self.change_roi_size([0, 0, 1, 1])

    def small_roi(self):
        self.change_roi_size([0, 0, -1, -1])

    def change_roi_size(self, val):
        self.controller.change_roi_size(self.__filename, self.current_roi_num, val)
        
        #display data and ROI
        self.set_trace(self.trace_ax1, 0, 'ChTrace' + str(2*self.current_roi_num-1))
        self.set_trace(self.trace_ax1, 1, 'ChTrace' + str(2*self.current_roi_num))
        self.roi_box[self.current_roi_num-1].set_roi()

        self.draw_ax()

    def add_roi(self):
        new_roi_box = RoiBox(self.__filename, self.controller, self.image_ax)
        self.roi_box.append(new_roi_box)
        self.controller.create_data(self.__filename, 'Trace')  # make 1xFullTrace, 2xChTrace, 1xRoi and bind
        new_roi_box.set_roi()
        self.draw_ax()
        
    def delete_roi(self):
        num_box = len(self.roi_box)
        if num_box == 1:
            print('This is the last ROI')
            return
        else:
            del self.roi_box[num_box-1]
            self.current_roi_num -= 1
            self.draw_ax()
            
class TraceAx:
    def __init__(self, canvas, ax):
        self.__model = None
        self.canvas_trace = canvas
        self.trace_ax = ax
        self.trace = []
        
    def update(self, view_data):
        data_list = view_data.get_data()
        self.show_data(data_list)
        
    def show_data(self, data_list: list):
        line_num = len(self.trace)
        if line_num >0:
            for i in range(line_num):
                self.trace[0].set_data([],[])
                del self.trace[0]
        self.trace_ax.set_prop_cycle(cycler('color', ['b', 'g', 'r', 'c', 'm', 'y', 'k']))
        for data in data_list:
            line_2d, = data.show_data(self.trace_ax)  # line"," means the first element of a list (convert from list to objet). Don't remove it.
            self.trace.append(line_2d)  # Add to the list for trace1 trace line objects [Line_2D] of axis object
        self.draw_ax()
            
    def draw_ax(self):
        self.trace_ax.relim()
        self.trace_ax.autoscale_view()
        self.canvas_trace.draw()


class ImageAx:
    def __init__(self, canvas, ax):
        self.__model = None
        self.canvas_image = canvas
        self.image_ax = ax
        self.image = []
        self.Roi = []
        
    def update(self, view_data):
        if 'Image' in view_data.name:  # for cell images
            data_list = view_data.get_data()
            self.show_data(data_list)
        elif 'Roi' in view_data.name:  # for RoiBoxs
            roi_box = view_data.roi_box
            self.show_roi(roi_box)
        self.draw_ax()
        
    def show_data(self, data_list: list):  # data_list = value obj list
        image_num = len(self.image)
        if image_num >0:
            for i in range(image_num):
                self.image[0].set_data([])
                del self.image[0]
        
        for data in data_list:
            image = data.show_data(self.image_ax)  # line, mean the first element of a list (convert from list to objet)
            self.image.append(image)  # Add to the list for trace line objects [Line_2D] of axis object
        self.draw_ax()

    def show_roi(self, roi_box: object):  # RoiBox always has only one data
        self.image[0].set_data([])
        
        self.image_ax.add_patch(roi_box.rectangle_obj)

    def draw_ax(self):
        self.canvas_image.draw()
        


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
    

class FileService:
    @staticmethod
    def get_fullname(event=None):
        # open file dialog
        fullname = tk.filedialog.askopenfilename(
            initialdir = os.getcwd(), # current dir
            filetypes=(('Tsm files', '*.tsm'),
                       ('Da files', '*.da'), 
                       ('Axon files', '*.abf'),
                       ('WinCP files', '*.wcp'),
                       ('All files', '*.*'))
                      )
        return fullname


if __name__ == '__main__':
    root = tk.Tk()
    root.title("SCANDATA")
    test = DataWindow(root)
    test.mainloop()