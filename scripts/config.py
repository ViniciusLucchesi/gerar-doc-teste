from pathlib import Path
from datetime import datetime
import hashlib
import time
import json


class JSONConfig:
    def __init__(self):
        self.config_path = 'config.json'
        self.docs = self.read()
        self.keys = list(self.docs['Documents'])


    def read(self) -> dict:
        """
        Read a config.json file that contains all documents information to the program work correctly
        This function will be trigger automatically when the class was initiated
        """
        with open(self.config_path, 'r', encoding='utf-8') as config:
            docs = json.load(config)
        return docs


    def write(self, modified_file:dict) -> None:
        """
        Write in the config.json file the dictionary passed as a parameter
        """
        with open(self.config_path, 'w', encoding='utf-8') as outfile:
            json.dump(modified_file, outfile)


    def add_new_doc(self, doc_name:str, directory:str, author_option:str) -> str:
        """
        Adds a new JSON object to the current JSON config file with the following information:
            [doc_id -> hash]:{                
                "name": [doc_name -> parameter],  
                "save_directory": [directory -> parameter],
                "template_path": str(Path('word_template').absolute()),
                "active": False
            }
        """
        active = True if self.get_current_active() == 'no-data' else False
        doc_id = self.generate_hash_id()

        new_doc = {
            "name": doc_name,                  
            "save_directory": directory,
            "template_path": str(Path('word_template').absolute()),
            "author_option": author_option,
            "active": active
        }
        self.docs['Documents'][doc_id] = new_doc
        self.write(self.docs)
        return doc_id


    def add_to_historic(self, path:str, change_number:str, doc_number:str) -> None:
        """
        Adds a new JSON object to the current JSON config file with the following information:
            [historic_id -> hash]:{                
                "change_number": [change_number -> parameter],
                "directory": [path -> parameter],
                "date": datetime.today().strftime('%d/%m/%Y')
            }
        """
        historic_id = self.generate_hash_id()
        new_doc = {
            "change_number": change_number,
            "directory": str(path),
            "version": doc_number,
            "date": datetime.today().strftime('%d/%m/%Y'),
            "exist": True
        }
        self.docs['Historic'][historic_id] = new_doc
        self.write(self.docs)


    def generate_hash_id(self) -> str:
        today = str(time.time())
        new_id = hashlib.md5()
        new_id.update(today.encode('utf-8'))
        return new_id.hexdigest()


    def remove_document(self, doc_id:str) -> None:
        doc_removido = self.docs['Documents'].pop(doc_id)
        self.write(self.docs)
    

    def remove_historic(self, historic_id:str) -> None:
        hist_removed = self.docs['Historic'].pop(historic_id)
        self.write(self.docs)


    def change_active(self, doc_id:str) -> None:
        """
        Changes the "active" attribute, which specifies which word template should be generated
        """
        current_active = self.get_current_active()
        
        if current_active != doc_id:
            self.docs['Documents'][current_active]["active"] = False
            self.docs['Documents'][doc_id]["active"] = True
            self.write(self.docs)


    def change_save_directory(self, doc_id:str, new_directory:str) -> bool:
        """
        Change the directory where generated work documents will be saved
        """        
        if self.docs['Documents'][doc_id]["save_directory"] != new_directory:
            self.docs['Documents'][doc_id]["save_directory"] = new_directory
            self.write(self.docs)
            return True
        return False


    def change_author_format(self, doc_id:str, new_option:str) -> bool:
        """
        Changes the formatting of the username used in the document
            Ex: Username => jeff
                Nome completo => Jeff Bezos
        """
        if self.docs['Documents'][doc_id]['author_option'] != new_option:
            self.docs['Documents'][doc_id]['author_option'] = new_option
            self.write(self.docs)
            return True
        return False
        

    def get_current_active(self) -> str:
        """
        Returns the doc_id of only the first document 
        (since a list with a single element will be returned in the for loop)
        """
        active = [doc_id for doc_id in self.docs['Documents'] if self.docs['Documents'][doc_id]['active'] == True]
        if len(active) > 0:
            return active[0]
        return 'no-data'


    def get_document_name(self, doc_id:str) -> str:
        doc = self.docs[doc_id]
        return doc['name']


    def get_amount_of_document(self, doc_name:str) -> bool:
        found = [doc for doc in self.docs['Documents'] if self.docs['Documents'][doc]['name'] == doc_name]
        return len(found)


    def validate_save_directory(self, save_directory:str) -> bool:
        path = Path(save_directory)
        return path.exists()


    def validate_doc_directory(self, doc_directory:str) -> bool:
        path = Path(doc_directory)
        return path.is_file()
    

    def validate_historic_data(self) -> None:
        all_historic = self.docs['Historic']
        need_change = []
        for historic_id, doc in all_historic.items():
            is_valid = self.validate_doc_directory(doc['directory'])
            if ((not is_valid) and (doc['exist'] == True)) or (is_valid and (doc['exist'] == False)):
                need_change.append(historic_id)
        self.change_valid_historic(need_change)
        
    
    def change_valid_historic(self, need_change:list) -> None:
        if len(need_change) > 0:
            for historic_id in need_change:
                self.docs['Historic'][historic_id]['exist'] = not self.docs['Historic'][historic_id]['exist']
            self.write(self.docs)
