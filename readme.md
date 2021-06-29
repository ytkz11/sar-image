## 1.Introduction

​		It mainly records the pauli decomposition of fully polarized synthetic aperture radar visualization (false color synthesis of SAR).

## 2.Pauli Decomposition

​		The Pauli decomposition uses the so-called Pauli basis to represent the measured scattering matrix [S]. If we consider the conventional orthogonal linear basis (h, v), under normal circumstances, the Pauli basis consists of four 2×2 matrices, and the specific formulas are not listed here. Please search for relevant papers on Google.

## 3.Visualization 

​		Take Gaofen No. 3 as an example, calculate its backscattering coefficient, geometrically correct it, and then perform pauli decomposition and false-color image synthesis.

### Experiment-raw data

Use arcgis to open the backscatter coefficient calculation and geometric correction data, as follows.

[![yBD7wV.jpg](https://z3.ax1x.com/2021/02/11/yBD7wV.jpg)](https://imgtu.com/i/yBD7wV)

HH image

[![yBDTe0.jpg](https://z3.ax1x.com/2021/02/11/yBDTe0.jpg)](https://imgtu.com/i/yBDTe0)

HV image

[![yBDILq.jpg](https://z3.ax1x.com/2021/02/11/yBDILq.jpg)](https://imgtu.com/i/yBDILq)

VH image

[![yBDxyR.jpg](https://z3.ax1x.com/2021/02/11/yBDxyR.jpg)](https://imgtu.com/i/yBDxyR)

VV image

### Experiment-Pauli decomposition

​		The data was decomposed by pauli, the data was resampled to 8bit, and then linearly stretched. The visualization results are as follows:

[![yBrNmq.jpg](https://z3.ax1x.com/2021/02/11/yBrNmq.jpg)](https://imgtu.com/i/yBrNmq)

Pauli decomposition false color of synthetic aperture radar



The other 2 scenes of sar image test are as follows:

![avatar](https://z3.ax1x.com/2021/03/11/6tq8q1.md.png)

[![6tq3rR.png](https://z3.ax1x.com/2021/03/11/6tq3rR.png)](https://imgtu.com/i/6tq3rR)

## 4.summary

The data is the image taken by the QPSI sensor of China Radar Image Gaofen-3.

Description of the data used: The images used have been calculated and geometrically corrected for backscattering coefficients.

The effect of pauli decomposition is good. The advantage is that the false-color synthesized image is more in line with the human visual perception, and it is easy to extract the coastline.