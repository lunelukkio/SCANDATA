# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 17:24:06 2022

lunelukkio@gmail.com

test for tkinter + matplotlib
https://www.simugrammer.com/python_tkinter_matplotlib_sin/
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
#ファイルのプロット処理
class c_inputData(ttk.Frame):
    def __init__(self, inputFrame):
        tk.Label(inputFrame, text = "f(t)=").pack(side=tk.LEFT)
        self.editBoxA = tk.Entry(inputFrame, width=5)
        self.editBoxA.pack(side=tk.LEFT)
        self.editBoxA.insert(tk.END, 1)
        self.trgFunc = tk.StringVar()
        self.ComboboxTrgFunc = ttk.Combobox(inputFrame, textvariable=self.trgFunc, width=3)
        self.ComboboxTrgFunc['values'] = ("sin", "cos", "tan")
        self.ComboboxTrgFunc.insert(tk.END, "sin")
        self.ComboboxTrgFunc.pack(side=tk.LEFT)
        tk.Label(inputFrame, text="(").pack(side=tk.LEFT)
        self.editBoxOmega = tk.Entry(inputFrame, width=5)
        self.editBoxOmega.pack(side=tk.LEFT)
        self.editBoxOmega.insert(tk.END, 1)
        tk.Label(inputFrame, text="t)+").pack(side=tk.LEFT)
        self.editBoxB = tk.Entry(inputFrame, width=5)
        self.editBoxB.pack(side=tk.LEFT)
        self.editBoxB.insert(tk.END, 0)
    def plot_sct(self, canvas, ax):
        A = float(self.editBoxA.get())
        B = float(self.editBoxB.get())
        omega = float(self.editBoxOmega.get())
        ax.cla() #前の描画データの削除
        x = np.arange(-5, 5, 0.01)
        trg = self.ComboboxTrgFunc.get()
        if trg == "sin":
            y = A * np.sin(omega * x) + B 
        elif trg == "cos":
            y = A * np.cos(omega * x) + B 
        else:
            y = A * np.tan(omega * x) + B
            ax.set_ylim([-30, 30])
        ax.grid()
        ax.plot(x, y) #グラフの描画
        canvas.draw() #Canvasを更新
if __name__ == "__main__":
    ### rootオブジェクト生成 ###
    root = tk.Tk()
    root.title("三角関数の描画アプリ")
    ### フレームの作成 ###
    inputFrame = ttk.Frame(root) # 入力エリア
    buttonFrame = ttk.Frame(root) # ボタンを表示するエリア
    graphFrame = ttk.Frame(root) # グラフを描画するエリア
    ### inputFrame ###
    inputData = c_inputData(inputFrame)
    inputFrame.pack()
    ### buttonFrame ###
    #Plotボタン
    ButtonWidth = 15
    UpdateButton = tk.Button(buttonFrame, text="Plot", width=ButtonWidth, \
        command = lambda:inputData.plot_sct(Canvas, ax))
    UpdateButton.grid(row = 0, column = 0)
    buttonFrame.pack()
    #グラフの初期化
    fig,ax = plt.subplots()
    Canvas = FigureCanvasTkAgg(fig, master = graphFrame) #Canvasにfigを追加
    Canvas.get_tk_widget().pack()
    graphFrame.pack()
    #描画を継続
    root.mainloop()