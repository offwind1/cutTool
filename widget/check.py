from model.window import *
from model.model import *
# from workbox.workbox import *
from workbox.utility import *
from workbox.define import *


class Check(BaseWidget):

    def setField(self):
        self.target_path = PathField(self, "目标路径")

    def setWidget(self):
        self.start_button = QPushButton("检查", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start)

    def start(self):
        target_path = self.target_path.text()

        if not os.path.exists(target_path):
            self.show_message("目标路径未选择")
            return

        for dir, path, files in os.walk(target_path):
            json_path = get_one_josn_with_path(dir)
            if json_path:
                self.check(json_path, dir)
            else:
                print("× ", dir, "没有json文件")

    def check(self, json_path, dir):
        json_data = read_json(json_path)
        key_set = set(json_data)
        file_set = set(get_pic_path_list(dir))

        for k in key_set - file_set:
            print("× ", dir, k, "仅json中存在")

        for k in file_set - key_set:
            print("× ", dir, k, "不存在与json中")


class Analysis(BaseWidget):
    def setField(self):

        self.target_path = FileField(self, "目標JSON")
        self.save_path = PathField(self, "保存路径")

    def setWidget(self):
        self.start_button = QPushButton("解析", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start)

    def start(self):
        target_path = self.target_path.text()
        save_path = self.save_path.text()

        if not os.path.exists(target_path):
            self.show_message("目標JSON未选择")
            return

        if not os.path.exists(save_path):
            self.show_message("保存路径未选择")
            return

        json = read_json(target_path)
        all_set = set(json)

        for key, value in read_yaml(INI_PATH).items():
            data = iterator_json(json, str(value))

            if data:
                save_json(os.path.join(save_path, "no_" + key + ".json"), data)

            all_set = all_set - set(data)

        data = {}
        for key in all_set:
            data.update({
                key: json[key]
            })

        save_json(os.path.join(save_path, "all_have" + ".json"), data)


def iterator_json(json, value):
    data = {}
    value_list = value.split(",")

    for file_name, page_value in json.items():

        falg = False

        for region in page_value["regions"]:
            if "page_class_id" in region["region_attributes"]:
                for v in value_list:
                    temp = region["region_attributes"]["page_class_id"]
                    if isinstance(temp, str):
                        temp = temp.strip()
                    if isinstance(temp, int):
                        temp = str(temp)

                    if temp == v:
                        falg = True

        if not falg:
            data.update({
                file_name: page_value
            })

    return data


class RemoveDuplicates(BaseWidget):
    def setField(self):

        self.target_path = PathField(self, "目標路径")
        self.save_path = PathField(self, "保存路径")

    def setWidget(self):
        self.addWidget(QLabel(" 目标路径下，必须同时存在json和图片\n 路径不能包含中文 \n "
                              "IOU 目前设置为 {} 距离检测设置为{}像素".format(IOU, DISTANCE)))

        self.start_button = QPushButton("去除重复box", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start)

    def start(self):
        target_path = self.target_path.text()
        save_path = self.save_path.text()

        if not os.path.exists(target_path):
            self.show_message("目標JSON未选择")
            return

        if not os.path.exists(save_path):
            self.show_message("保存路径未选择")
            return

        json = read_josn_from_path(target_path)
        check_json_box_repetition(json, target_path)
        save_json(os.path.join(save_path, "thin.json"), json)
