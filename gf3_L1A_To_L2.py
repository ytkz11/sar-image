# -*- coding: utf-8 -*-
import rasterio
from osgeo import gdal
import re
import numpy as np
import os
import xml.etree.ElementTree as ET
import warnings

# Cancel the warning
warnings.filterwarnings ('ignore')

# File name pattern matching
def Get_File_Name(pathlog):
    os.chdir (pathlog)
    # XML metadata information, marking XML names
    for f_name in os.listdir (pathlog):
        if f_name.endswith ('.meta.xml'):
            print (f_name)
            xmlfile = f_name

    # Label image name
    image_fn = []
    # image_fn =glob.glob('*.tiff')
    for f_name in os.listdir (pathlog):
        if f_name.endswith ('.tiff'):
            print (f_name)
            vhlfile = f_name
            image_fn.append (f_name)
    HH = []
    HV = []
    VH = []
    VV = []
    # image_fn =glob.glob('*.tiff')
    for image_name in image_fn:
        if "HH" in image_name:
            HH = image_name
        elif 'HV' in image_name:
            HV = image_name
        elif 'VH' in image_name:
            VH = image_name
        elif 'VV' in image_name:
            VV = image_name
    return xmlfile, HH, HV, VH, VV


# Read the XML file using the ElementTree function
# Read the XML file
def Get_QualifyValue_And_Calibration(xmlfile):
    tree = ET.parse (xmlfile)
    # Gets elements in an XML file
    root = tree.getroot ()

    # The QualifyValue parameter is in 13 of the 17 child

    HH_QualifyValue = root[17][13][0].text
    HV_QualifyValue = root[17][13][1].text
    VH_QualifyValue = root[17][13][2].text
    VV_QualifyValue = root[17][13][3].text
    QualifyValue = [HH_QualifyValue, HV_QualifyValue, VH_QualifyValue, VV_QualifyValue]
    QualifyValue_new = []
    for i in QualifyValue:
        if i != 'NULL':
            i = float (i)
            QualifyValue_new.append (i)
        else:
            i = np.NAN
            QualifyValue_new.append (i)

    HH_CalibrationConst = root[18][3][0].text
    HV_CalibrationConst = root[18][3][1].text
    VH_CalibrationConst = root[18][3][2].text
    VV_CalibrationConst = root[18][3][3].text
    CalibrationConst = [HH_CalibrationConst, HV_CalibrationConst, VH_CalibrationConst, VV_CalibrationConst]
    CalibrationConst_new = []
    for i in CalibrationConst:
        if i != 'NULL':
            i = float (i)
            CalibrationConst_new.append (i)
        else:
            i = np.NAN
            CalibrationConst_new.append (i)
    return QualifyValue_new, CalibrationConst_new


# According to the image type, extraction parameters: QualifyValue, Calibration
def Confirm_The_IMG_type(file):
    QualifyValue_new, CalibrationConst_new = Get_QualifyValue_And_Calibration (xmlfile)
    if 'HH' in file:
        QualifyValue_1A = QualifyValue_new[0]
        Calibration = CalibrationConst_new[0]
    if 'HV' in file:
        QualifyValue_1A = QualifyValue_new[1]
        Calibration = CalibrationConst_new[1]
    if 'VH' in file:
        QualifyValue_1A = QualifyValue_new[2]
        Calibration = CalibrationConst_new[2]
    if 'VV' in file:
        QualifyValue_1A = QualifyValue_new[3]
        Calibration = CalibrationConst_new[3]
    return QualifyValue_1A, Calibration


def save_to_tiff(ds, img_name, outpath):
    os.chdir (outpath)
    profile = {
        'driver': 'GTiff',
        'height': ds.shape[0],
        'width': ds.shape[1],
        'count': 1,
        'dtype': ds.dtype,
        'compress': 'lzw',

    }
    # Replace L1A with L1B in the output file name
    out_filename = img_name.replace ('L1A', 'L1B')
    out_filename = os.path.join (outpath, out_filename)
    print ("L1B data save in:", out_filename)
    with rasterio.open (out_filename, 'w', **profile) as out_file:
        out_file.write (ds[:], 1)
    return out_filename


