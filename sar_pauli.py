# -*- coding: utf-8 -*-
# @Time    : 2021/3/8 17:52

import gdal
import numpy as np
import cv2
import os
# Use Gaofen No. 3 as sample data
# pauli pauli decomposition

def get_file_name(pathlog):
    #
    """
    Query whether there is data of Gaofen 3 in the folder, and return if it exists
    :param pathlog:Destination folder
    :return:List, arranged in the order of xmlfile, HH, HV, VH, VV
    """
    # xml metadata information, mark xml name
    xmlfile = []
    for f_name in os.listdir(pathlog):
        if f_name.endswith('.meta.xml'):
            # print(f_name)
            xmlfile = f_name

    # Mark image name
    image_fn = []
    # image_fn =glob.glob('*.tiff')
    for f_name in os.listdir(pathlog):
        if f_name.endswith('.tiff'):
            # print(f_name)
            vhlfile = f_name
            image_fn.append(f_name)
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


def pauli(pathlog,outfiles):
    os.chdir(pathlog)
    xmlfile, HH, HV, VH, VV = get_file_name(pathlog)
    if HH != '':
        band1 = gdal.Open(HH)
        # The number of columns of the raster matrix
        im_width = band1.RasterXSize
        # The number of rows of the raster matrix
        im_height = band1.RasterYSize
        hh_data = band1.GetRasterBand(1).ReadAsArray(0, 0, im_width, im_height).astype(float)
        hh_data[hh_data == -9999] = np.nan
        hh_data[hh_data == 0] = np.nan
    if HV != '':
        band2 = gdal.Open(HV)
   
        im_width = band2.RasterXSize
   
        im_height = band2.RasterYSize
        hv_data = band2.GetRasterBand(1).ReadAsArray(0, 0, im_width, im_height).astype(float)
        hv_data[hv_data == -9999] = np.nan
        hv_data[hv_data == 0] = np.nan
    if VH != '':
        band3 = gdal.Open(VH)

        im_width = band3.RasterXSize

        im_height = band3.RasterYSize
        vh_data = band3.GetRasterBand(1).ReadAsArray(0, 0, im_width, im_height).astype(float)
        vh_data[vh_data == -9999] = np.nan
        vh_data[vh_data == 0] = np.nan
    if VV != '':
        band4 = gdal.Open(VV)

        im_width = band4.RasterXSize

        im_height = band4.RasterYSize
        vv_data = band3.GetRasterBand(1).ReadAsArray(0, 0, im_width, im_height).astype(float)
        vv_data[vv_data == -9999] = np.nan
        vv_data[vv_data == 0] = np.nan

    r = (hh_data + vv_data) * (hh_data + vv_data)


    b = (hh_data - vv_data) * (hh_data - vv_data)


    g = hv_data * hv_data


    datagray = a = np.zeros(shape=(im_height, im_width, 3))
    datagray[:, :, 0] = r
    datagray[:, :, 1] = g
    datagray[:, :, 2] = b

    # datagray = cv2.merge([b, g, r])
    #
    # tarpath= r'F:\project1\SAR\gf3_output\test2.jpg'
    # cv2.imwrite(tarpath, datagray)

    outFileName = HH[:-24]
    # Set the output band
    band1 = gdal.Open(HH)
    Driver = band1.GetDriver()
    geoTransform1 = band1.GetGeoTransform()
    ListgeoTransform1 = list(geoTransform1)
    ListgeoTransform1[5] = -ListgeoTransform1[5]
    newgeoTransform1 = tuple(ListgeoTransform1)
    proj1 = band1.GetProjection()
    OutRCname = os.path.join(outfiles,  outFileName + ".tiff")
    outDataset = Driver.Create(OutRCname, im_width, im_height,  3, gdal.GDT_Int32)
    outDataset.SetGeoTransform(newgeoTransform1)
    outDataset.SetProjection(proj1)
    for m in range(1, 4):
        outband = outDataset.GetRasterBand(m)
        outband.SetNoDataValue(0)
        new_band = datagray[:, :, m - 1]
        outband.WriteArray(new_band)
    
        print('Complete pauli decomposition')

    tarpath_01 = os.path.join(outfiles,  outFileName + ".jpg")
    print('Generate linear stretch results：', tarpath_01)
    rgb_linear(datagray, tarpath_01)

    tarpath_02 = os.path.join(outfiles, outFileName + "_linear01.jpg")
    print('Generate 1% linear stretch results：', tarpath_02)
    rgb_linear_percent_(datagray, tarpath_02, 1)

    tarpath_03 = os.path.join(outfiles, outFileName + "_linear02.jpg")
    print('Generate 2% linear stretch results：', tarpath_03)
    rgb_linear_percent_(datagray, tarpath_03, 2)
def rgb_linear(data,tarpath):
        
        x, y, z = np.shape(data)
        data_new = np.zeros(shape=(x, y, 3))
        for i in range(3):
            print(i)
            data_8bit = data[:, :, i]
            data_8bit = (data_8bit - np.nanmin(data_8bit)) / (np.nanmax(data_8bit) - np.nanmin(data_8bit)) * 255
            data_new[:, :, i] = data_8bit

        # The form of cv2.merge is opposite to the traditional matrix synthesis, the bgr form
        datagray = cv2.merge([data_new[:, :, 2], data_new[:, :, 1], data_new[:, :, 0]])
        cv2.imwrite(tarpath, datagray)
  

# n% linear stretch
def rgb_linear_percent_(data, tarpath, n):
 
    x, y, z = np.shape(data)
    data_new = np.zeros(shape=(x, y, 3))
    for i in range(3):
        print(i)
        data_8bit = data[:, :, i]

        # Convert data to 8 bit
        data_8bit = data_8bit / (np.nanmax(data_8bit)) * 255
        
        data_8bit[np.isnan(data_8bit)] = 0
        d1 = np.percentile(data_8bit, n)
        u99 = np.percentile(data_8bit, 100 -n)

        maxout = 255
        minout = 0

        data_8bit_new = minout + ((data_8bit - d1) / (u99 - d1)) * (maxout - minout)
        data_8bit_new[data_8bit_new < minout] = minout
        data_8bit_new[data_8bit_new > maxout] = maxout

        data_new[:, :, i] = data_8bit_new
    datagray = cv2.merge([data_new[:, :, 2], data_new[:, :, 1], data_new[:, :, 0]])
    cv2.imwrite(tarpath, datagray)
  


    


if __name__ == '__main__':
    pathlog = r'F:\project1\SAR\gf3_output\GF3_MYN_QPSI_021809E105.6_N19.6_20200930'
    outfiles = 'F:\project1\SAR\gf3_output'
    pauli(pathlog,outfiles)
