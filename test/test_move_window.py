# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 10:31:21 2022

lunelukkio@gmail.com
"""

import tkinter

#メイン画面をモニター右上隅に移動させるボタン
class MovePositionButton(tkinter.Button):
    def __init__(self, master):
        super().__init__(
            master,
            width=15,
            text="click",
            command=self.move_position, #クリック時に実行する関数
        )

        self.master = master

    def move_position(self):
        w = self.winfo_screenwidth()    #モニター幅取得
        w = w - 120                     #メイン画面幅分調整
        self.master.geometry("120x100+"+str(w)+"+0")    #位置設定


root = tkinter.Tk()
b = MovePositionButton(root)
b.pack()
root.mainloop()