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
import copy
import re
import matplotlib.patches as patches
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from SCANDATA.common_class import WholeFilename
from SCANDATA.controller.controller_main import ViewController
import json


class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.__controller = ViewController()
        
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
        memory_infor, maximum_memory, available_memory = self.__controller.get_memory_infor()
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
        self.data_window.append(DataWindow(self.window[len(self.window)-1], filename_obj, self.__controller))

    def open_file(self, event=None):
        filename_obj = self.__controller.open_file()
        fullname = filename_obj.fullname
        self.__filename_obj_list.append(filename_obj)
        self.window.append(tk.Toplevel())
        self.data_window.append(DataWindow(self.window[len(self.window)-1], filename_obj))
        print('Open ' + str(fullname))


class DataWindow(tk.Frame):
    def __init__(self, master=None, filename_obj=None):
        super().__init__(master)
        self.pack()
        self.__controller = ViewController(self)
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
        
        self.checkbox_flag_dict = {'Data0': tk.BooleanVar(value=False), 
                                   'Data1': tk.BooleanVar(value=True), 
                                   'Data2': tk.BooleanVar(value=False)}  # Should be the same as the default of trace flags
        ttk.Checkbutton(frame_bottom,
                        text='Full',
                        variable=self.checkbox_flag_dict['Data0'],
                        command=lambda: self.select_ch('FULL')).pack(side=tk.LEFT)
        ttk.Checkbutton(frame_bottom,
                        text='Ch 1',
                        variable=self.checkbox_flag_dict['Data1'],
                        command=lambda: self.select_ch('CH1')).pack(side=tk.LEFT)
        ttk.Checkbutton(frame_bottom,
                        text='Ch 2',
                        variable=self.checkbox_flag_dict['Data2'],
                        command=lambda: self.select_ch('CH2')).pack(side=tk.LEFT)
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
        self.ax_list.append(ImageAx(self.canvas_image, image_ax, self.__controller))  # ax_list[0]

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
                        command=self.image_update_pass).pack(side=tk.LEFT)
        
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
        self.ax_list.append(TraceAx(self.canvas_trace, trace_ax1, self.__controller))  # ax_list[1]
        
        # matplotlib elec trace axes
        trace_ax2 = trace_fig.add_subplot(gridspec_trace_fig[16:20], sharex=self.ax_list[1]._ax_obj)
        self.ax_list.append(TraceAx(self.canvas_trace, trace_ax2, self.__controller))  # ax_list[2]
        
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
        filename_obj = self.__controller.open_file(filename_obj)  # make a model and get filename obj
        controller_dict_keys = self.__controller.get_controller_infor()
        for i in range(3):
            self.ax_list[i].set_initial_controller_key(controller_dict_keys)
        self.default_view_data(controller_dict_keys)
        self.update_ax(3)  # 3 = draw whole ax
        
        # set image view doesn't update
        self.ax_list[0].change_update_switch(True)
        self.ax_list[1].change_update_switch(True)
        self.ax_list[2].change_update_switch(True)
        
    def default_view_data(self, controller_dict_keys):
        self.__controller.set_observer("ROI1", self.ax_list[1])
        self.__controller.set_observer("ROI2", self.ax_list[1])
        self.__controller.set_observer("IMAGE_CONTROLLER1", self.ax_list[0])
        self.__controller.set_observer("TRACE_CONTROLLER1", self.ax_list[2])
        
        """
        # set background roi to the mod class
        self.__controller.set_mod_val("ROI1", "BgCompMod")
        
        # set mod
        self.__controller.set_mod_key("ROI2", "BGCOMP")
        """
        # hide background ROI.
        for ax in range(2):
            self.ax_list[ax].set_active_controller_key("ROI1", False)  # to remove background roi
        # hide fluo trace from elec axis
        self.ax_list[2].set_active_controller_key("ROI1", False)
        self.ax_list[2].set_active_controller_key("ROI2", False)
        # hide images from the image axis
        self.ax_list[0].select_ch("IMAGE_CONTROLLER1", "CH0", False)  # to remove CH0 image data
        self.ax_list[0].select_ch("IMAGE_CONTROLLER1", "CH2", False)  # to remove CH2 image data
        # hide traces from the fluo trace axis
        self.ax_list[1].select_ch("ROI2", "CH0", False)  # to remove CH0 trace data
        self.ax_list[1].select_ch("ROI2", "CH2", False)  # to remove CH0 trace data
        #hide elec traces from the fluo axis
        for ch in range(1, 9):
            self.ax_list[0].select_ch("TRACE_CONTROLLER1", "ELEC" + str(ch), False)  # to remove CH0 image data
        for ch in range(1, 9):
            self.ax_list[1].select_ch("TRACE_CONTROLLER1", "ELEC" + str(ch), False)  # to remove CH0 image data
        # hide #2 ~ #8 elec traces from the elec axis
        for ch in range(2, 9):
            self.ax_list[2].select_ch("TRACE_CONTROLLER1", "ELEC" + str(ch), False)  # to remove CH0 image data
        
        # set current controller list
        self.__controller.set_operating_controller_list("ROI2")

        for i in range(3):
            self.ax_list[i].print_infor()
            
        """ about mod"""
        # Set ROI1 as background in ROI2 controller
        # send background ROI. but it done outside of the model.
        background_dict = self.__controller.get_data("ROI1")
        self.__controller.set_mod_val("ROI2", "BGCOMP", background_dict)
        # Turn on the switch of BGCOMP for ROI1.
        self.__controller.set_mod_key("ROI2", "BGCOMP")
        
    def update_ax(self, ax_num):
        if ax_num == 0:
            self.ax_list[0].update()
        elif ax_num == 1:
            self.ax_list[1].update()
        elif ax_num == 2:
            self.ax_list[2].update()
        elif ax_num == 3:
            for ax_num in range(3):
                self.ax_list[ax_num].update()

    def onclick_image(self, event):
        if event.dblclick is False:
            if event.button == 1:  # left click
                self.__controller.set_position_image_ax(event)
                # adjust for image data pixels
                x = round(event.xdata)-0.5
                y = round(event.ydata)-0.5
                self.ax_list[0].set_roibox(x, y)
                self.ax_list[0].update()
            elif event.button == 2:
                pass
            elif event.button == 3:
                # get current controller
                old_controller_list = self.__controller.get_operating_controller_list()
                # get whole ROI controller list. Violation of scorpe range.  _activePcontoller_dict should not be used from the outside of the class.
                filtered_list = [item for item in self.ax_list[1]._active_controller_dict.keys() if "ROI" in item]

                for old_controller in old_controller_list:
                    if old_controller in filtered_list:
                        index = filtered_list.index(old_controller)
                        if index < len(filtered_list) - 1:
                            next_controller =filtered_list[index + 1]
                        else:
                            next_controller =filtered_list[0]
                    else:
                        print("Not in the active controller list")
                        
                self.__controller.set_operating_controller_list(old_controller)
                self.__controller.set_operating_controller_list(next_controller)
                # Violation of scorpe range.  _activePcontoller_dict should not be used from the outside of the class.
                # Need refactoring.
                self.ax_list[1]._active_controller_dict[next_controller].update(self.ax_list[1]._active_controller_dict[old_controller])
                self.ax_list[1].set_active_controller_key(old_controller, False)
                print(f"Switch to {next_controller}")
                self.ax_list[1].update()
                self.ax_list[0].update()
        elif event.dblclick is True:
            print("Double click is for ----")
        print('')

    def select_ch(self, ch_key):
        # send flags to ax.
        operating_controller_list = self.__controller.get_operating_controller_list()
        for ax_num in range(2):
            for operating_controller_key in operating_controller_list:
                self.ax_list[ax_num].select_ch(operating_controller_key, ch_key)
        # need refactoring. Each ax need operating_controller_list???
        self.ax_list[0].select_ch("IMAGE_CONTROLLER1", ch_key)
        print('')
        # each axis window have own a dictionaly for drawing.
        
        
    def elec_ch_select(self, event):
        selected_value = self.combo_box_elec_ch.get()
        self.set_elec_ch(selected_value)
        print('')
        
    def set_elec_ch(self, ch: str):
        # reset flag
        pass

    def large_roi(self):
        self.change_roi_size([0, 0, 1, 1])

    def small_roi(self):
        self.change_roi_size([0, 0, -1, -1])

    # need refactoring. shold delete return from the roi values.
    def change_roi_size(self, val):
        new_roi = self.__controller.change_roi_size(val)
        if new_roi is not None:
            x = new_roi[0]
            y = new_roi[1]
            self.ax_list[0].set_roibox(x, y, val[2], val[3])
            self.ax_list[0].update()
        else:
            return
        
    def add_roi(self):
        print('')
        
    def delete_roi(self):
        print('')
        
    def add_mod(self, ch_key, mod_key):
        if mod_key == 'DFoverF':
            try:
                self.remove_mod(ch_key, 'Normalize')
            except:
                print('No normalize mod.')
        elif mod_key == 'Normalize':
            try:
                self.remove_mod(ch_key, 'DFoverF')
            except:
                print('No DFoverF mod.')
        self.__controller.add_mod(ch_key, mod_key)
        self.update_trace()
        self.ax_list[1].update_ax()
        print('')
        
    def image_update_pass(self):
        self.ax_list[0].change_update_switch()
        
