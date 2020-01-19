import math


def option1():

    character = 0
    watermark_string = ""

    with open("mess.txt") as mess:  
        data = mess.read()
        res = "{0:08b}".format(int(data, 16))
    print(res)
    with open("cover.html") as cover:
        for line in cover:
            line = line.strip()
            try:
                if (res[character] == "1"):
                    line += " "
                character += 1
                watermark_string += line + "\n"
                print(line)
            except:
                watermark_string += line + "\n"
    with open("watermark.html", "w") as watermark:
        watermark.write(watermark_string)


def decodeOption1():

    binary_string = ""
    encoded_string = ""
    with open("watermark.html") as watermark:  
        for line in watermark:
            if(line[len(line)-2] == " "):
                binary_string += "1"
            else:
                binary_string += "0"
    print(binary_string)
    
    rounds = len(binary_string)//4
    for i in range(0, rounds, 4):
        if(binary_string[i:i+4] == "0"):break
        encoded_string += ('{:x}'.format(int(binary_string[i:i+4], 2)))

    with open("detect.txt", "w") as detect:
        detect.write(encoded_string)


option1()
decodeOption1()