def Run_1Ato2(file, outpath):
    os.chdir (inputpath)
    img = gdal.Open (file)
    #Read into matrix
    inband1 = img.GetRasterBand (1)
    vh0 = img.ReadAsArray ()
    # Real and imaginary parts
    vh1 = np.array (vh0[0, :, :], dtype='float32')
    vh2 = np.array (vh0[1, :, :], dtype='float32')
    # I intensity formula, A amplitude formula
    I = (vh1 ** 2 + vh2 ** 2)
    A = np.sqrt (I)
    # The use of calibration constants to determine what type of image is
    QualifyValue_1A, Calibration = Confirm_The_IMG_type (file)
    print ('QualifyValue_1A=', QualifyValue_1A, '/n', 'Calibration=', Calibration)
    del vh0, vh1, vh2, I
    # np.nanmax The function finds the maximum value in the matrix
    QualifyValue_1B = np.nanmax ((A / 32767 * QualifyValue_1A))
    print ('QualifyValue_1B=', QualifyValue_1B)
    # The formula for 1A to 1B is as follows：
    DN = A / 32767 * QualifyValue_1A / QualifyValue_1B * 65535
    # 辐射定标
    k1 = DN * (QualifyValue_1B / 65535)
    k2 = k1 ** 2
    del k1, A, DN
    dB_1B = 10 * np.log (k2) / np.log (10) - Calibration
    del k2
    _1b_file = save_to_tiff(dB_1B, file, outpath)
    del dB_1B
    print("Process L1A through L1B：", file)
    _1b_file = file.replace('L1A', 'L1B')
    geometric_correction(_1b_file, outpath)



def Repeat_Run_1Ato1B(image_name, outpath):
    num_i = 1
    for file in image_name:
        print ('start：', num_i)
        if file != []:
            Run_1Ato2(file, outpath)
        else:
            print('There is no image data.')
        num_i += 1


