import re

from model.window import *
from model.model import *
from workbox.utility import *


class SplitWindow(BaseWidget):

    def setField(self):
        self.open_path_field = PathField(self, "原路径")
        self.save_path_field = PathField(self, "保存路径")
        self.split_spinbox = LineSpinBoxField(self, "份数", default=2)

    def setWidget(self):
        self.check_list = CheckList(["json", "图片"])
        self.addWidget(self.check_list)

        self.start_button = QPushButton("执行", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_split)

    def start_split(self):
        open_path = self.open_path_field.text()
        save_path = self.save_path_field.text()
        split_num = self.split_spinbox.value()
        is_json, is_pic = self.check_list.value()

        if not os.path.isdir(open_path):
            self.show_message("原路径未选择")
            return

        if not os.path.isdir(save_path):
            self.show_message("保存路径未选择")
            return

        if not is_json and not is_pic:
            self.show_message("未选择执行项")
            return

        if is_json and not get_one_josn_with_path(open_path):
            self.show_message("未找到json文件")

        if is_json and is_pic:
            json_data = read_josn_from_path(open_path)
            file_list = list(json_data)
            split_json_path(file_list, json_data, open_path, save_path, split_num)
        elif is_pic:
            file_list = get_pic_path_list(open_path)
            split_path(file_list, open_path, save_path, split_num)
        elif is_json:
            json_data = read_josn_from_path(open_path)
            split_json(json_data, open_path, save_path, split_num)
