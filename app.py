from flask import Flask, render_template, request, redirect, url_for, flash
from flaskwebgui import FlaskUI
from scripts.document import GerarDocTeste
from scripts.config import JSONConfig
from pathlib import Path
import secrets
import webbrowser



app = Flask(__name__)
app.secret_key = secrets.token_hex()

ui = FlaskUI(app=app, server='flask', width=1100, height=600, port=65000)



@app.route('/')
def index():
    config = JSONConfig()
    docs = config.docs
    keys = list(docs.keys())
    cur_doc = {
        "name": config.get_document_name(config.get_current_active()),
        "save_directory": docs[config.get_current_active()]['save_directory'],
        "author_option": docs[config.get_current_active()]['author_option']
    }
    author_options = ["NICKNAME", "FULL_NAME"]
    return render_template('index.html', docs=docs, keys=keys, cur_doc=cur_doc, author_options=author_options)


@app.route('/generate_document', methods=["GET", "POST"])
def generate_document():
    if request.method == "POST":
        change_number = request.form.get('change_number')
        document = GerarDocTeste(change_number)
        
        config = JSONConfig()
        doc_id = config.get_current_active()
        doc_name = config.docs[doc_id]['name']
        target_path = config.docs[doc_id]["save_directory"]
        author_option = config.docs[doc_id]['author_option']

        if document.is_valid:
            document.create_word_doc(doc_name, target_path, author_option)
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
        author_option = request.form.get('author_option')
        doc_name = Path(doc_path).name

        config = JSONConfig()
        is_valid = config.validate_save_directory(target_path)

        if is_valid:
            doc = GerarDocTeste()
            doc.save_document(doc_path)
            config.add_new_doc(doc_name, target_path, author_option)
            flash('Novo documento adicionado com sucesso', 'success')
        else:
            flash('ERRO: O diretório especificado não existe! Nenhuma modificação realizada.', 'danger')

        return redirect(url_for('index'))


@app.route('/alter_active', methods=['GET', 'POST'])
def alter_active():
    if request.method == 'POST':
        config = JSONConfig()
        doc_id = request.form['options']
        if doc_id != config.get_current_active():
            config.change_active(doc_id)
            flash('Documento padrão alterado com sucesso!', 'success')
        else:
            flash('Escolha um documento diferente do atual para que a mudança possa ser realizada', 'warning')           
    return redirect(url_for('index'))


@app.route('/change_doc_config', methods=['GET', 'POST'])
def change_doc_config():
    if request.method == 'POST':
        target_path = request.form['target_path']
        author_option = request.form['author_option']

        config = JSONConfig()
        is_valid = config.validate_save_directory(target_path)

        if is_valid:
            doc_id = config.get_current_active()
            new_format = config.change_author_format(doc_id, author_option)
            new_directory = config.change_save_directory(doc_id, target_path)

            if (new_directory and new_format):
                flash('Alterações realizadas com sucesso', 'success')
            elif (not new_directory) and new_format:
                flash('Formato do autor alterado com sucesso', 'success')
            elif new_directory and (not new_format):
                flash('Diretório de salvamento alterado com sucesso', 'success')
            else:
                flash('As informações devem ser alteradas para o envio do formulário', 'warning')
        else:
            flash('ERRO: O diretório especificado não existe! Nenhuma modificação realizada.', 'danger')
        return redirect(url_for('index'))
        

@app.route('/delete/<doc_id>', methods=['GET', 'POST'])
def delete(doc_id):
    config = JSONConfig()
    doc = config.docs[doc_id]
    doc_amount = config.get_amount_of_document(doc['name'])

    try:
        if doc_amount == 1:
            Path(doc["template_path"], doc['name']).unlink()
        config.remove(doc_id)
        flash(f'Documento {doc["name"]} removido com sucesso!', 'success')
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
    