# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 13:26:35 2022

lunelukkio@gmail.com
"""

import tkinter as tk

class Model():
	def __init__(self):
		self.width=self.height=300

	def moveModel(self,canvas,id):
		canvas.move(id,5,5)

class View():
	def __init__(self,master,model):
		self.master = master
		self.model = model

		self.canvas = tk.Canvas(self.master,width=self.model.width,height=self.model.height)
		self.canvas.pack()

		self.canvas.create_polygon(10,10,10,60,50,35,tag="id1")

class Controller():
	def __init__(self,master,model,view):
		self.master = master
		self.model = model
		self.view = view

		self.master.bind("<space>",self.moveController)

	def moveController(self,event):
		self.model.moveModel(self.view.canvas,"id1")

class Application(tk.Frame):
	def __init__(self,master):
		super().__init__(master)
		self.pack()

		self.model = Model()

		master.geometry(str(self.model.width)+"x"+str(self.model.height))
		master.title("mvcTest")

		self.view = View(master,self.model)
		self.controller = Controller(master,self.model,self.view)

def main():
	win = tk.Tk()
	app = Application(master=win)
	app.mainloop()

if __name__ == "__main__":
	main()