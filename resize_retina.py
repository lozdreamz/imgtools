from pathlib import Path
from PIL import Image
from shutil import copyfile
from tqdm import tqdm

EXT = ('jpg', 'jpeg')
IGNORE = ('contactsheet', 'cover', 'poster')
root = Path('.')

# list subdirectories of root
tasks = [x for x in root.iterdir() if x.is_dir()]
for task in tasks:
    level = str(task)[:2]
    if level == '00':
        photoset = [x for x in task.iterdir() if str(x).lower().endswith(EXT)]
        # TODO: backup option
        # create backup dir
        backup = task / ('original.' + level)
        backup.mkdir(exist_ok=True)
        print(task.name)
        # image processing with pretty progress bar
        for photo in tqdm(photoset):
            img = Image.open(photo)
            img_h, img_w = img.size
            # do not process covers, cover-clean and contactsheets
            # also don not process stretched images (maybe cs)
            if (
                (img_h / img_w > 2.25) or
                [kw for kw in IGNORE if kw in str(photo).lower()]
                ):
                continue
            # save backup
            copyfile(photo, backup / photo.name)
            # resize to 2880*4320 retina
            img.thumbnail((4320, 4320), Image.BICUBIC)
            img.save(photo, 'jpeg', quality=75, optimize=True)
        try:
            task.rename(str(task)[2:] + ' Mx')
        except:
            print("Unable to rename dir")
print("Done.")
