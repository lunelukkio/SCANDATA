# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 08:48:55 2024

@author: lunel
"""
# ライブラリのインポート
import imagej

# ゲートウェイを作成する
ij = imagej.init()

# 画像を読み込む
image_url = 'https://imagej.net/images/FluorescentCells.jpg'
jimage = ij.io().open(image_url)

# 配列に変換
image = ij.py.from_java(jimage)

# 画像を表示する
ij.py.show(image)