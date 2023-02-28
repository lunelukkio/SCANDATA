import tkinter as tk
class A:
    def __init__(self):
        root = tk.Tk()
        view = B(root)
        root.mainloop()

class B(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.check_var = tk.BooleanVar(value=True)
        self.check_button = tk.Checkbutton(master,text="Check", variable=self.check_var)
        self.check_button.pack()

if __name__ == '__main__':
    test = A()
