import sys
from PyQt5.QtWidgets import QApplication
from model.window import *
from widget import *


class Window2(MainWindow):
    def __init__(self):
        super().__init__()

        self.addWindow(CheckCombineWindow(), "效验并合并")
        self.addWindow(CheckWindow(), "效验")
        self.addWindow(SplitWindow(), "分割")
        self.addWindow(WorkWindow(), "标注")
        self.addWindow(CombineWindow(), "合并")
        self.addWindow(TongJiWindow(), "统计")
        self.addWindow(EmptyWindow(), "提空")
        self.addWindow(SpotCheckWindow(), "抽查")


class Window(MainWindow):
    def __init__(self):
        super().__init__()

        self.addWindow(SplitWindow(), "分割")
        self.addWindow(CombineWindow(), "合并")
        self.addWindow(PriorityCombineWindow(), "优劣合并")
        self.addWindow(Jiaoji(), "交集")
        self.addWindow(Extract(), "提取")
        self.addWindow(Replace(), "替换")
        self.addWindow(Check(), "检查")
        self.addWindow(Analysis(), "解析")
        self.addWindow(Filter(), "过滤")
        self.addWindow(RemoveDuplicates(), "去重")

        self.addSeparator()
        # self.addWindow(CheckCombineWindow(), "效验并合并")
        self.addWindow(CheckWindow(), "效验")
        self.addWindow(TongJiWindow(), "统计")
        self.addWindow(EmptyWindow(), "提空")
        self.addWindow(SpotCheckWindow(), "抽查")

        self.addSeparator()
        self.addWindow(WorkWindow(), "标注")


def start2():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start2()
