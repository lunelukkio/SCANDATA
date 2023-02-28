import tkinter as tk
class A:
    def __init__(self):
        root = tk.Tk()
        view = B(root)
        root.mainloop()
        
class B(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.var = tk.BooleanVar(value=True)
        checkbutton = tk.Checkbutton(text="Check", variable=self.var)
        checkbutton.pack()


if __name__ == '__main__':
    test = A()
    