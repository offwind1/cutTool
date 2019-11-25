
class MyException(Exception):
    def __init__(self, key, value):
        super().__init__()
        self.key = key
        self.err_list = [value]

    def __add__(self, obj):
        self.err_list = self.err_list + obj.err_list
        return self

    def __str__(self):
        return """
{}:-----------------
{}
--------------------
""".format(self.key, "\n".join(self.err_list))

class KeyException(MyException):
    pass

class ValueException(MyException):
    pass