class ViewAx(metaclass=ABCMeta):
    def __init__(self, ax, controller):
        self._tools = AxesTools(ax)
        self._ax_obj = ax
        self._controller = controller
        
        self.__user_controller_list = None  # the list for showing RoiBox including the background ROI.
        self.__operating_user_controller_list = None
        
        self.__operating_filename_list = None
        self.__operating_ch_list = None
        self._active_controller_dict = {}  # {"ROI1":{CH0:False,CH1:Ture, CH2:False}}
        self.sync_switch = False  # This switch is to show each data in each controllers.
        self.update_switch = True  # This switch is for avoiding image view update. Ture or False or empty: flip switch.
        
        try:
            os.chdir("../setting")
            with open("axis_data_setting.json", "r") as json_file:
                setting = json.load(json_file)
        except:
            os.chdir("./setting")
            with open("axis_data_setting.json", "r") as json_file:
                setting = json.load(json_file)
        self.__ch_color = setting.get("ch_color")
        self.__controller_color = setting.get("controller_color")

    @property
    def operating_user_controller_list(self):
        return self.__operating_user_controller_list
    
    @operating_user_controller_list.setter
    def operating_user_controller_list(self, user_controller_key_list):
        self.__operating_user_controller_list = user_controller_key_list
        
    @property
    def operating_filename_list(self):
        return self.__operating_filename_list
    
    @operating_filename_list.setter
    def operating_filename_list(self, filename_key_list):
        self.__operating_filename_list = filename_key_list
        
    @property
    def operating_ch_list(self):
        return self.__operating_ch_list
    
    @operating_ch_list.setter
    def operating_ch_list(self, ch_list):
        self.__operating_ch_list = ch_list

    @abstractmethod
    def set_view_data(self, active_controller_dict):
            raise NotImplementedError()
        
    # This doesn't affect to user controller in the model.
    def __set_active_ch_key(self, controller_key: str, ch_key: str, view_switch=None):
        if view_switch == True:
            self._active_controller_dict[controller_key][ch_key] = True
        elif view_switch == False:
            self._active_controller_dict[controller_key][ch_key] = False
        else:
            self._active_controller_dict[controller_key][ch_key] = not self._active_controller_dict[controller_key][ch_key]

    def select_ch(self, controller_key, ch_key, view_switch=None):
        self.__set_active_ch_key(controller_key, ch_key, view_switch)
        if self.sync_switch is True:
            for other_controller_key in self._active_controller_dict.keys():
                if ch_key in self._active_controller_dict[other_controller_key]:
                    self._active_controller_dict[other_controller_key][ch_key] = self._active_controller_dict[controller_key][ch_key]  
        self.update()

    # This doesn't affect to user controller in the model.
    def set_active_controller_key(self, controller_key: str, view_switch: bool):
        for ch_key in self._active_controller_dict[controller_key].keys():
            if view_switch == True:
                self.__set_active_ch_key(controller_key, ch_key, True)
            elif view_switch == False:
                self.__set_active_ch_key(controller_key, ch_key, False)        

    def change_update_switch(self, val=None):
        if val is True:
            self.update_switch = True
        elif val is False:
            self.update_switch = False
        else:
            self.update_switch = not self.update_switch
        
    def draw_ax(self):
        self.set_view_data(self._active_controller_dict)
        self._ax_obj.relim()
        self._ax_obj.autoscale_view()
        self.canvas.draw()
        
    def update(self):  # It is overrided by ImageAx
        if self.update_switch == True:
            self._ax_obj.cla()  # clear ax
            self.draw_ax()
    
    def print_infor(self):
        print("")
        print(f"{self.__class__.__name__} current data list = ")
        for controller_key in self._active_controller_dict.keys():
            for ch_key in self._active_controller_dict[controller_key].keys():
                if self._active_controller_dict[controller_key][ch_key] == True:
                    print(f"{controller_key} - {ch_key}")
    
    
