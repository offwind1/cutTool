import ntpath
import os
import re
# import struct
import shutil
import glob
# import cv2
# import numpy as np
import json


# import re
# import random
# from matplotlib import pyplot as plt
# from matplotlib.pyplot import figure


# 根据路径返回文件名
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


# 返回路径头部
def path_head(path):
    head, tail = ntpath.split(path)
    return head or ntpath.basename(head)


# 保存json
def save_json(path, data):
    with open(path, 'w') as f:
        f.write(json.dumps(data))


# 读取json
def read_json(json_path):
    jsons = json.load(open(json_path, encoding="utf-8"))
    data = {}
    for key, value in jsons.items():
        print(key)
        if "." in key:
            file_name = re.findall("(.+?\.[jJpP][pPnN][gG])\d?", key)[0]
            data.update({
                file_name: value
            })
        else:
            data.update({
                key: value
            })

    return data


# file_path：原始图片文件路径
# 递归过程中复制图片: 复制file_path中的所有图片到save_path路径
def copy_images(file_path, image_files, save_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    copy_images_length = 0
    if not image_files:
        image_files = glob.glob(os.path.join(file_path, '*.jpg'))
    #  print(image_files)
    #  image_files.extend(glob.glob(os.path.join(file_path, "*.JPG")))

    for image_path in image_files:
        file_name = path_leaf(image_path)
        #         print(file_name)
        copy_image_path = os.path.join(save_path, file_name)
        #         print(copy_image_path)
        if not os.path.exists(copy_image_path):
            copy_images_length += 1
            shutil.copy(image_path, copy_image_path)
    #     return copy_images_length
    return "{} 拷贝图片 {} 张".format(file_path, len(image_files))


# 递归过程中合并json 自动去重
def merge_json(file_path, image_files, save_path):
    json_paths = glob.glob(os.path.join(file_path, '*.json'))
    #     该目录下没有json文件则不进行拷贝
    merge_json_length = 0
    if len(json_paths) == 0:
        print("{} 路径没有json文件 json合并跳过".format(file_path))
        return "{} 路径没有json文件 json合并跳过".format(file_path)
    json_path = json_paths[0]
    save_json_path = os.path.join(save_path, '_merge.json')
    if os.path.exists(save_json_path):
        json_extend = read_json(save_json_path)
        print('已生成标签数据：', len(json_extend))
    else:
        print('无已生成标签数据')
        json_extend = {}
    annotations = read_json(json_path)
    json_extend = dict(json_extend, **annotations)
    #     print('json_extend length:',json_extend)
    save_json(save_json_path, json_extend)
    return "{} 合并json {}".format(file_path, len(annotations))


# 递归遍历含有图片的文件夹,一旦检测到含有图片,将会执行 recursive_method 方法
# recursive_method 方法包含 file_path,image_files,save_path三个参数
def find_image_paths_recursive(orgin_path, save_path, recursive_method):
    print('orgin_path:', orgin_path)
    if not os.path.isdir(orgin_path):
        print('不是目录', orgin_path)
        return
    images_length = 0
    files = os.listdir(orgin_path)
    for file in files:
        file_path = os.path.join(orgin_path, file)
        print(file_path)
        if os.path.isdir(file_path):
            #             print(json_path)
            image_files = glob.glob(os.path.join(file_path, '*.jpg'))
            image_files.extend(glob.glob(os.path.join(file_path, "*.JPG")))
            if len(image_files) == 0:
                print('无图片：', file_path)
                images_length += \
                    find_image_paths_recursive(file_path, save_path, recursive_method)
            else:
                print(file_path, '目录下图片数量：', len(image_files))
                print('images_length：', images_length)
                images_length += recursive_method(file_path, None, save_path)
    #         else:
    #             images_length += find_image_paths(file_path)
    #     print('进度：{:0.2f}%'.format(images_length/6641*100))

    return images_length


# 在jupyter中显示图片
def show_image(bgr_img, size=[1, 1], title='image'):
    b, g, r = cv2.split(bgr_img)  # get b,g,r
    rgb_img = cv2.merge([r, g, b])  # switch it to rgb
    figure(num=None, figsize=(size[0], size[1]), dpi=100, facecolor='w', edgecolor='k')
    #     image = np.squeeze(image,axis=0)
    plt.imshow(rgb_img)
    plt.title(title)
    plt.show()


# 根据box宽高生成 mask 坐标
def get_positions(x, y, change, max_change1, max_change2):
    if change == 'x':
        change1 = x
        change2 = y
    if change == 'y':
        change1 = y
        change2 = x
    positions1s = []
    positions2s = []
    counts = np.random.randint(5, 6)
    unit = (max_change1 - change1) / counts
    for i in range(counts):

        position1 = change1 + (i + 1) * unit
        if (position1 < max_change1):
            positions1s.append(int(position1))
        else:
            positions1s.append(max_change1 - 1)

        if change2 < max_change2:
            positions2s.append(int(change2))
        else:
            positions2s.append(int(max_change2 - 1))

    if change == 'x':
        return positions1s, positions2s
    if change == 'y':
        return positions2s, positions1s


# 打印 标注数据中 各个 page_class_id 的数量
def get_all_class_count(annotations, region_key='page_class_id'):
    numbers = {}
    chinese_numbers = {}
    english_numbers = {}
    white_pages = {}
    black_pages = {}
    for key, annotation in annotations.items():
        regions = annotation['regions']
        for region in regions:
            region_attributes = region['region_attributes']
            page_class_id = region_attributes[region_key]
            if page_class_id in [1]:
                numbers[key] = annotation
            if page_class_id in [2]:
                chinese_numbers[key] = annotation
            if page_class_id in [3]:
                english_numbers[key] = annotation
            if page_class_id in [4]:
                white_pages[key] = annotation
            if page_class_id in [5]:
                black_pages[key] = annotation
    print('numbers length:', len(numbers))
    print('chinese_numbers length:', len(chinese_numbers))
    print('english_numbers length:', len(english_numbers))
    print('white_pages length:', len(white_pages))
    print('black_pages length:', len(black_pages))


# from tqdm import tqdm_notebook as tqdm

# 遍历json ,for循环中执行自定义的handle_item(key, annotation)
# 以及 handle_region(region,key,annotation)方法处理数据,
# 避免总是需要重复写for循环代码
def loop_annotations(annotations, handle_item=None, handle_region=None):
    handle_result_annotations = {}
    for key, annotation in tqdm(annotations.items()):
        regions = annotation['regions']
        if handle_item is not None:
            if handle_item(key, annotation):
                handle_result_annotations[key] = annotation
        if handle_region is not None:
            for region in regions:
                if handle_region(region, key, annotation):
                    handle_result_annotations[key] = annotation
    return handle_result_annotations


#  将标注有问题的写入到bad_anno.txt中
# example: data_utils.add_bad('test.jpg#错误原因:test reason')
def add_bad(file_name):
    with open('./bad_anno.txt', 'a') as f1:
        f1.write(file_name + os.linesep)


def get_json_list(path):
    return glob.glob(os.path.join(path, '*.json'))


# 获取文件夹下的json文件，默认只有1个
def get_json_file(path):
    json_paths = glob.glob(os.path.join(path, '*.json'))
    merge_json_length = 0
    if len(json_paths) == 0:
        return merge_json_length
    return json_paths[0]


filder = [".jpg", ".JPG"]


def get_filelist_bysplit(path, split_num):
    count = 0
    file_list = [[] for i in range(split_num)]
    for root, dirs, files in os.walk(path):  # 遍历统计
        for each in files:
            if ".jpg" in each or ".JPG" in each:
                file_list[count % split_num].append(each)
            count += 1  # 统计文件夹下文件个数
        break
    return file_list


import time


def split_all_no_json(open_path, save_path, split_num):
    t = time.time()
    file_list = get_filelist_bysplit(open_path, split_num)
    i = 0
    for file_path in glob.iglob(os.path.join(open_path, '*.jpg')):
        save_path_index = os.path.join(save_path, str(i % split_num))
        if not os.path.exists(save_path_index):
            os.mkdir(save_path_index)
        _, file_ = os.path.split(file_path)
        newcopyflie(os.path.join(open_path, file_), os.path.join(save_path_index, file_))
        i += 1
        print(file_, "done")
    print("done", time.time() - t)


def split_all(open_path, save_path, split_num, json_file):
    obj = read_json(json_file)
    file_list = get_filelist_bysplit(open_path, split_num)

    error_file_list = []
    error_path = os.path.join(save_path, "error_file")
    if not os.path.exists(error_path):
        os.mkdir(error_path)

    t = time.time()
    temp = [{} for i in range(split_num)]
    i = 0

    for file_path in glob.iglob(os.path.join(open_path, '*.jpg')):
        save_path_index = os.path.join(save_path, str(i % split_num))
        if not os.path.exists(save_path_index):
            os.mkdir(save_path_index)

        _, file_ = os.path.split(file_path)
        o = obj.get(file_)

        if o:
            temp[i % split_num].update({file_: o})
            newcopyflie(os.path.join(open_path, file_), os.path.join(save_path_index, file_))
            i += 1
        else:
            newcopyflie(os.path.join(open_path, file_), os.path.join(error_path, file_))
            print("error {} 没有匹配的josn内容".format(file_))
            error_file_list.append("{} 没有匹配的josn内容".format(file_))
        print(file_, "done")

    for i, t_obj in enumerate(temp):
        savejson(os.path.join(save_path, str(i), "{}.json".format(i)), t_obj)

    print("done")
    return error_file_list


def _split_all(open_path, save_path, split_num, json_file):
    t = time.time()
    print("read_json", t)
    obj = read_json(json_file)
    print("over", time.time() - t)

    t = time.time()
    print("split_file", t)
    file_list = get_filelist_bysplit(open_path, split_num)
    print("over", time.time() - t)

    error_file_list = []
    error_path = os.path.join(save_path, "error_file")
    if not os.path.exists(error_path):
        os.mkdir(error_path)
    t = time.time()

    for i, list_ in enumerate(file_list):
        save_path_index = os.path.join(save_path, str(i))
        print("save_index", i)
        if not os.path.exists(save_path_index):
            os.mkdir(save_path_index)

        temp = {}
        for file_ in list_:
            o = obj.get(file_)
            print(file_, "done")
            if o:
                temp.update({file_: o})
                newcopyflie(os.path.join(open_path, file_), os.path.join(save_path_index, file_))
            else:
                newcopyflie(os.path.join(open_path, file_), os.path.join(error_path, file_))
                print("error {} 没有匹配的josn内容".format(file_))
                error_file_list.append("{} 没有匹配的josn内容".format(file_))

        savejson(os.path.join(save_path_index, "{}.json".format(i)), temp)

    print("done", time.time() - t)
    return error_file_list


def copy_all(open_path, save_path):
    lis_ = []
    for li in os.listdir(open_path):
        index_path = os.path.join(open_path, li)
        pic, js = copy_images(index_path, None, save_path), merge_json(index_path, "", save_path)
        lis_.append((pic, js))

    print("done")
    return lis_


curpath = os.path.dirname(os.path.abspath(__file__))  # 返回当前文件所在的绝对目录


def newcopyflie(inpath, outpath):
    # print("copy", inpath, outpath)
    if os.path.isfile(inpath):
        shutil.copy(inpath, outpath)
    else:
        print(inpath, "没有找到图片")
    return


def savejson(savepath, data):
    '''
    保存json数据形成文件
    savepath:保存路径
    data:保存数据
    '''
    print("savejson", savepath)
    with open(savepath, 'w') as f:
        f.write(json.dumps(data))
    return


def copytoallfile(src_dir, save_dir, valid):
    '''
    遍历源文件夹内指定格式文件，存到目标文件夹
    src_dir:源文件夹
    save_dir:目标文件夹
    valid:指定格式
    '''
    # curpath = os.path.dirname(__file__)  #返回当前文件所在的目录
    src_path = os.path.join(curpath, src_dir)
    save_path = os.path.join(curpath, save_dir)

    get_ext = lambda f: os.path.splitext(f)[1].lower()

    print('源路径 - ' + src_path)
    print('目标路径 - ' + save_path)
    print('------------------------')
    # name = 1
    result = {}
    for dirpath, dirnames, filenames in os.walk(src_path):
        vaildfiles = [f for f in filenames if get_ext(f) in valid]
        for one in vaildfiles:
            print(one)
            copyfile(os.path.join(dirpath, one), os.path.join(src_path, one))
    return


def copyjsontoallfile(src_dir, save_dir, savename):
    '''
    遍历源文件夹内所有json文件内容，存到目标文件夹
    src_dir:源文件夹
    save_dir:目标文件夹
    '''
    # curpath = os.path.dirname(__file__)  #返回当前文件所在的目录
    src_path = os.path.join(curpath, src_dir)
    save_path = os.path.join(curpath, save_dir)

    get_ext = lambda f: os.path.splitext(f)[1].lower()
    valid = [".json", ".JSON"]
    print('源路径 - ' + src_path)
    print('目标路径 - ' + save_path)
    print('------------------------')

    result = {}
    for dirpath, dirnames, filenames in os.walk(src_path):
        vaildfiles = [f for f in filenames if get_ext(f) in valid]
        for one in vaildfiles:
            print(one)
            annotations = json.load(open(os.path.join(dirpath, one)))
            result = dict(result, **annotations)

    savejson(os.path.join(save_path, savename), result)
    return


def validregionsdata(data):
    for item in data:
        if item['region_attributes'].__contains__('question_number'):
            item['region_attributes']['page_class_id'] = 1
        if item['region_attributes'].__contains__('c_question_number'):
            item['region_attributes']['page_class_id'] = 2
        if item['region_attributes'].__contains__('e_question_number'):
            item['region_attributes']['page_class_id'] = 3
        if item['region_attributes'].__contains__('s_question_number'):
            item['region_attributes']['page_class_id'] = 4
        if item['region_attributes'].__contains__('question_page'):
            item['region_attributes']['page_class_id'] = 101
        if item['region_attributes'].__contains__('question_page_b'):
            item['region_attributes']['page_class_id'] = 102

    return data


def validjsondataforclassID(allimg_dir, number_json_dir, page_json_dir, save_both_dir, save_justnumber_dir,
                            save_justpage_dir):
    src_path = os.path.join(curpath, allimg_dir)
    print("源路径 - ", src_path)
    # 读取json数据
    numberjsondata = json.load(open(os.path.join(curpath, number_json_dir)))
    pagejsondata = json.load(open(os.path.join(curpath, page_json_dir)))

    # cut numberjson中的key  ====== >  (name.type+size) - > (name | type+size)
    cutkeynumbernamejson = []
    cutkeynumbertypejson = []
    for key in numberjsondata.keys():
        cutkeyname, cutkeytype = key.split('.')
        cutkeynumbernamejson.append(cutkeyname)
        cutkeynumbertypejson.append(cutkeytype)
    # cut pagejson中的key  ====== >  (name.type+size) - > (name | type+size)
    cutkeypagenamejson = []
    cutkeypagetypejson = []
    for key in pagejsondata.keys():
        cutkeyname, cutkeytype = key.split('.')
        cutkeypagenamejson.append(cutkeyname)
        cutkeypagetypejson.append(cutkeytype)
    # 保存目标文件夹
    saveboth_path = os.path.join(curpath, save_both_dir)
    savejustnumber_path = os.path.join(curpath, save_justnumber_dir)
    savejustpage_path = os.path.join(curpath, save_justpage_dir)
    print("保存路径both - ", saveboth_path)
    print("保存路径justnumber - ", savejustnumber_path)
    print("保存路径justpage - ", savejustpage_path)
    print('------------------------')
    # 根据图片名称提取
    bothjson_result = {}
    justnumberjson_result = {}
    justpagejson_result = {}
    for dirpath, dirnames, filenames in os.walk(src_path):
        for one in filenames:
            # cut 文件名one  ====== >  (name.type) - > (name | type)
            cutonename, cutonetype = one.split('.')

            # 是否包涵key(因为json文件中key不是文件名,而是文件名+size,所以通过切割进行key匹配)
            hasnumber = cutkeynumbernamejson.__contains__(cutonename)
            haspage = cutkeypagenamejson.__contains__(cutonename)

            if hasnumber == True and haspage == True:
                # number json中key名
                indexofnumber = cutkeynumbernamejson.index(cutonename)
                realkeyofnumber = cutkeynumbernamejson[indexofnumber] + "." + cutkeynumbertypejson[indexofnumber]
                # page json中key名
                indexofpage = cutkeypagenamejson.index(cutonename)
                realkeyofpage = cutkeypagenamejson[indexofpage] + "." + cutkeypagetypejson[indexofpage]
                print("both - ", one)
                # json
                # 处理regions中的数据
                allregions = numberjsondata[realkeyofnumber]['regions'] + pagejsondata[realkeyofpage]['regions']
                allregions = validregionsdata(allregions)

                numberjsondata[realkeyofnumber]['regions'] = allregions

                bothjson_result[realkeyofnumber] = numberjsondata[realkeyofnumber]
                # img
                src = os.path.join(dirpath, one)
                save = os.path.join(saveboth_path, one)
                print(src, " ====> ", " : ", save)
                copyfile(src, save)

            if hasnumber == True and haspage == False:
                print("hasnumber - ", one)
                # number json中key名
                indexofnumber = cutkeynumbernamejson.index(cutonename)
                realkeyofnumber = cutkeynumbernamejson[indexofnumber] + "." + cutkeynumbertypejson[indexofnumber]
                # json
                # 处理regions中的数据
                numberjsondata[realkeyofnumber]['regions'] = validregionsdata(
                    numberjsondata[realkeyofnumber]['regions'])

                justnumberjson_result[realkeyofnumber] = numberjsondata[realkeyofnumber]
                # img
                src = os.path.join(dirpath, one)
                save = os.path.join(savejustnumber_path, one)
                print(src, " ====> ", " : ", save)
                copyfile(src, save)

            if haspage == True and hasnumber == False:
                print("haspage - ", one)
                # page json中key名
                indexofpage = cutkeypagenamejson.index(cutonename)
                realkeyofpage = cutkeypagenamejson[indexofpage] + "." + cutkeypagetypejson[indexofpage]
                # json
                # 处理regions中的数据
                pagejsondata[realkeyofpage]['regions'] = validregionsdata(pagejsondata[realkeyofpage]['regions'])

                justpagejson_result[realkeyofpage] = pagejsondata[realkeyofpage]
                # img
                src = os.path.join(dirpath, one)
                save = os.path.join(savejustpage_path, one)
                print(src, " ====> ", " : ", save)
                copyfile(src, save)

    savejson(os.path.join(saveboth_path, 'bothvia.json'), bothjson_result)
    savejson(os.path.join(savejustnumber_path, 'justnumbernvia.json'), justnumberjson_result)
    savejson(os.path.join(savejustpage_path, 'justpagevia.json'), justpagejson_result)

    return


def copyfile(infile, outfile):
    try:
        shutil.copyfile(infile, outfile)
    except:
        print('Can t open this file')

    return


def saveimg(infile, outfile):
    image = cv2.imread(infile, flags=cv2.IMREAD_COLOR)
    cv2.imwrite(outfile, image)
    return
