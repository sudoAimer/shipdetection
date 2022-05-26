import os 
import cv2
import numpy as np
from numpy import block

# 小图片保存目录
pic_dir = r'/home/server4/sudo_aimer/trans/testTif/'
# 合并后图片保存地址
save_name = r'/home/server4/sudo_aimer/trans/Combine.jpg'

block_xsize = 2000
block_ysize = 2000 
im_width = 48312
im_height = 44500
num_width = int(im_width / block_ysize) # 通过大图像素得知分了多少块
num_height = int(im_height / block_xsize)

# 创建空图片
img = np.empty((3, num_width * block_xsize, num_height * block_ysize)).astype(np.int16)

# 目录中依次取图片
for pic_name in os.listdir(pic_dir):
    x = int(pic_name.split("_",3)[1])
    y = int(pic_name.split("_",3)[2].split(".")[0])
    offset_x = block_xsize * x
    offset_y = block_ysize * y
    data = np.array(cv2.imread(os.path.join(pic_dir, pic_name))).transpose(2,1,0)
    img[:, offset_x:offset_x+block_xsize, offset_y:offset_y+block_ysize] = data
    print("图片" + str(pic_name) + '填充完成')
    del data

# 保存合并后图片
img = img.transpose(2,1,0) # 转换维度 
cv2.imencode('.jpg', img)[1].tofile(save_name)

