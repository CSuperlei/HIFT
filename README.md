# HFIT: First-principle heterogeneous memristor-based Fourier transform


![HIFT](https://github.com/CSuperlei/HIFT/raw/main/Pic/HIFT.png)

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
* pip install tensorflow-gpu

### Digits
    cd ~
    git clone https://github.com/NVIDIA/DIGITS.git digits
    cd digits
    sudo apt-get install graphviz gunicorn
    for req in $(cat requirements.txt); do sudo pip install $req; done 
    pip install -r ~/digits/requirements.txt 
    ./digits-devserver

### pysam
* pip install pysam

## Usage
### Data
BAM file & VCF file <br/>
First provide the bam files and vcf files for program<br/>
### Generation Candidates
Run Generate_Deletion_Image.py and Generate_Non_Deletion_Image.py in the custom path <br/> 
* python Generate_Deletion_Image.py --del_length <br/>
* python Generate_Non_Deletion_Image.py --del_length <br/>

### Geerationg Images Path
Generate the path of all pictures for training the network
* python my_file_travel.py

### Using Digits training CNN
Send all the generated pictures to the network training
* Using the CNN architecture in CNN_Source.py 

### Using a trained network for calling deletion
Generating whole genome pictures
* python Whole_genome_Image.py

### Extracting deletion information from test results
* python extract_breakpoint.py

### License
* This project is covered under the MIT License.
