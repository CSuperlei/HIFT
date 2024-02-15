'''
Author: CSuperlei
Date: 2024-02-15 17:43:05
LastEditTime: 2024-02-15 20:38:33
Description:  Process the raw EEG data
'''
import numpy as np 
import scipy.io as sio  
from scipy.signal import resample

def read_raw_data(file_names):
    for ch in range(8):
        Channel = []

        data = sio.loadmat(file_names)['data']
        data = data[ch, :, 1, :, 1]
        data = np.squeeze(data)
        data = resample(data, 128)  ## 降采样
        data = np.mean(data, axis=1)
        Channel.append(data)
        Channel = np.array(Channel)
        Channel = np.mean(Channel, axis=0)
        np.save('./eeg_data_process/Channel'+str(ch)+'.npy', Channel)
