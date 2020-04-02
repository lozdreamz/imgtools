#!/usr/bin/env python3

import click
from math import ceil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = 104_000_000
TILE_SIZE = 256
BORDER_WIDTH = 2
FONTS_DIR = '/usr/share/fonts/truetype'


def get_tile_pos(index):
    '''
    Convert tile index to position (box) in contactsheet

    :param index: index of tile
    :param width, height: tile size
    '''
    row = index // 4
    col = index % 4
    return TILE_SIZE*col, TILE_SIZE*row


def add_margins(img):
    '''
    Add margins and border to rectangle image

    :param img: original Pillow image
    '''
    result = Image.new(img.mode, (TILE_SIZE, TILE_SIZE), 0)
    w, h = img.size
    if w == h:
        return img
    elif w > h:
        result.paste(img, (0, (w-h) // 2))
    else:
        result.paste(img, ((h-w) // 2, 0))
    # add border
    ImageDraw.Draw(result).line(
        ((0, 0), (TILE_SIZE, 0), (TILE_SIZE, TILE_SIZE),
         (0, TILE_SIZE), (0, 0)),
        fill='gray', width=BORDER_WIDTH
    )
    return result


def add_text(img, text, font_size=11):
    result = img.copy()
    draw = ImageDraw.Draw(result)
    font = ImageFont.truetype(f'{FONTS_DIR}/dejavu/DejaVuSans.ttf', font_size)
    text_heigth = font.getsize(text)[1]
    # TODO get text length and wrap if necessary
    # draw black rectangle at bottom
    draw.rectangle((BORDER_WIDTH+1, TILE_SIZE-text_heigth-2,
                    TILE_SIZE-BORDER_WIDTH, TILE_SIZE-BORDER_WIDTH),
                   fill='black')
    # and write text
    draw.text((4, TILE_SIZE-text_heigth-1), text, 'white', font)
    return result


def process_images(files, text):
    '''
    Process images list

    :param files: list of file names
    :param text: add file name as caption on thumbnails
    '''
    # size is tuple (width, height)
    result = Image.new('RGB', (TILE_SIZE*4, ceil(len(files)/4)*TILE_SIZE),
                       'black')
    # image processing with pretty progress bar
    with tqdm(total=len(files),
              bar_format='{percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt}',
              ascii=' ░█') as pbar:
        for i, f in enumerate(files):
            img = Image.open(f)
            img.thumbnail((TILE_SIZE, TILE_SIZE))
            img = add_text(add_margins(img), f.stem)
            result.paste(img, get_tile_pos(i))
            pbar.update(1)
    result.save(files[1].parent / ('contactsheet.jpg'), 'jpeg',
                quality=75, optimize=True)


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
    if files:
        process_images(files, text)


def process_dirs(root, text):
    '''
    Process all directories in root directory

    :param root: selected root
    :param text: add file name as caption on thumbnails
    '''
    # list subdirectories of root
    tasks = [x for x in root.iterdir() if x.is_dir()]
    for index, task in enumerate(tasks):
        process_dir(task, text)
    print("Done.")


@click.command()
@click.argument('path', type=click.Path(exists=True), required=False)
@click.option('-f', '--files', 'mode', flag_value='files', default=True)
@click.option('-d', '--dirs', 'mode', flag_value='dirs')
@click.option('-t', '--text', is_flag=True, default=False)
def create_contactsheet(path, mode, text):
    if not path:
        path = Path.cwd()
    else:
        path = Path(path)
    if mode == 'dirs':
        print('Processing  dirs...')
        process_dirs(path, text)
    elif mode == 'files':
        print('Processing files in a directory...')
        process_dir(path, text)


if __name__ == '__main__':
    create_contactsheet()
