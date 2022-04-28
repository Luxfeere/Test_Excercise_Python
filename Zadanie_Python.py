import sys


class Color:
    def __init__(self, red, green, blue, alpha):
        self.r = red
        self.g = green
        self.b = blue
        self.a = alpha


def data_parsing(data_line, line_number):
    try:
        color_hex_format = 0
        data_line.index(',')
    except ValueError:
        color_hex_format = 1
    if color_hex_format:
        try:
            color_red = int(data_line[0:2], 16)
            color_green = int(data_line[2:4], 16)
            color_blue = int(data_line[4:6], 16)
            color_alpha = int(data_line[6:8], 16)
            if (color_alpha>255 or color_alpha<0 or color_red>255 or color_red<0 or color_green>255 or
                color_green<0 or color_blue>255 or color_blue<0):
                raise ValueError
            if len(data_line) > 9:
                print("Line ", line_number, " in file is too long, some data can be lost")
            return (color_red, color_green, color_blue, color_alpha)
        except ValueError:
            print("Error during hex color parsing in line: ", line_number)
            return 0
    else:
        try:
            first_comma = data_line.index(',')
            second_comma = data_line.index(',', first_comma + 1)
            third_comma = data_line.index(',', second_comma + 1)
            color_red = int(data_line[0:first_comma])
            color_green = int(data_line[first_comma + 1:second_comma])
            color_blue = int(data_line[second_comma + 1:third_comma])
            color_alpha = int(data_line[third_comma + 1:len(data_line)])
            if (color_alpha>255 or color_alpha<0 or color_red>255 or color_red<0 or color_green>255 or
                color_green<0 or color_blue>255 or color_blue<0):
                raise ValueError
            if len(data_line) > 16:
                print("Line ", line_number, " in file is too long, some data can be lost")
            return (color_red, color_green, color_blue, color_alpha)

        except ValueError:
            print("Error during decimal color parsing in line: ", line_number)
            return 0


def hue_calculating(red, green, blue):
    try:
        if red==green==blue:
            print("All RGB values are the same - can't calculate hue")
            return 0
        elif red >= green >= blue:
            return 60 * (green - blue) / (red - blue)
        elif green > red >= blue:
            return 60 * (2 - (red - blue) / (green - blue))
        elif green >= blue > red:
            return 60 * (2 + (blue - red) / (green - red))
        elif blue > green > red:
            return 60 * (4 - (green - red) / (blue - red))
        elif blue > red >= green:
            return 60 * (4 + (red - green) / (blue - green))
        elif red >= blue > green:
            return 60 * (6 - (blue - green) / (red - green))
    except ZeroDivisionError:
        print("Dividing by zero in hue calculations")


def saturation_calculating(red, green, blue, lightness):
    if lightness == 1:
        return 0
    else:
        rgb = [red / 255, green / 255, blue / 255]
        return (max(rgb) - min(rgb)) / (1 - (2 * lightness - 1))


def lightness_calculating(red, green, blue):
    rgb = [red / 255, green / 255, blue / 255]
    return 0.5 * (max(rgb) + min(rgb))


# Data parsing from file and CLI
Color_Matrix = []
try:
    try:
        if sys.argv[1] == '-m' or sys.argv[1] == '--mode' and sys.argv[2] == 'MODE':  # mode selection
            if sys.argv[3] == 'mix':
                mode = 0
            elif sys.argv[3] == 'lowest':
                mode = 1
            elif sys.argv[3] == 'highest':
                mode = 2
            elif sys.argv[3] == 'mix-saturate':
                mode = 3
            else:
                mode = 0
            for i in range(4, len(sys.argv)):
                result = (data_parsing(sys.argv[i], i))
                if result != 0:
                    Color_Matrix.append(Color(result[0], result[1], result[2], result[3]))
        else:
            mode = 0
            for i in range(1, len(sys.argv)):
                result = (data_parsing(sys.argv[i], i))
                if result != 0:
                    Color_Matrix.append(Color(result[0], result[1], result[2], result[3]))
    except:
        print("Mode set to default, mix")

except:
    print("Error during parsing CLI arguments.")
try:
    file = open("color.txt", "r")
    line = 0

    if file.readable():
        while True:
            data = file.readline()
            line = line + 1
            if not data:
                break
            result = data_parsing(data, line)
            if result != 0:
                Color_Matrix.append(Color(result[0], result[1], result[2], result[3]))
        file.close()
except IOError:
    print("Error during opening the file.")
except ValueError:
    print("Error during file parsing.")
except:
    print("Unexpected Error during file parsing.")
try:
    if mode == 0 or mode == 3:
        red = int(sum(Color.r for Color in Color_Matrix) / len(Color_Matrix))
        green = int(sum(Color.g for Color in Color_Matrix) / len(Color_Matrix))
        blue = int(sum(Color.b for Color in Color_Matrix) / len(Color_Matrix))
        alpha = int(sum(Color.a for Color in Color_Matrix) / len(Color_Matrix))
    elif mode == 1:
        red = min(Color.r for Color in Color_Matrix)
        green = min(Color.g for Color in Color_Matrix)
        blue = min(Color.b for Color in Color_Matrix)
        alpha = min(Color.a for Color in Color_Matrix)
    elif mode == 2:
        red = max(Color.r for Color in Color_Matrix)
        green = max(Color.g for Color in Color_Matrix)
        blue = max(Color.b for Color in Color_Matrix)
        alpha = max(Color.a for Color in Color_Matrix)
    hue = hue_calculating(red, green, blue)
    lightness = lightness_calculating(red, green, blue)
    saturation = saturation_calculating(red, green, blue, lightness)
    hex_value = str(hex(red)[2:]) + str(hex(green)[2:]) + str(hex(blue)[2:]) + str(hex(alpha)[2:])
    if mode == 3:
        hex_value = str(hex(Color_Matrix[-1].r)[2:]) + str(hex(Color_Matrix[-1].g)[2:]) + str(hex(Color_Matrix[-1].b)[2:]) + str(hex(Color_Matrix[-1].a)[2:])
        hue = hue_calculating(Color_Matrix[-1].r, Color_Matrix[-1].g, Color_Matrix[-1].b)
        lightness = lightness_calculating(Color_Matrix[-1].r, Color_Matrix[-1].g, Color_Matrix[-1].b)
        print("New color contains: red=", Color_Matrix[-1].r, " green:", Color_Matrix[-1].g, " blue:",
              Color_Matrix[-1].b, " aplha:", Color_Matrix[-1].a, " hex:", hex_value, " hue:", round(hue,3),
              " saturation:", round(saturation, 3), " lightness:", round(lightness, 3))
    else:
        print("New color contains: red=", red, " green:", green, " blue:", blue, " aplha:"
              , alpha, " hex:", hex_value, " hue:", round(hue,3), " saturation:", round(saturation, 3),
              " lightness:", round(lightness, 3))
except:
    print("Error during calculations")
