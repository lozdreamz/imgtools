#!/usr/bin/env python3

import click
from pathlib import Path
from PIL import Image
from shutil import copyfile
from tqdm import tqdm


def process_images(files, backup_path=None, resize=True, webp=False):
    '''
    Process images list

    :param files: list of file names
    :param backup_path: path to save original files
    :param resize: resize to "retina" or just resave image
    :param webp: convert to WebP
    '''
    # image processing with pretty progress bar
    for f in tqdm(files):
        img = Image.open(f)
        # don't process vertical stretched images (maybe cs) h/w > 2.25
        if (lambda x: x[1]/x[0] < 2.25)(img.size):
            # save backup
            if backup_path:
                copyfile(f, backup_path / f.name)
            # resize to 2880*4320 "retina"
            if resize:
                img.thumbnail((4320, 4320), Image.BICUBIC)
            # and save to requied image format
            if webp:
                img.save(f.with_suffix('.webp'), 'webp', quality=80, method=4)
                f.unlink()
            else:
                img.save(f, 'jpeg', quality=75, optimize=True)


def process_dir(path, backup, resize, webp):
    EXT = ('jpg', 'jpeg')
    # create backup dir
    if backup:
        backup_path = path / ('originals')
        backup_path.mkdir(exist_ok=True)
        # filter file list
        photoset = [x for x in path.iterdir() if str(x).lower().endswith(EXT)]
        photoset = list(filter(match_name, photoset))
        process_images(photoset, backup_path, resize, webp)
        try:
            path.rename(path.parent / (path.name[2:] + ' Mx'))
        except OSError:
            print("Unable to rename dir")


def process_dirs(root, backup, resize, webp):
    # list subdirectories of root with 00names
    tasks = [x for x in root.iterdir() if (x.is_dir() and x.name[:2] == '00')]
    for index, task in enumerate(tasks):
        print(f'{index+1}/{len(tasks)}: {task.name}')
        process_dir(task, backup, resize, webp)
    print("Done.")


def match_name(filename):
    ''' Match filename not contains ignored word '''
    IGNORE = ('contactsheet', 'cover', 'poster')
    return not [kw for kw in IGNORE if kw in filename.name.lower()]


@click.command() # noqa: C901
@click.argument('root', type=click.Path(exists=True), required=False)
@click.option('--backup/--no-backup', ' /-B', default=True)
@click.option('--resize/--no-resize', ' /-R', default=True)
@click.option('-w', '--webp', is_flag=True, default=False)
def resize_to_retina(root, backup, resize, webp):
    if not root:
        root = Path.cwd()
    else:
        root = Path(root)
    process_dirs(root, backup, resize, webp)


if __name__ == '__main__':
    resize_to_retina()
