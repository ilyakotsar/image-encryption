import numpy as np
from PIL import Image


def rail_fence_encrypt(text, key):
    if 1 < key < len(text):
        rail = [['\n' for i in range(len(text))] for j in range(key)]
        dir_down = False
        row, col = 0, 0
        for i in range(len(text)):
            if (row == 0) or (row == key - 1):
                dir_down = not dir_down
            rail[row][col] = text[i]
            col += 1
            if dir_down:
                row += 1
            else:
                row -= 1
        result = []
        for i in range(key):
            for j in range(len(text)):
                if rail[i][j] != '\n':
                    result.append(rail[i][j])
        return result
    else:
        return text


def rail_fence_decrypt(cipher, key):
    if 1 < key < len(cipher):
        rail = [['\n' for i in range(len(cipher))] for j in range(key)]
        dir_down = None
        row, col = 0, 0
        for i in range(len(cipher)):
            if row == 0:
                dir_down = True
            if row == key - 1:
                dir_down = False
            rail[row][col] = '*'
            col += 1
            if dir_down:
                row += 1
            else:
                row -= 1
        index = 0
        for i in range(key):
            for j in range(len(cipher)):
                if ((rail[i][j] == '*') and
                   (index < len(cipher))):
                    rail[i][j] = cipher[index]
                    index += 1
        result = []
        row, col = 0, 0
        for i in range(len(cipher)):
            if row == 0:
                dir_down = True
            if row == key-1:
                dir_down = False
            if (rail[row][col] != '*'):
                result.append(rail[row][col])
                col += 1
            if dir_down:
                row += 1
            else:
                row -= 1
        return result
    else:
        return cipher


def resize_image(im):
    x, y = im.size
    if x > y:
        height = round(500 * y / x)
        width = 500
    else:
        width = round(500 * x / y)
        height = 500
    im = im.resize((width, height), Image.ANTIALIAS)
    return im


def get_pixels(im, width, height):
    colors = []
    for r in range(0, width):
        for c in range(0, height):
            color = im.getpixel((r, c))
            colors.append(color)
    return colors


def generate_and_save_image(colors, width, height, filename):
    new_im = Image.new('RGB', (width, height))
    new_image = np.array(new_im)
    i = 0
    for r in range(0, width):
        for c in range(0, height):
            re = colors[i][0]
            gr = colors[i][1]
            bl = colors[i][2]
            new_image[c][r] = [re, gr, bl]
            i += 1
    new_img = Image.fromarray(new_image, 'RGB')
    new_img.save(filename)


def encrypt_image(input_filename, output_filename, password):
    im = Image.open(input_filename)
    width, height = im.size
    if width > 500 or height > 500:
        im = resize_image(im)
        width, height = im.size
    colors = get_pixels(im, width, height)
    encrypted = colors
    for i in password:
        encrypted = rail_fence_encrypt(encrypted, int(i))
    generate_and_save_image(encrypted, width, height, output_filename)


def decrypt_image(input_filename, output_filename, password):
    password = password[::-1]
    im = Image.open(input_filename)
    width, height = im.size
    colors = get_pixels(im, width, height)
    decrypted = colors
    for i in password:
        decrypted = rail_fence_decrypt(decrypted, int(i))
    generate_and_save_image(decrypted, width, height, output_filename)


PASSWORD = '2345678'

encrypt_image('filename.jpg', 'encrypted.png', PASSWORD)
decrypt_image('encrypted.png', 'decrypted.png', PASSWORD)
