# HIFT: First-principle heterogeneous memristor-based Fourier transform

<div align="center">
    <img src="https://github.com/CSuperlei/HIFT/raw/main/Pic/HIFT.png" alt="HIFT">
</div>

## Introduction
Fourier transform (FT) plays an extremely important role in mathematics, physics, engineering, and many other scientific fields. It is a fundamental method to analyze the frequency characteristics of functions or signals. Whereas remarkable progress has been achieved in the past for FT system design using Von Neumann or compute-in-memory (CIM) hardware, making breakthrough improvements in FT efficiency is becoming very challenging. This is because state-of-the-art FT systems are mainly based on traditional Cooly-Tukey scheme, which naturally introduces sequential window-after-window processing schedule, separate real and imaginary computations, and/or quadratically growing memory cost with increasing FT window size N. Here we report first-principle hetero-integrated Fourier transform (HIFT) enabled by volatile and non-volatile memristors to fundamentally break these bottlenecks. We investigate negative differential resistance of volatile memristors and build highly accurate oscillators that achieve frequency spectrum up to 1.74 MHz and calibratable resolution down to 50 Hz, enabling maximum 2048-point FT and cross-window parallelism. We fabricate highly uniform non-volatile memristors with iterative write-verify for in-memory multiply-and-accumulation of oscillation waves, realizing unified real and imaginary computations and scalable memory cost.

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

### HIFT ocean point cloud rendering using Mayavi
* We use Mayavi to render the FT results of HIFT and visualize the results
   ```python
   python mayavi.py
   ```

### 1T1R Crossbar theoretical verification model
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
* Vanilla Net is an extremely lightweight neural network model proposed by Chen [[1]](https://arxiv.org/abs/2305.12972). In our manuscript, Vanilla Net is used to recognize the HIFT Fourier transform EEG spectrum.

### UHDFour Net
* UHDFour-Net embeded Fourier transform into nerual network for ultra-high-definition low-Light image enhancement [[2]](https://arxiv.org/abs/2302.11831). In our manuscript， UHDFour Net is the backbone of HIFT's LLIE in real-world application.

## License
* This project is covered under the MIT License.
