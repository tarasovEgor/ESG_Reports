import os
import shutil
import re


def check_argument(path):
    if os.path.exists(path):
        return True
    else:
        print(f"Путь '{path}' не существует.")
        return False


def clean_after():
    try:
        shutil.rmtree("PDF_processing_module/ESGServer/temp")
        shutil.rmtree("PDF_processing_module/ESGServer/uploads")
        shutil.rmtree("PDF_processing_module/ESGServer/final")
        print("Временная папка и все ее содержимое успешно удалены.")
    except FileNotFoundError:
        print("Временная папка не существует.")


def final_coupling(pathtexteasyocr, pathtextapryse):
    if not pathtextapryse.strip():
        return pathtexteasyocr
    return pathtextapryse


def clean_text_if_needed(text, ocr):
    cleaned_text = re.sub(r" {3,}", "\n", text)
    cleaned_text_lines = cleaned_text.splitlines(keepends=True)
    if ocr:
        cleaned_text = '\n\n'.join(line for line in cleaned_text_lines if len(line.strip()) >= 4
                                   and re.search(r"[а-яА-Яa-zA-Z]", line)
                                   and not re.fullmatch(r"[0-9.,\s]+", line.strip()))
        return cleaned_text
    else:
        cleaned_text = '\n'.join(line for line in cleaned_text_lines if len(line.strip()) >= 4
                                 and re.search(r"[а-яА-Яa-zA-Z]", line)
                                 and not re.fullmatch(r"[0-9.,\s]+", line.strip()))
        return cleaned_text


def merge_lines(text):
    lines = text.split('\n')
    merged_text = ""
    lines = list(filter(lambda s: s.strip(), lines))
    print(lines)
    for i in range(len(lines) - 1):
        current_line = lines[i].strip()
        next_line = lines[i + 1].strip()
        if (current_line.endswith(tuple('abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя,:')) and
            not next_line.startswith(tuple('0123456789'))) or \
                (current_line.endswith(',') and next_line[0].isupper()):
            merged_text += current_line + ' '
        else:
            merged_text += current_line + '\n'
    merged_text += lines[-1].strip()
    return merged_text
