'''
Author: CSuperlei
Date: 2024-02-15 20:39:13
LastEditTime: 2024-02-15 21:38:41
Description: 
'''
import os
import json
import numpy as np
import numba as nb
import math
import warnings
import time
warnings.filterwarnings('ignore')

class Addr_manager:
    def __init__(self, config_path) -> None:
        self.config = Config(config_path)
        self.bcapa = self.config.dict["bank_capacity"]
        self.acapa = self.config.dict["array_capacity"]
        self.bnum = self.config.dict["bank_number"]
        self.anum = self.config.dict["crossbar_number"]
        self.acol = self.config.dict["crossbar_col"]
        self.arow = self.config.dict["crossbar_row"]
        self.ccapa = self.bcapa - self.acapa * self.anum
        self.cucapa = self.config.dict["cache_unit_capacity"]
        self.byte = self.config.dict["byte_unit"]
        self.bucapa = self.config.dict["buffer_capacity"]


class Config:
    def __init__(self, config_file_path) -> None:
        self.dict = {}
        self.file = config_file_path
        self.load_config_file()
        
    def load_config_file(self):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(curr_dir, self.file)
        with open(config_path, "r") as f:
            tmp_config_dict = json.load(f)

            for config_name, config_value in tmp_config_dict.items():
                self.dict[config_name] = config_value

        return


class Module:
    def __init__(self, config_path) -> None:
        self.config = Config(config_path)
        self.addrManager = Addr_manager("addr.json")
        self.power = 0
        self.latency = 0

    def process(self, **kwargs):
        return self.work(**kwargs)
        
    def work(self, **kwargs):
        return

    def load_config(self, ):
        self.config.load_config_file()
        for k, v in self.config.dict.items():
            setattr(self, k, v)
        

class Device:
    def __init__(self, rram_datatype, rram_resistance, rram_high_resis, rram_low_resis) -> None:
        self.rram_data_type = rram_datatype
        self.rram_resistance = rram_resistance
        self.rram_high_resis = rram_high_resis
        self.rram_low_resis = rram_low_resis


class Transistor:
    def __init__(self) -> None:
        pass
        

class MemCell:
    def __init__(self, rram_datatype, rram_resistance, rram_high_resis, rram_low_resis) -> None:
        self.mem_cell = Device(rram_datatype, rram_resistance, rram_high_resis, rram_low_resis)

    def write_cell(self, target_res):
        self.mem_cell.rram_resistance = target_res
        
    def read_cell(self):
        return self.mem_cell.rram_resistance


class DAC:
    def __init__(self, dac_inputbit, dac_power, dac_latency, dac_level, dac_area) -> None:
        self.dac_inputbit = dac_inputbit
        self.dac_power = dac_power
        self.dac_latency = dac_latency
        self.dac_level = dac_level
        self.dac_area = dac_area
        self.dac_value = None
        
    def work(self, input):
        self.dac_value = input


class ADC:
    def __init__(self, adc_power, adc_latency, adc_level, adc_area, adc_outbit) -> None:  
        self.adc_power = adc_power
        self.adc_latency = adc_latency
        self.adc_level = adc_level
        self.adc_area = adc_area
        self.adc_outbit = adc_outbit
        
    def work(self, input):
        res = input
        return res


class SA:
    def __init__(self, sa_threshold, sa_power, sa_latency, sa_area) -> None:  
        self.sa_threshold = sa_threshold
        self.sa_power = sa_power
        self.sa_latency = sa_latency
        self.sa_area = sa_area
        
    def work(self, input):
        res = input

        return res
        

