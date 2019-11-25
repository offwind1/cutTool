from model.window import *
from model.model import *
from workbox.workbox import *
from workbox.define import *
import webbrowser


class WorkWindow(BaseWidget):

    def setWidget(self):
        self.open_button = QPushButton("打开标注网站", self)
        self.addWidget(self.open_button)
        self.open_button.clicked.connect(self.start_open)

        self.button2 = QPushButton("打开标准规范", self)
        self.addWidget(self.button2)
        self.button2.clicked.connect(self.open2)

        self.button3 = QPushButton("打开割图工具说明文档", self)
        self.addWidget(self.button3)
        self.button3.clicked.connect(self.open3)

    def start_open(self):
        # os.popen(HTML_INDEX)
        webbrowser.open(HTML_INDEX)

    def open2(self):
        webbrowser.open(
            "https://docs.qq.com/doc/DWlFHWEd3alVtckts?opendocxfrom=admin&tdsourcetag=s_macqq_aiomsg&ADUIN=759584571&ADSESSION=1554770627&ADTAG=CLIENT.QQ.5603_.0&ADPUBNO=26882")
        """https://docs.qq.com/doc/DWlFHWEd3alVtckts?opendocxfrom=admin&tdsourcetag=s_macqq_aiomsg&ADUIN=759584571&ADSESSION=1554770627&ADTAG=CLIENT.QQ.5603_.0&ADPUBNO=26882"""

    def open3(self):
        webbrowser.open(
            "https://shimo.im/docs/hr9P9wv6g8DTg6HK")

    """https://shimo.im/docs/hr9P9wv6g8DTg6HK/ 《割图工具功能说明文档》，可复制链接后用石墨文档 App 或小程序打开"""