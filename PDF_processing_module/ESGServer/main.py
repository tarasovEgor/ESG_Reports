import os
import easyOCR
import apryse
import util
from flask import Flask, request, send_file
import re

app = Flask(__name__)

UPLOAD_FOLDER = 'PDF_processing_module/ESGServer/uploads'


def before():
    if not os.path.exists("PDF_processing_module/ESGServer/temp"):
        os.mkdir("PDF_processing_module/ESGServer/temp")
        os.mkdir("PDF_processing_module/ESGServer/final")
        os.mkdir("PDF_processing_module/ESGServer/temp/images")
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


@app.route('/clean')
def take():
    util.clean_after()
    before()
    return "good"


@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    text_filename = '/Users/georgetarasov/Desktop/ESG_Reports/ESGProject/PDF_processing_module/ESGServer/final/final.txt'
    try:
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        ocr_string = request.form.get('ocr', 'false').lower()
        ocr = ocr_string == 'true'
        if ocr is None:
            return "OCR flag not provided", 400
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            textapryse = ""
            if not ocr:
                textapryse = apryse.convert_to_text(filepath)
            easyOCRtext = ""
            if not textapryse.strip() or ocr:
                easyOCRtext = easyOCR.process_images(filepath)
            final = util.final_coupling(easyOCRtext, textapryse)
            with open(text_filename, 'w', encoding='utf-8') as text_file:
                text_file.write(final)
            return send_file(text_filename, as_attachment=True, download_name=text_filename)
    except Exception as e:
        print("Произошла ошибка с обработкой файла (вероятно - проблема с файлом)")
        with open(text_filename, 'w', encoding='utf-8') as text_file:
            text_file.write("Error")
        return send_file(text_filename, as_attachment=True, download_name=text_filename)


if __name__ == '__main__':
    before()
    app.run(debug=True, host='0.0.0.0', port=5050)
