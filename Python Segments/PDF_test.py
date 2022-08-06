# get_doc_info.py
import os
import PyPDF2
from PyPDF2 import PdfFileReader

##  Get PDF file data example   ##
# def get_info(path):
#     with open(path, 'rb') as f:
#         pdf = PdfFileReader(f)
#         info = pdf.getDocumentInfo()
#         number_of_pages = pdf.getNumPages()
#     print(info)    
# # print(os.path.abspath(os.getcwd()))

#     author = info.author
#     creator = info.creator
#     producer = info.producer
#     subject = info.subject
#     title = info.title
# if __name__ == '__main__':
#     path = 'sample_report.pdf'
#     get_info(path)


def text_extractor(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        # get the first page
        page = pdf.getPage(1)
        print(page)
        print('Page type: {}'.format(str(type(page))))
        text = page.extractText()
        print(text)
if __name__ == '__main__':
    path = 'sample_report.pdf'
    text_extractor(path)