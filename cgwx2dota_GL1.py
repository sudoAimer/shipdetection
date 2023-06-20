import os
from osgeo import gdal
import shapefile
import os.path as osp

def readTif(fileName):
    """
    打开Tif文件
    :param fileName:
    :return:
    """
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName+"文件无法打开")
    return dataset

def Getgeotrans(fileName):
    """
    得到仿射矩阵，示例 (359589.55651614454, 0.5, 0.0, 2040956.9293726773, 0.0, -0.5)
    :param fileName: Tif 文件路径
    :return:
    """
    dataset = readTif(fileName)
    return dataset.GetGeoTransform()

def CoordTransf(Xpixel,Ypixel,GeoTransform):
    """
    像素点转换为经纬度
    """
    XGeo = GeoTransform[0]+GeoTransform[1]*Xpixel+Ypixel*GeoTransform[2]
    YGeo = GeoTransform[3]+GeoTransform[4]*Xpixel+Ypixel*GeoTransform[5]
    return XGeo, YGeo

def SfTransCoord(x, y, GeoTransform):
    """
    根据经纬度转换为像素点
    :param x: 经度
    :param y: 维度
    :param GeoTransform: 仿射矩阵
    :return: 像素点的x,y
    """
    trans_x = (x - GeoTransform[0]) / GeoTransform[1]
    trans_y = (y - GeoTransform[3]) / GeoTransform[5]

    if trans_x < 0 :
        print(trans_x, trans_y)
        pass
    if trans_y < 0 :
        print(trans_x, trans_y)
        pass
    return trans_x, trans_y

def BoxTransCoord(box, GeoTransform):
    """
    将Box转化为像素点坐标, box中有五个点 我们只取前四个
    第五个和第四个能构成角度
    :param box: [0, 9]
    :param GeoTransform:
    :return:
    """
    bbox = []
    for point in box:
        x, y = SfTransCoord(point[0], point[1], GeoTransform)
        bbox.append(x)
        bbox.append(y)
    return tuple(bbox)

def ann_to_txt(ann_list):
    """
    将ann转化为txt
    :param ann:
    :return:
    """
    out_str = ''
    for ann in ann_list:
        poly = ann['bboxes']
        label = ann['labels']
        str_line = '{} {} {} {} {} {} {} {} {} {}\n'.format(
            poly[0], poly[1], poly[2], poly[3], poly[4], poly[5], poly[6], poly[7], label, '0')
        out_str += str_line
    return out_str

def cgwx2dota(tif_dir, shp_dir, label_dir):

    for tif_name in os.listdir(tif_dir):
        if tif_name.endswith('.tif') != True:
            pass
        else:
            img_name = tif_name.split('.')[0]
            shp_name = osp.join(shp_dir, img_name + '.shp')
            label_txt = osp.join(label_dir, img_name + '.txt')
            tif_name = osp.join(tif_dir, tif_name)
            geotrans = Getgeotrans(tif_name)
            shp_file = shapefile.Reader(shp_name)
            shps = shp_file.shapeRecords()
            ann_list = []
            for shp in shps:
                obj_type = str(shp.record.type)
                if obj_type == '':
                    print('obj_type==null')
                    continue
                obj_box = BoxTransCoord(shp.shape.points, geotrans)
                ann = dict(
                    bboxes=obj_box,
                    labels=obj_type)
                ann_list.append(ann)
            label_txt_str = ann_to_txt(ann_list)
            with open(label_txt, 'w') as f_txt:
                f_txt.write(label_txt_str)
    print('finish!')

def saveGeoTransform(tif_dir, shp_dir, label_dir):
    """
    保存图像的GeoTransform。
    :param tif_dir:
    :param shp_dir:
    :param label_dir:
    :return:
    """
    str_line = ''
    label_txt = osp.join(label_dir, 'imgTransform.txt')
    for shp_name in os.listdir(shp_dir):
        if shp_name.endswith('.shp') != True:
            pass
        else:
            img_name = shp_name.split('.')[0]
            tif_name = osp.join( tif_dir, img_name + '.tif')
            geotrans = Getgeotrans(tif_name)
            str_line += '{} {} \n'.format(
                img_name, geotrans)
    with open(label_txt, 'w') as f_txt:
        f_txt.write(str_line)
    print('finish!')

if __name__ == '__main__':
    # tif_dir
    tif_dir = r"\\192.168.100.52\PersonalWork\黄锵锵\JL1\tif"
    shp_dir = r"D:\data\shp"
    label_dir = r"D:\data\dota"
    cgwx2dota(tif_dir, shp_dir, label_dir)
    # saveGeoTransform(tif_dir, shp_dir, label_dir)



