
from osgeo import gdal



def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName+"文件无法打开")
    return dataset
#获取仿射矩阵信息
def Getgeotrans(fileName):
    dataset = readTif(fileName)
    return dataset.GetGeoTransform()

#像素坐标和地理坐标仿射变换
def CoordTransf(Xpixel,Ypixel,GeoTransform):
    XGeo = GeoTransform[0]+GeoTransform[1]*Xpixel+Ypixel*GeoTransform[2];
    YGeo = GeoTransform[3]+GeoTransform[4]*Xpixel+Ypixel*GeoTransform[5];
    return XGeo,YGeo

if __name__ == '__main__':
    """
        将像素坐标和地理坐标做仿射变换
    """
    filename = '/home/server4/sudo_aimer/trans/geotrans/geotiff.tiff'
    # 得到仿射矩阵
    # GeoTransform = Getgeotrans(fileName=filename) # 从图片中读取
    GeoTransform = (14.226996,0.000021,0,114.996139,0,0.000021) # 目前图片的
    print(GeoTransform)
    # 得到具体坐标
    x, y = CoordTransf(14222, 14204, GeoTransform=GeoTransform)
    print(x, '  ',y)

    

