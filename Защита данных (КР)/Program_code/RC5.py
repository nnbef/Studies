from hashlib import md5


class RC5:
    def __init__(self, w, R, passphrase, key_len=128, mode='ecb'):
        self.w = w  # block size (32, 64 or 128 bits)
        self.R = R  # number of rounds (0 to 255)
        self.key = self.generate_key(passphrase=passphrase, key_len=key_len)  # key (0 to 2040 bits)
        self.mode = mode

        self.salt = "1234".encode(encoding='cp1251')  # salt for passphrase verification
        self.T = 2 * (R + 1)
        self.w4 = w // 4
        self.w8 = w // 8
        self.mod = 2 ** self.w
        self.mask = self.mod - 1
        self.b = len(self.key)

        self.__key_align()
        self.__key_extend()
        self.__shuffle()

    def get_iv(self):
        if self.w == 16:
            return 'абвг'.encode(encoding='cp1251')
        elif self.w == 32:
            return 'абвгдежз'.encode(encoding='cp1251')
        elif self.w == 64:
            return 'абвгдежзеклмопрс'.encode(encoding='cp1251')

    @staticmethod
    def xor(x, y):
        return bytes(a ^ b for a, b in zip(x, y))

    @staticmethod
    def generate_key(passphrase, key_len):
        passphrase += 'qWeR123АбВ'
        hash = md5(passphrase.encode(encoding='cp1251')).hexdigest()
        key = ''
        for elem in hash:
            x = bin(elem.encode(encoding='cp1251')[0])[2:]
            if len(x) < 8:
                temp = '0' * (8 - len(x)) + x
            else:
                temp = x
            key += temp
        if len(key) < key_len:
            key = '0' * (key_len - len(key)) + key
        key = key[:key_len]
        if len(key) % 8 != 0:
            key = '0' * (8 - (len(key) % 8)) + key
        return bytes(int(key[i:i + 8], 2) for i in range(0, len(key), 8))

    def __lshift(self, val, n):
        n %= self.w
        return ((val << n) & self.mask) | ((val & self.mask) >> (self.w - n))

    def __rshift(self, val, n):
        n %= self.w
        return ((val & self.mask) >> n) | (val << (self.w - n) & self.mask)

    def __const(self):  # constants generation
        if self.w == 16:
            return 0xB7E1, 0x9E37  # return P, Q values
        elif self.w == 32:
            return 0xB7E15163, 0x9E3779B9
        elif self.w == 64:
            return 0xB7E151628AED2A6B, 0x9E3779B97F4A7C15

    def __key_align(self):
        if self.b == 0:  # key is empty
            self.c = 1
        elif self.b % self.w8:
            self.key += b'\x00' * (self.w8 - self.b % self.w8)  # fill key with \x00 bytes
            self.b = len(self.key)
            self.c = self.b // self.w8
        else:
            self.c = self.b // self.w8
        L = [0] * self.c
        for i in range(self.b - 1, -1, -1):
            L[i // self.w8] = (L[i // self.w8] << 8) + self.key[i]
        self.L = L

    def __key_extend(self):
        P, Q = self.__const()
        self.S = [(P + i * Q) % self.mod for i in range(self.T)]

    def __shuffle(self):
        i, j, A, B = 0, 0, 0, 0
        for k in range(3 * max(self.c, self.T)):
            A = self.S[i] = self.__lshift((self.S[i] + A + B), 3)
            B = self.L[j] = self.__lshift((self.L[j] + A + B), A + B)
            i = (i + 1) % self.T
            j = (j + 1) % self.c

    def encrypt_block(self, data):
        A = int.from_bytes(data[:self.w8], byteorder='little')
        B = int.from_bytes(data[self.w8:], byteorder='little')
        A = (A + self.S[0]) % self.mod
        B = (B + self.S[1]) % self.mod
        for i in range(1, self.R + 1):
            A = (self.__lshift((A ^ B), B) + self.S[2 * i]) % self.mod
            B = (self.__lshift((A ^ B), A) + self.S[2 * i + 1]) % self.mod
        return (A.to_bytes(self.w8, byteorder='little')
                + B.to_bytes(self.w8, byteorder='little'))

    def decrypt_block(self, data):
        A = int.from_bytes(data[:self.w8], byteorder='little')
        B = int.from_bytes(data[self.w8:], byteorder='little')
        for i in range(self.R, 0, -1):
            B = self.__rshift(B - self.S[2 * i + 1], A) ^ A
            A = self.__rshift(A - self.S[2 * i], B) ^ B
        B = (B - self.S[1]) % self.mod
        A = (A - self.S[0]) % self.mod
        return (A.to_bytes(self.w8, byteorder='little')
                + B.to_bytes(self.w8, byteorder='little'))

    def encrypt_bytes(self, data):
        res, run = b'', True
        data = self.salt + data
        if self.mode == 'ecb':
            while run:
                temp = data[:self.w4]
                if len(temp) != self.w4:
                    data = data.ljust(self.w4, b'\x00')
                    run = False
                res += self.encrypt_block(temp)
                data = data[self.w4:]
                if not data:
                    break
        elif self.mode == 'cbc':
            pred = self.get_iv()
            while run:
                temp = data[:self.w4]
                if len(temp) != self.w4:
                    data = data.ljust(self.w4, b'\x00')
                    run = False
                pred = self.encrypt_block(self.xor(temp, pred))
                res += pred
                data = data[self.w4:]
                if not data:
                    break
        elif self.mode == 'cfb':
            pred = self.get_iv()
            while run:
                temp = data[:self.w4]
                if len(temp) != self.w4:
                    data = data.ljust(self.w4, b'\x00')
                    run = False
                pred = self.xor(temp, self.encrypt_block(pred))
                res += pred
                data = data[self.w4:]
                if not data:
                    break
        elif self.mode == 'ofb':
            pred = self.get_iv()
            while run:
                temp = data[:self.w4]
                if len(temp) != self.w4:
                    data = data.ljust(self.w4, b'\x00')
                    run = False
                pred = self.encrypt_block(pred)
                res += self.xor(temp, pred)
                data = data[self.w4:]
                if not data:
                    break
        return res

    def decrypt_bytes(self, data):
        res, run = b'', True
        if self.mode == 'ecb':
            while run:
                temp = data[:self.w4]
                if len(temp) != self.w4:
                    run = False
                res += self.decrypt_block(temp)
                data = data[self.w4:]
                if not data:
                    break
        elif self.mode == 'cbc':
            pred = self.get_iv()
            while run:
                temp = data[:self.w4]
                if len(temp) != self.w4:
                    run = False
                res += self.xor(self.decrypt_block(temp), pred)
                pred = temp
                data = data[self.w4:]
                if not data:
                    break
        elif self.mode == 'cfb':
            pred = self.get_iv()
            while run:
                temp = data[:self.w4]
                if len(temp) != self.w4:
                    run = False
                pred = self.encrypt_block(pred)
                res += self.xor(temp, pred)
                pred = temp
                data = data[self.w4:]
                if not data:
                    break
        elif self.mode == 'ofb':
            pred = self.get_iv()
            while run:
                temp = data[:self.w4]
                if len(temp) != self.w4:
                    run = False
                pred = self.encrypt_block(pred)
                res += self.xor(temp, pred)
                data = data[self.w4:]
                if not data:
                    break
        if res[:len(self.salt)] == self.salt:
            res = res[len(self.salt):]
        else:
            raise Exception('Неверная парольная фраза')
        return res

    def encrypt_file(self, inp_file_name):
        with open(inp_file_name, 'r', encoding='utf-8') as file:
            return self.encrypt_bytes(file.read().encode(encoding='cp1251'))

    def decrypt_file(self, inp_file_name):
        with open(inp_file_name, 'r') as file:
            return self.decrypt_bytes(file.read().encode(encoding='cp1251'))
