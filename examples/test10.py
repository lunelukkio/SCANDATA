# coding: UTF-8
import tkinter as tk
from tkinter import ttk

class CreateScreen(object):
    def createMainWindow(self):

        obj = ttk.tkinter.Tk() 

        obj.geometry('300x200')

        return obj

    def _Dialog(self, parent):
        dev_dialog = tk.Toplevel(parent)
        dev_dialog.geometry('500x400')

        _InFrame_ = ttk.Frame(
            dev_dialog,
            )

        chk_view = tk.BooleanVar()
        chk_view.set(False)

        chkbutton = ttk.Checkbutton(_InFrame_,text = 'chk',variable = chk_view)
        chkbutton.pack()
        _InFrame_.pack()
        dev_dialog.resizable(0,0)
        dev_dialog.grab_set()


if __name__ == '__main__':
    screen_obj = CreateScreen()

    MainWindow_obj = screen_obj.createMainWindow()

    screen_obj._Dialog(MainWindow_obj)
    MainWindow_obj.mainloop()

