from flask import Flask, render_template, request, redirect, url_for, flash
from flaskwebgui import FlaskUI
from scripts.document import GerarDocTeste
from scripts.config import JSONConfig
from pathlib import Path
import secrets
import webbrowser


app = Flask(__name__)
app.secret_key = secrets.token_hex()

ui = FlaskUI(app=app, server='flask', width=1100, height=600, fullscreen=False)


@app.route('/')
def index():
    config = JSONConfig()
    docs = config.docs
    keys = list(docs.keys())
    cur_doc = {
        "name": config.get_current_active(),
        "save_directory": docs[config.get_current_active()]['save_directory']
    }
    return render_template('index.html', docs=docs, keys=keys, cur_doc=cur_doc)


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
    flash('Digite o número da change de acordo com o padrão do Service-Now!', 'warning')
    return redirect(url_for('index'))


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


@app.route('/change_directory', methods=['GET', 'POST'])
def change_directory():
    if request.method == 'POST':
        doc_name = request.form['doc_name']
        target_path = request.form['target_path']

        config = JSONConfig()
        if not config.change_save_directory(doc_name, target_path):
            flash('O caminho se manteve o mesmo, portanto não foi alterado', 'warning')
        else:
            flash('Caminho alterado com Sucesso!', 'success')
        return redirect(url_for('index'))
        

@app.route('/delete/<doc_name>', methods=['GET', 'POST'])
def delete(doc_name):
    config = JSONConfig()
    doc = config.docs[doc_name]
    try:
        Path(doc["template_path"], doc_name).unlink()
        config.remove(doc_name)
        flash(f'Documento {doc_name} removido com sucesso!', 'success')
    except RuntimeError as error:
        flash(f'Erro: {error}', 'danger')

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
    ui.run()