import re
import sys


class VigenereCipher:

    letters_frequencies = {"a": 82, "b": 15, "c": 28, "d": 43, "e": 127, "f": 22, "g": 20, "h": 61, "i": 70, "j": 2,
                           "k": 8, "l": 40, "m": 24, "n": 67, "o": 75, "p": 29, "q": 1, "r": 60, "s": 63, "t": 91,
                           "u": 28, "v": 10, "w": 23, "x": 1, "y": 20, "z": 1}
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def prepare_files(self):
        with open("orig.txt", "r+") as file:
            f = file.read()
        result = ""
        for line in f:
            result += line.lower().strip()
        result = re.sub('\W+', '', result)
        with open("plain.txt", "w") as file:
            file.write(result)

    def key_length(self):
        with open("key.txt") as file:
            k = file.readline()

        k_length = 0

        for line in k:
            for char in line:
                if char != "\n":
                    k_length += 1

        return k_length

    def encrypt(self):
        with open("key.txt") as file:
            k = file.readline()
        with open("plain.txt") as file:
            f2 = file.read()

        result = ""

        i = 0

        for line in f2:
            for char in line:
                if i >= self.key_length():
                    i = 0
                if char != "\n":
                    if (char.isupper()):
                        result += chr((ord(char) + ord(k[i]) - 130) % 26 + 65)
                    else:
                        result += chr((ord(char) + ord(k[i]) - 194) % 26 + 97)
                    i += 1
                else:
                    result += "\n"

            with open("crypto.txt", "w") as file:
                file.write(result)

    def decrypt(self):
        with open("key-crypto.txt") as file:
            k = file.readline()
        with open("crypto.txt") as file:
            f2 = file.read()

        result = ""

        i = 0

        for line in f2:
            for char in line:
                if i >= self.key_length():
                    i = 0
                if char != "\n":
                    if (char.isupper()):
                        result += chr((ord(char) - ord(k[i])) % 26 + 65)
                    else:
                        result += chr((ord(char) - ord(k[i])) % 26 + 97)
                    i += 1
                else:
                    result += "\n"

            with open("decrypt.txt", "w") as file:
                file.write(result)

    def cryptanalysis(self):
        dict = {}
        result = ""

        with open("crypto.txt") as file:
            message = file.readline()

        key_length = 4

        for r in range(0, key_length):
            dict.clear()
            sum = 0
            sum2 = 0
            biggest = 0

            kl = 0
            for x in range(r, len(message), key_length):
                if message[x] not in dict:
                    dict[message[x]] = 1
                else:
                    dict[message[x]] += 1
                    sum += 1
                kl += key_length

            for key in dict:
                dict[key] = dict[key]/sum

            i = 0
            j = 0
            pos = 0

            for counter in dict:
                for key in dict:
                    if ord(key) - i < 97:
                        shift = chr(ord(key) - i + 25)
                        sum2 += self.letters_frequencies[shift] * dict[key]
                    else:
                        shift = chr(ord(key) - i)
                        sum2 += self.letters_frequencies[shift] * dict[key]
                i += 1
                j += 1
                if biggest < sum2:
                    biggest = sum2
                    pos = j
                sum2 = 0
            result += self.alphabet[pos-1]
        with open("key-crypto.txt", "w") as file:
            file.write(result)




for argument in sys.argv:
    print(argument)

    vc = VigenereCipher()

    if argument == "p":
        vc.prepare_files()
    elif argument == "e":
        vc.encrypt()
    elif argument == "d":
        vc.decrypt()
    elif argument == "c":
        vc.cryptanalysis()
