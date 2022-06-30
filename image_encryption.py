import numpy as np
from itertools import cycle
from PIL import Image


MAX_SIZE = 500


def rail_pattern(n):
    r = list(range(n))
    return cycle(r + r[-2:0:-1])


def rail_fence_encrypt(plaintext, rails):
    if 1 < rails < len(plaintext):
        p = rail_pattern(rails)
        return sorted(plaintext, key=lambda i: next(p))
    else:
        return plaintext


def rail_fence_decrypt(ciphertext, rails):
    if 1 < rails < len(ciphertext):
        p = rail_pattern(rails)
        indexes = sorted(range(len(ciphertext)), key=lambda i: next(p))
        result = [''] * len(ciphertext)
        for i, c in zip(indexes, ciphertext):
            result[i] = c
        return result
    else:
        return ciphertext


def resize_image(im):
    x, y = im.size
    if x > y:
        height = round(MAX_SIZE * y / x)
        width = MAX_SIZE
    else:
        width = round(MAX_SIZE * x / y)
        height = MAX_SIZE
    im = im.resize((width, height), Image.ANTIALIAS)
    return im


def get_pixels(im, width, height):
    colors = []
    for x in range(width):
        for y in range(height):
            color = im.getpixel((x, y))
            colors.append(color)
    return colors


def generate_and_save_image(colors, width, height, filename):
    new_im = Image.new('RGB', (width, height))
    new_image = np.array(new_im)
    i = 0
    for x in range(width):
        for y in range(height):
            r = colors[i][0]
            g = colors[i][1]
            b = colors[i][2]
            new_image[y][x] = (r, g, b)
            i += 1
    new_img = Image.fromarray(new_image, 'RGB')
    new_img.save(filename)


def encrypt_image(input_filename, output_filename, password):
    im = Image.open(input_filename)
    width, height = im.size
    if width > MAX_SIZE or height > MAX_SIZE:
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


PASSWORD = '432876523109687524169757'

encrypt_image('filename.jpg', 'encrypted.png', PASSWORD)
decrypt_image('encrypted.png', 'decrypted.png', PASSWORD)
