import io
import os
import zipfile
import pillow_heif
from PIL import Image
from pillow_heif import register_heif_opener
from config import IMAGE_FOLDER_OUTPUT_PATH as FOLDER_OUTPUT_PATH

def convert_images(file_path):
    pillow_heif.register_heif_opener()
    if "zip" in file_path:
        print('ZIP detected, unzipping and converting')
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            for image_file in zip_ref.namelist():
                if image_file.endswith(('.HEIC', 'HEIF', '.JPG','.PNG')) or image_file.startswith(('PXL')):
                    image_name = image_file.split('.')[0]
                    with zip_ref.open(image_file) as file:
                        try:
                            image = Image.open(io.BytesIO(file.read()))
                            image.save(FOLDER_OUTPUT_PATH + image_name + '.jpg', format="JPEG")
                            print(f'"{image_file}" saved as JPG')
                        except Exception as e:
                            print(e)
    elif any(suffix in file_path for suffix in ['heic','heif']):
        print('Single image detected, converting single image')
        try:
            photo = Image.open(file_path)
            photo.save(FOLDER_OUTPUT_PATH + file_path.split('/')[-1][:-5] + ".jpg", format="JPEG")
            print(f'"{file_path.split('/')[-1][:-5]}" saved as JPG')
        except Exception as e:
            print(e)
    else:
        print('Folder detected, converting images')
        for subdir, dirs, files in os.walk(file_path):
            for image in files:
                try:
                    photo = Image.open(file_path + '/' + image)
                    photo.save(FOLDER_OUTPUT_PATH + image[:-5] + ".jpg", format="JPEG")
                    print(f'"{image[:-5]}" saved as JPG')
                except Exception as e:
                    print(e)

# def change_timestamp():
#     timestamp_dir = IMAGE_FILE_PATH + 'FindlenGoldenPhotos/'
#     for filename in os.listdir(timestamp_dir):
#         timestamp_file_name = timestamp_dir + filename
#         desired_timestamp = DATETIME_SET.timestamp()
#         os.utime(timestamp_file_name, (desired_timestamp, desired_timestamp))
#         # print(f"New modification time: {datetime.fromtimestamp(os.path.getmtime(filename))}")

# convert_image(IMAGE_FILE_PATH)
# convert_images(IMAGE_FOLDER_PATH)
# convert_images(SINGLE_IMAGE_FILE_PATH)
