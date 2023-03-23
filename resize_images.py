import os
import sys
from PIL import Image, ExifTags

def resize_image(input_image_path, output_image_path, max_size):
    img = Image.open(input_image_path)

    # Rotate image if needed
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    try:
        exif = img._getexif()
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # In case of no exif data or no orientation info, do nothing
        pass

    # Resize image
    width, height = img.size
    if width > height:
        new_width = max_size
        new_height = int(height * max_size / width)
    else:
        new_height = max_size
        new_width = int(width * max_size / height)

    img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)
    img_resized.save(output_image_path)

def process_images(input_dir, output_dir, max_size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.jpg'):
            input_image_path = os.path.join(input_dir, filename)
            output_image_path = os.path.join(output_dir, filename)
            resize_image(input_image_path, output_image_path, max_size)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python resize_images.py <input_directory> <output_directory>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    max_size = 768

    process_images(input_dir, output_dir, max_size)
