# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import torch
import time

# デバイスの選択 (cuda: GPU, cpu: CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 行列のサイズ
matrix_size = 10000

# ランダムな行列の生成
matrix_a = torch.rand((matrix_size, matrix_size), device=device)
matrix_b = torch.rand((matrix_size, matrix_size), device=device)

# GPUでの計算
start_time = time.time()
result_gpu = matrix_a + matrix_b
gpu_time = time.time() - start_time

# CPUにデータを移動して計算
matrix_a_cpu = matrix_a.cpu()
matrix_b_cpu = matrix_b.cpu()

start_time = time.time()
result_cpu = matrix_a_cpu + matrix_b_cpu
cpu_time = time.time() - start_time

# 結果の表示
print("GPU計算時間: {:.6f} 秒".format(gpu_time))
print("CPU計算時間: {:.6f} 秒".format(cpu_time))

# GPUとCPUでの結果が一致していることを確認
if torch.allclose(result_gpu, result_cpu.to(device)):
    print("GPUとCPUでの計算結果は一致しています。")
else:
    print("GPUとCPUでの計算結果が一致しません。")
