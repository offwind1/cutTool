from model.window import *
from model.model import *
# from workbox.workbox import *
from workbox.utility import *


class Filter(BaseWidget):

    def setField(self):
        self.input_file_field = FileField(self, "Json")
        self.key_text = TextEditField(self, "Key")
        self.value_text = TextEditField(self, "Value")
        self.out_path_field = PathField(self, "输出路径")

    def setWidget(self):
        self.start_button = QPushButton("过滤", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start)

    def start(self):
        input_file = self.input_file_field.text()
        key_text = self.key_text.text()
        value_text = self.value_text.text()
        out_path = self.out_path_field.text()

        json_data = read_json(input_file)
        save_json(os.path.join(out_path, "filtered.json"), iterator_json(json_data, key_text, value_text))


def check_attributes(data, value):
    for line in value.split(","):
        data = str(data)
        data = data.strip()

        if data == line:
            return True

    return False


def filter_regions(regions, key, value):
    new_regions = []
    for region in regions:
        attributes = region["region_attributes"]
        if key in attributes and check_attributes(attributes[key], value):
            new_regions.append(region)

    return new_regions


def iterator_json(json, key, value):
    new_json_data = {}

    for file_name, page_value in json.items():
        regions = filter_regions(page_value["regions"], key, value)
        if regions:
            page_value["regions"] = regions
            new_json_data.update({
                file_name: page_value
            })

    return new_json_data
