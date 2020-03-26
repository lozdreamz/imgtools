#!/usr/bin/env python3

import click
from math import ceil
from pathlib import Path
from PIL import Image, ImageDraw
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = 104_000_000


def get_tile_pos(index, width, height):
    '''
    Convert tile index to position (box) in contactsheet

    :param index: index of tile
    :param width, height: tile size
    '''
    row = (index - 1) // 4
    col = (index - 1) % 4
    return 256*col, 256*row


def add_margins(img):
    '''
    Add margins and border to rectangle image

    :param img: original Pillow image
    '''
    result = Image.new(img.mode, (256, 256), 0)
    w, h = img.size
    if w == h:
        return img
    elif w > h:
        result.paste(img, (0, (w-h) // 2))
    else:
        result.paste(img, ((h-w) // 2, 0))
    # add border
    draw = ImageDraw.Draw(result)
    draw.line(((0, 0), (256, 0), (256, 256), (0, 256)),
              fill=(255, 255, 255), width=2)
    draw.rectangle((0, 0, 256, 256), outline=(255, 255, 255))
    return result


def add_text(img, text):
    result = img.copy()
    draw = ImageDraw.Draw(result)
    # draw black rectangle
    draw.rectangle((3, 256-12, 253, 253), fill='black')
    # and write text
    draw.text((4, 256-12), text, (255, 255, 255))
    return result


def process_images(files, text):
    '''
    Process images list

    :param files: list of file names
    :param text: add file name as caption on thumbnails
    '''
    # size is tuple (width, height)
    result = Image.new("RGB", (1024, ceil(len(files)/4*256)), 'black')
    # image processing with pretty progress bar
    for i, f in tqdm(enumerate(files), ascii=' #'):
        img = Image.open(f)
        img.thumbnail((256, 256), Image.NEAREST)
        img = add_text(add_margins(img), f.stem)
        result.paste(img, get_tile_pos(i, *img.size))
    result.save('contactsheet.jpg', 'jpeg', quality=75, optimize=True)


def match_name(filename):
    ''' Match filename not contains ignored word '''
    IGNORE = ('cover', 'poster')
    return not [kw for kw in IGNORE if kw in filename.name.lower()]


def process_dir(path, text):
    '''
    Process all image files from directory

    :param path: selected path
    :param text: add file name as caption on thumbnails
    '''
    EXT = ('jpg', 'jpeg')
    # collect, filter and process
    files = [x for x in path.iterdir() if str(x).lower().endswith(EXT)]
    files = sorted(list(filter(match_name, files)))
    process_images(files, text)


@click.command()
@click.argument('path', type=click.Path(exists=True), required=False)
@click.option('-t', '--text', is_flag=True, default=False)
def create_contactsheet(path, text):
    if not path:
        path = Path.cwd()
    else:
        path = Path(path)
    process_dir(path, text)


if __name__ == '__main__':
    create_contactsheet()
