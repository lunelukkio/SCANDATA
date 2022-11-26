# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:44:58 2022

lunelukkio@gmail.com
"""

import tkinter as tk
from tkinter import filedialog
import os


class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        # ウィンドウタイトル
        self.master.title("ウィジェット配置サンプル(packを使用)")

        self.master.geometry("500x300") 

        # メニューの作成
        self.create_menu()
        # ツールバーの作成
        self.create_tool_bar()
        # ステータスバーの作成
        self.create_status_bar()
        # サイドパネル
        self.create_side_panel()

        # 残りの領域にキャンバスを作成
        canvas = tk.Canvas(self.master, background="#008080")
        canvas.pack(expand=True,  fill=tk.BOTH)

    def create_menu(self):
        ''' メニューの作成'''
        menu_bar = tk.Menu(self)
 
        file_menu = tk.Menu(menu_bar, tearoff = tk.OFF)
        menu_bar.add_cascade(label="ファイル", menu = file_menu) 

        file_menu.add_command(label = "開く", command = self.menu_open_click, accelerator = "Ctrl+O")
        file_menu.add_separator() # セパレータ
        file_menu.add_command(label = "終了", command = self.master.destroy)
        # ショートカットの設定
        menu_bar.bind_all("<Control-o>", self.menu_open_click)

        # 親のメニューに設定
        self.master.config(menu = menu_bar)

    def menu_open_click(self, event=None):
        ''' ファイルを開く'''

        # ファイルを開くダイアログ
        filename = tk.filedialog.askopenfilename(
            initialdir = os.getcwd() # カレントディレクトリ
            )
        print(filename)

    def create_tool_bar(self):
        ''' ツールバー'''

        frame_tool_bar = tk.Frame(self.master, borderwidth = 2, relief = tk.SUNKEN)

        button1 = tk.Button(frame_tool_bar, text = "1", width = 2)
        button2 = tk.Button(frame_tool_bar, text = "2", width = 2)
        button3 = tk.Button(frame_tool_bar, text = "3", width = 2)

        button1.pack(side = tk.LEFT)
        button2.pack(side = tk.LEFT)
        button3.pack(side = tk.LEFT)

        frame_tool_bar.pack(fill = tk.X)

    def create_status_bar(self):
        '''ステータスバー'''
        frame_status_bar = tk.Frame(self.master, borderwidth = 2, relief = tk.SUNKEN)

        self.label1 = tk.Label(frame_status_bar, text = "ステータスラベル１")
        self.label2 = tk.Label(frame_status_bar, text = "ステータスラベル２")

        self.label1.pack(side = tk.LEFT)
        self.label2.pack(side = tk.RIGHT)

        frame_status_bar.pack(side = tk.BOTTOM, fill = tk.X)

    def create_side_panel(self):
        '''サイドパネル'''
        side_panel = tk.Frame(self.master, borderwidth = 2, relief = tk.SUNKEN)

        button1 = tk.Button(side_panel, text = "ボタン１", width = 15)
        button2 = tk.Button(side_panel, text = "ボタン２", width = 15)

        button1.pack()
        button2.pack()

        side_panel.pack(side = tk.RIGHT, fill = tk.Y)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()