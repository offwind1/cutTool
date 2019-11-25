# coding=utf-8
# -*- coding: UTF-8 -*-
# 中文乱码处理
import ntpath
import os
import shutil
import glob

# import numpy as np
import json
import re
import random
# from matplotlib import pyplot as plt
# from matplotlib.pyplot import figure
# import cv2
import codecs


# 根据路径返回文件名
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


# 返回路径头部
def path_head(path):
    head, tail = ntpath.split(path)
    return head or ntpath.basename(head)


#
# 保存json 如果已经存在该文件,则将data添加进去,不覆盖
def save_json_extend(path, data):
    if os.path.exists(path):
        jsons = read_json(path)
        last_path = os.path.split(path)
        with open(os.path.join(last_path[0], 'backup_' + last_path[1]), 'w') as f:
            f.write(json.dumps(jsons))
        data.update(jsons)

    with open(path, 'w') as f:
        f.write(json.dumps(data))


# 保存json
def save_json(path, data):
    with open(path, 'w') as f:
        f.write(json.dumps(data))


# 读取json
def read_json(json_path):
    jsons = json.load(codecs.open(json_path, 'r', 'utf-8-sig'))
    #     jsons = json.loads(open(json_path).read().decode('utf-8-sig'))
    #     jsons = json.load(open(json_path))
    #     print(len(jsons))
    return jsons


