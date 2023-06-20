import os.path
import os.path as osp
import glob
import numpy as np
import matplotlib.pyplot as plt

txt_path = r"D://mmrotate//data//cgwx//trainval//annfiles//"
# des_path = r"D://mmrotate//data//new//test//annfiles//"


# cls_map = {
#     '00': 'Other',
#     '01': 'General_Cargo_Ship',
#     '02': 'Bulk_Carrier',
#     '03': 'Tank_Ship',
#     '04': 'Container_Ship',
#     '06': 'Ro-Ro_Cargo_Ship',
#     '07': 'Trawler',
#     '08': 'General_Fishing_Vessel',
#     '09': 'Cruise_Line',
#     '10': 'Yacht',
#     '11': 'Dredger',
#     '12': 'Tugboat',
#     '13': 'Offshore_Supply_Ship',
#     '14': 'Warship',
#     '05': 'LNG/LPG_Ship',
#     '15': 'Medical_Ship',
#     '16': 'Oil_Platform',
#     '17': 'Scientific_Research_Platform'
# }

test = \
    {'Yacht': 476, 'General_Fishing_Vessel': 4890, 'Tank_Ship': 36, 'Bulk_Carrier': 106,
     'Trawler': 747, 'Warship': 102, 'Tugboat': 26, 'Dredger': 9, 'Other': 19, 'General_Cargo_Ship': 9,
     'Oil_Platform': 2, 'Cruise_Line': 25, 'Container_Ship': 12, 'Ro-Ro_Cargo_Ship': 23, 'Offshore_Supply_Ship': 6,
     'Scientific_Research_Platform': 2}
# test 6,467
# trainval = {'General_Fishing_Vessel': 18294, 'Yacht': 3186, 'Tank_Ship': 129, 'Trawler': 1234,
#             'Warship': 300, 'Tugboat': 73, 'Bulk_Carrier': 526, 'Dredger': 55, 'Other': 91,
#             'General_Cargo_Ship': 32, 'Cruise_Line': 178, 'Oil_Platform': 6, 'Offshore_Supply_Ship': 32,
#             'Ro-Ro_Cargo_Ship': 117, 'Container_Ship': 39, 'Scientific_Research_Platform': 3, 'LNG/LPG_Ship': 1}
trainval = {'General_Fishing_Vessel': 18294, 'Yacht': 3186, 'Tank_Ship': 129, 'Trawler': 1234,
            'Warship': 300, 'Tugboat': 73, 'Bulk_Carrier': 526, 'Dredger': 55,
            'General_Cargo_Ship': 32, 'Cruise_Line': 178,  'Offshore_Supply_Ship': 32,
            'Ro-Ro_Cargo_Ship': 117, 'Container_Ship': 39 }
# trainval total : 24,195

val = \
    {'Yacht': 636, 'General_Fishing_Vessel': 4935, 'Bulk_Carrier': 152, 'Trawler': 234, 'Dredger': 12,
     'Other': 24, 'Tank_Ship': 31, 'Tugboat': 16, 'General_Cargo_Ship': 12, 'Warship': 54, 'Cruise_Line': 54,
     'Ro-Ro_Cargo_Ship': 37, 'Container_Ship': 8, 'Offshore_Supply_Ship': 12,
     'Scientific_Research_Platform': 2, 'Oil_Platform': 2}
# val 6,193
ann_files = glob.glob(txt_path + '/*.txt')
cate_dict = {}
#
for ann_file in ann_files:
    txt_name = os.path.basename(ann_file)
    # print(ann_file)
    with open(ann_file) as f:
        s = f.readlines()
        for si in s:
            bbox_info = si.split(' ')
            # cat = cls_map[str(bbox_info[8])]
            cat = bbox_info[8]
            area = abs(float(bbox_info[7]) - float(bbox_info[1])) * abs(float(bbox_info[2]) - float(bbox_info[0]))
            if cat in cate_dict:
                cate_dict[cat] += 1
                cate_dict[cat + '_area'].append(area)
            else:
                cate_dict[cat] = 1
                cate_dict[cat + '_area'] = list()
                cate_dict[cat + '_area'].append(area)

for cat in cate_dict:
    if cat.split('_')[-1] != 'area' or len(cat.split('_')) == 1:
        cate_dict[cat + '_area'] = sum(cate_dict[cat + '_area']) / cate_dict[cat]
        print(cat, ":::", cate_dict[cat], ':::', cate_dict[cat + '_area'])
            # str_line = '{} {} {} {} {} {} {} {} {} {}\n'.format(
                # bbox_info[0], bbox_info[1], bbox_info[2], bbox_info[3], bbox_info[4], bbox_info[5], bbox_info[6], bbox_info[7], cls_map[str(bbox_info[8])], '0')
#
#
# print(cate_dict)
# including General Cargo Ship(GCS), Bulk Carrier(BC), Tank Ship(TS), Container Ship(CS),
# Ro-Ro Ship (RRS), Trawler(TR), General Fishing Vessel(GFV), Cruise Line(CL), Yacht(YA)
# Dredger(DR), Tug Boat(TB), Offshore Supply Ship(OSS) and Warship(WS).
# print(cate_dict)
# labels = ["train", "val", "test"]
# data = [18002, 6193, 6467]
# # data2 = [1111, 1111, 1111]
# # x1 = range(len(labels))
# width = 0.1
# # plt.xticks([i + width for i in x1], labels)
#
# # plt.figure(figsize=(7, 7))
# plt.figure()
# plt.bar(labels, data, label='number of instances')
# # plt.bar(labels, data2, label='number of instances')
#
# plt.legend()  # 显示图例
#
# plt.show()  # 显示图形
