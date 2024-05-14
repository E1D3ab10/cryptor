import itertools
from src.abstract_encryptor import AbstractEncrypter
from src.const_int import ConstInt


class MessageEncrypter(AbstractEncrypter):
    def __init__(self, text):
        super().__init__(None)
        if not isinstance(text, str):
            raise ValueError("Invalid text type")
        self.text = text

    def caesar_encrypt(self, key: int):
        encr_table = {i: ConstInt.MINSYMB + (i - ConstInt.MINSYMB + key) % (ConstInt.MAXSYMB - ConstInt.MINSYMB)
                      for i in range(ConstInt.MINSYMB, ConstInt.MAXSYMB)}
        return self.text.translate(encr_table)

    def caesar_decrypt(self, key: int):
        return self.caesar_encrypt(-key)

    def vigenere_encrypt(self, key: str):
        enc_iter = itertools.cycle(map(ord, key))
        ans = []
        for symb in self.text:
            if ConstInt.MINSYMB <= ord(symb) < ConstInt.MAXSYMB:
                ans.append(chr(ConstInt.MINSYMB + (ord(symb) + next(enc_iter) - ConstInt.MINSYMB) %
                               (ConstInt.MAXSYMB - ConstInt.MINSYMB)))
            else:
                ans.append(symb)
        return ''.join(ans)

    def vigenere_decrypt(self, key: str):
        enc_iter = itertools.cycle(map(ord, key))
        ans = []
        for symb in self.text:
            if ConstInt.MINSYMB <= ord(symb) < ConstInt.MAXSYMB:
                ans.append(chr(ConstInt.MINSYMB + (ord(symb) - next(enc_iter) - ConstInt.MINSYMB) %
                               (ConstInt.MAXSYMB - ConstInt.MINSYMB)))
            else:
                ans.append(symb)
        return ''.join(ans)
