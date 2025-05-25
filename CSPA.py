
import numpy as np
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