# This is a function that reads a Gaofen-3 RPC file
def Read_Rpb (rpbfile):
    with open(rpbfile, 'r') as f:
        buff = f.read()

        # Name the url of the reference：http://geotiff.maptools.org/rpc_prop.html
        ERR_BIAS1 = 'errBias'  # Error - deviation. RMS error for all points in the image (in m/horizontal axis) (-1.0, if unknown)
        ERR_BIAS2 = ';'

        ERR_RAND1 = 'errRand'  # Error - random. RMS random error in meters for each horizontal axis of each point in the image (-1.0 if unknown)
        ERR_RAND2 = ';'

        LINE_OFF1 = 'lineOffset'
        LINE_OFF2 = ';'

        SAMP_OFF1 = 'sampOffset'
        SAMP_OFF2 = ';'

        LAT_OFF1 = 'latOffset'
        LAT_OFF2 = ';'

        LONG_OFF1 = 'longOffset'
        LONG_OFF2 = ';'

        HEIGHT_OFF1 = 'heightOffset'
        HEIGHT_OFF2 = ';'

        LINE_SCALE1 = 'lineScale'
        LINE_SCALE2 = ';'

        SAMP_SCALE1 = 'sampScale'
        SAMP_SCALE2 = ';'

        LAT_SCALE1 = 'latScale'
        LAT_SCALE2 = ';'

        LONG_SCALE1 = 'longScale'
        LONG_SCALE2 = ';'

        HEIGHT_SCALE1 = 'heightScale'
        HEIGHT_SCALE2 = ';'

        LINE_NUM_COEFF1 = 'lineNumCoef'
        LINE_NUM_COEFF2 = ';'

        LINE_DEN_COEFF1 = 'lineDenCoef'
        LINE_DEN_COEFF2 = ';'

        SAMP_NUM_COEFF1 = 'sampNumCoef'
        SAMP_NUM_COEFF2 = ';'

        SAMP_DEN_COEFF1 = 'sampDenCoef'
        SAMP_DEN_COEFF2 = ';'

        # Regularized extraction values
        pat_ERR_BIAS = re.compile(ERR_BIAS1 + '(.*?)' + ERR_BIAS2, re.S)
        result_ERR_BIAS = pat_ERR_BIAS.findall(buff)
        ERR_BIAS = result_ERR_BIAS[0]
        ERR_BIAS = ERR_BIAS.replace(" ", "")

        pat_ERR_RAND = re.compile(ERR_RAND1 + '(.*?)' + ERR_RAND2, re.S)
        result_ERR_RAND = pat_ERR_RAND.findall(buff)
        ERR_RAND = result_ERR_RAND[0]
        ERR_RAND = ERR_RAND.replace(" ", "")

        pat_LINE_OFF = re.compile(LINE_OFF1 + '(.*?)' + LINE_OFF2, re.S)
        result_LINE_OFF = pat_LINE_OFF.findall(buff)
        LINE_OFF = result_LINE_OFF[0]
        LINE_OFF = LINE_OFF.replace(" ", "")

        pat_SAMP_OFF = re.compile(SAMP_OFF1 + '(.*?)' + SAMP_OFF2, re.S)
        result_SAMP_OFF = pat_SAMP_OFF.findall(buff)
        SAMP_OFF = result_SAMP_OFF[0]
        SAMP_OFF = SAMP_OFF.replace(" ", "")

        pat_LAT_OFF = re.compile(LAT_OFF1 + '(.*?)' + LAT_OFF2, re.S)
        result_LAT_OFF = pat_LAT_OFF.findall(buff)
        LAT_OFF = result_LAT_OFF[0]
        LAT_OFF = LAT_OFF.replace(" ", "")

        pat_LONG_OFF = re.compile(LONG_OFF1 + '(.*?)' + LONG_OFF2, re.S)
        result_LONG_OFF = pat_LONG_OFF.findall(buff)
        LONG_OFF = result_LONG_OFF[0]
        LONG_OFF = LONG_OFF.replace(" ", "")

        pat_HEIGHT_OFF = re.compile(HEIGHT_OFF1 + '(.*?)' + HEIGHT_OFF2, re.S)
        result_HEIGHT_OFF = pat_HEIGHT_OFF.findall(buff)
        HEIGHT_OFF = result_HEIGHT_OFF[0]
        HEIGHT_OFF = HEIGHT_OFF.replace(" ", "")

        pat_LINE_SCALE = re.compile(LINE_SCALE1 + '(.*?)' + LINE_SCALE2, re.S)
        result_LINE_SCALE = pat_LINE_SCALE.findall(buff)
        LINE_SCALE = result_LINE_SCALE[0]
        LINE_SCALE = LINE_SCALE.replace(" ", "")

        pat_SAMP_SCALE = re.compile(SAMP_SCALE1 + '(.*?)' + SAMP_SCALE2, re.S)
        result_SAMP_SCALE = pat_SAMP_SCALE.findall(buff)
        SAMP_SCALE = result_SAMP_SCALE[0]
        SAMP_SCALE = SAMP_SCALE.replace(" ", "")

        pat_LAT_SCALE = re.compile(LAT_SCALE1 + '(.*?)' + LAT_SCALE2, re.S)
        result_LAT_SCALE = pat_LAT_SCALE.findall(buff)
        LAT_SCALE = result_LAT_SCALE[0]
        LAT_SCALE = LAT_SCALE.replace(" ", "")

        pat_LONG_SCALE = re.compile(LONG_SCALE1 + '(.*?)' + LONG_SCALE2, re.S)
        result_LONG_SCALE = pat_LONG_SCALE.findall(buff)
        LONG_SCALE = result_LONG_SCALE[0]
        LONG_SCALE = LONG_SCALE.replace(" ", "")

        pat_HEIGHT_SCALE = re.compile(HEIGHT_SCALE1 + '(.*?)' + HEIGHT_SCALE2, re.S)
        result_HEIGHT_SCALE = pat_HEIGHT_SCALE.findall(buff)
        HEIGHT_SCALE = result_HEIGHT_SCALE[0]
        HEIGHT_SCALE = HEIGHT_SCALE.replace(" ", "")

        pat_LINE_NUM_COEFF = re.compile(LINE_NUM_COEFF1 + '(.*?)' + LINE_NUM_COEFF2, re.S)
        result_LINE_NUM_COEFF = pat_LINE_NUM_COEFF.findall(buff)
        LINE_NUM_COEFF = result_LINE_NUM_COEFF[0]
        LINE_NUM_COEFF3 = LINE_NUM_COEFF
        # LINE_NUM_COEFF3 = LINE_NUM_COEFF3.strip('()')
        # LINE_NUM_COEFF3 = LINE_NUM_COEFF3.strip('()')
        LINE_NUM_COEFF3 = LINE_NUM_COEFF3.replace(" ", "")
        LINE_NUM_COEFF3 = LINE_NUM_COEFF3.replace('(', '')
        LINE_NUM_COEFF3 = LINE_NUM_COEFF3.replace(')', '')
        LINE_NUM_COEFF3 = LINE_NUM_COEFF3.replace('\n', '')
        LINE_NUM_COEFF3 = LINE_NUM_COEFF3.replace('\t', '')
        LINE_NUM_COEFF3 = LINE_NUM_COEFF3.replace(',', ' ')

        pat_LINE_DEN_COEFF = re.compile(LINE_DEN_COEFF1 + '(.*?)' + LINE_DEN_COEFF2, re.S)
        result_LINE_DEN_COEFF = pat_LINE_DEN_COEFF.findall(buff)
        LINE_DEN_COEFF = result_LINE_DEN_COEFF[0]
        LINE_DEN_COEFF3 = LINE_DEN_COEFF
        LINE_DEN_COEFF3 = LINE_DEN_COEFF3.replace(" ", "")
        LINE_DEN_COEFF3 = LINE_DEN_COEFF3.replace('(', '')
        LINE_DEN_COEFF3 = LINE_DEN_COEFF3.replace(')', '')
        LINE_DEN_COEFF3 = LINE_DEN_COEFF3.replace('\n', '')
        LINE_DEN_COEFF3 = LINE_DEN_COEFF3.replace('\t', '')
        LINE_DEN_COEFF3 = LINE_DEN_COEFF3.replace(',', ' ')

        pat_SAMP_NUM_COEFF = re.compile(SAMP_NUM_COEFF1 + '(.*?)' + SAMP_NUM_COEFF2, re.S)
        result_SAMP_NUM_COEFF = pat_SAMP_NUM_COEFF.findall(buff)
        SAMP_NUM_COEFF = result_SAMP_NUM_COEFF[0]
        SAMP_NUM_COEFF3 = SAMP_NUM_COEFF
        SAMP_NUM_COEFF3 = SAMP_NUM_COEFF3.replace(" ", "")

        SAMP_NUM_COEFF3 = SAMP_NUM_COEFF3.replace('(', '')
        SAMP_NUM_COEFF3 = SAMP_NUM_COEFF3.replace(')', '')
        SAMP_NUM_COEFF3 = SAMP_NUM_COEFF3.replace('\n', '')
        SAMP_NUM_COEFF3 = SAMP_NUM_COEFF3.replace('\t', '')
        SAMP_NUM_COEFF3 = SAMP_NUM_COEFF3.replace(',', ' ')

        pat_SAMP_DEN_COEFF = re.compile(SAMP_DEN_COEFF1 + '(.*?)' + SAMP_DEN_COEFF2, re.S)
        result_SAMP_DEN_COEFF = pat_SAMP_DEN_COEFF.findall(buff)
        SAMP_DEN_COEFF = result_SAMP_DEN_COEFF[0]
        SAMP_DEN_COEFF3 = SAMP_DEN_COEFF
        SAMP_DEN_COEFF3 = SAMP_DEN_COEFF3.replace(" ", "")

        SAMP_DEN_COEFF3 = SAMP_DEN_COEFF3.replace('(', '')
        SAMP_DEN_COEFF3 = SAMP_DEN_COEFF3.replace(')', '')
        SAMP_DEN_COEFF3 = SAMP_DEN_COEFF3.replace('\n', '')
        SAMP_DEN_COEFF3 = SAMP_DEN_COEFF3.replace('\t', '')
        SAMP_DEN_COEFF3 = SAMP_DEN_COEFF3.replace(',', ' ')

    rpc = ['ERR_BIAS'+ERR_BIAS, 'ERR_RAND'+ERR_RAND, 'LINE_OFF'+LINE_OFF,
           'SAMP_OFF'+SAMP_OFF, 'LAT_OFF'+LAT_OFF, 'LONG_OFF'+LONG_OFF,
           'HEIGHT_OFF'+HEIGHT_OFF, 'LINE_SCALE'+LINE_SCALE, 'SAMP_SCALE'+SAMP_SCALE,
           'LAT_SCALE'+LAT_SCALE, 'LONG_SCALE'+LONG_SCALE, 'HEIGHT_SCALE'+HEIGHT_SCALE,
           'LINE_NUM_COEFF'+LINE_NUM_COEFF3,'LINE_DEN_COEFF'+LINE_DEN_COEFF3,
           'SAMP_NUM_COEFF'+SAMP_NUM_COEFF3,'SAMP_DEN_COEFF'+SAMP_DEN_COEFF3]
    #rpc = ['ERR BIAS=' + ERR_BIAS, 'ERR RAND=' + ERR_RAND, 'LINE OFF=' + LINE_OFF, 'SAMP OFF=' + SAMP_OFF,'LAT OFF=' + LAT_OFF, 'LONG OFF=' + LONG_OFF, 'HEIGHT OFF=' + HEIGHT_OFF, 'LINE SCALE=' + LINE_SCALE,'SAMP SCALE=' + SAMP_SCALE, 'LAT SCALE=' + LAT_SCALE, 'LONG SCALE=' + LONG_SCALE,'HEIGHT SCALE=' + HEIGHT_SCALE, 'LINE NUM COEFF=' + LINE_NUM_COEFF3, 'LINE DEN COEFF=' + LINE_DEN_COEFF3,'SAMP NUM COEFF=' + SAMP_NUM_COEFF3, 'SAMP DEN COEFF=' + SAMP_DEN_COEFF3]
    return rpc
