import os
from PIL import ImageEnhance

from pdf2image import convert_from_path
import easyocr
import util
import re


def to_png(path):
    images = convert_from_path(path)
    for i, image in enumerate(images):
        image_path = f'PDF_processing_module/ESGServer/temp/images/page{i}.jpg'
        image.save(image_path, 'JPEG')
        print(f'Saved image: {image_path}')


def convert_folder_to_grayscale(folder_path):
    from PIL import Image
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            try:
                image = Image.open(full_path)
                grayscale_image = image.convert("L")

                enhancer = ImageEnhance.Contrast(grayscale_image)
                enhanced_image = enhancer.enhance(2)

                enhanced_image.save(full_path, dpi=(300, 300))
                print(
                    f'Изображение {filename} успешно преобразовано в оттенки серого с повышенной контрастностью и сохранено.')
            except Exception as e:
                print(f'Ошибка при обработке изображения {filename}: {e}')


def process_images(path):
    to_png(path)
    convert_folder_to_grayscale("PDF_processing_module/ESGServer/temp/images")
    text = ""
    reader = easyocr.Reader(['ru', 'en'], gpu=True)
    sorted_list = sorted(os.listdir('PDF_processing_module/ESGServer/temp/images'), key=lambda x: int(x.split('.')[0][4:]))
    for filename in sorted_list:
        if filename.endswith('.jpg'):
            image_path = os.path.join('PDF_processing_module/ESGServer/temp/images', filename)
            result = reader.readtext(image_path, detail=0, paragraph=True)
            print(image_path)
            temp = ""
            for paragraph in result:
                if len(paragraph) > 2:
                    temp += paragraph + "\n"
            text += re.sub(r"[^\w\s,.?!]", "", temp + "\n")

    text = util.clean_text_if_needed(text, True)
    text = util.merge_lines(text)
    return text
