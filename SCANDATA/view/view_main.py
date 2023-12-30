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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from SCANDATA.common_class import WholeFilename
from SCANDATA.controller.controller_axis import TraceAxisController, ImageAxisController
from SCANDATA.controller.controller_main import MainController


class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.__main_controller = MainController()
        
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
        memory_infor, maximum_memory, available_memory = self.__main_controller.get_memory_infor()
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
        self.data_window.append(DataWindow(self.window[len(self.window)-1], filename_obj, self.__main_controller))

    def open_file(self, event=None):
        filename_obj = self.__main_controller.open_file()
        fullname = filename_obj.fullname
        self.__filename_obj_list.append(filename_obj)
        self.window.append(tk.Toplevel())
        self.data_window.append(DataWindow(self.window[len(self.window)-1], filename_obj))
        print('Open ' + str(fullname))


class DataWindow(tk.Frame):
    def __init__(self, master=None, filename_obj=None):
        super().__init__(master)
        self.pack()
        self.__main_controller = MainController(self)
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
        self.__main_controller.add_axis("IMAGE_AXIS",ImageAxisController(self.canvas_image, image_ax))  # ax_dict["ImageAxis"]

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
        self.__main_controller.add_axis("FLUO_AXIS", TraceAxisController(self.canvas_trace, trace_ax1))  # _ax_dict["FluoAxis"]
        
        # matplotlib elec trace axes
        trace_ax2 = trace_fig.add_subplot(gridspec_trace_fig[16:20], sharex=self.__main_controller._ax_dict["FluoAxis"]._ax_obj)  # sync to FluoAxis
        self.__main_controller.add_axis("ELEC_AXIS", TraceAxisController(self.canvas_trace, trace_ax2))  # _ax_dict["ElecAxis"]
        
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
        self.__main_controller.open_file(filename_obj)  # make a model and get filename obj
        self.default_view_data()
        self.__main_controller.ax_update("IMAGE_AXIS")
        self.__main_controller.ax_update("FLUO_AXIS")
        self.__main_controller.ax_update("ELEC_AXIS")
        
        # set image view doesn't update
        self.__main_controller.ax_update_switch("IMAGE_AXIS", True)
        self.__main_controller.ax_update_switch("FLUO_AXIS", True)
        self.__main_controller.ax_update_switch("ELEC_AXIS", True)
        
    def default_view_data(self):
        print("===== Start default settings. =====")
        
        self.__main_controller.set_observer("ROI0", "FLUO_AXIS")   #background for bg_comp, (controller_key, axis number)
        self.__main_controller.set_observer("ROI1", "FLUO_AXIS")
        self.__main_controller.set_observer("IMAGE_CONTROLLER0", "IMAGE_AXIS")  # base image for difference image
        self.__main_controller.set_observer("IMAGE_CONTROLLER1", "IMAGE_AXIS")  # for difference image
        self.__main_controller.set_observer("TRACE_CONTROLLER0", "ELEC_AXIS")  # no use
        self.__main_controller.set_observer("TRACE_CONTROLLER1", "ELEC_AXIS")
        
        
        
        
        
        
        
        self.__main_controller._ax_list[0].set_operating_filename_list(filename_obj.name)
        self.__main_controller._ax_list[0].set_user_controller_list("IMAGE_CONTROLLER0")  # This is for difference image
        self.__main_controller._ax_list[0].set_user_controller_list("IMAGE_CONTROLLER1")
        self.__main_controller._ax_list[0].set_operating_user_controller_list("IMAGE_CONTROLLER1")
        self.__main_controller._ax_list[0].set_operating_ch_list("CH1")

        self.__main_controller._ax_list[1].set_operating_filename_list(filename_obj.name)
        self.__main_controller._ax_list[1].set_user_controller_list("ROI0")
        self.__main_controller._ax_list[1].set_user_controller_list("ROI1")
        self.__main_controller._ax_list[1].set_operating_user_controller_list("ROI1")
        self.__main_controller._ax_list[1].set_operating_ch_list("CH1")
        
        self.__main_controller._ax_list[2].set_operating_filename_list(filename_obj.name)
        self.__main_controller._ax_list[2].set_user_controller_list("TRACE_CONTROLLER0")  # currntly no use
        self.__main_controller._ax_list[2].set_user_controller_list("TRACE_CONTROLLER1")
        self.__main_controller._ax_list[2].set_operating_user_controller_list("TRACE_CONTROLLER1")
        self.__main_controller._ax_list[2].set_operating_ch_list("ELEC0")

        """ about mod"""
        # Set ROI0 as background in ROI1 controller
        # send background ROI. but it done outside of the model.
        background_dict = self.__main_controller.get_controller_data("ROI0")
        self.__main_controller.set_mod_val("ROI1", "BGCOMP", background_dict)
        # Turn on the switch of BGCOMP for ROI1.
        self.__main_controller.set_mod_key("ROI1", "BGCOMP")
        """
        # set background roi to the mod class
        self.__main_controller.set_mod_val("ROI1", "BgCompMod")
        
        # set mod
        self.__main_controller.set_mod_key("ROI2", "BGCOMP")
        """
        print("===== End default settings. =====")
        
        self.__main_controller.ax_update("IMAGE_AXIS")
        self.__main_controller.ax_update("FLUO_AXIS")
        self.__main_controller.ax_update("ELEC_AXIS")
        self.__main_controller.ax_print_infor("IMAGE_AXIS")
        self.__main_controller.ax_print_infor("FLUO_AXIS")
        self.__main_controller.ax_print_infor("ELEC_AXIS")

    def onclick_image(self, event):
        if event.dblclick is False:
            if event.button == 1:  # left click
                x = round(event.xdata)
                y = round(event.ydata)
                # set roi value in ROI
                controller_list = self.__main_controller.get_operating_user_controller_list(1)
                for controller_key in controller_list:
                    self.__main_controller.set_controller_val(controller_key, [x, y, None, None])
                    new_roi_val_obj = self.__main_controller.get_controller_val(controller_key)
                    roi_pos = new_roi_val_obj.data
                    # adjust for image data pixels 0.5
                    roi_box_pos = roi_pos[0]-0.5, roi_pos[1]-0.5,roi_pos[2],roi_pos[3]
                    self.__main_controller.set_roibox(controller_key, roi_box_pos)
                self.__main_controller.ax_update("FLUO_AXIS")
            elif event.button == 2:
                pass
            elif event.button == 3:
                # get current controller
                old_controller_list = self.__main_controller.get_operating_controller_list()
                # get whole ROI controller list. Violation of scorpe range.  _activePcontoller_dict should not be used from the outside of the class.
                filtered_list = [item for item in self.__main_controller.ax_dict["FLUO_AXIS"]._active_controller_dict.keys() if "ROI" in item]

                for old_controller in old_controller_list:
                    if old_controller in filtered_list:
                        index = filtered_list.index(old_controller)
                        if index < len(filtered_list) - 1:
                            next_controller =filtered_list[index + 1]
                        else:
                            next_controller =filtered_list[0]
                    else:
                        print("Not in the active controller list")
                        
                self.__main_controller.set_operating_controller_list(old_controller)
                self.__main_controller.set_operating_controller_list(next_controller)
                # Violation of scorpe range.  _activePcontoller_dict should not be used from the outside of the class.
                # Need refactoring.
                self.__main_controller.ax_dict["FLUO_AXIS"]._active_controller_dict[next_controller].update(self.__main_controller._ax_dict["FLUO_AXIS"]._active_controller_dict[old_controller])
                self.__main_controller._ax_dict["FLUO_AXIS"].set_active_controller_key(old_controller, False)
                print(f"Switch to {next_controller}")
                self.update_ax(0)
                self.update_ax(1)
        elif event.dblclick is True:
            print("Double click is for ----")
        print('')
        
    def select_ch(self, ch_key):
        # send flags to ax.
        if ch_key == "FULL":
            ch_key = "CH0"
            
            need change
            
            
            
            self.__main_controller._ax_dect["IMAGE_AXIS"].set_operating_ch_list(ch_key)
            self.__main_controller._ax_dect["FLUO_AXIS"].set_operating_ch_list(ch_key)
            
            
            
            
            
            self.__main_controller.ax_update("IMAGE_AXIS")
            self.__main_controller.ax_update("FLUO_AXIS")
        print('')
        
    def elec_ch_select(self, event):
        selected_value = self.combo_box_elec_ch.get()
        self.set_elec_ch(selected_value)
        print('')
        
    def set_elec_ch(self, ch: str):
        # reset flag
        pass

    def large_roi(self):
        self.change_roi_size([None, None, 1, 1])

    def small_roi(self):
        self.change_roi_size([None, None, -1, -1])

    # need refactoring. shold delete return from the roi values.
    def change_roi_size(self, val):
        controller_list = self.__main_controller.get_operating_user_controller_list(1)
        for controller_key in controller_list:
            # set roi in user controller
            self.__main_controller.set_controller_val(controller_key, val)
            # get new roi value object
            new_roi_val_obj = self.__main_controller.get_controller_val(controller_key)
            # get roi value numpy data.
            new_roi_val = new_roi_val_obj.data  
            # adjust for image data pixels 0.5
            roi_box_pos = [new_roi_val[0]-0.5, new_roi_val[1]-0.5, new_roi_val[2], new_roi_val[3]]
            # send data to image axis
            self.__main_controller.set_roibox(controller_key, roi_box_pos)
        self.update_ax(1)
         
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
        self.__main_controller.add_mod(ch_key, mod_key)
        self.update_trace()
        self.__main_controller.ax_update("FLUO_AXIS")
        print('')
        
    def image_update_pass(self):
        self.__main_controller.ax_update_switch()
        

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
    

if __name__ == '__main__':
    

    fullname = '..\\..\\220408\\20408B002.tsm'
    filename_obj = WholeFilename(fullname)
    root = tk.Tk()
    root.title("SCANDATA")
    view = DataWindow(root, filename_obj)
    root.mainloop()
    
    print("＝＝＝to do list＝＝＝")
    print("second trace time shift ")
    print("make change roi size functions")
    print("ch を変えるとroiboxが消える")
    print("スターtp字のROIBOXが見えない")
    print("")