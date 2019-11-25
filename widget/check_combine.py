import re

from model.window import *
from model.model import *
from workbox.workbox import *
from workbox import data_utils


class CheckCombineWindow(BaseWidget):

    def setField(self):
        self.rule_file_field = FileField(self, "效验规则")
        self.json_path_field = PathField(self, "Json文件夹")
        self.triget_path_field = PathField(self, "目标文件夹")

    def setWidget(self):
        self.start_button = QPushButton("执行", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_check)

    def start_check(self):
        py_file = self.rule_file_field.text()
        json_path = self.json_path_field.text()
        trigger_path = self.triget_path_field.text()

        for trigger in os.listdir(trigger_path):
            out_path = os.path.join(trigger_path, trigger)
            json_patter = "{}*.json"
            patter = "{}[^0-9].".format(trigger)

            json_files = glob.glob(os.path.join(json_path, json_patter.format(trigger)))
            for j in json_files:
                _, j_name = os.path.split(j)
                if re.match(patter, j_name):
                    shutil.copy(j, out_path)
                    self.action(py_file, out_path, out_path)

    def action(self, py_file, open_path, out_path):
        if os.path.isfile(py_file) and os.path.isdir(open_path) and os.path.isdir(out_path):

            pass_out_path = os.path.join(out_path, "pass")
            error_out_path = os.path.join(out_path, "error")

            if not os.path.exists(pass_out_path):
                os.mkdir(pass_out_path)
            if not os.path.exists(error_out_path):
                os.mkdir(error_out_path)

            temp_all = {}
            temp_error = {}

            with open(py_file, "r", encoding="utf-8") as f:
                code = f.read()

            for tmp_path in get_json_list(open_path):
                json_obj = read_json(tmp_path)
                data_utils.loop_check_json(json_obj, code, open_path, out_path, temp_error, temp_all)

                for line in os.listdir(open_path):
                    print(line)

            savejson(os.path.join(pass_out_path, "pass.json"), temp_all)
            savejson(os.path.join(error_out_path, "error.json"), temp_error)
