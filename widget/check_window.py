from model.window import *
from model.model import *
from workbox.workbox import *
# from workbox import data_utils
from workbox.utility import *
from widget.empty_window import get_empty


class CheckWindow(BaseWidget):

    def setField(self):
        self.rule_file_field = FileField(self, "效验规则")
        self.open_path_field = PathField(self, "目标文件夹")
        self.out_path_field = PathField(self, "输出路径")

    def setWidget(self):
        self.start_button = QPushButton("执行", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_check)

    def start_check(self):
        py_file = self.rule_file_field.text()
        out_path = self.out_path_field.text()
        open_path = self.open_path_field.text()

        all_json = get_empty(open_path, out_path, out_pass=False, move=True)


        print("检查 标注信息")
        no_regions = get_noll_regions(all_json)

        if no_regions:
            no_regions_path = os.path.join(out_path, "没有任何标注信息")
            if not os.path.exists(no_regions_path):
                os.mkdir(no_regions_path)

            save_json(os.path.join(no_regions_path, "no_regions.json"), get_in_set_json(no_regions, all_json))
            move_move_files(no_regions, open_path, no_regions_path)

            all_json = get_in_set_json(set(all_json) - set(no_regions), all_json)

        print("检查 标注数据")
        error_files, error_msg_list = iterator_json(all_json, read_yaml(py_file))

        if error_files:
            value_error_path = os.path.join(out_path, "标注数据非法")
            if not os.path.exists(value_error_path):
                os.mkdir(value_error_path)

            save_json(os.path.join(value_error_path, "value_error.json"), get_in_set_json(error_files, all_json))
            move_move_files(error_files, open_path, value_error_path)

            with open(os.path.join(value_error_path, "error.txt"), "w", encoding="utf-8") as f:
                for line in error_msg_list:
                    f.write(line + "\n")

            all_json = get_in_set_json(set(all_json) - set(error_files), all_json)

        if all_json:
            pass_path = os.path.join(out_path, "pass")
            if not os.path.exists(pass_path):
                os.mkdir(pass_path)

            save_json(os.path.join(pass_path, "all.json"), all_json)
            move_move_files(set(all_json), open_path, pass_path)


def get_noll_regions(json):
    list = []
    for key, value in json.items():
        regions = value["regions"]
        if not regions:
            list.append(key)
    return list


def check_value_is_pass(page_value, values):
    page_value = str(page_value).strip().replace('\n', '')
    page_value = int(page_value)

    id_list = eval(values)
    for patter in id_list:
        if isinstance(patter, int):
            if page_value == patter:
                return True
        elif isinstance(patter, str):
            if re.match(patter, str(page_value)):
                return True

    return False


def check_attributes(attributes, keys_value, file_name):
    list = []
    for key, values in keys_value.items():
        if key in attributes:
            page_value = attributes[key]

            if not check_value_is_pass(page_value, values):
                list.append("{}:{} 非法:{}".format(file_name, key, page_value))
    return list


def iterator_json(json, keys_values):
    error_file = []
    error_msg_list = []
    for file_name, page_value in json.items():
        error_lists = []
        for region in page_value["regions"]:
            attributes = region["region_attributes"]
            error_list = check_attributes(attributes, keys_values, file_name)
            if error_list:
                error_lists.extend(error_list)

        if error_lists:
            error_file.append(file_name)
            error_msg_list.extend(error_lists)

        print(file_name)

    return error_file, error_msg_list
