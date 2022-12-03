# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 17:21:44 2022

lunelukkio@gmail.com
"""

import tkinter as tk
import inspect, pprint

class Application(tk.Frame):
  def __init__(self,master):
    super().__init__(master)
    self.pack()
    master.geometry("300x300")
    master.title("ベースウィンドウ")

    self.window = []
    self.user = []

    self.button = tk.Button(master,text="ウィンドウ作成",command=self.buttonClick,width=10)
    self.button.place(x=110, y=150)
    self.button.config(fg="black", bg="skyblue")

    print(self.window)
    print(self.user)

  def buttonClick(self):
    self.window.append(tk.Toplevel())
    self.user.append(User(self.window[len(self.window)-1],len(self.window)))
    print(self.window)
    print(self.user)

class User(tk.Frame):
  def __init__(self,master,num):
    super().__init__(master)
    self.pack()
    self.num = num
    master.geometry("300x300")
    master.title(str(self.num)+"つ目に作成されたウィンドウ")

    self.button = tk.Button(master,text="コンソール上での確認",command=self.buttonClick,width=20)
    self.button.place(x=70, y=150)
    self.button.config(fg="black", bg="pink")

    
    

  def buttonClick(self):
    print("こちらは"+str(self.num)+"つ目に作成されたウィンドウです。")

def main():
  win = tk.Tk()
  app = Application(win)
  app.mainloop()

if __name__ == '__main__':
  main()