# file_path：原始图片文件路径
# 递归过程中复制图片: 复制file_path中的所有图片到save_path路径
def copy_images(file_path, image_files, save_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    copy_images_length = 0
    #     last_path = path_head(image_files[0])
    json_files = glob.glob(os.path.join(file_path, '*.json'))
    #     该目录下没有json文件则不进行拷贝
    if len(json_files) == 0:
        return copy_images_length
    if image_files is None:
        image_files = glob.glob(os.path.join(file_path, '*.jpg'))
        image_files.extend(glob.glob(os.path.join(file_path, "*.JPG")))
    for image_path in image_files:
        file_name = path_leaf(image_path)
        #         print(file_name)
        copy_image_path = os.path.join(save_path, file_name)
        #         print(copy_image_path)
        if not os.path.exists(copy_image_path):
            copy_images_length += 1
            shutil.copy(image_path, copy_image_path)
    #     return copy_images_length
    return len(image_files)


# 递归过程中合并json 自动去重
def merge_json(file_path, image_files, save_path):
    json_paths = glob.glob(os.path.join(file_path, '*.json'))
    #     该目录下没有json文件则不进行拷贝
    merge_json_length = 0
    if len(json_paths) == 0:
        return merge_json_length
    json_path = json_paths[0]
    save_json_path = os.path.join(save_path, '_merge.json')
    if os.path.exists(save_json_path):
        json_extend = read_json(save_json_path)
        print('已生成标签数据：', len(json_extend))
    else:
        print('无已生成标签数据')
        json_extend = {}
    # print(json_path)
    annotations = read_json(json_path)
    json_extend = dict(json_extend, **annotations)
    #     print('json_extend length:',json_extend)
    save_json(save_json_path, json_extend)
    return len(annotations)


# 递归遍历含有图片的文件夹,一旦检测到含有图片,将会执行 recursive_method 方法
# recursive_method 方法包含 file_path,image_files,save_path三个参数
def find_image_paths_recursive(orgin_path, save_path, recursive_method):
    # print('orgin_path:', orgin_path)
    if not os.path.isdir(orgin_path):
        # print('不是目录', orgin_path)
        return
    images_length = 0
    files = os.listdir(orgin_path)
    for file in files:
        file_path = os.path.join(orgin_path, file)
        # print(file_path)
        if os.path.isdir(file_path):
            #             print(json_path)
            image_files = glob.glob(os.path.join(file_path, '*.jpg'))
            image_files.extend(glob.glob(os.path.join(file_path, "*.JPG")))
            if len(image_files) == 0:
                # print('无图片：', file_path)
                images_length += \
                    find_image_paths_recursive(file_path, save_path, recursive_method)
            else:
                # print(file_path, '目录下图片数量：', len(image_files))
                print('images_length：', images_length)
                images_length += recursive_method(file_path, None, save_path)
    #         else:
    #             images_length += find_image_paths(file_path)
    #     print('进度：{:0.2f}%'.format(images_length/6641*100))

    return images_length
# 递归遍历含有图片的文件夹,一旦检测到含有json,将会执行 recursive_method 方法
# recursive_method 方法包含 file_path,json_files,save_path三个参数
def find_json_paths_recursive(orgin_path, save_path, recursive_method):
    # print('orgin_path:', orgin_path)
    if not os.path.isdir(orgin_path):
        # print('不是目录', orgin_path)
        return
    images_length = 0
    files = os.listdir(orgin_path)
    for file in files:
        file_path = os.path.join(orgin_path, file)
        # print(file_path)
        if os.path.isdir(file_path):
            #             print(json_path)
            image_files = glob.glob(os.path.join(file_path, '*.json'))
            # image_files.extend(glob.glob(os.path.join(file_path, "*.JPG")))
            if len(image_files) == 0:
                # print('json：', file_path)
                images_length += \
                    find_image_paths_recursive(file_path, save_path, recursive_method)
            else:
                # print(file_path, '目录下图片数量：', len(image_files))
                print('json_length：', images_length)
                images_length += recursive_method(file_path, None, save_path)
    #         else:
    #             images_length += find_image_paths(file_path)
    #     print('进度：{:0.2f}%'.format(images_length/6641*100))

    return images_length

# 判断是否是数字
def is_digit(value):
    if value is not None and value != '' and (str(value).strip().replace('\n', '')).isdigit():
        return True
    else:
        return False


# 在jupyter中显示图片
def show_image(bgr_img, size=[1, 1], title='image'):
    b, g, r = cv2.split(bgr_img)  # get b,g,r
    rgb_img = cv2.merge([r, g, b])  # switch it to rgb
    figure(num=None, figsize=(size[0], size[1]), dpi=100, facecolor='w', edgecolor='k')
    #     image = np.squeeze(image,axis=0)
    plt.imshow(rgb_img)
    plt.title(title)
    plt.show()


# 根据box宽高生成 mask 坐标
def get_positions(x, y, change, max_change1, max_change2):
    if change == 'x':
        change1 = x
        change2 = y
    if change == 'y':
        change1 = y
        change2 = x
    positions1s = []
    positions2s = []
    counts = np.random.randint(5, 6)
    unit = (max_change1 - change1) / counts
    for i in range(counts):

        position1 = change1 + (i + 1) * unit
        if (position1 < max_change1):
            positions1s.append(int(position1))
        else:
            positions1s.append(max_change1 - 1)

        if change2 < max_change2:
            positions2s.append(int(change2))
        else:
            positions2s.append(int(max_change2 - 1))

    if change == 'x':
        return positions1s, positions2s
    if change == 'y':
        return positions2s, positions1s


# 打印 标注数据中 各个 page_class_id 的数量
def get_all_class_count(annotations, region_key='page_class_id'):
    numbers = {}
    chinese_numbers = {}
    english_numbers = {}
    white_pages = {}
    black_pages = {}
    for key, annotation in annotations.items():
        regions = annotation['regions']
        for region in regions:
            region_attributes = region['region_attributes']
            page_class_id = region_attributes[region_key]
            if page_class_id in [1]:
                numbers[key] = annotation
            if page_class_id in [2]:
                chinese_numbers[key] = annotation
            if page_class_id in [3]:
                english_numbers[key] = annotation
            if page_class_id in [4]:
                white_pages[key] = annotation
            if page_class_id in [5]:
                black_pages[key] = annotation
    print('numbers length:', len(numbers))
    print('chinese_numbers length:', len(chinese_numbers))
    print('english_numbers length:', len(english_numbers))
    print('white_pages length:', len(white_pages))
    print('black_pages length:', len(black_pages))


# from tqdm import tqdm_notebook as tqdm


# 遍历json ,for循环中执行自定义的handle_item(key, annotation)
# 以及 handle_region(region,key,annotation)方法处理数据,
# 避免总是需要重复写for循环代码
def loop_annotations(annotations, handle_item=None, handle_region=None):
    handle_result_annotations = {}
    # for key, annotation in tqdm(annotations.items()):
    for key, annotation in annotations.items():

        regions = annotation['regions']
        if handle_item is not None:
            if handle_item(key, annotation):
                handle_result_annotations[key] = annotation
        if handle_region is not None:
            for region in regions:
                if handle_region(region, key, annotation):
                    handle_result_annotations[key] = annotation
    return handle_result_annotations


#  将标注有问题的写入到bad_anno.txt中
# example: data_utils.add_bad('test.jpg#错误原因:test reason')
def add_bad(file_name, save_path='./'):
    save_path = os.path.join(save_path, 'bad_annotations.txt')
    with open(save_path, 'a') as f1:
        f1.write(file_name + os.linesep)


# 读取bad_nano.txt 返回文件名list
def get_bad_names(bad_image_path):
    bad_names = []
    for line in open(bad_image_path):
        line = line.strip('\n')
        contents = line.split('#', 1)
        image_name = contents[0]
        #         if len(contents)>= 2:
        #             print(image_name,',',contents[1])
        if image_name != '':
            bad_names.append(image_name)
    return bad_names


from .exception import KeyException, ValueException, MyException
from .workbox import *

def loop_check_json(json_obj , code, open_path, out_path, temp_error, temp_all):
    pass_out_path = os.path.join(out_path, "pass")
    error_out_path = os.path.join(out_path, "error")

    for key, value in json_obj.items():
        loc = {
            "key":key,
            "value":value,
            "open_path":open_path,
            "ValueException":ValueException,
            "KeyException":KeyException,
            "re":re,
        }

        try:
            try:
                exec(code, loc)
            except ValueException as e:
                newcopyflie(os.path.join(open_path, key), os.path.join(error_out_path, key))
                raise e
            except KeyException as e:
                #key问题，没有图片。不进行图片复制
                raise e
        except MyException as e:
            print(e)
            with open(os.path.join(out_path, "error.log"), "a+", encoding="utf-8") as f:
                f.write(str(e))
            with open(os.path.join(out_path, "keylist.txt"), "a+", encoding="utf-8") as f:
                f.write(e.key+"\n")
            temp_error.update({key:value})
        else:
            # print("pass", key)
            temp_all.update({key:value})
            newcopyflie(os.path.join(open_path, key), os.path.join(pass_out_path, key))