# Gets the RPC file name
def Get_Rpc_file(pathlog):
    os.chdir (pathlog)
    rpc_fn=[]
    # Searching for RPC files
    for f_name in os.listdir (pathlog):
        if f_name.endswith ('.rpc'):
            rpbfile = f_name
            rpc_fn.append (rpbfile)
        elif f_name.endswith ('.rpb'):
            rpbfile = f_name
            rpc_fn.append (rpbfile)
    # Matches the RPC file of the sensor
    HH_rpc = []
    HV_rpc = []
    VH_rpc = []
    VV_rpc = []
    for rpc_name in rpc_fn:
        if "HH" in rpc_name:
            HH_rpc = rpc_name
        if 'HV' in rpc_name:
            HV_rpc = rpc_name
        if 'VH' in rpc_name:
            VH_rpc = rpc_name
        if 'VV' in rpc_name:
            VV_rpc = rpc_name
    rpcfile_collection = [HH_rpc, HV_rpc, VH_rpc, VV_rpc]
    return rpcfile_collection

# According to the type of image, extract parameter: RPC file name
def Confirm_The_rpc_type(file):
    file = os.path.basename(file)
    rpcfile_collection = Get_Rpc_file(inputpath)
    if 'HH' in file:
        rpcfile01 = rpcfile_collection[0]

    if 'HV' in file:
        rpcfile01  = rpcfile_collection[1]

    if 'VH' in file:
        rpcfile01  = rpcfile_collection[2]

    if 'VV' in file:
        rpcfile01 = rpcfile_collection[3]

    return rpcfile01



