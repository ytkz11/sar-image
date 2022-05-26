Welcome to give me the stars. ![Github stars](https://img.shields.io/github/stars/ytkz11/sar-image.svg) 

:heartpulse:Thank you

## 1.How to produce 1L of data to 2L of data

Take GF3 for example.

Acquisition of calibration constants

The calibration constant is determined by using an angular reflector and an active scaler whose calibration field has known the radar cross-sectional area.
$$
K = |P^I-P_NG_{img2}|/\sigma_c        \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \      (1)
$$

where：

$P^I= I^2+Q^2 $ Corresponding to the power of active scaler or Angle reflector in SAR complex image, I and Q correspond to the real and imaginary parts of class 1A complex image respectively
$$
P_N:Echo noise power;G_{img2}：Image processing gain of noise;
sigma_c：Point target RCS;K:Calibration constant
$$
The equivalent backscattering coefficient of Gaofen-3 satellite is as follows:

1) Resolution of 1m~10m, imaging edge is better than -19dB;

2) The resolution is 25m~500m, the imaging center is better than -25dB, and the imaging edge is better than -21dB.

Therefore, ignoring the impact of noise, the above equation can be simplified as:
$$
K = P^I/\sigma_c        \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \      (2)
$$
Replace each parameter with a dB value, i.e				
$$
K_{dB} = 10log_{10}P^I-10log_{10}\sigma_c        \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \      (3)
$$

In the product metadata file, the field CalibrationConst corresponds to KdB.	

### Use of Calibration constant		

The backscattering coefficient can be calculated according to the following relationship:
$$
\sigma_{dB}^0 = 10log_{10}(P^I*(QualifyValue/32767)^2-K_{dB}        \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \      (4)
$$

In the L1A image, where
$$
P^I= I^2+Q^2
$$

I is the real part of grade 1A product, Q is the virtual part of grade 1A product, QualifyValue is the maximum value of the scene image before quantization, which can be obtained through the metadata file field.
$$
\sigma_{dB}^0 = 10log_{10}(P^I*(QualifyValue/65535)^2-K_{dB}        \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \      (5)
$$

In the L1B image, where
$$
P^I= I^2+Q^2
$$

DN is the real part of grade 1A product, I is the virtual part of grade 1A product, QualifyValue is the maximum value of the scene image before quantization, which can be obtained through the metadata file field.

The quantization formula of level 2 image is the same as that of Level L1B, as shown in Equation (5), where
$$
P^I= DN^2
$$
Note: For multi-polarization and full-polarization images, QualifyValue of each polarization image is different, so it needs to be searched under QulifyValue. Take the corresponding field of a certain landscape wave mode as an example, as shown below:

![5KwCmn.png](https://z3.ax1x.com/2021/10/13/5KwCmn.png)

For example, when quantizing HH image, the corresponding value of QulifyValue should be 32.469337.

### From grade 1A to 1B calculation formula

$$
DN = sqrt(I^2+Q^2)/32767*QualifyValue_1A/QualifyValue_1B*65535
$$

where，I: Real part of grade 1A products;

Q: Imaginary part of class 1A product;

QualifyValue_1A: Level 1A normalized peak;

DN: Range of class 1B products;

QualifyValue_1B: Normalized peak value of class 1B product, which can be obtained from the Class 1B product meta-information file or from the following calculation formula:

下计算公式得到：
$$
QualifyValue_1B = max(sqrt(I^2+Q^2)/32767*QualifyValue_1A)
$$
QualifyValue_1B is the maximum value after the amplitude of each pixel of grade 1A product.

### The conversion from 1BL to 2L

Orthophoto correction module using GDAL RPC



## 2.Pauli Decomposition



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