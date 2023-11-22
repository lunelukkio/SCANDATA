# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 15:47:39 2023

@author: lunelukkio@gmail.com
"""

import os
import sys
import string
import shutil
import numpy as np
from scipy import optimize
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt
import ctypes
import _ctypes
import hashlib
import subprocess

class segment():
    # 数字は特記したもの以外はQian & Sejnowski (1989)からとった
    DK = 1.96e-5 # cm^2/s
    #DNa = 1.33e-5
    DNa = 6.0e-6 # cm^2/s （宮崎さん）
    PKrest = 3.64e-6 # cm/s
    PNarest = 6.07e-8 # cm/s
    #Kin0 = 140.0 # mM
    Kin0 = 140.0 # mM （宮崎さん）
    #Nain0 = 12 # mM
    Nain0 = 4.3 # mM （宮崎さん）
    #Kout = 4 # mM
    Kout = 2.5 # mM （宮崎さん）
    # Naout = 145 # mM
    Naout = 151.0 # mM （宮崎さん）
    T = 20+273.15 # K
    Cm = 2 # µF/cm^2
    R = 8.31 # J/(K mol)
    F = 96485 # C/mol
    #Vrest = -84.05425062366417
    electrodiffusion = 1
    spexp = sp.Function('exp')
    
    def __init__(self, diameter, length, rho, mfactor): # d and dz given in µm converted to cm
        self.K = self.Kin0
        self.Na = self.Nain0
        self.connect = [[], []]
        self.d = 1e-4*diameter
        self.dz = 1e-4*length
        self.rho = rho
        self.mfactor = mfactor
    
    @classmethod
    def exp(cls, x):
        # Load a shared library with float128 support (if available)
        libc = ctypes.CDLL("msvcrt.dll")

        # Use the float128 type if available
        if hasattr(libc, "__float128"):
            float128 = ctypes.c_longdouble
        else:
            # Fallback to long double if __float128 is not available
            float128 = ctypes.c_longdouble

        # Now you can use float128 as a NumPy data type
        np.float128 = np.dtype(float128)
        
        if type(x) in (float, np.float16, np.float32, np.float64, np.float128):
            return np.exp(x)
        else:
            return cls.spexp(x)
    
    @classmethod
    def get_alpha(cls):
        return 1000*cls.R*cls.T/cls.F # mV
    
    @classmethod
    def get_beta(cls):
        return 1000*cls.F/(4*cls.Cm) # mV/(mM cm)
        
    def set_connect(self, left, right):
        for s in left:
            for i0 in self.connect[0]+self.connect[1]:
                if s==i0:
                    print('Cannot connect to the same segment twice.')
                    raise ValueError()
            self.connect[0].append(s)
        for s in right:
            for i0 in self.connect[0]+self.connect[1]:
                if s==i0:
                    print('Cannot connect to the same segment twice.')
                    raise ValueError()
            self.connect[1].append(s)
        
    def V(self):
        beta = self.get_beta()
        return self.Vrest+beta*self.d*self.rho*((self.K-self.Kin0)+(self.Na-self.Nain0))
        
    def evolve(self, PK, PNa):
        alpha = self.get_alpha()
        DK, DNa, Kout, Naout, electrodiffusion = self.DK, self.DNa, self.Kout, self.Naout, self.electrodiffusion
        dK = dNa = 0
        dz = self.dz
        d = self.d
        rho = self.rho
        V = self.V()
        nK = self.K
        nNa = self.Na
        for lr in range(2):
            rl = 1-lr
            for s in self.connect[lr]:
                sigma = rho*np.pi*d**2/4/len(self.connect[lr])
                dz1 = s.dz
                dz2 = (dz+dz1)/2
                d1 = s.d
                rho1 = s.rho
                sigma1 = rho1*np.pi*d1**2/4/len(s.connect[rl])
                sigma2 = (sigma+sigma1)/2
                V1 = s.V()
                nK1 = s.K
                nNa1 = s.Na
                dphi = (V1-V)/dz2
                dK += DK*sigma2/(dz*rho*np.pi*d**2/4)*((nK1-nK)/dz2+electrodiffusion*1/alpha*(dz*sigma*nK+dz1*sigma1*nK1)/(dz*sigma+dz1*sigma1)*dphi)
                dNa += DNa*sigma2/(dz*rho*np.pi*d**2/4)*((nNa1-nNa)/dz2+electrodiffusion*1/alpha*(dz*sigma*nNa+dz1*sigma1*nNa1)/(dz*sigma+dz1*sigma1)*dphi)
        expValpha = self.exp(V/alpha)
        dK += -4*PK*self.mfactor*V/(alpha*d*rho)*(Kout-nK*expValpha)/(1-expValpha)
        dNa += -4*PNa*self.mfactor*V/(alpha*d*rho)*(Naout-nNa*expValpha)/(1-expValpha)
        return dK, dNa
    
if True:
    def getI(V):
        alpha = segment.get_alpha()
        PKrest, Kout, Kin0 = segment.PKrest, segment.Kout, segment.Kin0
        PNarest, Naout, Nain0 = segment.PNarest, segment.Naout, segment.Nain0
        expValpha = np.exp(V/alpha)
        I = -4*PKrest*V/alpha*(Kout-Kin0*expValpha)/(1-expValpha)-4*PNarest*V/alpha*(Naout-Nain0*expValpha)/(1-expValpha)
        return I
    V = np.linspace(-100, -1, 100)
    I = getI(V)
    if False:
        plt.plot(V, I)
        plt.plot(V, np.zeros_like(V))
        plt.show()
    res = optimize.root_scalar(getI, bracket=(-100, -1), x0=-50)
    print(res.root)
    segment.Vrest = res.root


def run3(tree, dt=2e-6, T=5, interleave=100, C=False,
         #tau = 1, # s (1 ms)
         tau = 4, # s （宮崎さん）
         Alpha = 4
        ):
    tp = tau/1000
    dirname = 'lib'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    
    def recursive(tree):
        listmode = False
        firstseg = None
        lastseg = None
        segments = []
        for i, node in enumerate(tree):
            if type(node)==tuple or type(node)==dict:
                if listmode:
                    raise ValueError('A tuple/dictionary cannot come after a list.')
                if type(node)==tuple:
                    if len(node)!=2 and len(node)!=3:
                        raise ValueError('A tuple must contain 2 or 3 elements.')
                    d = node[0]
                    dz = node[1]
                    rho = 1
                    PNa = None
                    if len(node)==3:
                        name = node[2]
                    else:
                        name = None
                    rho = 1
                    mfactor = 1
                elif type(node)==dict:
                    d = node['diam']
                    dz = node['length']
                    PNa = node.get('PNaM', None)
                    name = node.get('name', None)
                    rho = node.get('rho', 1)
                    mfactor = node.get('mfactor', 1)
                    unknown = set(node.keys())-set(['diam', 'length', 'PNaM', 'name', 'rho', 'mfactor'])
                    if len(unknown)>0:
                        raise ValueError('Unknown keywords: '+' '.join(list(unknown))+'.')
                segments.append((segment(diameter=d, length=dz, rho=rho, mfactor=mfactor), name, PNa))
                if lastseg is not None:
                    lastseg.set_connect([], [segments[-1][0]])
                    segments[-1][0].set_connect([lastseg], [])
                if firstseg is None:
                    firstseg = segments[-1][0]
                lastseg = segments[-1][0]
            elif type(node)==list:
                listmode = True
                head, segments1 = recursive(node)
                if lastseg is None:
                    raise ValueError('A tuple must be placed before a list.')
                lastseg.set_connect([], [head])
                head.set_connect([lastseg], [])
                segments += segments1
            else:
                raise ValueError('A tuple or list must be here.')
        return firstseg, segments
    
    _, segments = recursive(tree)
    
    names = [name for _, name, _ in segments]
    for n1 in range(len(names)):
        for n2 in range(n1):
            if names[n1] is not None and names[n2] is not None and names[n1]==names[n2]:
                raise ValueError(f'Name {names[n1]} is doubly defined.')
    
    def PNafun(t, PNaM):
        return segment.PNarest+PNaM*(np.exp(1)*t/tp)**Alpha*segment.exp(-Alpha*t/tp)

    for seg, _, _ in segments:
        for lr in range(2):
            rl = 1-lr
            for seg2 in seg.connect[lr]:
                exist = False
                for seg3 in seg2.connect[rl]:
                    if seg3==seg:
                        exist = True
                        break
                if not exist:
                    print('inconsistent', seg1.d, seg1.dz, seg2.d, seg2.dz)
                    raise ValueError()

    tv = []
    valdict = {'time': []}
    for _, name, _ in segments:
        if name is not None:
            valdict[name+'_V'] = []
            valdict[name+'_K'] = []
            valdict[name+'_Na'] = []
    
    if C:
        numerical_instability = -1
        n = len(segments)
        steps = int(T/dt)
        namedunits = 0
        t = sp.Symbol('t')
        for i, (seg, _, _) in enumerate(segments):
            seg.K = sp.Symbol(f'segK[{i}]')
            seg.Na = sp.Symbol(f'segNa[{i}]')
        com = f'''#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

int solve(double *K0, double *Na0, double *Vs, double *Ks, double *Ns)
｛
  double segK[{n}], segNa[{n}], dK[{n}], dNa[{n}];
  double t;
  long long i;
  int j, k;
  k = 0;
  for (i=0 ; i<{n} ; i++) ｛
    segK[i] = K0[i];
    segNa[i] = Na0[i];
  ｝
  for (i=0 ; i<{steps} ; i++) ｛
    t = i*{dt/1000};
'''
        for i, (seg, _, PNa) in enumerate(segments):
            PKt = segment.PKrest
            PNat = segment.PNarest if PNa is None else PNafun(t, PNa)
            dK, dNa = seg.evolve(PKt, PNat)
            com += f'''    dK[{i}] = {sp.ccode(dt/1000*dK)};
    dNa[{i}] = {sp.ccode(dt/1000*dNa)};
'''
        com += f'''    for (j=0 ; j<{n} ; j++) ｛
      segK[j] += dK[j];
      segNa[j] += dNa[j];
      if (!(isfinite(segK[j]) && isfinite(segNa[j]))) ｛
        return {numerical_instability};
      ｝
    ｝
'''
        com += f'''    if (i%{interleave}=={interleave-1}) ｛
'''
        for i, (seg, name, _) in enumerate(segments):
            if name is not None:
                namedunits += 1
                com += f'''      Vs[k] = {seg.V()};
      Ks[k] = segK[{i}];
      Ns[k] = segNa[{i}];
      k += 1;
'''
        com += '''    ｝
  ｝
  return 0;
｝
'''
        com = com.replace('｛', '{').replace('｝', '}')
        #print(com)
        fname = hashlib.sha256(com.encode()).hexdigest()
        cname = f'{dirname}/lib{fname}.c'
        libname = f'{dirname}/lib{fname}.so'
        open(cname, 'w').write(com)
        subprocess.call(['gcc', '-O2', '-L/usr/local/lib', '-lm', '-fPIC', '-shared', cname, '-o', libname])
        os.remove(cname)
        randomname = ''.join(np.random.choice(list(string.ascii_letters+string.digits), size=8, replace=True))
        libname2 = f'{dirname}/lib{fname}'+randomname+'.so'
        shutil.copy2(libname, libname2)
        mod = np.ctypeslib.load_library(libname2, '.')
        os.remove(libname2)
        mod.solve.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), # K0
                                 np.ctypeslib.ndpointer(dtype=np.float64), # Na0
                                 np.ctypeslib.ndpointer(dtype=np.float64), # Vs
                                 np.ctypeslib.ndpointer(dtype=np.float64), # Ks
                                 np.ctypeslib.ndpointer(dtype=np.float64) # Nas
        ]
        mod.solve.restype = c_int32
        K0 = np.array([segment.Kin0]*n, np.float64)
        Na0 = np.array([segment.Nain0]*n, np.float64)
        Ts = steps//interleave
        K = Ts*namedunits
        Vs = np.zeros(K, np.float64)
        Ks = np.zeros(K, np.float64)
        Nas = np.zeros(K, np.float64)
        sys.stdout.flush()
        sys.stderr.flush()
        status = mod.solve(K0, Na0, Vs, Ks, Nas)
        if status==numerical_instability:
            raise ValueError('Numerical instability.')
        Vs = Vs.reshape(Ts, namedunits)
        Ks = Ks.reshape(Ts, namedunits)
        Nas = Nas.reshape(Ts, namedunits)
        valdict['time'] = np.arange(interleave-1, steps, interleave)*dt
        k = 0;
        for _, name, _ in segments:
            if name is not None:
                valdict[name+'_V'] = Vs[:, k]
                valdict[name+'_K'] = Ks[:, k]
                valdict[name+'_Na'] = Nas[:, k]
                k += 1
    else:
        for i in range(int(T/dt)):
            t = i*dt/1000
            for seg, _, PNa in segments:
                PKt = segment.PKrest
                PNat = segment.PNarest if PNa is None else PNafun(t, PNa)
                dK, dNa = seg.evolve(PKt, PNat)
                seg.K += dt/1000*dK
                seg.Na += dt/1000*dNa
            if i%interleave==0:
                valdict['time'].append(t*1000)
                for seg, name, _ in segments:
                    if name is not None:
                        valdict[name+'_V'].append(seg.V())
                        valdict[name+'_K'].append(seg.K)
                        valdict[name+'_Na'].append(seg.Na)
    return pd.DataFrame(valdict)



if __name__ == '__main__':

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