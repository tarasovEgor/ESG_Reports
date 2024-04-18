import requests
# import docker
import os
import re


def correct_path(path):
    directory, filename = os.path.split(path)
    corrected_filename = re.sub(r'_+', '', filename)
    print(corrected_filename)
    os.rename(path, os.path.join(directory, corrected_filename))
    print(path)
    return os.path.join(directory, corrected_filename)


def before():
    if not os.path.exists("PDF_processing_module/ESG-master/final"):
        os.mkdir("PDF_processing_module/ESG-master/final")


def main(url, path, ocr):
    before()
    if os.path.exists(path):
        path = correct_path(path)
        print("Начинается обработка")
        files = {'file': open(path, 'rb')}
        data = {'ocr': ocr}
        name_pdf = os.path.splitext(os.path.basename(path))[0]
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            with open(f'PDF_processing_module/ESG-master/final/{name_pdf}.txt', 'wb') as f:
                f.write(response.content)
                print("Text file downloaded successfully.")
                requests.get("http://localhost:5050/clean")
                return False
        else:
            print("Failed to download text file.")
            return False
    else:
        print("Такого пути нет")
        return False


if __name__ == '__main__':
    print("Введите аргумент(путь до pdf): ")
    argument = input()
    print("\n")
    print("Введите способ обработки (1 - Без OCR, 2 - OCR)")
    print("Если без OCR не получится, то автоматически начнётся обработка с OCR")
    print("Обработка с OCR может быть хуже")
    print("\n")
    print("Ввод(1 - 2 | Без OCR - OCR):")
    ocr = False
    inpOCR = input()
    if inpOCR == "2":
        ocr = True
    while not main("http://localhost:5050/upload-pdf", argument, ocr):
        print("\n")
        print("Пожалуйста, введите ешё путь: ")
        argument = input()
        print("\n")
        print("Ввод(1 - 2 | Без OCR - OCR):")
        ocr = False
        inpOCR = input()
        if inpOCR == "2":
            ocr = True
