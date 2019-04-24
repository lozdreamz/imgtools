import os
import sys
import shutil
from PIL import Image

EXT = ('jpg', 'JPG', 'JPEG', 'jpeg')
IGNORE = ('contactsheet', 'cover', 'poster')
root = os.getcwd()

# пройтись по списку каталогов выбранного каталога
for work_dir in os.listdir(root):
    level = work_dir[0:2]
    if os.path.isdir(work_dir) and level == '00':
        photoset = [file_name for file_name in os.listdir(work_dir) if file_name.endswith(EXT)]
        total_photos = len(photoset)
        progressbar_len = 50
        # создать каталог для бэкапа
        backup_dir = 'original.' + level
        os.chdir(work_dir)
        os.mkdir(backup_dir)
        # обработка списка изображений
        print(work_dir)
        for index, photo in enumerate(photoset):
            # не обрабатывать каверы, кавер_клины и контактшиты
            img = Image.open(photo)
            img_h, img_w = img.size
            # переход к следующему файлу, если запрещенное имя
            # или высота сильно превышает ширину
            if (img_h / img_w > 2.25) or [kw for kw in IGNORE if kw in photo.lower()]:
                continue
            shutil.copy(photo, os.path.join(backup_dir, photo))
            # привести к 2880*4320 retina
            img.thumbnail((4320, 4320), Image.BICUBIC)
            img.save(photo, 'jpeg', quality=75, optimize=True)
            done = int(progressbar_len * (index + 1)  / total_photos)
            sys.stdout.write(f'\r{index+1}/{total_photos}[{done * "="}{" " * (progressbar_len - done)}]')
            sys.stdout.flush()
        os.chdir(root)
        try:
            os.rename(work_dir, work_dir[2:] + " Mx")
        except:
            print("Unable to rename dir")
        print("\n")
print("Done.")