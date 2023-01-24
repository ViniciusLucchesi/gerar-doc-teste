from pathlib import Path
import hashlib
import time
import json


class JSONConfig:
    def __init__(self):
        self.config_path = 'config.json'
        self.docs = self.read()


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
        docs = self.read()

        today = str(time.time())
        new_id = hashlib.md5()
        new_id.update(today.encode('utf-8'))
        doc_id = new_id.hexdigest()

        new_doc = {
            "name": doc_name,                  
            "save_directory": directory,
            "template_path": str(Path('word_template').absolute()),
            "author_option": author_option,
            "active": False
        }
        docs[doc_id] = new_doc
        self.write(docs)
        return doc_id


    def remove(self, doc_name:str) -> None:
        doc_removido = self.docs.pop(doc_name)
        self.write(self.docs)


    def change_active(self, doc_id:str) -> None:
        """
        Changes the "active" attribute, which specifies which word template should be generated
        """
        docs = self.read()
        current_active = self.get_current_active()
        
        if current_active != doc_id:
            docs[current_active]["active"] = False
            docs[doc_id]["active"] = True
            self.write(docs)


    def change_save_directory(self, doc_id:str, new_directory:str) -> bool:
        """
        Change the directory where generated work documents will be saved
        """
        docs = self.read()
        if docs[doc_id]["save_directory"] != new_directory:
            docs[doc_id]["save_directory"] = new_directory        
            self.write(docs)
            return True
        return False


    def change_author_format(self, doc_id:str, new_option:str) -> bool:
        """
        Changes the formatting of the username used in the document
            Ex: Username => jeff
                Nome completo => Jeff Bezos
        """
        if self.docs[doc_id]['author_option'] != new_option:
            self.docs[doc_id]['author_option'] = new_option
            self.write(self.docs)
            return True
        return False
        

    def get_current_active(self) -> str:
        """
        Returns the doc_id of only the first document 
        (since a list with a single element will be returned in the for loop)
        """
        active = [doc_id for doc_id in self.docs if self.docs[doc_id]['active'] == True]
        return active[0]


    def get_document_name(self, doc_id:str) -> str:
        doc = self.docs[doc_id]
        return doc['name']


    def get_amount_of_document(self, doc_name:str) -> bool:
        found = [doc for doc in self.docs if self.docs[doc]['name'] == doc_name]
        return len(found)


    def validate_save_directory(self, save_directory:str) -> bool:
        path = Path(save_directory)
        return path.exists()
    
    def validate_doc_directory(self, doc_directory:str) -> bool:
        path = Path(doc_directory)
        return path.is_file()
