import glob
import os
import json
import shutil
import yaml
import re
import cv2
import numpy as np
import math
from .define import *


# import shapely
# from shapely.geometry import Polygon


def get_one_josn_with_path(path):
    json_path_list = glob.glob(os.path.join(path, "*.json"))
    if len(json_path_list) == 1:
        return json_path_list[0]
    elif len(json_path_list) > 1:
        return json_path_list[0]
    else:
        return False


def _read_json(json_path):
    if json_path:
        print("-" * 10, json_path, "-" * 10)
        try:
            jsons = json.load(open(json_path, encoding="utf-8"))
        except json.decoder.JSONDecodeError:
            jsons = json.load(open(json_path, encoding="utf-8-sig"))
        return jsons
    return {}


# 读取json
def read_json(json_path):
    jsons = _read_json(json_path)
    data = {}
    for key, value in jsons.items():
        # print(key)
        if "." in key:
            file_name = re.findall("(.+?\.[jJpP][pPnN][gG])\d?", key)[0]
            data.update({
                file_name: value
            })
        else:
            data.update({
                key: value
            })

    return data


# 保存json
def save_json(path, data):
    with open(path, 'w') as f:
        f.write(json.dumps(data))


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)


def read_josn_from_path(path):
    return read_json(get_one_josn_with_path(path))


def copy_file(old_path, new_path):
    shutil.copy(old_path, new_path)


def move_file(old_path, new_path):
    shutil.move(old_path, new_path)


def get_pic_path_list(open_path):
    list = []
    for file_name in os.listdir(open_path):

        if os.path.isfile(os.path.join(open_path, file_name)) and is_image(file_name):
            list.append(file_name)
    return list


def save_and_update_json(save_to_path, data):
    json_data = read_josn_from_path(save_to_path)
    json_data.update(data)
    save_json(os.path.join(save_to_path, "json.json"), json_data)


