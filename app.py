from flask import Flask, render_template, request, redirect, url_for
from scripts.document import GerarDocTeste
from scripts.config import JSONConfig
from pathlib import Path
import webbrowser


app = Flask(__name__)

@app.route('/')
def index():
    config = JSONConfig()
    docs = config.docs
    keys = list(docs.keys())
    return render_template('index.html', docs=docs, keys=keys)

@app.route('/generate_document', methods=["GET", "POST"])
def generate_document():
    if request.method == "POST":
        change_number = request.form.get('change_number')
        document = GerarDocTeste(change_number)
        
        config = JSONConfig()
        doc_name = config.get_current_active()
        target_path = config.docs[doc_name]["save_directory"]

        if document.is_valid:
            document.create_word_doc(doc_name, target_path)
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
        doc_path = request.form.get('doc_path')
        target_path = request.form.get('target_path')
        doc_name = Path(doc_path).name

        doc = GerarDocTeste()
        doc.save_document(doc_path)

        config = JSONConfig()
        config.add_new_doc(doc_name, target_path)

        return redirect(url_for('index'))

@app.route('/alter', methods=['GET', 'POST'])
def alter():
    if request.method == 'POST':
        config = JSONConfig()        
        selected_doc = request.form['options']        
        if selected_doc != config.get_current_active():
            config.change_active(selected_doc)            
    return redirect(url_for('index'))

@app.route('/delete/<doc_name>', methods=['GET', 'POST'])
def delete(doc_name):
    config = JSONConfig()
    doc = config.docs[doc_name]

    Path(doc["template_path"], doc_name).unlink()
    config.remove(doc_name)

    return redirect(url_for('index'))

@app.route('/open_document/<document>')
def open_document(document):
    config = JSONConfig()
    doc_name = config.get_current_active()
    doc = config.docs[doc_name]

    filename = doc['save_directory'] + document
    webbrowser.open(filename)
    return redirect(url_for('success', document=document))



if __name__ == '__main__':
    app.run(debug=True)