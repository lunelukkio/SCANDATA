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
import gc
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from SCANDATA.controller.controller_main import MainController, ImagingController
from SCANDATA.view.data_repository import ViewDataRepository
from SCANDATA.controller.controller_main import WholeFilename


class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = MainController()
        
        self.__filename_obj_list = []
        self.window = []
        self.data_window = []  # data window obj
        self.my_color_main = 'azure'
        
        self.pack()
        master.geometry('500x100')
        master.title('SCANDATA')
               
        """
        Widgit mapping
        """
        
        "Top frame"
        frame_top = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=0, bg = self.my_color_main)
        button_open_data = tk.Button(frame_top,text='Open data',command=self.open_file,width=10)
        button_open_data.place(x=110, y=150)
        button_open_data.config(fg='black', bg='skyblue')
        button_open_data.pack(side=tk.LEFT)
        frame_top.pack(side=tk.TOP, fill=tk.X)
        
        button_memory = tk.Button(frame_top,text='Check memory',command=self.check_memory,width=10)
        button_memory.place(x=110, y=150)
        button_memory.config(fg='black', bg='skyblue')
        button_memory.pack(side=tk.LEFT)
        frame_top.pack(side=tk.TOP, fill=tk.X)
        
        "Bottom frame"
        frame_bottom = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=0, bg = self.my_color_main)
        button_open_data2 = tk.Button(frame_bottom,text='Open data',state='disable',command=self.open_file_with_list,width=10)
        button_open_data2.place(x=110, y=150)
        button_open_data2.config(fg='black', bg='skyblue')
        button_exit = tk.Button(frame_bottom, text='Exit')
        
        button_open_data2.pack(side=tk.LEFT)
        button_exit.pack(side=tk.RIGHT, padx=5)

        frame_bottom.pack(side=tk.BOTTOM, fill=tk.X)
        
        "Middle frame"
        frame_middle = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=2, bg = self.my_color_main)
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
        
    def check_memory(self):
        memory_infor, maximum_memory, available_memory = self.controller.get_memory_infor()
        print(f"Current memory usage: {memory_infor / 1024 / 1024:.2f} MB / {maximum_memory / 1024 / 1024:.2f} MB, Available memory: {available_memory / 1024 / 1024:.2f} MB")
        
        
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
        fullname = FileService.get_fullname()  # This is str filename
        filename_obj = WholeFilename(fullname)
        self.__filename_obj_list.append(filename_obj)
        self.window.append(tk.Toplevel())
        self.data_window.append(DataWindow(self.window[len(self.window)-1], filename_obj))
        print('Open ' + str(fullname))
        

