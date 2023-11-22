# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:42:37 2023

@author: lunelukkio@gmail.com
"""

PNaM = 6.07e-3/30 # cm/s
#synapse.DNa = 2.0e-6 # 勝手なパラメタ

diam = 1
length = 100
points = 200
headpoints = 2
neckpoints = 10
dt = 5e-7
#T = 100
T = 0.1
tree = [{'diam': diam, 'length': length/points, 'name': f'seg{i}', 'PNaM': PNaM} for i in range(headpoints)]
tree += [{'diam': diam/2, 'length': length/points, 'name': f'seg{i}'} for i in range(headpoints, headpoints+neckpoints)]
tree += [{'diam': diam, 'length': length/points, 'name': f'seg{i}'} for i in range(headpoints+neckpoints, points)]
df = run3(tree, dt=dt, T=T, interleave=10000, C=False)
for c in ['V', 'K', 'Na']:
    plt.clf()
    plt.plot(df['time'], df[f'seg0_{c}'], label='synapse head')
    plt.plot(df['time'], df[f'seg{headpoints-1}_{c}'], label='synapse tail')
    for dendseg in [0, 1, 2, 3, 4, points-3]:
        plt.plot(df['time'], df[f'seg{headpoints+dendseg}_{c}'], label=f'{length/points*(dendseg+0.5)} µm')
    plt.xlabel('Time/ms')
    if c=='V':
        plt.ylabel('Membrane potential/mV')
    elif c=='K':
        plt.ylabel(r'K$^{+}$ concentration/mM')
    elif c=='Na':
        plt.ylabel(r'Na$^{+}$ concentration/mM')
    plt.legend()
    plt.savefig(f'figures/fig_{c}.pdf')
    plt.show()