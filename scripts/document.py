import re
import os
from docx import Document
from win32api import GetUserNameEx
from datetime import datetime
from scripts.path import FindFiles
from scripts.config import JSONConfig


class GerarDocTeste:
    def __init__(self, change:str='padrao'):
        self.change = change.upper()
        self.author = GetUserNameEx(3)
        self.today = datetime.today().strftime('%d/%m/%Y')
        self.doc_file = ''
        self.is_valid = self._validate_change_number()
        if self.is_valid:
            self.doc_number = self._get_doc_number()
        else:
            self.doc_number = ''

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
    
    def create_word_doc(self, doc_name:str, directory:str):
        doc = Document(f'word_template/{doc_name}')
        metadata = doc.core_properties
        metadata.author = self.author
        metadata.title = self.change
        header = doc.sections[0].header
        for paragraph in header.paragraphs:
            text = paragraph.text
            text = text.replace('TITLE', self.change)
            text = text.replace('AUTOR', self.author)
            text = text.replace('DATA', self.today)
            paragraph.text = text   
        self.doc_file = f'{self.change}_{self.doc_number}.docx'
        doc.save(f'{directory}{self.doc_file}')

    def _get_file_name(self, file_path) -> str:
        file_name = re.sub('/', '###', file_path).split('###')[-1]
        return file_name

    def save_document(self, doc_path) -> None:
        default_path = re.sub('"', '', doc_path)
        default_path = re.sub('\\\\', '/', default_path)
        doc = Document(default_path)
        file_name = self._get_file_name(default_path)
        full_path = os.path.join('word_template', file_name)
        doc.save(full_path)

    def __str__(self):
        print(f'change: {self.change}')
        print(f'author: {self.author}')
        print(f'today: {self.today}')
        print(f'doc_file: {self.doc_file}')
        print(f'is_valid: {self.is_valid}')
        print(f'doc_number: {self.doc_number}')
        return ''


if __name__ == '__main__':
    document = GerarDocTeste('CHG0023893')        
    print(document)

    config = JSONConfig()
    doc_name = config.get_current_active()
    target_path = config.docs[doc_name]["save_directory"]

    if document.is_valid:
        document.create_word_doc(doc_name, target_path)
        print(document)