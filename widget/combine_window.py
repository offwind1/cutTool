from model.window import *
from model.model import *
# from workbox.workbox import *
# from workbox import data_utils
from workbox.utility import *


class CombineWindow(BaseWidget):

    def setField(self):
        self.open_Path_field = PathField(self, "源路径")
        self.save_path_field = PathField(self, "保存路径")

    def setWidget(self):
        self.check_list = CheckList(["json", "图片", "拼接文件夹名称到各文件名前(保留重复，路径中不能有中文)", "去除重复(必须同时选择json和图片)"])
        self.addWidget(self.check_list)

        self.start_button = QPushButton("执行", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_combine)

        self.info_label = QLabel()
        self.addWidget(self.info_label)

    def start_combine(self):
        open_path = self.open_Path_field.text()
        save_path = self.save_path_field.text()

        is_json, is_pic, is_repetition, is_lost_weight = self.check_list.value()

        if not os.path.isdir(open_path):
            self.show_message("原路径未选择")
            return

        if not os.path.isdir(save_path):
            self.show_message("保存路径未选择")
            return

        if not is_json and not is_pic:
            self.show_message("未选择执行项")
            return

        if is_pic:
            combine_pic(open_path, save_path, is_repetition)

        if is_json:
            combine_json(open_path, save_path, is_repetition, is_lost_weight)


class PriorityCombineWindow(BaseWidget):

    def setField(self):
        self.A_file_field = FileField(self, "优先级json")
        self.B_file_field = FileField(self, "劣后级json")
        self.save_path_field = PathField(self, "保存路径")

    def setWidget(self):
        self.start_button = QPushButton("执行", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_combine)

    def start_combine(self):
        A_file = self.A_file_field.text()
        B_file = self.B_file_field.text()
        save_path = self.save_path_field.text()

        if not os.path.isfile(A_file):
            self.show_message("原路径未选择")
            return
        if not os.path.isfile(B_file):
            self.show_message("原路径未选择")
            return

        if not os.path.isdir(save_path):
            self.show_message("保存路径未选择")
            return

        save_json(os.path.join(save_path, "all.json"),
                  combine_json_list([read_json(A_file), read_json(B_file)],
                                    extent=False))
