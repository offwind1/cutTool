import sys
import os

from utility import *


class CacaJson():

    def __init__(self, json_data):
        self._json = json_data

    def __iter__(self):
        return self._get_iter()

    def _get_iter(self):
        for key, value in self._json.items():
            yield FileData(key, value)

    def __getitem__(self, item):
        value = self._json.get(item)
        if value:
            return FileData(item, value)
        raise KeyError(item)

    def add_file(self, file):
        self._json.update({
            file.key: file.value
        })

    def merge(self, other):
        for file in other:
            if file in self:
                self[file.key].merge(file)
            else:
                self.add_file(file)

    def filter_region(self, func):
        for file in self:
            for region in file:
                print(2)
                if not func(region):
                    print(1)
                    file.remove(region)

    def pop(self, file):
        self._json.pop(file.key)

    def filter_file(self, func):
        for file in self:
            if not func(file):
                self.pop(file)


class FileData():

    def __init__(self, file_name, file_value):
        self._file_value = file_value
        self._file_name = file_name
        # self.regions = [Region(region) for region in self._file_value["regions"]]

    @property
    def key(self):
        return self._file_name

    @property
    def value(self):
        return self._file_value

    @property
    def regions(self):
        return self._file_value["regions"]

    def __iter__(self):
        return self._get_iter()

    def _get_iter(self):
        for region in self.regions:
            yield Region(region)

    def __eq__(self, other):
        if not isinstance(other, FileData):
            return False

        if self.key != other.key:
            return False

        return True

    def add_region(self, region):
        self.regions.append(region.data)

    def merge(self, other):
        for region in other:
            if region not in self:
                self.add_region(region)

    def filter(self, func):
        for region in self:
            if func(region):
                return

    def remove(self, region):
        self.regions.remove(region.data)


class Region():
    """框 范围，局部"""

    def __init__(self, region_data):
        self._data = region_data

    @property
    def data(self):
        return self._data

    @property
    def region_attributes(self):
        return self._data["region_attributes"]

    @property
    def shape_attributes(self):
        return ShapeAttributes(self._data["shape_attributes"])

    def get_id(self, key="page_class_id"):
        return self.region_attributes[key]

    def get_key_value(self):
        list = []
        for k, v in self.region_attributes.items():
            list.append((k, v))
        return list

    def __eq__(self, other):
        if not isinstance(other, Region):
            return False

        return self.shape_attributes == other.shape_attributes


class ShapeAttributes():

    def __init__(self, attrib):
        self._attr = attrib

    @property
    def name(self):
        return self._attr["name"]

    @property
    def width(self):
        return self._attr["width"]

    @property
    def height(self):
        return self._attr["height"]

    @property
    def org_x(self):
        return self._attr["x"]

    @property
    def org_y(self):
        return self._attr["y"]

    @property
    def opp_x(self):
        return self.org_x + self.width

    @property
    def opp_y(self):
        return self.org_y + self.height

    @property
    def origin(self):
        return (self.org_x, self.org_y)

    @property
    def opposite(self):
        return (self.opp_x, self.opp_y)

    def __eq__(self, other):
        if not isinstance(other, ShapeAttributes):
            return False

        if other.name != self.name:
            return False

        if self.origin != other.origin or self.opposite != other.opposite:
            return False

        return True


def filter_page_class_id_is_30(region: Region):

    if region.get_id("page_class_id") == 30:
        return True
    return False


if __name__ == "__main__":
    a = CacaJson(read_json(r"D:\CODE\python\cuttool\cuttool\save\all.json"))
    # b = CacaJson(read_json(r"D:\CODE\python\cuttool\cuttool\save\no_题号标注.json"))

    a.filter_region(filter_page_class_id_is_30)

    # a.merge(b)
    print(a._json)
