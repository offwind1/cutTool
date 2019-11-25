from model.window import *
from model.model import *
# from workbox.workbox import *
from workbox.utility import *


class Jiaoji(BaseWidget):

    def setField(self):
        self.a_json_path = FileField(self, "A")
        self.b_json_path = FileField(self, "B")
        self.out_path_field = PathField(self, "输出路径")

    def setWidget(self):
        self.start_button = QPushButton("提取", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start)

    def start(self):
        a_json_path = self.a_json_path.text()
        b_json_path = self.b_json_path.text()
        out_path = self.out_path_field.text()

        if not os.path.exists(a_json_path):
            self.show_message("A json未选择")
            return

        if not os.path.exists(b_json_path):
            self.show_message("B json未选择")
            return

        if not os.path.exists(out_path):
            self.show_message("输出路径未选择")
            return

        a_json = read_json(a_json_path)
        b_json = read_json(b_json_path)

        a_set = set(a_json)
        b_set = set(b_json)

        # a_set = set([x.strip() for x in a_set])
        # b_set = set([x.strip() for x in b_set])

        save_json(os.path.join(out_path, "only_a.json"), get_in_set_json(a_set - b_set, a_json))
        save_json(os.path.join(out_path, "only_b.json"), get_in_set_json(b_set - a_set, b_json))

        a = get_in_set_json(a_set & b_set, a_json)
        b = get_in_set_json(a_set & b_set, b_json)
        save_json(os.path.join(out_path, "and_ab.json"), combine_json_list([a, b]))
