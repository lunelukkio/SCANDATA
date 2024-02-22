# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 17:41:14 2022

lunelukkio@gmail.com
"""

import sys
import gc
from SCANDATA.view.view_main import TkDataWindow, QtDataWindow



class Main:
    def __init__(self):
        print("============== Main ==============")
        print('          Start SCANDATA')
        print("==================================")
        gc.collect()
        
        
        view = "qt"   # or "tk"
        

        
        if view == "qt":
            try:
                import PyQt5
                #print(f"PyQt5 is installed. Version: {PyQt5.QtCore.QT_VERSION_STR}")
                scandata = PyQt5.QtWidgets.QApplication(sys.argv)
                mainWindow = QtDataWindow()
                mainWindow.show()
                # Start the Qt event loop unless the user is in an interactive prompt
                if sys.flags.interactive == 0:
                    scandata.exec_()
            except ImportError:
                try:
                    import PyQt6
                    #print(f"PyQt6 is installed. Version: {PyQt6.QtCore.QT_VERSION_STR}")
                except ImportError:
                    print("Neither PyQt5 nor PyQt6 is installed.")
                    try:
                        import tkinter as tk
                        #print("tkinter is installed.")
                        #print("Use Tkinter")
                        root = tk.Tk()
                        root.title("SCANDATA")
                        TkDataWindow(root)
                        root.mainloop()
                    except ImportError:
                        print("tkinter is not installed.")
                    
        elif view == "tk":
            import tkinter as tk
            #print("tkinter is installed.")
            #print("Use Tkinter")
            root = tk.Tk()
            root.title("SCANDATA")
            TkDataWindow(root)
            root.mainloop()
            
        else:
            print("No GUI installed......Quit")

if __name__ == '__main__':
    scandata = Main()