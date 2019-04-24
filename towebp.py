# -*- coding: utf-8 -*-

import os
import sys
import shutil
from subprocess import Popen, PIPE

ext = ('jpg', 'JPG', 'JPEG', 'jpeg')
work_dir = os.getcwd()
# https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html
exe_path = 'd:\\Applications\\libwebp-0.6.0-windows-x86-no-wic\\bin\\cwebp.exe'
cmd_pattern = '"{0}" -preset {1} q {2} "{3}" -o "{4}" -quiet'
preset = 'photo'
quality = 80

# бэкап
backup_dir = 'original'
os.mkdir(backup_dir)
files = os.listdir(work_dir)
for index, file_name in enumerate(files):
    # обработка списка изображений
    sys.stdout.write(f'\r{index + 1 }/{len(files)}')
    sys.stdout.flush()
    if file_name.endswith(ext):
        base_name = os.path.splitext(file_name)[0]
        cmd = cmd_pattern.format(exe_path, preset, quality, '.\\' + file_name, '.\\' + base_name + '.webp')
        p = Popen(cmd, shell=True, stdout=PIPE)
        out, err = p.communicate()
        shutil.move(file_name, backup_dir + '/' + file_name)
print("Done")
