'''
Author: CSuperlei
Date: 2024-02-15 17:37:17
LastEditTime: 2024-02-15 17:40:17
Description: Theoretical proof of the feasibility of HIFT principles
'''
import numpy as np 
from scipy.signal import get_window 
import matplotlib.pyplot as plt 

def gen_tri(signal_length, vo_fre_interval=50, flag='cos'):
    '''
    Different frequency of the triangle wave
    '''
    freq_list = np.arange(0, signal_length * vo_fre_interval, vo_fre_interval)

    time_points = signal_length * vo_fre_interval
    tri_list = list()

    for freq in freq_list:
        time = np.array([i / time_points for i in range(signal_length)])

        ## sin and cosine wave
        a = np.cos(2 * np.pi * freq * time)
        b = np.sin(2 * np.pi * freq * time)

        y = a + 1j * b
        tri_list.append(y)
    
    return time, tri_list

def fft(signal=None, vo_fre_interval=50):
    '''
    HIFT FFT result of the 1-demension signal with the triangle wave as the basis function 
    '''
    signal_length = len(signal)
    time, tri_list = gen_tri(signal_length)

    fft_res = list()
    for i in range(signal_length):
        Xk = 0 + 0j
        idx = i / (signal_length * vo_fre_interval)
        for j in range(signal_length):
            index = np.abs(time - idx).argmin()
            
            tri_value = tri_list[j][index]

            Xk += tri_value * signal[j]   
        fft_res.append(Xk)
    
    return np.array(fft_res)

def ifft(signal=None, vo_fre_interval=50):
    '''
    HIFT iFFT result of the 1-demension signal with the triangle wave as the basis function 
    '''
    signal_length = len(signal)
    time, tri_list = gen_tri(signal_length)

    fft_res = list()
    for i in range(signal_length):
        Xk = 0 + 0j
        idx = i / (signal_length * vo_fre_interval)
        for j in range(signal_length):
            index = np.abs(time - idx).argmin()
            tri_value = tri_list[j][index]
            Xk += 1 / signal_length * tri_value * signal[j]

        fft_res.append(Xk)
    
    return np.array(fft_res)

def ifft_2d(df):
    '''
    HIFT iFFT result of the 2-demension signal with the triangle wave as the basis function
    '''
    ifft_res_tmp = list()
    for i in range(len(df)):
        ifft_res_tmp.append(ifft(df[i]))
    
    ifft_res_tmp = np.array(ifft_res_tmp)
    
    ifft_res = list()
    for j in range(len(ifft_res_tmp[0])):
        ifft_res.append(ifft(ifft_res_tmp[:, j]))
    
    ifft_real = np.real(np.array(ifft_res).T)
    return ifft_real
