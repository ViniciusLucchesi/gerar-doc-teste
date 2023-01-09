from flask import Flask, render_template, request, redirect, url_for
from scripts.document import GerarDocTeste
from scripts import config
from scripts.path import FindFiles
import webbrowser
from pathlib import Path
import re


app = Flask(__name__)

@app.route('/')
def index():
    # default_path = config.DEFAULT_PATH
    default_path = re.sub('\\\\', '/', config.DEFAULT_PATH)
    doc_template = FindFiles(path=config.DOCUMENT_PATH)
    doc_template.find_documents()
    docs_available = doc_template.found

    data = {}
    count = 1
    for doc in docs_available:
        if doc not in config.DOCUMENT_FILE:
            data[count] = (doc, '')
        else:
            data[count] = (doc, 'checked')
        count += 1
    
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
        # file_path = Path(file_name).absolute()
        doc = GerarDocTeste()
        doc.save_document(file_path)
        return redirect(url_for('index'))

@app.route('/alter', methods=['GET', 'POST'])
def alter():
    if request.method == 'POST':
        options = request.form['options']
        if options != config.DOCUMENT_FILE:
            with open('scripts/config.py', encoding='utf-8') as f:
                text = f.readlines()
                text[-1] = f'DOCUMENT_FILE = "{options}"'
                complete_file = ''
                for line in text:
                    complete_file += line            
            with open('scripts/config.py', 'w', encoding='utf-8') as f:
                f.write(complete_file)                
        return redirect(url_for('index'))

@app.route('/delete/<doc_name>', methods=['GET', 'POST'])
def delete(doc_name):
    Path(config.DOCUMENT_PATH, doc_name).unlink()
    return redirect(url_for('index'))


@app.route('/open_document/<document>')
def open_document(document):
    filename = Path(config.DEFAULT_PATH, document)
    print(filename)
    webbrowser.open(filename.absolute())
    return redirect(url_for('success', document=document))


if __name__ == '__main__':
    app.run(debug=True)