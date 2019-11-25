from model.window import *
from model.model import *
# from workbox.workbox import *
from workbox.utility import *


class EmptyWindow(BaseWidget):

    def setField(self):
        self.open_path_field = PathField(self, "选择图片源")
        self.save_path_field = PathField(self, "保存图片路径")

    def setWidget(self):
        self.start_button = QPushButton("执行", self)
        self.addWidget(self.start_button)
        self.start_button.clicked.connect(self.get_empty)

    def get_empty(self):
        open_path = self.open_path_field.text()
        save_path = self.save_path_field.text()

        get_empty(open_path, save_path)


def get_empty(open_path, save_path, out_pass=True, move=False):
    pass_path = os.path.join(save_path, "pass")
    error_path = os.path.join(save_path, "json中的图不存在")
    empty_path = os.path.join(save_path, "图不存在json中")

    if not os.path.exists(error_path):
        os.mkdir(error_path)
    if not os.path.exists(empty_path):
        os.mkdir(empty_path)

    json_obj = read_josn_from_path(open_path)
    pic_list = get_pic_path_list(open_path)

    josn_set = set(json_obj)
    pic_set = set(pic_list)

    # josn中有key，但没有图片。error
    print("检查 json中的图不存在")
    save_json(os.path.join(error_path, "no_pic.json"), get_in_set_json(josn_set - pic_set, json_obj))

    # 有图片，但json中无key。empty
    print("检查 图不存在json中")
    if move:
        move_move_files(pic_set - josn_set, open_path, empty_path)
    else:
        move_files(pic_set - josn_set, open_path, empty_path)

    # 有图片有key。pass
    pass_set = josn_set & pic_set
    if out_pass:

        if not os.path.exists(pass_path):
            os.mkdir(pass_path)
        save_json(os.path.join(pass_path, "all.json"), get_in_set_json(pass_set, json_obj))

        if move:
            move_move_files(pass_set, open_path, pass_path)
        else:
            move_files(pass_set, open_path, pass_path)

    return get_in_set_json(pass_set, json_obj)