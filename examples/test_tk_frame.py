# tkinterのインポート
import tkinter as tk
import tkinter.ttk as ttk

# rootメインウィンドウの設定
root = tk.Tk()
root.title("Frame")
root.geometry("300x200")

# toolbarの設定
frame_top = tk.Frame(root, pady=5, padx=5, relief=tk.RAISED, bd=2)

button1 = tk.Button(frame_top, text='Open')
button2 = tk.Button(frame_top, text='Close')

button1.pack(side=tk.LEFT)
button2.pack(side=tk.LEFT, padx=5)

frame_top.pack(fill=tk.X)

# 左カラム
frame_left = tk.Frame(root, pady=5, padx=5, relief=tk.RAISED, bd=1, bg="white")
button1_left = tk.Button(frame_left, text="Func1", width=10)
button2_left = tk.Button(frame_left, text="Func2", width=10)

# 右カラム
frame_right = tk.Frame(root, pady=5, padx=5)
label = tk.Label(frame_right, text='This is Label.')

# ウィジェットの配置
frame_left.pack(side=tk.LEFT, fill=tk.Y)
frame_right.pack(side=tk.LEFT, fill=tk.Y)

button1_left.pack()
button2_left.pack(pady=5)

label.pack()

root.mainloop()