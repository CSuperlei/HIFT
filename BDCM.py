'''
Author: CSuperlei
Date: 2025-05-25 20:36:54
LastEditTime: 2025-05-25 20:50:07
Description: 
'''
import numpy as np
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