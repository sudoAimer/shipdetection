# import gdal
# *_*coding: utf-8 *_*
#############################################################
#                                                           #
#############################################################
import os
import numpy as np
from osgeo import gdal
# import gdal
# 定义读取和保存图像的类
class GRID:

    def load_image(self, filename):
        image = gdal.Open(filename)
        img_width = image.RasterXSize
        img_height = image.RasterYSize

        img_geotrans = image.GetGeoTransform()
        img_proj = image.GetProjection()
        img_data = image.ReadAsArray(0, 0, img_width, img_height)

        del image

        return img_proj, img_geotrans, img_data

    def write_image(self, filename, img_proj, img_geotrans, img_data):
        # 判断栅格数据类型
        if 'int8' in img_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in img_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        # 判断数组维度
        if len(img_data.shape) == 3:
            img_bands, img_height, img_width = img_data.shape
        else:
            img_bands, (img_height, img_width) = 1, img_data.shape

        # 创建文件
        driver = gdal.GetDriverByName('GTiff')
        image = driver.Create(filename, img_width, img_height, img_bands, datatype)

        image.SetGeoTransform(img_geotrans)
        image.SetProjection(img_proj)

        if img_bands == 1:
            image.GetRasterBand(1).WriteArray(img_data)
        else:
            for i in range(img_bands):
                image.GetRasterBand(i + 1).WriteArray(img_data[i])

        del image  # 删除变量,保留数据

if __name__ == '__main__':
    # 读取图片
    img_path = r"/home/server4/shipdetection/KS_HN1_01_20220312_000198_006_L0_DL1.tif"
    # 裁剪图片尺寸
    img_size = 1000
    # 图片保存位置
    img_save = r"/home/server4/shipdetection/tmp"
    proj, geotrans, data = GRID().load_image(img_path)
    print(proj)
    print(geotrans)
    # print(data)
    patch_size = img_size
    patch_save = img_save
    # print(data)
    # channel, width, height = data.shape
    width, height = data.shape
    num = 0
    for i in range(width // patch_size):
        for j in range(height // patch_size):
            num += 1
            # sub_image = data[:, i * patch_size:(i + 1) * patch_size, j * patch_size:(j + 1) * patch_size]
            sub_image = data[i * patch_size:(i + 1) * patch_size, j * patch_size:(j + 1) * patch_size]
            GRID().write_image(patch_save + '/hqq20220323_{}.tif'.format(num), proj, geotrans, sub_image)