# Geometric correction using RPC
def geometric_correction(file ,outputpath):
    print('processing file is :', file)
    # Replace L1B with L2 in the output file name
    out_filename = file.replace('L1B', 'L2')
    rpcfile = Confirm_The_rpc_type(file)
    print("rpb file is:", rpcfile)
    rpc = Read_Rpb(rpcfile)
    # Changes the current working directory to the specified path
    os.chdir(outputpath)
    dataset = gdal.Open(file)
    dataset.SetMetadata(rpc, 'RPC')
    gdal.Warp(out_filename, dataset, dstSRS='EPSG:4326', xRes=0.0002, yRes=0.0002,
                       rpc=True,
                       transformerOptions=[r'path of your dem file'])
    print('completed：', out_filename)
    del dataset





if __name__ == '__main__':
    inputpath = 'xxxx\GF3_SAY_FSII_025440_E113.7_N35.0_20210609_L1A_HHHV_L10005692177'
    outputpath = inputpath+'_output'
    if not os.path.exists (outputpath):
        os.mkdir(outputpath)
    os.chdir (inputpath)
    xmlfile, HH, HV, VH, VV = Get_File_Name(inputpath)
    image_name = [HH, HV, VH, VV]
    Repeat_Run_1Ato1B(image_name, outputpath)

