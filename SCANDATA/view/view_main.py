# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:43:13 2022

lunelukkio@gmail.com
main for view
"""
from abc import ABCMeta, abstractmethod
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import os
import math
import copy
import matplotlib.patches as patches
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from SCANDATA.common_class import WholeFilename
from SCANDATA.controller.controller_main import MainController, ViewController


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
        filename_obj = WholeFilename(fullname)
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
        self.controller = ViewController(self)
        self.ax_list = []  # [0] = main cell image ax (ImageAxsis class), [1] = fluoresent trace ax (TraceAx class), [2] = elec trace ax
        self.my_color = '#BCD2EE'
        
        # for data window
        master.geometry('1400x700')
        master.configure(background=self.my_color)
        master.title('None')

        #self.button_func = ButtonFunction(self)

        """ 
        Top Buttons
        """
        frame_top = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=2, bg = 'white')
        tk.Button(frame_top, text='Open',command=self.open_file).pack(side=tk.LEFT)
        tk.Button(frame_top, text='Close').pack(side=tk.LEFT, padx=5)
        frame_top.pack(fill=tk.X)
        
        """
        Bottom Buttons
        """
        frame_bottom = tk.Frame(master, pady=0, padx=0, relief=tk.RAISED, bd=0, bg = self.my_color)
        
        # for ROI control
        tk.Button(frame_bottom, text='Large ROI', command=self.large_roi, width=10).pack(side=tk.LEFT)
        tk.Button(frame_bottom, text='Small ROI', command=self.small_roi, width=10).pack(side=tk.LEFT)
        tk.Button(frame_bottom, text='Add ROI', fg="black", bg="pink", state='disable', command=self.add_roi, width=5).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_bottom, text='Delete ROI', fg="black", bg="pink", state='disable', command=self.delete_roi, width=5).pack(side=tk.LEFT)
        
        #for the ch select buttons
        style = ttk.Style()
        style.configure('TCheckbutton', background=self.my_color)
        
        self.checkbox_flag_dict = {'Data0': tk.BooleanVar(), 'Data1': tk.BooleanVar(), 'Data2': tk.BooleanVar()}  # Should be the same as the default of trace flags
        ttk.Checkbutton(frame_bottom,
                        text='Full',
                        variable=self.checkbox_flag_dict['Data0'],
                        command=lambda: self.select_ch('Data0')).pack(side=tk.LEFT)
        ttk.Checkbutton(frame_bottom,
                        text='Ch 1',
                        variable=self.checkbox_flag_dict['Data1'],
                        command=lambda: self.select_ch('Data1')).pack(side=tk.LEFT)
        ttk.Checkbutton(frame_bottom,
                        text='Ch 2',
                        variable=self.checkbox_flag_dict['Data2'],
                        command=lambda: self.select_ch('Data2')).pack(side=tk.LEFT)
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
        # check button
        self.mod_bg_comp = tk.BooleanVar()
        ttk.Checkbutton(frame_bottom,
                        text='BG Comp',
                        variable=self.mod_bg_comp,
                       command=lambda: self.add_mod('Trace', 'BgComp')).pack(side=tk.LEFT)
        
        elec_ch = ['Ch 1', 'Ch 2', 'Ch 3', 'Ch 4', 'Ch 5', 'Ch 6', 'Ch 7', 'Ch 8', ]
        self.combo_box_elec_ch = ttk.Combobox(frame_bottom, values=elec_ch, width=4)
        self.combo_box_elec_ch.current(0)
        self.combo_box_elec_ch.pack(side=tk.LEFT)
        self.combo_box_elec_ch.bind('<<ComboboxSelected>>', self.elec_ch_select)
        
        
        """
        Image Frame
        """
        # tkinter image frame
        frame_left = tk.Frame(master, pady=0, padx=0)
        frame_left.pack(side=tk.LEFT)
        # matplotlib image figure
        image_fig = Figure(figsize=(5, 5), dpi=100, facecolor=self.my_color)  #Figure
        # matplotlib image axes
        image_ax = image_fig.add_subplot(1, 1, 1)           #Axes
        image_ax.tick_params(which='both', length=0)
        image_ax.set_xticklabels([])
        image_ax.set_yticklabels([])
        
        self.canvas_image = FigureCanvasTkAgg(image_fig, frame_left)
        #canvas_image.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        self.ax_list.append(ImageAx(self.canvas_image, image_ax, self.controller))  # ax_list[0]

        # for tool bar in the image window
        self.canvas_image.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar_image = NavigationToolbarMyTool(self.canvas_image, frame_left, self.my_color)
        # delete tools
        toolbar_image.children['!button2'].pack_forget()
        toolbar_image.children['!button3'].pack_forget()
        toolbar_image.children['!button4'].pack_forget()
        toolbar_image.update()
        image_fig.subplots_adjust(left=0.03, right=0.97, bottom=0.01, top=0.97)

        
        # mouse click events
        self.canvas_image.mpl_connect('button_press_event', self.onclick_image)   
        
        # image update switch
        self.checkbox_update_pass_switch = tk.BooleanVar()
        ttk.Checkbutton(frame_left,
                        text='Pass update',
                        variable=self.checkbox_update_pass_switch,
                        command=self.update_pass_switch_function).pack(side=tk.LEFT)
        
        """ 
        Trace Frames
        """
        # tkinter trace frame
        frame_right = tk.Frame(master, pady=0, padx=0)
        frame_right.pack(side=tk.RIGHT,expand=True,fill=tkinter.BOTH)
        frame_right.pack_propagate(False)
        
        # matplotlib trace figure
        trace_fig = Figure(figsize=(5, 5), dpi=100, facecolor=self.my_color)  #Figure
        gridspec_trace_fig = trace_fig.add_gridspec(20, 1)

        self.canvas_trace = FigureCanvasTkAgg(trace_fig, frame_right)
        
        # matplotlib trace axes
        trace_ax1 = trace_fig.add_subplot(gridspec_trace_fig[0:15])
        self.ax_list.append(TraceAx(self.canvas_trace, trace_ax1, self.controller))  # ax_list[1]
        
        # matplotlib elec trace axes
        trace_ax2 = trace_fig.add_subplot(gridspec_trace_fig[16:20], sharex=self.ax_list[1]._ax_obj)
        self.ax_list.append(TraceAx(self.canvas_trace, trace_ax2, self.controller))  # ax_list[2]
        
        #canvas_trace.get_tk_widget().pack()
        toolbar_trace = NavigationToolbarMyTool(self.canvas_trace, frame_right, self.my_color)
        toolbar_trace.children['!button2'].pack_forget()
        toolbar_trace.children['!button3'].pack_forget()
        toolbar_trace.children['!button4'].pack_forget()
        toolbar_trace.update()
        self.canvas_trace.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        trace_fig.subplots_adjust(left=0.06, right=0.97, bottom=0.05, top=0.9)
        
        if filename_obj is not None:
            self.open_file(filename_obj)
        
    def open_file(self, filename_obj=None):
        controller_dict_keys = self.controller.open_file(filename_obj)
        for i in range(3):
            self.ax_list[i].set_initial_controller_key(controller_dict_keys)
        self.controller.print_model_infor()
        print(f"   !!! Open {filename_obj.name}: suceeded!!!")
        print("")
        self.default_view_data(controller_dict_keys)
        self.draw_ax(3)  # 3 = draw whole ax
        
    def default_view_data(self, controller_dict_keys):
        print("Default setting")
        print("Whole controller keys = ", end='')
        print(controller_dict_keys)
        print(self.ax_list[0]._active_controller_dict)
        self.ax_list[0].remove_specific_controller("TRACE_CONTROLLER")  # to remove ELEC_CONTROLLER from ax
        self.ax_list[0].remove_specific_controller("ROI")  # to remove ROI from ax
        self.ax_list[1].remove_specific_controller("TRACE_CONTROLLER")  # to remove ELEC_CONTROLLER from ax
        self.ax_list[1].remove_specific_controller("IMAGE_CONTROLLER")  # to remove IMAGE_CONTROLLER from ax
        self.ax_list[2].remove_specific_controller("ROI")  # to remove ROI from ax
        self.ax_list[2].remove_specific_controller("IMAGE_CONTROLLER")  # to remove IMAGE_CONTROLLER from ax
        
        self.ax_list[1].set_active_controller_key("ROI1", False)  # to remove background roi
        for filename_key in controller_dict_keys["IMAGE_CONTROLLER1"].keys():
            self.ax_list[0].set_active_data_key("IMAGE_CONTROLLER1", filename_key, "FULL")  # to remove FULL image data
            self.ax_list[0].set_active_data_key("IMAGE_CONTROLLER1", filename_key,  "CH2")  # to remove CH2 image data
        """
        self.ax_list[0].set_data_key("CH2")  # to remove FULL image data
        self.ax_list[1].set_data_key("FULL")  # to remove FULL image data
        self.ax_list[1].set_data_key("CH2")  # to remove FULL image data
        self.ax_list[2].set_data_key("ELEC2")  
        self.ax_list[2].set_data_key("ELEC3")
        self.ax_list[2].set_data_key("ELEC4")
        self.ax_list[2].set_data_key("ELEC5")
        self.ax_list[2].set_data_key("ELEC6")
        self.ax_list[2].set_data_key("ELEC7")
        self.ax_list[2].set_data_key("ELEC8")
        """
        
        for i in range(3):
            self.ax_list[i].print_infor()
        
    def draw_ax(self, ax_num):
        if ax_num == 0:
            self.ax_list[0].draw_ax()
        elif ax_num == 1:
            self.ax_list[1].draw_ax()
        elif ax_num == 2:
            self.ax_list[2].draw_ax()
        elif ax_num == 3:
            for ax_num in range(3):
                self.ax_list[ax_num].draw_ax()

    def onclick_image(self, event):
        if event.button == 1:  # left click
            self.ax_list[1].set_position(event)
            #self.ax_list[0].set_position(event)
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
        print('')

    def select_ch(self, key):
        num_roi = self.view_data_repository.view_data_counter['RoiView']
        # send flags to ax.
        self.ax_list[1].select_ch(key)  # This is for flag to showing traces.
        self.ax_list[0].select_ch(key)  # for changing images
        
        for i in range(1, num_roi+1):
            if '0' in key:
                entity_key = 'FullTrace' + str(i)
            elif '1' in key:
                entity_key = 'ChTrace' + str(i*2-1)
            elif '2' in key:
                entity_key = 'ChTrace' + str(i*2)

            # for binding trace and controller
            self.controller.bind_keys('Roi' + str(i), entity_key)
        print('')

    def elec_ch_select(self, event):
        selected_value = self.combo_box_elec_ch.get()
        self.set_elec_ch(selected_value)
        print('')
        
    def set_elec_ch(self, ch: str):
        # reset flag
        pass

    def large_roi(self):
        self.change_roi_size([0, 0, 1, 1])
        print('')

    def small_roi(self):
        self.change_roi_size([0, 0, -1, -1])
        print('')

    def change_roi_size(self, val):
        self.controller.change_roi_size(self.current_roi_num, val)
        print('')

    def add_roi(self):
        self.view_data_repository.create_roi(self.ax_list)
        print('')
        
    def delete_roi(self):
        self.view_data_repository.delete_roi(self.ax_list)
        for i in range(len(self.ax_list)):
            self.ax_list[i].draw_ax()
        self.current_roi_num -= 1
        print('')
        
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
        self.update_trace()
        self.ax_list[1].draw_ax()
        print('')
    
    def update_trace(self):
        self.controller.update_data('Roi' + str(self.current_roi_num))
        
    def update_pass_switch_function(self):
        self.ax_list[0].update_pass_switch = not self.ax_list[0].update_pass_switch
        
class ViewAx(metaclass=ABCMeta):
    def __init__(self, ax, controller):
        self._tools = AxesTools(ax)
        self._ax_obj = ax
        self._controller = controller
        self._color_selection = ['black', 'red', 'blue', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'orange']
        self._ax_data_dict = {}
        self._active_controller_dict = {}  # {"ROI1":{20501A001.tsm:{FULL:False,CH1:Ture}}}
    
    def set_initial_controller_key(self, controller_key_dict):
        self._active_controller_dict = copy.deepcopy(controller_key_dict)
        self._ax_data_dict = copy.deepcopy(controller_key_dict)
    
    def remove_specific_controller(self, specific_controller_key):
        # remove specific_controller_key from self._active_controller_dict
        filtered_list = [item for item in self._active_controller_dict.keys() if specific_controller_key in item]
        for controller_key in filtered_list:
            filenamse_key_list = self._active_controller_dict[controller_key].keys()
            for filename_key in filenamse_key_list:
                data_key_list = self._active_controller_dict[controller_key][filename_key].keys()
                for data_key in data_key_list:
                    self._active_controller_dict[controller_key][filename_key][data_key] = False
                    
        print(self.__class__.__name__)
        print(f"Removed {specific_controller_key}---> {self._active_controller_dict}")
        print("")
        
    # This doesn't affect to user controller in the model.
    def set_active_controller_key(self, controller_key: str, view_switch: bool):
        for filename_key in self._active_controller_dict[controller_key].keys():
            for data_key in self._active_controller_dict[controller_key][filename_key].keys():
                if view_switch == True:
                    self._active_controller_dict[controller_key][filename_key][data_key] = True
                elif view_switch == False:
                    self._active_controller_dict[controller_key][filename_key][data_key] = False

    def set_active_data_key(self, controller_key, filename_key, data_key):
        if self._active_controller_dict[controller_key][filename_key][data_key] is True:
            self._active_controller_dict[controller_key][filename_key][data_key] = False
        elif self._active_controller_dict[controller_key][filename_key][data_key] is False:
            self._active_controller_dict[controller_key][filename_key][data_key] = True
        
    @abstractmethod
    def set_data(self, current_controller):
            raise NotImplementedError()
        
    def draw_ax(self):
        self.set_data(self._active_controller_dict)
        self._ax_obj.relim()
        self._ax_obj.autoscale_view()
        self.canvas.draw()
    
    def print_infor(self):
        print("")
        print(f"{self.__class__.__name__} current data list = ")
        for controller_key in self._active_controller_dict.keys():
            for filename_key in self._active_controller_dict[controller_key].keys():
                for data_key in self._active_controller_dict[controller_key][filename_key].keys():
                    if self._active_controller_dict[controller_key][filename_key][data_key] == True:
                        print(f"{controller_key} - {filename_key} - {data_key}")
    
    
class TraceAx(ViewAx):
    def __init__(self, canvas, ax, controller):
        super().__init__(ax, controller)
        self.canvas = canvas
     
    def set_data(self, active_controller_dict):
        for controller_key in active_controller_dict.keys():
            for filename_key in active_controller_dict[controller_key].keys():
                for data_key in active_controller_dict[controller_key][filename_key]:
                    active_data = active_controller_dict[controller_key][filename_key][data_key]
                    ax_data = self._ax_data_dict[controller_key][filename_key][data_key]
                    if active_data is True:
                        #get data from current user controller
                        controller_data_dict = self._controller.get_data(controller_key)
                        controller_data = controller_data_dict[filename_key][data_key]
                        if type(controller_data).__name__ == "TraceData":
                            if ax_data is None or isinstance(ax_data, bool):
                                ax_data, = controller_data.show_data(self._ax_obj)
                                # color setting
                                if data_key[-1].isdigit():
                                    ax_data.set_color(self._color_selection[int(data_key[-1])])
                                else:
                                    ax_data.set_color(self._color_selection[0])
                            else:
                                data = controller_data.data
                                time = controller_data.time
                                ax_data.set_data(time,data)
                        else:
                            ax_data = None
                    elif active_controller_dict[controller_key][filename_key][data_key] is False:
                        ax_data = None
        print("")
    
    def set_position(self, event):
        #print(event.button, event.x, event.y, event.xdata, event.ydata)
        roi_controller_key = [controller_key for controller_key in self._active_controller_dict if "ROI" in controller_key]
        for controller_key in roi_controller_key:
            # Set roi center to click poist.
            # Check roi width from controller RoiVal.
            roi_x = math.floor(event.xdata)
            roi_y = math.floor(event.ydata)
            roi = [roi_x, roi_y, None, None]
            self._controller.set_position(controller_key, roi)
            self.draw_ax()


class ImageAx(ViewAx):
    def __init__(self, canvas, ax, controller):
        super().__init__(ax, controller)
        self.canvas = canvas
                
    # There are three dict. active_controller_dict is to switching. self._ax_data_dict is to keep ax data. controller_data_dict is from user controller.
    def set_data(self, active_controller_dict):
        for controller_key in active_controller_dict.keys():
            for filename_key in active_controller_dict[controller_key].keys():
                for data_key in active_controller_dict[controller_key][filename_key]:
                    active_data = active_controller_dict[controller_key][filename_key][data_key]
                    ax_data = self._ax_data_dict[controller_key][filename_key][data_key]
                    if active_data is True:
                        #get data from current user controller
                        controller_data_dict = self._controller.get_data(controller_key)
                        controller_data = controller_data_dict[filename_key][data_key]
                        if type(controller_data).__name__ == "ImageData":
                            if ax_data is None or isinstance(ax_data, bool):
                                ax_data = controller_data.show_data(self._ax_obj)
                            else:
                                data = controller_data.data
                                ax_data.set_data(data)
                        else:
                            ax_data = None
                    elif active_data is False:
                        ax_data = None
        print("")
                    

    def set_position(self, event): 
        pass

        rectangles = self._tools.axes_patches_check(plt.Rectangle)
        if len(rectangles) < self.current_roi_num:
            self._ax_obj.add_patch(self.roi_box.rectangle_obj)
        else:
            pass
        rectangles = self._tools.axes_patches_check(plt.Rectangle)

class RoiBox():
    """ class method """
    roi_num = 0
    color_selection = ['white', 'red', 'blue', 'orange', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    
    @classmethod
    def get_roi_num(cls):
        return cls.roi_num
    
    @classmethod
    def increase_roi_num(cls):
        cls.roi_num += 1
    
    @classmethod
    def reset(cls):
        cls.roi_num = 0
    
    """ instance method """
    def __init__(self, controller_key):
        self.__key = controller_key
        self.color_num = RoiBox.get_roi_num()
        self.__rectangle_obj = patches.Rectangle(xy=(40, 40), 
                                                 width=1, 
                                                 height=1,
                                                 linewidth=0.7,
                                                 ec=RoiBox.color_selection[self.color_num], 
                                                 fill=False)

    def set_roi(self):
        roi_obj = self.__model.get_data(self.__key)
        self.__rectangle_obj.set_xy([roi_obj.data[0], roi_obj.data[1]])
        self.__rectangle_obj.set_width(roi_obj.data[2])
        self.__rectangle_obj.set_height(roi_obj.data[3])
        
    def delete(self):
        raise NotImplementedError()

    @property
    def rectangle_obj(self):
        return self.__rectangle_obj


class NavigationToolbarMyTool(NavigationToolbar2Tk):
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
    
    print("")
    print("user controller,trace_axのリファクタリング。スーパークラスにまとめる")
    print("controller_mainのいらないメソッド消す")
    print("controllerにオブザーバー")
    print("")
    fullname = '..\\..\\220408\\20408B002.tsm'
    filename_obj = WholeFilename(fullname)
    root = tk.Tk()
    root.title("SCANDATA")
    view = DataWindow(root, filename_obj)
    root.mainloop()