class CrossBar(Module):
    def __init__(self, config_path) -> None:
        super().__init__(config_path)    
        self.load_config()

        start = time.time()
        self.crossbar, self.cross_colflag, self.cross_rowflag = self._construct_crossbar()

        self.dac = self._construct_dac()
        self.adc = self._construct_adc()
        self.sa = self._construct_sa()
    
    def _construct_crossbar(self):
        crossbar = []
        crossbar_colflag = [True for _ in range(self.cross_colnum)]
        crossbar_rowflag = [True for _ in range(self.cross_rownum)]
        total_cell_num = self.cross_rownum * self.cross_colnum
        
        for _ in range(total_cell_num):
            crossbar.append(MemCell(self.rram_datatype, self.rram_resistance, self.rram_high_resis, self.rram_low_resis ))

        crossbar = np.array(crossbar).reshape((self.cross_rownum, self.cross_colnum))

        return crossbar, crossbar_colflag, crossbar_rowflag

    def _construct_dac(self):
        dac = []
        for _ in range(self.cross_rownum):
            dac.append(DAC(self.dac_inputbit, self.dac_power, self.dac_latency, self.dac_level, self.dac_area))
        
        dac = np.array(dac)
        return dac

    def _construct_adc(self):
        adc = []
        for _ in range(self.cross_colnum // self.cross_colreuse):
            adc.append(ADC(adc_power=self.adc_power, adc_latency=self.adc_latency, adc_level=self.adc_level, adc_area=self.adc_area, adc_outbit=self.adc_outbit))
        adc = np.array(adc)
        return adc

    def _construct_sa(self):
        sa = []
        for _ in range(self.cross_colnum):
            sa.append(SA(sa_threshold=self.sa_threshold, sa_power=self.sa_power, sa_latency=self.sa_latency, sa_area=self.sa_area))

        sa = np.array(sa)
        return sa
    
    def compute_area(self):
        total_area = (self.adc_area + self.dac_area + self.sa_area ) * self.area_margin
        return total_area
    
    def _compute_cycle(self, value=None):
        local_latency = math.ceil(value / self.cycle_time)
        return local_latency

    def _compute_power(self, row_index, col_index):
        row_index = np.array(row_index)
        col_index = np.array(col_index)
        open_cell = np.sum(row_index) * np.sum(col_index)
        close_cell = self.addrManager.acol * self.addrManager.arow - open_cell
        open_cell = open_cell * self.cell_open_power
        close_cell = close_cell * self.cell_close_power
        return close_cell + open_cell + self.adc_power

    def process(self, op_code, row_index=None, col_index=None, rram_resistance=None, input_cross=None):
        self.log.update_latency(self.__class__.__name__, self.config.dict["latency"])
        res =  self.work(op_code, row_index, col_index, rram_resistance, input_cross)
        self.log.update_power(self.__class__.__name__, res[2])
        return res[0], res[1]

    def work(self, op_code, row_index=None, col_index=None, rram_resistance=None, input_cross=None):
        '''
        op_code: crossbar operation
        row_index: row index including: open row number index
        col_index: column index including: open col number index
        rram_resistance: write crossbar resistance
        input_cross: input data in crossbar
        '''
        if op_code == "wt_cross":
            '''
            write crossbar
            '''
            index = -1
            local_cycle_wt = 0
            local_power_wt = 0
            for h in range(len(row_index)):
                for w in range(len(col_index)):
                    if row_index[h] == 1 and col_index[w] == 1 and self.cross_rowflag[h] and self.cross_colflag[w]:
                        index += 1
                        self.crossbar[h][w].write_cell(rram_resistance[index])
                        if rram_resistance[index] > 0.5:
                            local_cycle_wt += self.write_low_latency
                            local_power_wt + self.write_low_power
                        else:
                            local_cycle_wt += self.write_high_latency
                            local_power_wt + self.write_high_power
            
                        local_cycle_wt += self.cross_wirelatency
                        local_power_wt += self.wire_power

            return None, self._compute_cycle(local_cycle_wt), local_power_wt  

        if op_code == "reset_cross":
            for idx in range(len(row_index)):
                if row_index[idx] == 1:
                    self.cross_rowflag[idx] = True

            for idx in range(len(col_index)):
                if col_index[idx] == 1:
                    self.cross_colflag[idx] = True
 
            return None, 0, 0 

        if op_code == 'rd_cross':
            '''
            read crossbara
            '''
            local_cycle_rd = 0
            local_power_rd = 0
            for idx, r in enumerate(zip(self.cross_rowflag, row_index)):
                if r[0] and r[1] == 1: 
                    self.dac[idx].work(input_cross[idx])
                    local_cycle_rd += self.dac_latency
                    local_power_rd += self.dac_power
                else:
                    self.dac[idx].work(0)

            self.out_cross = np.zeros(self.cross_colnum)
            for i in range(self.cross_rownum):
                tmp_row = np.zeros(self.cross_colnum) 
                for j, r in enumerate(zip(self.cross_colflag, col_index)):
                    if r[0] and r[1] == 1:
                        tmp_row[j] = self.crossbar[i][j].read_cell()
                        if tmp_row[j] > 0.5:
                            local_power_rd += self.read_voltage ** 2 / self.rram_high_resis
                        else:
                            local_power_rd += self.read_voltage ** 2 / self.rram_low_resis            
                self.out_cross += self.dac[i].dac_value * tmp_row
            local_cycle_rd += self.read_latency

            if self.cross_isadc:
                res = []
                for idx, t in enumerate(range(0, self.cross_colnum, self.cross_colreuse)):
                    res.extend(self.adc[idx].work(self.out_cross[t : t + self.cross_colreuse]))
                    local_power_rd += self.adc_power
                local_cycle_rd += self.adc_latency * self.cross_colreuse
                return np.array(res), self._compute_cycle(local_cycle_rd), local_power_rd  
            else:
                res = []
                for idx in range(self.cross_colnum):
                    res.append(self.sa[idx].work(self.out_cross[idx]))
                    local_power_rd += self.sa_power
                
                local_cycle_rd += self.sa_latency
                return np.array(res), self._compute_cycle(local_cycle_rd), local_power_rd 

        return None
