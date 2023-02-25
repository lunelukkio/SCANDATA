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
import gc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from SCANDATA.controller.controller_main import ImagingController
from SCANDATA.view.data_repository import ViewDataRepository, RoiBox
from SCANDATA.controller.controller_main import WholeFilename



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
        self.view_data_repository = ViewDataRepository()
        self.current_roi_num = 1
        
        master.geometry('1400x700')
        master.configure(background='azure')
        master.title(self.__filename.name)
        
        self.ax_list = []  # [0] = main cell image ax (ImageAxsis class), [1] = fluoresent trace ax (TraceAx class), [2] = elec trace ax

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
        
        self.ax_list.append(ImageAx(self.canvas_image, image_ax))  # ax_list[0]
        
        self.ax_list[0].image_ax.set_xticks([])  # To remove ticks of image window.
        self.ax_list[0].image_ax.set_yticks([])  # To remove ticks of image window.
        self.ax_list[0].trace_show_flag = [True, False]  # ch1, ch2

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
        self.ax_list.append(TraceAx(self.canvas_trace, trace_ax1))  # ax_list[1]
        self.ax_list[1].trace_show_flag = [False,  # full trace
                                           True,  # ch1 trace
                                           False]  # ch2 trace
        
        # elec trace axes
        trace_ax2 = trace_fig.add_subplot(gridspec_trace_fig[16:20], sharex=self.ax_list[1].trace_ax)
        self.ax_list.append(TraceAx(self.canvas_trace, trace_ax2))  # ax_list[2]
        self.ax_list[2].trace_show_flag = [True,  # ch1
                                           False,  # ch2
                                           False,  # ch3
                                           False,  # ch4
                                           False,  # ch5
                                           False,  # ch6
                                           False,  # ch7
                                           False]  # ch8
        
        toolbar_trace = NavigationToolbarTrace(self.canvas_trace, frame_right)
        toolbar_trace.update()
        self.canvas_trace.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.file_open(self.__filename)
            
    def file_open(self, *filename):
        if filename == ():
            fullname = FileService.get_fullname()  # This is str filename
            if fullname == None:
                return
            self.__filename = self.create_filename_obj(fullname)

        self.reset()        
        

        
    def create_model(self):
        self.model = self.controller.create_model(self.__filename)
        self.view_data_repository.model = self.model
        self.view_data_repository.initialize_view_data_repository(self.ax_list)
        
    def create_filename_obj(self, filename: str):
        filename_obj = WholeFilename(filename)  # Convert from str to value object.
        self.__filename = filename_obj
        return filename_obj

    def onclick_image(self, event):
        if event.button == 1:  # left click
            self.controller.set_roi_position(event, self.current_roi_num)
        elif event.button == 2:
            pass
        elif event.button == 3:
            num = self.view_data_repository.count_data('RoiView')
            self.current_roi_num += 1
            if self.current_roi_num > num:  #if the number of roi is larger than current roi num
                self.current_roi_num = 1
            else:
                pass
            self.view_data_repository.update('RoiView' + str(self.current_roi_num))
                
    def large_roi(self):
        self.change_roi_size([0, 0, 1, 1])

    def small_roi(self):
        self.change_roi_size([0, 0, -1, -1])

    def change_roi_size(self, val):
        self.controller.change_roi_size(self.current_roi_num, val)

    def add_roi(self):
        self.view_data_repository.create_roi(self.ax_list)
        
    def delete_roi(self):
        self.view_data_repository.delete_roi(self.ax_list)
        for i in range(len(self.ax_list)):
            self.ax_list[i]..clear()
        self.current_roi_num -= 1
        
    def reset(self):
        self.current_roi_num = 1
        RoiBox.roi_num = 0
        #self.view_data_repository.delete()
        
        self.model = None
        self.controller = None
        self.view_data_repository = None
        for i in range(3):
            self.ax_list[i].reset()
        gc.collect()

        self.view_data_repository = ViewDataRepository()
        self.controller = ImagingController(self, self.__filename)
        self.create_model()
            
class TraceAx:
    def __init__(self, canvas, ax):
        self.canvas_trace = canvas
        self.trace_ax = ax
        self.current_ch = 1

        self.trace = []
        # Need refactoring for valiable number of traces
        self.trace_show_flag = []
        
        self.color_selection = ['black', 'red', 'blue', 'orange', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
 
    def update(self, view_data):
        data_list = view_data.get_data()
        self.show_data(data_list)

        
    def show_data(self, data_list: list):
        line_num = len(self.trace)
        if line_num > 0:
            i = 0
            for trace_value_obj in data_list:
                if self.trace_show_flag[i] is True:
                    time = trace_value_obj.time
                    data = trace_value_obj.data
                elif self.trace_show_flag[i] is False:
                    time = None
                    data = None
                self.trace[i].set_data(time,data)
                i += 1
        elif line_num == 0:
            self.trace_ax.clear()
            i = 0
            for trace_value_obj in data_list:
                line_2d, = trace_value_obj.show_data(self.trace_ax)  # line"," means the first element of a list (convert from list to objet). Don't remove it.
                self.trace.append(line_2d)  # Add to the list for trace1 trace line objects [Line_2D] of axes object
                line_2d.set_color(self.color_selection[i])
                if self.trace_show_flag[i] == False:
                    line_2d.set_data(None,None)
                i += 1 
        self.draw_ax()
        
    def draw_ax(self):
        self.trace_ax.relim()
        self.trace_ax.autoscale_view()
        self.canvas_trace.draw()
        
    def reset(self):
        self.current_ch = 1
        self.trace = []
        """
        num = len(self.trace)
        for i in range(num):
            del self.trace[0]
        """

class ImageAx:
    def __init__(self, canvas, ax):
        self.__model = None
        self.canvas_image = canvas
        self.image_ax = ax
        self.image = []
        self.current_ch = 1
        # Need refactoring for valiable number for images.
        self.image_show_flag = [True, False]   # 0 = full trace, 1 = ch1 trace, 2 = ch2 trace
        
    def update(self, view_data):
        if 'Image' in view_data.name:  # for cell images
            data_list = view_data.get_data()  # get data from view data
            self.show_data(data_list)
        elif 'Roi' in view_data.name:  # for RoiBoxs
            roi_box = view_data.roi_box
            self.show_roi(roi_box)
        self.draw_ax()
        
    def show_data(self, data_list: list):  # data_list = value obj list  Delete old images, and make new images
        image_num = len(self.image)
        if image_num >0:
            i = 0
            for image_value_obj in data_list:
                if self.image_show_flag[i] is True:
                    data = image_value_obj.data
                elif self.image_show_flag[i] is False:
                    data = [[],[]]
                self.image[i].set_data(data)  # for delete privious images
                i += 1

        elif image_num == 0:
            self.image_ax.clear()
            i = 0
            for image_value_obj in data_list:
                image = image_value_obj.show_data(self.image_ax)  # line, mean the first element of a list (convert from list to objet)
                self.image.append(image)  # Add to the list for trace line objects [Line_2D] of axes object
                if self.image_show_flag[i] is False:
                    image.set_data([[],[]])
                i += 1

    def show_roi(self, roi_box: object):  # not delete but update rectangle. RoiBox always has only one data in RoiView class
        self.image_ax.add_patch(roi_box.rectangle_obj)

    def draw_ax(self):
        self.image_ax.relim()
        self.image_ax.autoscale_view()
        self.canvas_image.draw()
        
    def reset(self):
        self.current_ch = 1
        self.image = []
        self.image_ax.clear()
        """
        num = len(self.image)
        for i in range(num):
            del self.image[0]


        """

        self.draw_ax()
        

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