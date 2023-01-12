from pathlib import Path
import json


class JSONConfig:
    def __init__(self):
        self.docs = self.read()

    def read(self) -> dict:
        """
        Read a config.json file that contains all documents information to the program work correctly
        This function will be trigger automatically when the class was initiated
        """
        with open('config.json', 'r', encoding='utf-8') as config:
            docs = json.load(config)
        return docs


    def write(self, modified_file:dict) -> None:
        """
        Write in the config.json file the dictionary passed as a parameter
        """
        with open('config.json', 'w', encoding='utf-8') as outfile:
            json.dump(modified_file, outfile)


    def add_new_doc(self, doc_name:str, directory:str) -> None:
        """
        Adds a new JSON object to the current JSON config file with the following information:
            [doc_name -> parameter]: {
                "save_directory": [directory -> parameter],
                "template_path": str(Path('word_template').absolute()),
                "active": False
            }
        """
        docs = self.read()
        new_doc = {                  
            "save_directory": directory,
            "template_path": str(Path('word_template').absolute()),
            "active": False                
        }
        docs[doc_name] = new_doc
        self.write(docs)


    def change_save_directory(self, doc_name:str, new_directory:str) -> None:
        """
        Change the directory where generated work documents will be saved
        """
        docs = self.read()
        docs[doc_name]["save_directory"] = new_directory
        self.write(docs)
    

    def change_active(self, doc_name:str):
        """
        Changes the "active" attribute, which specifies which word template should be generated
        """
        docs = self.read()
        current_active = self.get_current_active()
        
        docs[current_active]["active"] = False
        docs[doc_name]["active"] = True

        self.write(docs)


    def get_current_active(self):
        """
        Returns only the first document 
        (since a list with a single element will be returned in the for loop)
        """
        active = [doc_name for doc_name, doc_value in self.docs.items() if doc_value["active"] == True]
        return active[0]


    def remove(self, doc_name:str) -> None:
        doc_removido = self.docs.pop(doc_name)
        self.write(self.docs)


if __name__ == '__main__':
    config = JSONConfig()
    docs = config.docs
    print(config.get_current_active())