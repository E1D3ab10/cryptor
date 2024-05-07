import collections
import itertools
import json
import string
import os
__all__ = ['TextEncrypter',  'MessageEncrypter']


class AbstractEncrypter(object):
    MAXsymb: int = 127
    MINsymb: int = 32
    TEXTFMT: str = 'txt'

    def __init__(self, filename: str):
        if filename is None:
            return
        if not isinstance(filename, str):
            raise TypeError("filename must be string")
        if not os.path.isfile(filename):
            raise ValueError("file does not exist")
        self.filename: str = filename
        self.check_filename(filename, self.TEXTFMT)

    @staticmethod
    def check_filename(filename: str, fmt: str):
        if filename.rsplit('.', 1)[-1] != fmt:
            raise ValueError("filename is not correct")


class TextEncrypter(AbstractEncrypter):
    def __init__(self, filename: str):
        super().__init__(filename)
        with open(filename, encoding='utf8') as file:
            self.text = file.read()

    def caesar_encrypt(self, key: int, printfile=None):
        if printfile is None:
            printfile = self.filename
        else:
            self.check_filename(printfile, self.TEXTFMT)
        encr_table = {i: self.MINsymb + (i - self.MINsymb + key) % (self.MAXsymb - self.MINsymb)
                      for i in range(self.MINsymb, self.MAXsymb)}
        with open(printfile, 'w') as pfile:
            pfile.write(self.text.translate(encr_table))

    def xor_encrypt(self, filekey: str, printfile=None):
        if printfile is None:
            printfile = self.filename
        if not os.path.isfile(filekey):
            self.check_filename(filekey, self.TEXTFMT)
            raise ValueError("Invalid key")
        with open(filekey) as file:
            enc_string = file.read()
        if len(enc_string) != len(self.text):
            raise ValueError("Invalid key")
        with open(printfile, 'w') as pfile:
            for symb, ksymb in zip(self.text, enc_string):
                pfile.write(chr(ord(symb) ^ ord(ksymb)))

    def vigenere_encrypt(self, filekey: str, printfile=None):
        if printfile is None:
            printfile = self.filename
        if not os.path.isfile(filekey):
            self.check_filename(filekey, self.TEXTFMT)
            raise ValueError("Invalid key")
        with open(filekey) as file:
            enc_string = file.read()
        if not all(self.MINsymb <= ord(i) < self.MAXsymb for i in enc_string):
            print(repr(enc_string))
            raise ValueError("Invalid key")
        enc_iter = itertools.cycle(map(ord, enc_string))
        with open(printfile, 'w') as pfile:
            for symb in self.text:
                if self.MINsymb <= ord(symb) < self.MAXsymb:
                    pfile.write(chr(self.MINsymb + (ord(symb) + next(enc_iter) - self.MINsymb) %
                                    (self.MAXsymb - self.MINsymb)))
                else:
                    pfile.write(symb)

    def caesar_decrypt(self, key: int, printfile=None):
        self.caesar_encrypt(-key, printfile)

    def xor_decrypt(self, filekey: str, printfile=None):
        self.xor_encrypt(filekey, printfile)

    def vigenere_decrypt(self, filekey: str, printfile=None):
        with open(filekey) as file:
            enc_string = file.read()
        if not os.path.isfile(filekey):
            self.check_filename(filekey, self.TEXTFMT)
            raise ValueError("Invalid key")
        if not all(self.MINsymb <= ord(i) < self.MAXsymb for i in enc_string):
            raise ValueError("Invalid key")
        enc_iter = itertools.cycle(enc_string)
        with open(printfile, 'w') as pfile:
            for symb in self.text:
                if self.MINsymb <= ord(symb) < self.MAXsymb:
                    pfile.write(chr(self.MINsymb + (ord(symb) - self.MINsymb - ord(next(enc_iter))) %
                                    (self.MAXsymb - self.MINsymb)))
                else:
                    pfile.write(symb)

    def break_caesar(self, freqtable: str, printfile=None):
        if not os.path.isfile(freqtable):
            self.check_filename(freqtable, 'json')
            raise ValueError("Invalid frequency table")
        with open('freq.json') as f:
            ftable = collections.Counter(json.load(f))
        if printfile is None:
            printfile = self.filename
        c = collections.Counter((i for i in self.text.lower() if i in string.ascii_lowercase))
        trdct = {}
        for pair1, pair2 in zip(c.most_common(len(c)), ftable.most_common(len(c))):
            trdct[ord(pair1[0])] = ord(pair2[0])
            trdct[ord(pair1[0]) - 32] = ord(pair2[0]) - 32
        with open(printfile, 'w') as pfile:
            pfile.write(self.text.translate(trdct))


class MessageEncrypter(AbstractEncrypter):
    def __init__(self, text):
        super().__init__(None)
        if not isinstance(text, str):
            raise ValueError("Invalid text type")
        self.text = text

    def caesar_encrypt(self, key:int):
        encr_table = {i: self.MINsymb + (i - self.MINsymb + key) % (self.MAXsymb - self.MINsymb)
                      for i in range(self.MINsymb, self.MAXsymb)}
        return self.text.translate(encr_table)

    def caesar_decrypt(self, key: int):
        return self.caesar_encrypt(-key)

    def vigenere_encrypt(self, key: str):
        enc_iter = itertools.cycle(map(ord, key))
        ans = []
        for symb in self.text:
            if self.MINsymb <= ord(symb) < self.MAXsymb:
                ans.append(chr(self.MINsymb + (ord(symb) + next(enc_iter) - self.MINsymb) %
                                (self.MAXsymb - self.MINsymb)))
            else:
                ans.append(symb)
        return ''.join(ans)

    def vigenere_decrypt(self, key: str):
        enc_iter = itertools.cycle(map(ord, key))
        ans = []
        for symb in self.text:
            if self.MINsymb <= ord(symb) < self.MAXsymb:
                ans.append(chr(self.MINsymb + (ord(symb) - next(enc_iter) - self.MINsymb) %
                                (self.MAXsymb - self.MINsymb)))
            else:
                ans.append(symb)
        return ''.join(ans)