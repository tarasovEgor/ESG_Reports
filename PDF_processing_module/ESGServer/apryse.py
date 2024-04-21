import os
import subprocess
import re
import util


def convert_to_text(path):
    print(path)
    name_pdf = os.path.splitext(os.path.basename(path))[0]
    print(name_pdf)
    text = ""
    apryse_text_dir = "PDF_processing_module/ESGServer/temp/apryse_text"
    demo_string = "PDFTron PDF2Text: This page is skipped when running in the demo mode."

    try:
        subprocess.run(["/Users/georgetarasov/Desktop/ESG_Reports/ESGProject/PDF_processing_module/ESGServer/pdf2text", "--output", apryse_text_dir, path], check=True)
        print("Файл PDF успешно конвертирован в текст и сохранен.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при конвертации файла PDF: {e}")
        return

    text_files = [f for f in os.listdir(apryse_text_dir) if f.endswith(".txt")]
    text_files_sorted = sorted(text_files, key=lambda x: int(x.split('_')[1].split('.')[0]))
    print(text_files_sorted)
    for text_file in text_files_sorted:
        file_path = os.path.join(apryse_text_dir, text_file)
        while True:
            content = ""
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                print(content)
            if demo_string in content:
                page_number = text_file.split('_')[1].split('.')[0]
                os.remove(file_path)
                print(page_number)
                subprocess.run(
                    ["/Users/georgetarasov/Desktop/ESG_Reports/ESGProject/PDF_processing_module/ESGServer/pdf2text", "--output", apryse_text_dir, "--pages", page_number, path],
                    check=True)
                os.rename(os.path.join(apryse_text_dir, name_pdf + ".txt"),
                          os.path.join(apryse_text_dir, name_pdf + "_" + page_number + ".txt"))
            else:
                break

    for text_file in text_files_sorted:
        file_path = os.path.join(apryse_text_dir, text_file)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                if demo_string not in content:
                    text += re.sub(r"[^\w\s,.?!]", "", content + "\n")
                else:
                    print(content)

    print("Создан текстовый файл от Apryse")
    text = util.clean_text_if_needed(text, False)
    text = util.merge_lines(text)
    return text
