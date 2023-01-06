import re
import os
from docx import Document
from win32api import GetUserNameEx
from datetime import datetime
from scripts.path import FindFiles
from scripts.config import DEFAULT_PATH


class GerarDocTeste:
    def __init__(self, change:str):
        self.change = change
        self.author = GetUserNameEx(3)
        self.today = datetime.today().strftime('%d/%m/%Y')
        self.doc_file = ''
        self.doc_number = self._get_doc_number()
        self.is_valid = self._validate_change_number()
    
    def _get_doc_number(self) -> str:
        file = FindFiles(self.change)
        file.find_documents()
        file.return_last_document_number()
        return file.doc_number
    
    def _validate_change_number(self) -> bool:
        found = re.search('^(CHG[0-9]{7})$', self.change)
        if found == None:
            return False
        return True
    
    def create_word_doc(self):
        doc = Document('DocPadrao.docx')
        header = doc.sections[0].header
        for paragraph in header.paragraphs:
            text = paragraph.text
            text = text.replace('TITLE', self.change)
            text = text.replace('AUTOR', self.author)
            text = text.replace('DATA', self.today)
            paragraph.text = text   
        self.doc_file = f'{self.change}_{self.doc_number}.docx'
        doc.save(f'{DEFAULT_PATH}{self.doc_file}')
    
    # def open_word_doc(self):
    #     word_doc = os.path.join(DEFAULT_PATH, self.doc_file)
    #     os.startfile(word_doc)
