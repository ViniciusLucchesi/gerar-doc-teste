from flask import Flask, render_template, request, redirect, url_for
from scripts.document import GerarDocTeste
from scripts.config import DEFAULT_PATH
import os, re


app = Flask(__name__)

@app.route('/')
def index():
    default_path = re.sub('\\\\', '/', DEFAULT_PATH)
    return render_template('index.html', default_path=default_path)

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


@app.context_processor
def utility_processor():
    def open_document(document):
        word_doc = os.path.join(DEFAULT_PATH, document)
        os.startfile(word_doc)
    return dict(open_document=open_document)

if __name__ == '__main__':
    app.run(debug=True)