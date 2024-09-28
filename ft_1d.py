'''
Author: CSuperlei
Date: 2024-09-28 15:28:55
LastEditTime: 2024-02-15 17:23:56
Description: Theoretical proof of the feasibility of HIFT principles
'''
import numpy as np 
from scipy.signal import get_window 
import matplotlib.pyplot as plt 
from matplotlib.pyplot import plot, savefig, figure
#plt.rcParams["font.size"] = 12
#plt.rcParams["axes.titlesize"] = 12
#plt.rcParams["axes.labelsize"] = 12
#plt.rcParams["xtick.labelsize"] = 12
#plt.rcParams["ytick.labelsize"] = 12
#plt.rcParams["legend.fontsize"] = 12

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

def stft(signal, window_size, hop_size, window_type='hann'):
    '''
    HIFT STFT result of the 1-demension signal with the triangle wave as the basis function 
    '''
    signal_length = len(signal)
    num_frames = (signal_length - window_size) // hop_size + 1
    window = get_window(window_type, window_size)
    stft_matrix = np.zeros((window_size // 2 + 1, num_frames))
    for i in range(num_frames):
        start = i * hop_size
        end = start + window_size
        frame = signal[start:end]
        window_frame = window * frame
        spectrum = fft(window_frame)
        spectrum = np.abs(spectrum)[:len(frame) // 2 + 1]
        stft_matrix[:, i] = spectrum 
    
    return num_frames, stft_matrix

def frame_time(num_frames, window_size, hop_size, fs):
    ll = np.array([i for i in range(num_frames)])
    frameTime = (ll * hop_size + window_size // 2) * 1 / fs ## 每帧中点作为时间点
    return  frameTime

def fre_scale(window_size, fs):
    freScale = [i * fs / window_size for i in range(window_size // 2 + 1)]
    return freScale


if __name__ == '__main__':
    ''' fs means sample rate, N means time domain points'''
    N = fs = 32  ## User Settings
    t = np.linspace(0, 1, fs, endpoint=False)
    signal = np.sin(2 * np.pi * 4 * t) + np.sin(2 * np.pi * 8 * t)

    k = np.arange(N)
    freq_X = k * fs / N
    freq_X = freq_X[:int(N / 2)]
    fft_res = fft(signal)
    Y = np.abs(fft_res) / N
    Y = Y[:int(N / 2)]

    window_size = 24   # User Settings
    hop_size = 4       # User Settings
    num_frames, specgram = stft(signal, window_size, hop_size)
    frameTime_X = frame_time(num_frames, window_size, hop_size, fs)
    freScale_Y = fre_scale(window_size, fs)

    ## FFT theoretical result of HIFT
    fig = plt.figure(figsize=(10, 8)) 
    ax0 = fig.add_subplot(311)
    ax0.set_xlabel('Time')
    ax0.set_ylabel('Value')
    ax0.plot(t, signal)
    ax0.set_title('Origin Signal')

    ax1 = fig.add_subplot(312)
    ax1.plot(freq_X, Y)
    ax1.set_xlabel('Frequency')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('HIFT 1D-FT Spectrum')

    # STFT theoretical result of HIFT
    ax2 = fig.add_subplot(313)  
    ax2.pcolormesh(frameTime_X, freScale_Y, specgram, shading='gouraud', cmap='viridis')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Frequency')
    ax2.set_title('HIFT 1D-STFT Sepctrum')

    plt.tight_layout()
    #print('save results')
    plt.savefig('./HIFT_FT_STFT.png')
    #savefig('../results/HIFT_FT_STFT.png')
    plt.show()
