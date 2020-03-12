from pathlib import Path
from PIL import Image
from shutil import copyfile
from tqdm import tqdm

EXT = ('jpg', 'jpeg')
IGNORE = ('contactsheet', 'cover', 'poster')

root = Path('.')

# list subdirectories of root with 00names
tasks = [x for x in root.iterdir() if (x.is_dir() and str(x)[:2] == '00')]
for index, task in enumerate(tasks):
    photoset = [x for x in task.iterdir() if str(x).lower().endswith(EXT)]
    # TODO: backup option
    # create backup dir
    backup = task / ('original')
    backup.mkdir(exist_ok=True)
    print(f'{index}/{len(tasks)}: {task.name}')
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
        copyfile(photo, backup / photo.name)
        # resize to 2880*4320 "retina"
        img.thumbnail((4320, 4320), Image.BICUBIC)
        img.save(photo, 'jpeg', quality=75, optimize=True)
    try:
        task.rename(str(task)[2:] + ' Mx')
    except OSError:
        print("Unable to rename dir")
print("Done.")