class TraceAx(ViewAx):
    def __init__(self, canvas, ax, view_controller):
        super().__init__(ax, view_controller)
        self.canvas = canvas
        self.mode = "CH_MODE"  # or "ROI MODE" for showing sigle ch of several ROIs.
     
    def set_view_data(self):
        if self.update_switch is True:
            for controller_key in self.__operating_user_controller_list:
                #get data from current user controller
                data_dict = self._controller.get_data(controller_key)
                for ch_key in data_dict.keys():
                    data = data_dict[ch_key]
                    if type(data).__name__ == "TraceData":
                        # get a graph
                        ax_data, = data.show_data(self._ax_obj)
                        # color setting
                        if self.mode == "CH_MODE":
                            ax_data.set_color(self.__ch_color[ch_key])
                        elif self.mode == "ROI_MODE":
                            ax_data.set_color(controller_key)
        else:
            pass


class ImageAx(ViewAx):
    def __init__(self, canvas, ax, view_controller):
        super().__init__(ax, view_controller)
        self.canvas = canvas
        self._roibox_data_dict = {}
        self.mode = None  # no use
        
    # There are three dict. active_controller_dict is to switching. self._ax_data_dict is to keep ax data. controller_data_dict is from user controller.
    def set_view_data(self):
        if self.update_switch is True:
            for controller_key in self.__operating_user_controller_list:
                #get data from current user controller
                data_dict = self._controller.get_data(controller_key)
                for ch_key in data_dict.keys():
                    data = data_dict[ch_key]
                    if type(data).__name__ == "ImageData":
                        # get a graph
                        data.show_data(self._ax_obj)  # ax_data can use for image setting.
                        RoiBox(roi_num)
                        
                        
        else:
            pass
                    
                    



            self._roibox_data_dict[roi] = RoiBox(roi_num)
        for not_roi in not_roi_list:
            self._roibox_data_dict[not_roi] = None
                    
    # override            
    def update(self):
        if self.update_switch == True:
            self._ax_obj.cla()
            self.set_view_data(self._active_controller_dict)
        for roi_box in self._roibox_data_dict.values():
            if roi_box is not None:
                self._ax_obj.add_patch(roi_box.rectangle_obj)
        self.canvas.draw()   
                 
    def set_roibox(self, x, y, width=0, height=0):  # roi[x,y,width,height]
        for roi in self._controller.get_operating_controller_list():
            old_width = self._roibox_data_dict[roi].rectangle_obj.get_width()
            old_height = self._roibox_data_dict[roi].rectangle_obj.get_height()
            new_width = old_width + width
            new_height = old_height + height
            if new_width > 0 and new_height >0:
                self._roibox_data_dict[roi].set_roi([x, y, new_width, new_height])
            else:
                print("RoiBox: The ROI value is too small.")

class RoiBox():
    def __init__(self, roi_num, color):
        self.__rectangle_obj = patches.Rectangle(xy=(40, 40), 
                                                 width=1, 
                                                 height=1,
                                                 linewidth=0.7,
                                                 ec=color, 
                                                 fill=False)

    def set_roi(self, roi_val):
        x = roi_val[0]
        y = roi_val[1]
        self.__rectangle_obj.set_xy([x, y])
        width = roi_val[2]
        height = roi_val[3]
        self.__rectangle_obj.set_width(width)
        self.__rectangle_obj.set_height(height)
        
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
    

    fullname = '..\\..\\220408\\20408B002.tsm'
    filename_obj = WholeFilename(fullname)
    root = tk.Tk()
    root.title("SCANDATA")
    view = DataWindow(root, filename_obj)
    root.mainloop()
    
    print("＝＝＝to do list＝＝＝")
    print("second trace time shift ")
    print("current problem is that missmatch of trace switch and image switch. sharing view active switch is also problem. ")
    print("syc to every dict for a view. ")
    print("")