class DataWindow(tk.Frame):
    def __init__(self, master=None, filename_obj=None):
        super().__init__(master)
        self.pack()
        self.__filename = []  # filename_obj
        self.ax_list = []  # [0] = main cell image ax (ImageAxsis class), [1] = fluoresent trace ax (TraceAx class), [2] = elec trace ax
        self.my_color = '#BCD2EE'
        master.geometry('1400x700')
        master.configure(background=self.my_color)
        master.title('None')

        #self.button_func = ButtonFunction(self)

        """ Top Buttons"""
        frame_top = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=2, bg = 'white')
        tk.Button(frame_top, text='Open',command=self.file_open).pack(side=tk.LEFT)
        tk.Button(frame_top, text='Close').pack(side=tk.LEFT, padx=5)
        frame_top.pack(fill=tk.X)
        
        """Bottom Buttons"""
        frame_bottom = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=0, bg = self.my_color)
        
        # for ROI control
        tk.Button(frame_bottom, text='Large ROI', command=self.large_roi, width=20).pack(side=tk.LEFT)
        tk.Button(frame_bottom, text='Small ROI', command=self.small_roi, width=20).pack(side=tk.LEFT)
        tk.Button(frame_bottom, text='Add ROI', fg="black", bg="pink", state='disable', command=self.add_roi, width=5).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_bottom, text='Delete ROI', fg="black", bg="pink", state='disable', command=self.delete_roi, width=5).pack(side=tk.LEFT)
        
        #for the ch select buttons
        style = ttk.Style()
        style.configure('TCheckbutton', background=self.my_color)
        
        self.checkbox_flag_list = [tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()]  # Should be the same as the default of trace flags
        ttk.Checkbutton(frame_bottom,
                        text='Full',
                        variable=self.checkbox_flag_list[0],
                        command=lambda: self.select_ch(0)).pack(side=tk.LEFT)
        ttk.Checkbutton(frame_bottom,
                        text='Ch 1',
                        variable=self.checkbox_flag_list[1],
                        command=lambda: self.select_ch(1)).pack(side=tk.LEFT)

        ttk.Checkbutton(frame_bottom,
                        text='Ch 2',
                        variable=self.checkbox_flag_list[2],
                        command=lambda: self.select_ch(2)).pack(side=tk.LEFT)
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH)
        
        # for the mod radio buttons
        style.configure('TRadiobutton', background=self.my_color)
        self.radio_button_var_1 = tk.StringVar()
        ttk.Radiobutton(frame_bottom,
                       text="F",
                       variable=self.radio_button_var_1,
                       value="F",
                       command=lambda: self.remove_mod('Trace', 'F')).pack(side=tk.LEFT)
        ttk.Radiobutton(frame_bottom,
                       text="DF/F",
                       variable=self.radio_button_var_1,
                       value="DFoverF",
                       command=lambda: self.add_mod('Trace', 'DFoverF')).pack(side=tk.LEFT)
        ttk.Radiobutton(frame_bottom,
                       text="Norm",
                       variable=self.radio_button_var_1,
                       value="Norm",
                       command=lambda: self.add_mod('Trace', 'Normalize')).pack(side=tk.LEFT)
        
        """ Image Frame"""
        # tkinter image frame
        frame_left = tk.Frame(master, pady=0, padx=0)
        frame_left.pack(side=tk.LEFT)
        # matplotlib image figure
        image_fig = Figure(figsize=(5, 5), dpi=100, facecolor=self.my_color)  #Figure
        # matplotlib image axes
        image_ax = image_fig.add_subplot(1, 1, 1)           #Axes
        
        self.canvas_image = FigureCanvasTkAgg(image_fig, frame_left)
        #canvas_image.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        self.ax_list.append(ImageAx(self.canvas_image, image_ax))  # ax_list[0]

        self.canvas_image.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # mouse click events
        self.canvas_image.mpl_connect('button_press_event', self.onclick_image)   
        
        """ Trace Frames"""
        # tkinter trace frame
        frame_right = tk.Frame(master, pady=1, padx=1)
        frame_right.pack(side=tk.RIGHT,expand=True,fill=tkinter.BOTH)
        frame_right.pack_propagate(False)
        
        # matplotlib trace figure
        trace_fig = Figure(figsize=(5, 5), dpi=100, facecolor=self.my_color)  #Figure
        gridspec_trace_fig = trace_fig.add_gridspec(20, 1)

        self.canvas_trace = FigureCanvasTkAgg(trace_fig, frame_right)
        
        # matplotlib trace axes
        trace_ax1 = trace_fig.add_subplot(gridspec_trace_fig[0:15])
        self.ax_list.append(TraceAx(self.canvas_trace, trace_ax1))  # ax_list[1]
        
        # matplotlib elec trace axes
        trace_ax2 = trace_fig.add_subplot(gridspec_trace_fig[16:20], sharex=self.ax_list[1].ax_obj)
        self.ax_list.append(TraceAx(self.canvas_trace, trace_ax2))  # ax_list[2]
        
        #canvas_trace.get_tk_widget().pack()
        toolbar_trace = NavigationToolbarTrace(self.canvas_trace, frame_right, self.my_color)
        toolbar_trace.update()
        
        self.canvas_trace.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        if filename_obj is not None:
            master.title(filename_obj.name)
            self.__filename = filename_obj
            self.file_open(self.__filename)
        
    def reset(self):
        self.model = None
        self.controller = None
        self.view_data_repository = ViewDataRepository()
        self.current_roi_num = 2  # roi class start from Roi1
        self.ax_list[0].current_roi_num = 2
            
        # for image axes
        self.ax_list[0].ax_obj.set_xticks([])  # To remove ticks of image window.
        self.ax_list[0].ax_obj.set_yticks([])  # To remove ticks of image window.
        
        self.ax_list[0].show_flag = [True, True]  # ch1, ch2  #  shold be the same as the default checkbox BooleanVar
        
        # for RoiBox
        self.ax_list[0].remove_rectangles()
        
        # for the ch select buttons
        for i in range(3):
            self.checkbox_flag_list[i].set(True)
        self.ax_list[1].show_flag = [True, True, True]  #  shold be the same as the default checkbox BooleanVar
        self.radio_button_var_1.set("F")
        
        self.ax_list[2].show_flag = [True,  # ch1
                                           True,  # ch2
                                           True,  # ch3
                                           True,  # ch4
                                           True,  # ch5
                                           True,  # ch6
                                           True,  # ch7
                                           True]  # ch8
            
    def file_open(self, *filename):
        if filename == ():
            fullname = FileService.get_fullname()  # This is str filename
            if fullname == None:
                return
            self.__filename = WholeFilename(fullname)

        self.reset()        
        gc.collect()
        self.view_data_repository = ViewDataRepository()
        self.controller = ImagingController(self, self.__filename)
        self.create_model()
        
    def create_model(self):
        self.model = self.controller.create_model(self.__filename)
        self.view_data_repository.model = self.model
        
        self.view_data_repository.initialize_view_data_repository(self.ax_list)
        self.controller.current_roi_num = self.current_roi_num
        
        self.default_setting()

        print('==============================Initialized the Data Window.==============================')
        print('')
        
    def default_setting(self):
        """ write here for default switches."""
                
        self.checkbox_flag_list[0].set(False)
        self.select_ch(0)
        self.checkbox_flag_list[2].set(False)
        self.select_ch(2)
        self.radio_button_var_1.set("DFoverF")
        self.add_mod('Trace', 'DFoverF')
        
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
            self.ax_list[0].current_roi_num = self.current_roi_num
            self.view_data_repository.update('RoiView' + str(self.current_roi_num))

            
    # this method need refactoring.
    def select_ch(self, ch):
        self.ax_list[1].select_ch(ch)  # This is for flag to showing traces.
        self.ax_list[0].select_ch(ch)  # for changing images
        
        num_roi = self.view_data_repository.view_data_counter['RoiView']
        for i in range(1, num_roi+1):
            if ch == 0:  #This is for getting trace value objects. it shold be match to flags of trace_ax.
                self.controller.bind_keys('Roi' + str(i),
                                          'FullTrace' + str(i))
            else:
                self.controller.bind_keys('Roi' + str(i),
                                          'ChTrace' + str(i*2-2+ch))

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
            self.ax_list[i].draw_ax()
        self.current_roi_num -= 1
        
    def add_mod(self, data_key, mod_key):
        if mod_key == 'DFoverF':
            try:
                self.remove_mod(data_key, 'Normalize')
            except:
                print('No normalize mod.')
        elif mod_key == 'Normalize':
            try:
                self.remove_mod(data_key, 'DFoverF')
            except:
                print('No DFoverF mod.')
        self.controller.add_mod(data_key, mod_key)
        self.ax_list[1].draw_ax()
    
    def remove_mod(self, data_key, mod_key):
        if mod_key == 'F':
            try:
                self.controller.remove_mod(data_key, 'DFoverF')
            except:
                pass
            try:
                self.controller.remove_mod(data_key, 'Normalize')
            except:
                pass
                
        self.controller.remove_mod(data_key, mod_key)
        self.ax_list[1].draw_ax()
        

