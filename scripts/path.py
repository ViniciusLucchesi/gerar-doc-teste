import os
import re
import glob
from scripts.config import DEFAULT_PATH


class FindFiles:
    def __init__(self, change_number:str='padrao', path:str=DEFAULT_PATH):
        self.change_number = change_number
        self.found = []
        self.doc_number = '01'
        self.doc_path = os.path.join(path, '*.docx')
        self.doc_regex = self.select_correct_pattern()
    
    
    def select_correct_pattern(self):
        if self.change_number != 'padrao':
            return self.change_number + '_[0-9]{2}.docx'    
        return '(?<=\\\\).{1,}\.docx$'
    

    def find_documents(self):
        if self.change_number != 'padrao':
            for file_path in glob.glob(self.doc_path):
                file_name = re.findall(self.doc_regex, file_path)
                if len(file_name) > 0:
                    self.found.append(file_name[0])
        else:
            for file_path in glob.glob(self.doc_path):
                file_name = re.sub('\\\\', '####', file_path).split('####')[-1]
                if len(file_name) > 0:
                    self.found.append(file_name)            
        self.found.sort
    

    def return_last_document_number(self):
        if len(self.found) > 0:
            last_doc = self.found[-1]
            splitted = re.sub('(_)|(\.)', ' ', last_doc).split()
            
            last_number = int(splitted[1])
            next_number = last_number + 1

            self.doc_number = self._integer_to_string(next_number)
    

    def _integer_to_string(self, next_number):
        if next_number < 10:
            return f'0{next_number}'
        return str(next_number)
    

    def return_found_docs(self):
        return self.found
