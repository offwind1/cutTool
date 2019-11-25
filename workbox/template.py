from jinja2 import PackageLoader, Environment, FileSystemLoader
from workbox.define import *


def saveTemp(data):
    loader = FileSystemLoader(searchpath=HTML_PATH_TEMP)
    env = Environment(loader=loader)  # 创建一个包加载器对象
    template = env.get_template('base.html')  # 获取一个模板文件

    with open(TEMP_HTML, "w", encoding="utf-8") as f:
        f.write(template.render(**data))
    return TEMP_HTML
