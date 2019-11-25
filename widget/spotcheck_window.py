import re
import random

from model.window import *
from model.model import *
# from workbox.workbox import *
# from workbox import data_utils
from workbox.utility import *


class SpotCheckWindow(BaseWidget):

    def setField(self):
        self.open_path_field = PathField(self, "选择文件夹")
        self.save_path_field = PathField(self, "输出路径")
        self.spinbox = LineSpinBoxField(self, "抽查数量")

    def setWidget(self):
        self.check_list = CheckList(["批量"])
        self.addWidget(self.check_list)

        self.start_button = QPushButton("执行", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_split)

    def start_split(self):
        open_path = self.open_path_field.text()
        save_path = self.save_path_field.text()
        spotchecknum = self.spinbox.value()

        is_batch = self.check_list.value()

        if open_path and save_path:
            if is_batch:
                self.sample_drawn_batch(open_path, save_path, spotchecknum)
            else:
                self.sample_drawn(open_path, save_path, spotchecknum)

    def sample_drawn_batch(self, open_path, save_path, num):
        for line in os.listdir(open_path):
            temp_path = os.path.join(open_path, line)

            if os.path.isdir(temp_path):
                self.sample_drawn(temp_path, save_path, num)

    def sample_drawn(self, open_path, save_path, num):
        parent, pair = os.path.split(open_path)
        to_path = os.path.join(save_path, pair + "_sample")
        if not os.path.exists(to_path):
            os.mkdir(to_path)

        json_data = read_josn_from_path(open_path)
        json_list = list(json_data)

        if len(json_list) < num:
            num = len(json_list)

        random.shuffle(json_list)
        random_list_key = json_list[0:num]

        save_json(os.path.join(to_path, "sample.json"), get_in_set_json(random_list_key, json_data))
        move_files(random_list_key, open_path, to_path)
