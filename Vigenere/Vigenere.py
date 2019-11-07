import re
import sys


class VigenereCipher:

    def prepare(self):
        result = ""
        with open("key.txt", "r+") as file:
            for line in file:
                result += line.lower().strip()
            result = re.sub('\W+', '', result)
            file.seek(0)
            file.truncate()
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

                print(result)
            with open("encrypt.txt", "w") as file:
                file.write(result)


    def decrypt(self):
        with open("key.txt") as file:
            k = file.readline()
        with open("encrypt.txt") as file:
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

                print(result)
            with open("decrypt.txt", "w") as file:
                file.write(result)


for argument in sys.argv:
    print(argument)

    vc = VigenereCipher()

    if argument == "p":
        vc.prepare()
    elif argument == "e":
        vc.encrypt()
    elif argument == "d":
        vc.decrypt()
