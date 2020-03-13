#!/usr/bin/env python3

import click
from pathlib import Path
from PIL import Image
from shutil import copyfile
from tqdm import tqdm


@click.command()
@click.option('-b', '--backup', is_flag=True)
@click.option('--format', type=click.Choice(['jpeg', 'webp']), default='jpeg')
@click.argument('root', type=click.Path(exists=True), required=False)
def resize_to_retina(root, format, backup=False):
    EXT = ('jpg', 'jpeg')
    IGNORE = ('contactsheet', 'cover', 'poster')
    if not root:
        root = Path.cwd()
    else:
        root = Path(root)
    # list subdirectories of root with 00names
    tasks = [x for x in root.iterdir() if (x.is_dir() and x.name[:2] == '00')]
    for index, task in enumerate(tasks):
        photoset = [x for x in task.iterdir() if str(x).lower().endswith(EXT)]
        print(f'{index+1}/{len(tasks)}: {task.name}')
        # create backup dir
        if backup:
            backup = task / ('original')
            backup.mkdir(exist_ok=True)
        # image processing with pretty progress bar
        for photo in tqdm(photoset):
            # don't process covers, cover-clean and contactsheets
            if [kw for kw in IGNORE if kw in str(photo).lower()]:
                continue
            img = Image.open(photo)
            img_h, img_w = img.size
            # don't process stretched images (maybe cs)
            if img_h / img_w > 2.25:
                continue
            # save backup
            if backup:
                copyfile(photo, backup / photo.name)
            # resize to 2880*4320 "retina"
            img.thumbnail((4320, 4320), Image.BICUBIC)
            if format == 'jpeg':
                img.save(photo, 'jpeg', quality=75, optimize=True)
            elif format == 'webp':
                img.save(photo.with_suffix('.webp'), 'webp',
                         quality=80, method=4)
                photo.unlink()
        try:
            task.rename(task.parent / (task.name[2:] + ' Mx'))
        except OSError:
            print("Unable to rename dir")
    print("Done.")


if __name__ == '__main__':
    resize_to_retina()
