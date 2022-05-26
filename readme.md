Welcome to give me the stars. ![Github stars](https://img.shields.io/github/stars/ytkz11/sar-image.svg) 

:heartpulse:Thank you

## 1.How to produce 1L of data to 2L of data

Take GF3 for example.

Acquisition of calibration constants

The calibration constant is determined by using an angular reflector and an active scaler whose calibration field has known the radar cross-sectional area.

[![XEildK.png](https://s1.ax1x.com/2022/05/26/XEildK.png)](https://imgtu.com/i/XEildK)

where：

P^I= I^2+Q^2  Corresponding to the power of active scaler or Angle reflector in SAR complex image, I and Q correspond to the real and imaginary parts of class 1A complex image respectively



The equivalent backscattering coefficient of Gaofen-3 satellite is as follows:

1) Resolution of 1m~10m, imaging edge is better than -19dB;

2) The resolution is 25m~500m, the imaging center is better than -25dB, and the imaging edge is better than -21dB.

Therefore, ignoring the impact of noise, the above equation can be simplified as:

[![XEiKqx.png](https://s1.ax1x.com/2022/05/26/XEiKqx.png)](https://imgtu.com/i/XEiKqx)

Replace each parameter with a dB value, i.e

[![XEius1.png](https://s1.ax1x.com/2022/05/26/XEius1.png)](https://imgtu.com/i/XEius1)

In the product metadata file, the field CalibrationConst corresponds to KdB.	

### Use of Calibration constant		

The backscattering coefficient can be calculated according to the following relationship:

[![XEiQZ6.png](https://s1.ax1x.com/2022/05/26/XEiQZ6.png)](https://imgtu.com/i/XEiQZ6)

I is the real part of grade 1A product, Q is the virtual part of grade 1A product, QualifyValue is the maximum value of the scene image before quantization, which can be obtained through the metadata file field.

[![XEi1IO.png](https://s1.ax1x.com/2022/05/26/XEi1IO.png)](https://imgtu.com/i/XEi1IO)

DN is the real part of grade 1A product, I is the virtual part of grade 1A product, QualifyValue is the maximum value of the scene image before quantization, which can be obtained through the metadata file field.

[![XEi8iD.png](https://s1.ax1x.com/2022/05/26/XEi8iD.png)](https://imgtu.com/i/XEi8iD)For example, when quantizing HH image, the corresponding value of QulifyValue should be 32.469337.

### From grade 1A to 1B calculation formula

[![XEFxun.png](https://s1.ax1x.com/2022/05/26/XEFxun.png)](https://imgtu.com/i/XEFxun)

### The conversion from 1BL to 2L

Orthophoto correction module using GDAL RPC



## 2.Some applications



## 3.Pauli Decomposition

:blue_book:[Sample data](https://drive.google.com/file/d/1leBeDtRLFN2SBA0IwhJWe3Et-0gPTEIN/view?usp=sharing) 		

​	It mainly records the pauli decomposition of fully polarized synthetic aperture radar visualization (false color synthesis of SAR).		

​	The Pauli decomposition uses the so-called Pauli basis to represent the measured scattering matrix [S]. If we consider the conventional orthogonal linear basis (h, v), under normal circumstances, the Pauli basis consists of four 2×2 matrices, and the specific formulas are not listed here. Please search for relevant papers on Google.

​	Take Gaofen No. 3 as an example, calculate its backscattering coefficient, geometrically correct it, and then perform pauli decomposition and false-color image synthesis.



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

The data is the image taken by the QPSI sensor of China Radar Image Gaofen-3.

Description of the data used: The images used have been calculated and geometrically corrected for backscattering coefficients.

The effect of pauli decomposition is good. The advantage is that the false-color synthesized image is more in line with the human visual perception, and it is easy to extract the coastline.