def creat_path(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def split_json(json_data, open_path, save_path, split_num):
    _, patten = os.path.split(open_path)

    for i, key in enumerate(json_data):
        save_to_path = creat_path(os.path.join(save_path, patten + "({})".format(i % split_num)))
        save_and_update_json(save_to_path, {key: json_data[key]})


def split_path(list, open_path, save_path, split_num):
    _, patten = os.path.split(open_path)

    for i, file_name in enumerate(list):
        save_to_path = creat_path(os.path.join(save_path, patten + "({})".format(i % split_num)))

        old_path = os.path.join(open_path, file_name)
        new_path = os.path.join(save_to_path, file_name)
        copy_file(old_path, new_path)


def split_json_path(list, json_data, open_path, save_path, split_num):
    _, patten = os.path.split(open_path)

    error_list = []

    for i, file_name in enumerate(list):
        save_to_path = creat_path(os.path.join(save_path, patten + "({})".format(i % split_num)))

        old_path = os.path.join(open_path, file_name)
        new_path = os.path.join(save_to_path, file_name)

        if os.path.exists(old_path):
            copy_file(old_path, new_path)
        else:
            error_list.append(old_path)
            print(old_path, "不存在")
        save_and_update_json(save_to_path, {file_name: json_data[file_name]})

    error_path = creat_path(os.path.join(save_path, "error"))
    not_in_json = set(get_pic_path_list(open_path)) - set(list)
    move_files(not_in_json, open_path, error_path)

    if error_list or not_in_json:
        save_yaml(os.path.join(error_path, "error.yml"), {"文件不存在": error_list,
                                                          "json里不存在的图片": not_in_json})


def is_image(file):
    if file.endswith(".json") or file.endswith(".JSON"):
        return False

    return True


def combine_pic(open_path, save_path, is_repetition=False):
    all_error_list = []

    for dir, path, files in os.walk(open_path):
        error_list = move_files([file for file in files if is_image(file)], dir, save_path, is_repetition)
        all_error_list.extend(error_list)

    return all_error_list


def move_files(list, form_path, to_path, is_repetition=False):
    error_list = []
    parent, pair = os.path.split(form_path)

    for file_name in list:
        old_path = os.path.join(form_path, file_name)
        if is_repetition:
            new_path = os.path.join(to_path, "{}_{}".format(pair, file_name))
        else:
            new_path = os.path.join(to_path, file_name)

        if os.path.exists(new_path):
            print(new_path, "已存在 被覆盖")

        try:
            copy_file(old_path, new_path)
        except Exception as e:
            error_list.append(old_path)
            print(old_path, "不存在", e)
            # raise e

    return error_list


def move_move_files(list, form_path, to_path):
    error_list = []
    for file_name in list:
        old_path = os.path.join(form_path, file_name)
        new_path = os.path.join(to_path, file_name)

        if os.path.exists(new_path):
            print(new_path, "已存在 被覆盖")

        try:
            move_file(old_path, new_path)
        except Exception as e:
            error_list.append(old_path)
            print(old_path, "不存在", e)
            # raise e

    return error_list


def extend_path_to_key(dir, file):
    json_data = read_json(os.path.join(dir, file))
    parent, pair = os.path.split(dir)

    new_json = {}
    for key, value in json_data.items():
        new_file_name = "{}_{}".format(pair, key)
        value["filename"] = new_file_name
        new_json.update({
            new_file_name: value
        })

    return new_json


def combine_json(open_path, save_path, is_repetition=False, is_lost_weight=False):
    json_list = []
    for dir, path, files in os.walk(open_path):
        for f in [file for file in files if file.endswith(".json") or file.endswith(".JSON")]:
            if is_repetition:
                json_list.append(extend_path_to_key(dir, f))
            else:
                json_list.append(read_json(os.path.join(dir, f)))

    all_json = combine_json_list(json_list)

    if is_lost_weight:
        check_json_box_repetition(all_json, save_path)

    save_json(os.path.join(save_path, "all.json"), all_json)


def get_dir_all_json_data(open_path):
    all_josn_data_list = []
    for sub_dir_name in os.listdir(open_path):
        sub_path = os.path.join(open_path, sub_dir_name)
        sub_json = read_josn_from_path(sub_path)
        all_josn_data_list.append(sub_json)

    return all_josn_data_list


def combine_json_list(json_list, extent=True):
    all_json = {}

    for sub_json in json_list:
        for key, value in sub_json.items():
            if key in all_json:
                if extent:
                    all_json[key]["regions"].extend(value["regions"])
            else:
                all_json.update({
                    key: value
                })

    return all_json


def get_in_set_json(set_data, json_data):
    dic = {}
    for key in set_data:
        dic.update({
            key: json_data[key]
        })

    return dic


class BOX():

    def __init__(self, data, img_path, k_v=(1, 1)):
        if data["name"] == "rect":
            self.isbox = True
        else:
            self.isbox = False

        self.key, self.value = k_v
        self.img_path = img_path
        self._data = data
        self._polygon = None
        self.img = None

    @property
    def org_y(self):
        if self.isbox:
            return self._data["y"]

        return sorted(self.all_points_y)[0]

    @property
    def org_x(self):
        if self.isbox:
            return self._data["x"]
        return sorted(self.all_points_x)[0]

    @property
    def center(self):
        if self.isbox:
            return [(self.org_x + self.opp_x) / 2, (self.org_y + self.opp_y) / 2]
        else:
            x_list = sorted(self.all_points_x)
            y_list = sorted(self.all_points_y)
            return [(x_list[0] + x_list[-1]) / 2, (y_list[0] + y_list[-1]) / 2]

    @property
    def width(self):
        return self._data["width"]

    @property
    def height(self):
        return self._data["height"]

    @property
    def opp_y(self):
        return self.org_y + self._data["height"]

    @property
    def opp_x(self):
        return self.org_x + self._data["width"]

    @property
    def all_points_x(self):
        return self._data["all_points_x"]

    @property
    def all_points_y(self):
        return self._data["all_points_y"]

    @property
    def all_points(self):
        return np.array([list(zip(self.all_points_x, self.all_points_y))], dtype=np.int32)

    @property
    def image(self):
        if self.img is None:
            try:
                self.img = cv2.imread(self.img_path)
            except Exception as e:
                print(e)
        return self.img

    @property
    def mask(self):
        im = np.zeros(self.image.shape[:2], dtype="uint8")
        return cv2.fillPoly(im, self.all_points, 255)

    def getlen(self, point1, point2):
        p1 = np.array(point1)
        p2 = np.array(point2)
        p3 = p2 - p1
        return math.hypot(p3[0], p3[1])

    def overlap(self, box):
        if self.isbox is not box.isbox:
            return 0

        # if self.key == box.key:
        #     # key相等
        #     if self.value == box.value:
        #         # 值也相等
        #         pass
        #     else:
        #         # 值不等
        #         return 0
        # else:
        #     # key 不相等
        #     return 0

        if self.isbox:
            return bb_overlab(self.org_x, self.org_y, self.width, self.height,
                              box.org_x, self.org_y, self.width, self.height)

        if self.getlen(self.center, box.center) > DISTANCE:
            return 0

        if self.image is not None and box.image is not None:
            masked_and = cv2.bitwise_and(self.mask, box.mask)
            masked_or = cv2.bitwise_or(self.mask, box.mask)
            or_area = np.sum(np.float32(np.greater(masked_or, 0)))
            and_area = np.sum(np.float32(np.greater(masked_and, 0)))

            return and_area / or_area
        return 0


def compute_polygon_area(points):
    point_num = len(points)
    if (point_num < 3): return 0.0
    s = points[0][1] * (points[point_num - 1][0] - points[1][0])
    # for i in range(point_num): # (int i = 1 i < point_num ++i):
    for i in range(1, point_num):  # 有小伙伴发现一个bug，这里做了修改，但是没有测试，需要使用的亲请测试下，以免结果不正确。
        s += points[i][1] * (points[i - 1][0] - points[(i + 1) % point_num][0])
    return abs(s / 2.0)


def check_json_box_repetition(json_data, path):
    index = 0
    for k, v in json_data.items():
        print(k)
        if check_one_pic_has_repetition(v, os.path.join(path, k)) > 0:
            print(k + "有重复")
            index += 1

    print("总共有{}张图片重复".format(index))


def check_one_pic_has_repetition(jpg, img_path):
    list = []
    index = 0

    for i, a in enumerate(jpg["regions"]):
        flag = True
        for j, b in enumerate(jpg["regions"]):

            if i < j and check_box_is_repetition(a, b, img_path) > IOU:
                print(i, j)
                flag = False
                index += 1
                break

        if flag:
            list.append(a)

    jpg["regions"] = list
    return index


def check_box_is_repetition(a_box, b_box, img_path):
    a = BOX(a_box["shape_attributes"], img_path)
    b = BOX(b_box["shape_attributes"], img_path)
    return a.overlap(b)


# 两个检测框框是否有交叉，如果有交集则返回重叠度 IOU, 如果没有交集则返回 0
def bb_overlab(x1, y1, w1, h1, x2, y2, w2, h2):
    '''
    说明：图像中，从左往右是 x 轴（0~无穷大），从上往下是 y 轴（0~无穷大），从左往右是宽度 w ，从上往下是高度 h
    :param x1: 第一个框的左上角 x 坐标
    :param y1: 第一个框的左上角 y 坐标
    :param w1: 第一幅图中的检测框的宽度
    :param h1: 第一幅图中的检测框的高度
    :param x2: 第二个框的左上角 x 坐标
    :param y2:
    :param w2:
    :param h2:
    :return: 两个如果有交集则返回重叠度 IOU, 如果没有交集则返回 0
    '''
    if (x1 > x2 + w2):
        return 0
    if (y1 > y2 + h2):
        return 0
    if (x1 + w1 < x2):
        return 0
    if (y1 + h1 < y2):
        return 0
    colInt = abs(min(x1 + w1, x2 + w2) - max(x1, x2))
    rowInt = abs(min(y1 + h1, y2 + h2) - max(y1, y2))
    overlap_area = colInt * rowInt
    area1 = w1 * h1
    area2 = w2 * h2
    return overlap_area / (area1 + area2 - overlap_area)
