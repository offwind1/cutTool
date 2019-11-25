from model.window import *
from model.model import *
from workbox.workbox import *
from workbox import data_utils
import workbox.utility as u
from workbox.define import *
from copy import deepcopy

class TongJiWindow(BaseWidget):

    def __init__(self):
        super().__init__()
        self.guize = self.___(u.read_yaml(INI_PATH))

    def ___(self, dict):
        data = {}
        for key, value in dict.items():
            data[key] = {
                "list": [int(x) for x in value.split(",")],
                "count": 0
            }

        return data

    def setField(self):
        self.json_file_field = FileField(self, "选择json（统计单个）")
        self.open_path_field = PathField(self, "选择文件夹（统计多个）")

    def setWidget(self):
        self.tihao_label = QLabel()
        self.biji_label = QLabel()
        self.addWidget(self.tihao_label)
        self.addWidget(self.biji_label)

        self.start_button = QPushButton("统计单文件夹", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start)

        self.tj_all_button = QPushButton("统计多文件夹", self)
        self.addWidget(self.tj_all_button)
        self.tj_all_button.clicked.connect(self.start_all)

    def start_alllll(self):
        open_path = self.open_path_field.text()

        if open_path:
            info_list = []
            all_all_num = 0

            for line in os.listdir(open_path):
                temp_path = os.path.join(open_path, line)

                json_list = glob.glob(os.path.join(temp_path, "*.json"))

                for json in json_list:
                    all_num, tongji = self.jongji(json)
                    all_all_num += all_num

                    info_list.append((line, all_num, tongji))

            from workbox.template import saveTemp
            import webbrowser

            html = saveTemp({"list": info_list, "all": all_all_num})
            webbrowser.open(html)


    def start_all(self):
        open_path = self.open_path_field.text()

        info_list = []
        all_all_num = 0

        for dir, path, filename in os.walk(open_path):
            json_list = glob.glob(os.path.join(dir, "*.json"))

            for json in json_list:
                all_num, tongji = self.jongji(json)
                all_all_num += all_num

                info_list.append((json, all_num, tongji))

        from workbox.template import saveTemp
        import webbrowser

        html = saveTemp({"list": info_list, "all": all_all_num})
        webbrowser.open(html)


    def jongji(self, json_path):
        all_num = 0
        tongji = deepcopy(self.guize)

        if json_path:
            obj = read_json(json_path)
            for page, value in obj.items():
                all_num += len(value["regions"])

                for region in value["regions"]:
                    if "region_attributes" in region and "page_class_id" in region["region_attributes"]:
                        v = region["region_attributes"]["page_class_id"]
                        try:
                            self.check_id(v, tongji)
                        except Exception as e:
                            print(e, v)
        return all_num, tongji

    def check_id(self, v, tongji):
        for key, value in tongji.items():
            if int(v) in value['list']:
                value["count"] += 1

    def start(self):
        json_file = self.json_file_field.text()
        all_num, tongji = self.jongji(json_file)

        self.tihao_label.setText("框数量: %s \n %s" % (all_num, tongji))