class TraceAx:
    def __init__(self, canvas, ax):
        self.tools = AxesTools(ax)
        self.canvas_trace = canvas
        self.ax_obj = ax
        self.current_ch = 1
        self.data_list = []  # value object list
        self.show_flag = []

        # Need refactoring for valiable number of traces. Now num of flags is only 3.
        #self.show_flag = []
        
        self.color_selection = ['black', 'red', 'blue', 'orange', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
 
    def update(self, view_data):  # TraceAx shold not hold view_data ex.RoiView because other axes also might have  the same view_data.
        self.data_list = view_data.get_data()
        self.show_data()
        
    def select_ch(self, ch):
        self.show_flag[ch] = not self.show_flag[ch]

    def show_data(self):
        line_num = len(self.ax_obj.get_lines())
        if line_num == 0:
            i = 0
            for trace_value_obj in self.data_list:  # self.data_list = TraceData Value objects
                line_2d, = trace_value_obj.show_data(self.ax_obj)  # line"," means the first element of a list (convert from list to objet). Don't remove it.
                line_2d.set_color(self.color_selection[i])
                i += 1 
        elif line_num > 0:
            i = 0
            j = 0
            for trace_flag in self.show_flag:
                if trace_flag is True:
                    time = self.data_list[i].time
                    data = self.data_list[i].data
                    i += 1
                elif trace_flag is False:
                    time = None
                    data = None
                self.ax_obj.lines[j].set_data(time,data)
                j += 1

        self.draw_ax()
        
    def draw_ax(self):
        self.ax_obj.relim()
        self.ax_obj.autoscale_view()
        self.canvas_trace.draw()
        print('')
        
    def reset(self):
        self.current_ch = 1
        self.ax_obj.clear()


class ImageAx:
    def __init__(self, canvas, ax):
        self.tools = AxesTools(ax)
        self.canvas_image = canvas
        self.ax_obj = ax
        self.current_ch = 1
        self.current_roi_num = 2  # Roi class start from  "1"
        self.data_list = []  # value object list
        self.roi_box = None  # RoiBox class
        # Need refactoring for valiable number for images.
        self.show_flag = [True, True]   # 0 = full trace, 1 = ch1 trace, 2 = ch2 trace
        
    def update(self, view_data):
        if 'Image' in view_data.name:  # for cell images
            self.data_list = view_data.get_data()  # get data from view data
            self.show_data()
        elif 'Roi' in view_data.name:  # for RoiBoxs
            self.roi_box = view_data.roi_box
            self.show_roi()
            
    def select_ch(self, ch):
        if ch == 0:
            pass
        else:
            self.show_flag[ch-1] = not self.show_flag[ch-1]
        self.show_data()
        
    def show_data(self):  # self.data_list = value obj list  Delete old images, and make new images
        image_num = len(self.ax_obj.get_images())
        if image_num == 0:
            i = 0
            for image_value_obj in self.data_list:
                image_value_obj.show_data(self.ax_obj)  # add image to self.ax_obj.images
            print(self.ax_obj.images)
                
        elif image_num >0:
            i = 0
            j = 0
            for image_flag in self.show_flag:
                if image_flag is True:
                    data = self.data_list[i].data
                    i += 1
                elif image_flag is False:
                    data = [[],[]]
                self.ax_obj.images[j].set_data(data)  # for delete privious images
                j += 1
        self.draw_ax()

    def show_roi(self): 
        rectangles = self.tools.axes_patches_check(plt.Rectangle)
        if len(rectangles) < self.current_roi_num:
            self.ax_obj.add_patch(self.roi_box.rectangle_obj)
        else:
            pass
        rectangles = self.tools.axes_patches_check(plt.Rectangle)

        self.draw_ax()
        
    def remove_rectangles(self):
        rectangles = self.tools.axes_patches_check(plt.Rectangle)
        for rectangle in rectangles:
            rectangle.remove()
        
    def draw_ax(self):
        self.ax_obj.relim()
        self.ax_obj.autoscale_view()
        self.canvas_image.draw()
        print('')
        
    def reset(self):
        self.current_ch = 1
        self.ax_obj.clear()
        

class NavigationToolbarTrace(NavigationToolbar2Tk):
    def __init__(self, canvas=None, master=None, my_color=None):
        super().__init__(canvas, master)   
        self.canvas = canvas
        self.master = master
        self.bg_color = my_color

        self['bg'] = self.bg_color
        for item in self.winfo_children():
           item['bg'] = self.bg_color

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
    
    
class AxesTools:
    def __init__(self, axes):
        self.axes = axes
    
    def axes_patches_check(self, target_class):
        target_list = []
        for target in  self.axes.patches:
            if isinstance(target, target_class):
                target_list.append(target)
        return target_list
    



if __name__ == '__main__':
        root = tk.Tk()
        root.title("SCANDATA")
        fullname = '..\\..\\220408\\20408B002.tsm'
        filename_obj = WholeFilename(fullname)
        
        view = DataWindow(root, filename_obj)
        
        root.mainloop()