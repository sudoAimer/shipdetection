import os.path
import os.path as osp
import glob

txt_path = r"D://mmrotate//data//cgwx(old//val//annfiles//"
des_path = r"D://mmrotate//data//cgwx_1//val//annfiles//"


ann_files = glob.glob(txt_path + '/*.txt')

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
#     '05' : 'LNG/LPG_Ship',
#     '15': 'Medical_Ship',
#     '16': 'Oil_Platform',
#     '17': 'Scientific_Research_Platform'
# }
cls_map = {
    '00': 'Ship',
    '01': 'Ship',
    '02': 'Ship',
    '03': 'Ship',
    '04': 'Ship',
    '06': 'Ship',
    '07': 'Ship',
    '08': 'General_Fishing_Vessel',
    '09': 'Ship',
    '10': 'Yacht',
    '11': 'Ship',
    '12': 'Ship',
    '13': 'Ship',
    '14': 'Ship',
    '05' : 'LNG/LPG_Ship',
    '15': 'Medical_Ship',
    '16': 'Oil_Platform',
    '17': 'Scientific_Research_Platform'
}
for ann_file in ann_files:
    txt_name = os.path.basename(ann_file)
    # print(ann_file)
    with open(ann_file) as f:

        out_str = ''

        s = f.readlines()
        for si in s:
            bbox_info = si.split(' ')
            # print(f"bbox:{bbox_info[:8]}, cls_name:{bbox_info[8]}, difficulty:{bbox_info[9]}")
            str_line = '{} {} {} {} {} {} {} {} {} {}\n'.format(
                bbox_info[0], bbox_info[1], bbox_info[2], bbox_info[3], bbox_info[4], bbox_info[5], bbox_info[6], bbox_info[7], cls_map[str(bbox_info[8])], '0')
            out_str += str_line

        label_txt = osp.join(des_path, txt_name)
        with open(label_txt, 'w') as f_txt:
            f_txt.write(out_str)