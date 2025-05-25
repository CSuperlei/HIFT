'''
Author: CSuperlei
Date: 2025-05-25 20:41:19
LastEditTime: 2025-05-25 20:44:54
Description: 
'''

import numpy as np

def diff_data(data, cmin):
    empty = np.zeros(len(data) * 2)
    for i in range(0, len(data), 2):
        empty[i * 2]     = data[i]  
        empty[i * 2 + 1] = data[i+1]
        empty[i * 2 + 2] = cmin 
        empty[i * 2 + 3] = cmin 
    
    return empty

def BDCM(ft):
    cnt = 0
    cmin = 2
    clower = 13
    cupper = 30
    cmax = 47
    c_reality = 44

    ft_max = np.max(np.abs(ft))
    print(f'ft_max: {ft_max}')
    ft = ft / ft_max * c_reality

    quant = np.zeros((ft.shape[0] * 2))

    for i in range(ft.shape[0]):
        if ft[i] >= 0:
            if 0 <= ft[i] <= clower - cmin:
                quant[cnt] = ft[i] + cmin
                quant[cnt + 1] = cmin
            elif 0 <= ft[i] <= cmax - cupper:
                quant[cnt] = ft[i] + cupper
                quant[cnt + 1] = cupper
     
            elif cupper - clower <= ft[i] <= cmax - cmin:
                if ft[i] + clower <= cmax:
                    quant[cnt] = ft[i] + clower
                    quant[cnt + 1] = clower
                else:
                    quant[cnt] = ft[i] + cmin
                    quant[cnt + 1] = cmin
        else:
            if cmin - clower <= ft[i] <= 0:
                quant[cnt] = cmin
                quant[cnt + 1] = -ft[i] + cmin
            elif cupper - cmax <= ft[i] <= 0:
                quant[cnt] = cupper
                quant[cnt + 1] = -ft[i] + cupper
            elif cmin - cmax <= ft[i] <= clower - cupper:
                if -ft[i] + clower <= cmax:
                    quant[cnt] = clower
                    quant[cnt + 1] = -ft[i] + clower
                else:
                    quant[cnt] = cmin
                    quant[cnt + 1] = -ft[i] + cmin

        if 13 < quant[cnt] < 30:
            print('error: ', quant[cnt])
        if 13 < quant[cnt + 1] < 30:
            print('error: ', quant[cnt + 1])
        if quant[cnt] < 0 or quant[cnt + 1] < 0:
            print('error: ', quant[cnt], quant[cnt + 1])
        if quant[cnt] > 47 or quant[cnt + 1] > 47:
            print('error: ', quant[cnt], quant[cnt + 1])
        if quant[cnt] == 0 or quant[cnt + 1] == 0:
            print('error: ',ft[i], quant[cnt], quant[cnt + 1])

        cnt += 2

    return quant, c_reality, ft_max, cmin

def CSPA(signal_length=128, vo_freq_interval=200, varaince_num=20):
    freq_list = [_ for _ in range(0, signal_length * vo_freq_interval, vo_freq_interval)]

    k = signal_length
    N = signal_length * vo_freq_interval
    time = np.array([i / N for i in range(k)])
    real = []
    img = []

    scale = lambda : 0.1 
    noise = lambda : np.random.uniform(-varaince_num/100, varaince_num/100, size=len(time))

    for freq in freq_list:
        freq = freq + np.random.randint(-int(varaince_num), int(varaince_num))
        a_1 = np.cos(2 * np.pi * freq * time)            * scale() + noise()
        a_2 = np.cos(2 * np.pi * freq * time + np.pi)    * scale() + noise() 
        b_1 = np.sin(2 * np.pi * freq * time)            * scale() + noise() 
        b_2 = np.sin(2 * np.pi * freq * time + np.pi)    * scale() + noise()

        real.append(a_1)
        real.append(a_2)
        real.append(b_1)
        real.append(b_2)

        a_1 = np.sin(2 * np.pi * freq * time + np.pi)    * scale() + noise() 
        a_2 = np.sin(2 * np.pi * freq * time )           * scale() + noise() 
        b_1 = np.cos(2 * np.pi * freq * time)            * scale() + noise() 
        b_2 = np.cos(2 * np.pi * freq * time + np.pi)    * scale() + noise()

        img.append(a_1)
        img.append(a_2)
        img.append(b_1)
        img.append(b_2)
    
    real = np.array(real).T
    img = np.array(img).T

    return real, img

def HIFT_system(data):
    N = len(data)

    data_quant, c_reality, ft_max, cmin = BDCM(data)
   
    data_diff = diff_data(data_quant, cmin)

    real, img = CSPA(N)

    real_data = np.dot(real, data_diff)
    img_data = np.dot(img, data_diff)   
    real_data, img_data = np.array(real_data), np.array(img_data)

    fft_sqrt_data = np.sqrt(real_data ** 2 + img_data ** 2)
  
    return fft_sqrt_data 