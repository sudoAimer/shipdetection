import os.path as osp
import os
import shapefile

shp_dir = r"D:\data\GF2\shp"
total = 0
type_dist = {}
for file in os.listdir(shp_dir):
    if file.endswith('.shp') != True:
        pass
    else:
        shp_name = osp.join(shp_dir, file)
        shp_file = shapefile.Reader(shp_name)
        shps = shp_file.shapeRecords()
        for shp in shps:
            obj_type = str(shp.record.type)
            if obj_type not in type_dist:
                type_dist[obj_type] = 1
            else:
                type_dist[obj_type] = type_dist[obj_type] + 1
        total = total + len(shps)
        if len(shps) == 0:
            print(shp_name)
print(total) # 17156 6919
print(type_dist)
# GF2 {'', '14', '12', '08', '01', '03', '06', '17', '04', '13', '05', '11', '00', '09', '02', '07', '16', '10'}
# GL1 {'', '01', '03', '07', '10', '09', '04', '08', '16', '14', '06', '13', '02', '00', '12', '11'} 无 5 15 17
# GL1 {'08': 4965, '02': 207, '09': 22, '00': 22, '03': 35, '': 6, '11': 22, '14': 75, '04': 18, '07': 930, '01': 9, '06': 47, '12': 11, '10': 539, '16': 3, '13': 8}
# GF2 {'08': 12902, '10': 2241, '02': 388, '': 11, '04': 34, '07': 732, '16': 6, '09': 192, '13': 18, '14': 207, '03': 116, '06': 95, '12': 68, '00': 77, '11': 31, '01': 34, '17': 3, '05': 1}