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
from SCANDATA2.common_class import WholeFilename


from SCANDATA2.controller.controller_main import MainController, ViewController



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
        trace_ax2 = trace_fig.add_subplot(gridspec_trace_fig[16:20], sharex=self.ax_list[1].ax_obj)
        self.ax_list.append(TraceAx(self.canvas_trace, trace_ax2, self.controller))  # ax_list[2]
        
        #canvas_trace.get_tk_widget().pack()
        toolbar_trace = NavigationToolbarMyTool(self.canvas_trace, frame_right, self.my_color)
        toolbar_trace.children['!button2'].pack_forget()
        toolbar_trace.children['!button3'].pack_forget()
        toolbar_trace.children['!button4'].pack_forget()
        toolbar_trace.update()
        self.canvas_trace.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        trace_fig.subplots_adjust(left=0.06, right=0.97, bottom=0.05, top=0.9)
        
        #if filename_obj is not None:
        #    master.title(filename_obj.name)
        #    self.__filename = filename_obj
        #    self.contoller.file_open(self.__filename)
        
        
    def open_file(self):
        self.controller.open_file()
        
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
        

class TraceAx:
    def __init__(self, canvas, ax, controller):
        self.tools = AxesTools(ax)
        self.canvas_trace = canvas
        self.ax_obj = ax
        self.controller = controller
        self.color_selection = ['black', 'red', 'blue', 'orange', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        
        self.__current_filename_key = []  # ["20408B002.tsm"]
        self.__current_controller_key = []  # ["ROI1", "ROI2", "IMAGE_CONTROLLER2"]
        self.__current_data_key = []  # ["FULL", "CH1"]
        
        
    def set_data(self, current_controller, current_filename, current_data):
        print("Trace_ax set keys = ")
        i = 0
        roi_list = [key for key in current_controller if "ROI" in key]
        for controller_key in roi_list:
            print(f"{controller_key}, ")
            for filename_key in current_filename:
                print(f"     {filename_key} ")
                print("          ", end='')
                for data_key in current_data:
                    view_data = self.controller.get_data(filename_key, controller_key, data_key)
                    line_2d_plot_obj, =view_data.show_data(self.ax_obj)  # Show_data return (tuple). line"," means the first element of a list (convert from list to objet). Don't remove it.
                    # check the number of colors
                    if i > len(self.color_selection)-1:
                        i = 0
                    line_2d_plot_obj.set_color(self.color_selection[i])
                    print(f"{data_key} ", end='')
                    i += 1
                print()
            print()
        
    def draw_ax(self):
        [current_controller, current_filename, current_data] = self.controller.get_view_list()
        self.set_data(current_controller, current_filename, current_data)
        
        self.ax_obj.relim()
        self.ax_obj.autoscale_view()
        self.canvas_trace.draw()



class ImageAx:
    def __init__(self, canvas, ax, controller):
        self.tools = AxesTools(ax)
        self.canvas_image = canvas
        self.controller = controller
        self.ax_obj = ax
        
        self.__displayed_key = []
        self.__current_imagecontroller_ch = 1
        
        
    def add_displayed_key(self, key:str):
        if key in self.__displayed_key:
            self.__displayed_key.remove(key)
        else:
            if "IMAGE_CONTROLLER" in key.upper():
                self.__displayed_key.append(key)
        
    def update(self, view_data):
        if 'Image' in view_data.name:  # for cell images
            self.data_dict = view_data.get_data()  # get data from view data
            self.show_data()
        elif 'Roi' in view_data.name:  # for RoiBoxs
            self.roi_box = view_data.roi_box
            self.show_roi()
            
    def select_ch(self, key):
        self.flag_dict[key] = not self.flag_dict[key]
        self.show_data()
        
    def show_data(self):  # self.data_dict = {key: value obj} Delete old images, and make new images
        if self.update_pass_switch is True:
            return
        image_num = len(self.ax_obj.images)
        if image_num == 0:
            for key in self.data_dict:
                image = self.data_dict[key].show_data(self.ax_obj)  # add image to self.ax_obj.images
                self.image_dict[key] = image  # bind key and image data. the key is the same name as value data dict
                
        elif image_num > 0:
            for key in self.data_dict:
                if self.flag_dict[key] is True:
                    self.image_dict[key].set_data(self.data_dict[key].data)  # for delete privious images
                elif self.flag_dict[key] is False:
                    self.image_dict[key].set_data([[],[]])
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
            
            
            
            
            
            
            
            
            
    def set_data(self):
        self.controller.get_data()
        
        
    def draw_ax(self):
        self.ax_obj.relim()
        self.ax_obj.autoscale_view()
        self.canvas_image.draw()
        
    def reset(self):
        self.current_ch = 1
        self.ax_obj.clear()
        

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
        root = tk.Tk()
        root.title("SCANDATA")
        
        #view = MainView(root)
        view = DataWindow(root)
        
        root.mainloop()