# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:43:13 2022

lunelukkio@gmail.com
main for view
"""
from abc import abstractmethod
import tkinter as tk
from tkinter import ttk
import os
import matplotlib.pyplot as plt

class AbstractWindow(tk.Frame):
    @abstractmethod
    def create_view():
        raise NotImplementedError

class View(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.model = None
        self.controller = None
        print('imported view')

    def start_gui(self):
        root = tk.Tk()
        root.title("SCANDATA")
        main_view = MainWindow(master=None)
        main_view.mainloop()


class MainWindow(View, AbstractWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.main_controller = 0

        
        self.master.title("Main Window")
        self.master.geometry("1000x200")



if __name__ == "__main__":
    view = View()