# imgtools

Set of PIL-based tools for image processing

## retina.py

Batch resize photos to 'retina' (2880p) size

### Requirements:

- click
- Pillow (Pillow-SIMD recommended)\
  For convertion to WebP Pillow must be complied with WebP support (first install libwebp-dev)
- tqdm

### Usage

retina.py [OPTIONS] [PATH]

#### Options

##### --dirs, -d / --files, -f
Choose mode: directories with names starting with 00 or files in directory (default: dirs mode)

##### --backup / --no-backup, -B
Save original files (default: save)

##### --webp, -w
Save to WebP format (default: JPEG)

#### --resize / --no-resize, -R
Resize images or just resave (default: resize)

