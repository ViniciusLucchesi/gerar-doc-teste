from flask import Flask, render_template, request, redirect, url_for
from scripts.document import GerarDocTeste
from scripts import config
from scripts.path import FindFiles
from pathlib import Path
import re
import webbrowser


app = Flask(__name__)

@app.route('/')
def index():
    default_path = re.sub('\\\\', '/', config.DEFAULT_PATH)
    doc_template = FindFiles(path=config.DOCUMENT_PATH)
    doc_template.find_documents()
    data = all_available_documents(doc_template.found)    
    return render_template('index.html', default_path=default_path, data=data)

@app.route('/generate_document', methods=["GET", "POST"])
def generate_document():
    if request.method == "POST":
        change_number = request.form.get('change_number')        
        document = GerarDocTeste(change_number)
        if document.is_valid:
            document.create_word_doc()
            return redirect(url_for('success', document=document.doc_file))
        return redirect(url_for('error'))

@app.route('/success/<document>')
def success(document):
    return render_template('success.html', document=document)

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        file_path = request.form.get('file_path')
        doc = GerarDocTeste()
        doc.save_document(file_path)
        return redirect(url_for('index'))

@app.route('/alter', methods=['GET', 'POST'])
def alter():
    if request.method == 'POST':
        selected_option = request.form['options']
        if selected_option != config.DOCUMENT_FILE:
            replace_variable_value('DOCUMENT_FILE', selected_option)            
    return redirect(url_for('index'))

@app.route('/alter_path', methods=['GET', 'POST'])
def alter_path():
    if request.method == 'POST':
        new_path = request.form['new_path']
        new_path = re.sub('"', '', new_path)
        if new_path != config.DEFAULT_PATH:
            replace_variable_value('DEFAULT_PATH', new_path)               
    return redirect(url_for('index'))

@app.route('/delete/<doc_name>', methods=['GET', 'POST'])
def delete(doc_name):
    Path(config.DOCUMENT_PATH, doc_name).unlink()
    return redirect(url_for('index'))

@app.route('/open_document/<document>')
def open_document(document):
    filename = config.DEFAULT_PATH + document
    webbrowser.open(filename)
    return redirect(url_for('success', document=document))


def all_available_documents(docs_available):
    data = {}
    count = 1
    for doc in docs_available:
        if doc not in config.DOCUMENT_FILE:
            data[count] = (doc, '')
        else:
            data[count] = (doc, 'checked')
        count += 1
    return data

def replace_variable_value(variable, new_path): 
    with open('scripts/config.py', encoding='utf-8') as f:
        script = f.readlines()
        for line in script:
            if variable in line:
                variable_index = script.index(line)

    script[variable_index] = f'{variable} = "{new_path}"\n'    
    script_file = ''.join(map(str, script))

    with open('scripts/config.py', 'w', encoding='utf-8') as f:
        f.write(script_file)


if __name__ == '__main__':
    app.run(debug=True)