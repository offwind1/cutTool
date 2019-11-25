import re

from model.window import *
from model.model import *
from workbox.utility import *


class Replace(BaseWidget):

    def setField(self):
        self.json_path = FileField(self, "json")
        self.key = TextEditField(self, "key")
        self.from_value = TextEditField(self, "目标值")
        self.to_value = TextEditField(self, "替换值")

    def setWidget(self):
        self.check_list = CheckList(["key", "value"], QRadioButton)
        self.addWidget(self.check_list)

        self.start_button = QPushButton("读取 page_id", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start)

        self.replace_button = QPushButton("替换", self)
        self.addWidget(self.replace_button)
        self.replace_button.clicked.connect(self.replace)

        self.list_view = QListWidget()
        self.list_view.setMinimumHeight(200)
        self.addWidget(self.list_view)
        self.list_view.itemDoubleClicked.connect(self.test)

    def test(self, item):
        tuple = eval(item.text())
        self.key.setText(tuple[0])
        self.from_value.setText(tuple[1])



    def replace(self):
        from_value = self.from_value.text()
        to_value = self.to_value.text()
        json_path = self.json_path.text()
        from_key = self.key.text()

        is_key, is_value = self.check_list.value()

        if not is_key and not is_value:
            self.show_message("未选择执行项")
            return

        if not os.path.exists(json_path):
            self.show_message("json未选择")
            return

        json_data = read_json(json_path)

        for key in json_data:
            for region in json_data[key]["regions"]:
                region_attribute = region["region_attributes"]

                if is_value:
                    page_class_id = region_attribute.get(from_key)
                    if page_class_id and str(page_class_id) == str(from_value):
                        region_attribute[from_key] = to_value

                if is_key:
                    if from_key in region_attribute:
                        page_class_id = region_attribute.get(from_key)
                        if page_class_id and str(page_class_id) == str(from_value):
                            region_attribute.update({
                                to_value: region_attribute.pop(from_key)
                            })

        save_json(json_path, json_data)
        self.start()

    def start(self):
        json_path = self.json_path.text()

        if not os.path.exists(json_path):
            self.show_message("json未选择")
            return

        self.list_view.clear()

        json_data = read_json(json_path)
        se = set()

        for jpg in json_data.values():
            for region in jpg["regions"]:
                region_attribute = region["region_attributes"]

                for key, value in region_attribute.items():
                    se.add((key, str(value)))

        for d in sorted(se):
            self.list_view.addItem(str(d))
