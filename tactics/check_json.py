# -*- coding: UTF-8 -*-
# import data_utils
# import os

id_list = ['[0-9]','1[0-9]',101,103,104,105,106,401,501,402,'20[1-7]']


# 判断是否是数字
def is_digit(value):
    if value is not None and value != '' and (str(value).strip().replace('\n', '')).isdigit():
        return True
    else:
        return False

def check_regions(region, file_name, annotation):
    if region is None:
        return 'region: 为空'

    region_attributes = region['region_attributes']
    is_bad = False

    if 'page_class_id' in region_attributes.keys():
        page_class_id = region_attributes['page_class_id']
        if is_digit(page_class_id):
            page_class_id = str(page_class_id).strip().replace('\n', '')
            page_class_id = int(page_class_id)

            flag = False

            for patter in id_list:
                if isinstance(patter, int):
                    if page_class_id == patter:
                        flag = True
                        break
                elif isinstance(patter, str):
                    if re.match(patter, str(page_class_id)):
                        flag = True
                        break

            if not flag:
                print('page_class_id非法:', file_name, ':', page_class_id)
                is_bad = 'page_class_id非法:'+ file_name+ ': '+ str(page_class_id)
            
            print("region_attributes['page_class_id']", region_attributes['page_class_id'])
        else:
            # data_utils.add_bad(file_name + '#错误原因:page_class_id非法', save_json_path)
            print('page_class_id非数字:', file_name, ',page_class_id=', page_class_id)
            is_bad = 'page_class_id非数字:'+file_name+',page_class_id='+str(page_class_id)
    else:
        print("无page_class_id:", file_name, ',',region_attributes.keys())
        # is_bad = "无page_class_id:"+file_name
    return is_bad

def loop_annotations(annotation, key, handle_item=None, handle_region=None):
    regions = annotation['regions']
    ex = None
    if not regions:
        raise ValueException(key, "regions为空")

    if handle_item is not None:
        if handle_item(key, annotation):
            handle_result_annotations[key] = annotation
    if handle_region is not None:
        for region in regions:
            flag = handle_region(region, key, annotation)
            if flag:
                e = ValueException(key, flag)
                ex = ex+e if ex else e

    if ex: raise ex

loop_annotations(value, key, handle_region=check_regions)


