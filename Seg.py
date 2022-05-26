from osgeo import gdal
import numpy as np
import cv2
import os
###############################子函数###################################
def normalization(data, low, high):
    _range = high - low
    return (data - low) / _range

def imgto8bit(img, low_value, high_value):
    img_nrm = normalization(img, low_value, high_value)
    img_8 = np.uint8(255 * img_nrm)
    return img_8

def checkDir(dir):
    if os.path.isdir(dir):
        return
    else:
        os.mkdir(dir)
        return 

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
    print(f'low_value:{low_value}')
    print(f'high_value:{high_value}')
    return low_value, high_value

# ##############################读取图片信息###################################
in_ds = gdal.Open(r"/home/server4/sudo_aimer/trans/geotrans/geotiff.tiff")
save_dir = r'/home/server4/sudo_aimer/trans/testTif/'
pic_name = r'test' # 图片名
checkDir(save_dir)
# 我们只有一个波段，读取第一个波段
in_band = in_ds.GetRasterBand(1)
low_value, high_value = calMaxMin(in_band)
# 获取原图的原点坐标信息
# ori_transform = in_ds.GetGeoTransform()
ori_transform = (14.226996,0.000021,0,114.996139,0,0.000021)
top_left_x = ori_transform[0]  # 左上角x坐标
top_left_y = ori_transform[3]  # 左上角y坐标
w_e_pixel_resolution = ori_transform[1]  # 东西方向像素分辨率
n_s_pixel_resolution = ori_transform[5]  # 南北方向像素分辨率

# ##############################裁切信息设置###################################
# ##定义切图的起始点像素位置
offset_x = 0
offset_y = 0
# ##定义切图的大小（矩形框）
block_xsize = 1000  # 行
block_ysize = 1000  # 列
# ##裁切数量
im_width = in_ds.RasterXSize  # 栅格矩阵的列数
im_height = in_ds.RasterYSize  # 栅格矩阵的行数
num_width = int(im_width / block_ysize)
num_height = int(im_height / block_xsize)
print(f'图像宽度:{im_width}')
print(f'图像高度:{im_height}')
# ################################开始裁切#####################################

for i in range(num_width):
    for j in range(num_height):
        offset_x1 = offset_x + block_xsize * i
        offset_y1 = offset_y + block_ysize * j

        out_band = in_band.ReadAsArray(offset_x1, offset_y1, block_xsize, block_ysize).astype(np.int16)
        out_pic = imgto8bit(out_band, low_value, high_value)
        # 图片命名
        filename = pic_name + '_'+ str(i) + '_' + str(j) + '.jpg'
        # 图片保存
        cv2.imencode('.jpg', out_pic)[1].tofile(os.path.join(save_dir,filename))
        

        