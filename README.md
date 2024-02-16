# HIFT: First-principle heterogeneous memristor-based Fourier transform

<div align="center">
    <img src="https://github.com/CSuperlei/HIFT/raw/main/Pic/HIFT.png" alt="HIFT">
</div>

## Introduction
HIFT is designed from first principle of Fourier transform using VO<sub>2</sub> memristor arrays and TaO<sub>x</sub> memristor arrays. HIFT features new schemes with VO<sub>2</sub> oscillator based frequency spectrum synthesize and cross-window accumulation with TaO<sub>x</sub> memristor arrays with bipolar differential conductance mapping. HIFT fully exploits the symmetry of the positive and negative thresholds of VO<sub>2</sub> memristors to generate stable oscillation frequency. This work demonstrates the potential and high efficiency of the HIFT system in realizing Fourier transformation and we are aiming to integrate the two memristors and their related circuits together into a single chip for future developments of HIFT.

![WorkFlow](https://github.com/CSuperlei/HIFT/raw/main/Pic/instruction.png)

## Requirements
  * numpy>=1.20.0
  * scipy>=1.10.0
  * torch>=1.12.1
  * torchvision>=0.14.0
  * matplotlib>=3.7.0
  * open3d>=0.17.0
  * mayavi>=4.8.0
  * scikit-learn>=0.21.3
  * pandas>=2.0.2

## Installation

### Anaconda
  bash Anaconda3-2023.09-0-Linux-x86_64.sh <br/>
### Pytorch 
   ```python
   pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu116
   ```

### Other Packages
 ```python
   pip install mayavi   
   pip install PyQt5   
   pip install matplotlib
   pip install scipy
   pip install numpy
   ...
   ```

## Usage

### HIFT theoretical verification of one-dimensional and two-dimensional Fourier transform
 * ft_1d is theoretical verification of HIFT's one-dimension Fourier transform result.  
 * ft_2d is theoretical verification of HIFT's two-dimension Fourier transform result.  
   ```python
   python ft_1d.py
   python ft_2d.py
   ```
   
### EEG Data Preprocess
* The data processing process after OpenBCI EEG acquisition
   ```python
   python eeg_preprocess.py
   ```

### HIFT ocean point cloud rendering using Maya
* We use Mayavi to render the FT results of HIFT and visualize the results
   ```python
   python mayavi.py
   ```

### 1T1R Crossbar theoretical verification model about RRAM
* We constructed a memristor behavior level model for in memory computing to verify the theoretical feasibility of HIFT. Crossbar.py contains 9 classes that can be combined to complete 1T1R array functionality as needed. These 9 categories are:
   ```python
   1. Crossbar: crossbar framework
   2. MemCell: 1T1R cell
   3. Transistor: transistor
   4. DAC:  Digital/Analog Unit
   5. ADC:  Analog/Digital Unit
   6. SA:   Sample and Hold
   7. Device: memristor
   8. Config: Configuration of 1T1R
   9. Addr_manager: attribute settings
   ```

### Crossbar Configuration
* crossbar.json is used to configure the 1T1R crossbar.

### Vanilla Net
* Vanilla Net is an extremely lightweight neural network model proposed by Chen [[1]](https://arxiv.org/abs/2305.12972). In our paper, Vanilla Net is used to recognize the HIFT Fourier transform EEG spectrum.

## License
* This project is covered under the MIT License.
