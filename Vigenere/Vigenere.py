import re
import sys


class VigenereCipher:

    letters_frequencies = {"a": 82, "b": 15, "c": 28, "d": 43, "e": 127,
                           "f": 22, "g": 20, "h": 61, "i": 70, "j": 2,
                           "k": 8, "l": 40, "m": 24, "n": 67, "o": 75,
                           "p": 29, "q": 1, "r": 60, "s": 63, "t": 91,
                           "u": 28, "v": 10, "w": 23, "x": 1, "y": 20, "z": 1}

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def prepare_files(self):

        with open("orig.txt", "r+") as file:
            f = file.read()

        result = ""

        for line in f:
            result += line.lower().strip()
        result = re.sub('\W+', '', result)

        with open("plain.txt", "w") as file:
            file.write(result)

    def prepare(self, file):

        result = ""

        for line in file:
            result += line.lower().strip()
        result = re.sub('\W+', '', result)
        file.seek(0)
        file.truncate()
        file.write(result)

    def get_key_length(self):
        with open("crypto.txt") as file:
            text = file.readline()

        coincidence = []
        avg_repeats = []

        for i in range(1, len(text)-99):
            coincidence.append(sum([1 if a == b else 0 for a, b in zip(text, text[i:])]))
        for i in range(3, 25):
            inner_avg_repeats = []
            for index, value in enumerate(coincidence):
                if (index + 1) % i == 0:
                    sum_arg = 0
                    for inner in range(index + 1 - i, index):
                        sum_arg -= coincidence[inner]
                        sum_arg += value
                    inner_avg_repeats.append(sum_arg)
            avg_repeats.append(sum(inner_avg_repeats)/len(inner_avg_repeats)/i)
        return avg_repeats.index(max(avg_repeats)) + 3

    def encrypt(self):
        with open("key.txt") as file:
            key = file.readline()
        with open("plain.txt") as file:
            f2 = file.read()

        result = ""
        iterator = 0
        key_length = len(key)

        for line in f2:
            for char in line:
                if iterator >= key_length:
                    iterator = 0
                if char != "\n":
                    if char.isupper():
                        result += chr((ord(char) + ord(key[iterator]) - 130) % 26 + 65)
                    else:
                        result += chr((ord(char) + ord(key[iterator]) - 194) % 26 + 97)
                    iterator += 1
                else:
                    result += "\n"

            with open("crypto.txt", "w") as file:
                file.write(result)

    def decrypt(self):

        with open("key-crypto.txt") as file:
            key = file.readline()
        with open("crypto.txt") as file:
            f2 = file.read()

        result = ""
        iterator = 0

        for line in f2:
            for char in line:
                if iterator >= len(key):
                    iterator = 0
                if char != "\n":
                    if (char.isupper()):
                        result += chr((ord(char) - ord(key[iterator])) % 26 + 65)
                    else:
                        result += chr((ord(char) - ord(key[iterator])) % 26 + 97)
                    iterator += 1
                else:
                    result += "\n"

            with open("decrypt.txt", "w") as file:
                file.write(result)

    def cryptanalysis(self):

        letters_frequencies_in_crypto = {}
        result = ""

        with open("crypto.txt") as file:
            message = file.readline()

        key_length = self.get_key_length()

        for key_len_range_shift in range(0, key_length):

            letters_frequencies_in_crypto.clear()
            frequency = 0
            biggest_frequency = 0
            biggest_frequency_alphabet_position = 0
            iterator = 0

            for character in range(key_len_range_shift, len(message), key_length):
                if message[character] not in letters_frequencies_in_crypto:
                    letters_frequencies_in_crypto[message[character]] = 1
                else:
                    letters_frequencies_in_crypto[message[character]] += 1

            for key in letters_frequencies_in_crypto:
                letters_frequencies_in_crypto[key] = \
                    letters_frequencies_in_crypto[key]/len(message)

            while iterator <= len(letters_frequencies_in_crypto):
                for key in letters_frequencies_in_crypto:
                    if ord(key) - iterator < 97:
                        shift = chr(ord(key) - iterator + 25)
                        frequency += self.letters_frequencies[shift] * letters_frequencies_in_crypto[key]
                    else:
                        shift = chr(ord(key) - iterator)
                        frequency += self.letters_frequencies[shift] * letters_frequencies_in_crypto[key]
                iterator += 1

                if biggest_frequency < frequency:
                    biggest_frequency = frequency
                    biggest_frequency_alphabet_position = iterator
                frequency = 0

            result += self.alphabet[biggest_frequency_alphabet_position-1]

        with open("key-crypto.txt", "w") as file:
            file.write(result)


for argument in sys.argv:

    vc = VigenereCipher()

    if argument == "p":
        vc.prepare_files()
    elif argument == "e":
        vc.encrypt()
    elif argument == "d":
        vc.decrypt()
    elif argument == "c":
        vc.cryptanalysis()
