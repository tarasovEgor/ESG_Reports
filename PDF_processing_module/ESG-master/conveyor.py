import os
import main
import re

url = "http://localhost:5050/upload-pdf"
pdf_path = "PDF_processing_module/ESG-master/pdf_storage"
pdf_list = os.listdir('PDF_processing_module/ESG-master/pdf_storage')

if ('.DS_Store' in pdf_list):
    pdf_list.remove('.DS_Store')

def convey_to_server(url, pdf_path, pdf_list):
    print("Convey launched.")
    for pdf in pdf_list:
        print("Conveying " + pdf + " to server...")
        # pdf_path = pdf_path + '/' + pdf
        main.main(url, pdf_path + '/' + pdf, 2)
        print(pdf + " was successfully converted to txt, conveying the next item...")

convey_to_server(url, pdf_path, pdf_list)
