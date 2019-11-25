from model.window import *
from model.model import *
# from workbox.workbox import *
from workbox.utility import *


class Extract(BaseWidget):

    def setField(self):
        self.json_path = FileField(self, "json")
        self.target_path = PathField(self, "目标路径")
        self.save_path = PathField(self, "保存路径")

    def setWidget(self):
        self.start_button = QPushButton("提取", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start)

    def start(self):
        json_path = self.json_path.text()
        target_path = self.target_path.text()
        save_path = self.save_path.text()

        if not os.path.exists(json_path):
            self.show_message("json未选择")
            return

        if not os.path.exists(target_path):
            self.show_message("目标路径未选择")
            return

        if not os.path.exists(save_path):
            self.show_message("保存路径未选择")
            return

        json_data = read_json(json_path)
        key_set = set(list(json_data))

        # error_list = []
        for dir, path, files in os.walk(target_path):
            # print(set(files) & key_set, set(files), key_set)
            move_files(set(files) & key_set, dir, save_path)
            # error_list.extend(list(key_set-set(files)))

        # if error_list:
        #     save_yaml(os.path.join(save_path, "error.yml"), {"文件不存在": error_list})
