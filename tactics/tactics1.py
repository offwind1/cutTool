import os

def check_key(key, open_path):
    if key:
        if os.path.isfile(os.path.join(open_path, key)):
            return True
        else:
            raise KeyException(key, "图片不存在")
    else:
        raise KeyException(key, "文件名不规范")


def check_attributes(attributes, index):
    global key

    ex = None
    for k, v in attributes.items():
        if not v:
            e = ValueException(key, "第{}的{}为空".format(index,k))
            ex = ex + e if ex else e
    if ex:
        raise ex

def check_region_attributes(attributes, index):
    global key
    flag = 0
    ex = None

    for k, v in attributes.items():
        if k.lower() == "page_class_id":
            flag +=1
            if not k.islower():
                e = ValueException(key, "第{}的{}不全为小写".format(index+1,k))
                ex = ex + e if ex else e

    if flag!=1:
        e = ValueException(key, "第{}的{}存在{}个".format(index+1,k,flag))
        ex = ex + e if ex else e

    if ex: raise ex

def check_regions(key, regions:list):
    if not regions:
        raise ValueException(key, "regions为空")

    ex = None
    for index, attrib in enumerate(regions):
        try:
            check_region_attributes(attrib.get("region_attributes"), index)
        except ValueException as e:
            ex = ex + e if ex else e
    if ex:
        raise ex

def check_json(value:dict, key, open_path):
    # check_key(key, open_path)
    check_regions(key, value.get("regions"))

check_json(value, key, open_path)
