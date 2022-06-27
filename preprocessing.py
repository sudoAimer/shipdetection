from unittest.mock import patch
from osgeo import gdal
import numpy as np
import cv2
import os
from osgeo import gdal
import numpy as np
import cv2
import os
#---------------------#
#    正则化
#---------------------#


def normalization(data, low, high):
    _range = high - low
    return (data - low) / _range

#---------------------#
#    转为8bit
#---------------------#


def imgto8bit(img, low_value, high_value):
    img_nrm = normalization(img, low_value, high_value)
    img_8 = np.uint8(255 * img_nrm)
    return img_8

#---------------------#
#    检查目录
#---------------------#


def checkDir(dir):
    if os.path.isdir(dir):
        return
    else:
        os.mkdir(dir)
        return

#---------------------#
#   找到图片最大最小值
#---------------------#


def calMaxMin(in_band, lower_percent=0.5, higher_percent=99.5):
    """
    # 找出大图片中的最大最小值方便小图片进行映射。
    :param lower_percent:
    :param higher_percent:
    :return:
    """
    data = in_band.ReadAsArray().astype(np.int16)
    low_value = np.percentile(data, lower_percent)
    high_value = np.percentile(data, higher_percent)
    return low_value, high_value


#---------------------#
#         设置
#---------------------#
patchsize = 1000                                # 块大小


#---------------------#
#         路径
#---------------------#
root_path = r"/home/server4/sudo_aimer/trans/geotrans/test1.tiff"
save_dir = r'/home/server4/sudo_aimer/trans/geotrans/test1_out'
pic_name = r'test1'

#---------------------#
#       读取图片
#---------------------#
in_ds = gdal.Open(root_path)
checkDir(save_dir)
xsize = in_ds.RasterXSize                       # X
ysize = in_ds.RasterYSize                       # Y
bands = in_ds.RasterCount                       # 波段数目
geotransform = in_ds.GetGeoTransform()          # 仿射矩阵X
projection = in_ds.GetProjectionRef()           # 投影矩阵

assert bands == 1                               # 目前只支持波段为1
in_band = in_ds.GetRasterBand(1)
low_value, high_value = calMaxMin(in_band)      # 找到最大、最小值

#---------------------#
#       分割图片
#---------------------#
x = int(xsize / patchsize)
y = int(ysize / patchsize)
# print(x,y)
x_mod = xsize % patchsize
y_mod = ysize % patchsize
# print(x_mod,y_mod)
# print(xsize, ysize)
# div_images = []
for i in range(1, x + 1):
    for j in range(1, y + 1):
        if i == x and j == y:
            div_image = in_band.ReadAsArray((i - 1) * patchsize, (j - 1) * patchsize,
                                            patchsize + x_mod, patchsize + y_mod).astype(np.int16)
        elif i == x:
            div_image = in_band.ReadAsArray((i - 1) * patchsize, (j - 1) * patchsize,
                                            patchsize, patchsize + y_mod).astype(np.int16)
        elif j == y:
            div_image = in_band.ReadAsArray((i - 1) * patchsize, (j - 1) * patchsize,
                                            patchsize + x_mod, patchsize).astype(np.int16)
        else:
            div_image = in_band.ReadAsArray((i - 1) * patchsize, (j - 1) * patchsize,
                                            patchsize, patchsize).astype(np.int16)

        div_image = imgto8bit(div_image, low_value, high_value)  # 转为8bit
        div_image = cv2.imencode('.jpg', div_image)  # 解码为jpg
        # 图片命名
        filename = pic_name + '_' + str(i) + '_' + str(j) + '.jpg'
        # 图片保存
        div_image[1].tofile(os.path.join(save_dir, filename))
        # div_images.append(div_image) 可选是否保存image

# print(len(div_images))
print('Split complete')
#---------------------#
#       合并图片
#---------------------#
ori_pic = np.empty((xsize, ysize)).astype(np.uint8)
for i in range(1, x + 1):
    for j in range(1, y + 1):
        print(i, j)
        cut_image = pic_name + '_' + str(i) + '_' + str(j) + ".jpg"
        img = cv2.imread(os.path.join(save_dir, cut_image)
                         ).astype(np.uint8).transpose(2, 1, 0)[0]
        if i == x and j == y:
            ori_pic[(i - 1) * patchsize: i * patchsize + x_mod,
                    (j - 1) * patchsize: j * patchsize + y_mod] = img
        elif i == x:
            ori_pic[(i - 1) * patchsize: i * patchsize,
                    (j - 1) * patchsize: j * patchsize + y_mod] = img
        elif j == y:
            ori_pic[(i - 1) * patchsize: i * patchsize + x_mod,
                    (j - 1) * patchsize: j * patchsize] = img
        else:
            ori_pic[(i - 1) * patchsize: i * patchsize,
                    (j - 1) * patchsize: j * patchsize] = img
# 保存图片
cv2.imencode('.jpg', ori_pic)[1].tofile(
    os.path.join(save_dir, pic_name + '.jpg'))
print('Combine complete')
