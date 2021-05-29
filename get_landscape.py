from PIL import Image


def get_landscape(filename, _a):
    image = Image.open(filename)
    _width = image.size[0]
    _height = image.size[1]
    pix = image.load()
    landscape = []
    if image.mode == "L":
        for _x in range(_width):
            landscape.append([])
            for _y in range(_height):
                landscape[_x].append(pix[_x, _y] / (3 * _a))
    elif image.mode == "RGB":
        for _x in range(_width):
            landscape.append([])
            for _y in range(_height):
                landscape[_x].append((pix[_x, _y][0] + pix[_x, _y][1] + pix[_x, _y][2]) / (9 * _a))
    else:
        image = image.convert("RGB")
        pix = image.load()
        for _x in range(_width):
            landscape.append([])
            for _y in range(_height):
                landscape[_x].append((pix[_x, _y][0] + pix[_x, _y][1] + pix[_x, _y][2]) / (9 * _a))
    return landscape, _width, _height
