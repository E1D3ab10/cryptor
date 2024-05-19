import os

from src.const_int import ConstInt


class AbstractEncrypter(object):

    def __init__(self, filename: str):
        if filename is None:
            return
        if not isinstance(filename, str):
            raise TypeError("filename must be string")
        if not os.path.isfile(filename):
            raise ValueError("file does not exist")
        self.filename: str = filename
        self.check_filename(filename, ConstInt.TEXTFMT)

    @staticmethod
    def check_filename(filename: str, fmt: str):
        if filename.rsplit('.', 1)[-1] != fmt:
            raise ValueError("filename is not correct")
