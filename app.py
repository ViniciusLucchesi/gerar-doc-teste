from flask import Flask, render_template, request, redirect, url_for, flash
from scripts.document import GerarDocTeste
from scripts.config import JSONConfig
from flaskwebgui import FlaskUI
from pathlib import Path
import webbrowser
import secrets



app = Flask(__name__)
app.secret_key = secrets.token_hex()

ui = FlaskUI(app=app, server='flask', width=1010, height=505, port=65000)



# Views
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/configuration', methods=['GET'])
def configuration():
    config = JSONConfig()
    docs = config.docs
    keys = list(docs.keys())
    cur_doc_id = config.get_current_active()
    return render_template('partials/all_docs.html', docs=docs, keys=keys, cur_doc_id=cur_doc_id)

@app.route('/configuration/edit_doc/<doc_id>', methods=['GET'])
def edit_doc(doc_id:str):
    config = JSONConfig()
    doc = config.docs[doc_id]    
    author_options = ["Username", "Nome completo"]
    return render_template('partials/edit_doc.html', doc=doc, cur_doc_id=doc_id, author_options=author_options)

@app.route('/configuration/new_doc', methods=['GET'])
def new_doc():
    config = JSONConfig()
    cur_doc_id = config.get_current_active()
    author_options = ["Username", "Nome completo"]
    return render_template('partials/new_doc.html', author_options=author_options, cur_doc_id=cur_doc_id)

@app.route('/success/<document>', methods=['GET'])
def success(document:str):
    return render_template('success.html', document=document)


# Methods
@app.route('/generate_document', methods=['POST'])
def generate_document():
    change_number = request.form.get('change_number')
    document = GerarDocTeste(change_number)
    
    if document.is_valid:
        config = JSONConfig()
        doc_id = config.get_current_active()
        doc_name = config.docs[doc_id]['name']
        target_path = config.docs[doc_id]["save_directory"]
        author_option = config.docs[doc_id]['author_option']

        if config.validate_save_directory(target_path):                
            document.create_word_doc(doc_name, target_path, author_option)
            return redirect(url_for('success', document=document.doc_file))
        
        msg='O diretório especificado não existe!'
        type='danger'
        return redirect(url_for('alert_message', msg=msg, type=type, route='index'))

    msg='Digite o número da change de acordo com o padrão do Service-Now!'
    type='warning'
    return redirect(url_for('alert_message', msg=msg, type=type, route='index'))

@app.route('/alert_message/<msg>&<type>&<route>', methods=['GET'])
def alert_message(msg:str, type:str, route:str):
    flash(msg, type)
    return redirect(url_for(route))

@app.route('/add', methods=['POST'])
def add():
    config = JSONConfig()
    doc_path = request.form.get('doc_path')
    target_path = request.form.get('target_path')
    author_option = request.form.get('author_option')        
    
    is_valid_file = config.validate_doc_directory(doc_path)
    is_valid_path = config.validate_save_directory(target_path)

    if is_valid_path:
        if is_valid_file:
            doc_name = Path(doc_path).name
            doc = GerarDocTeste()
            doc.save_document(doc_path)
            doc_id = config.add_new_doc(doc_name, target_path, author_option)            

            change_active = request.form.getlist('makeActive')
            if change_active[0] == 'on':
                config.change_active(doc_id)
            
            msg='Novo documento adicionado com sucesso'
            type='success'
        else:
            msg='ERRO: Documento Word não encontrado! Nenhuma modificação realizada.'
            type='danger'
    else:
        msg='ERRO: O diretório especificado não existe! Nenhuma modificação realizada.'
        type='danger'
    
    return redirect(url_for('alert_message', msg=msg, type=type, route='configuration'))

@app.route('/alter_active/<route>', methods=['POST'])
def alter_active(route:str):
    config = JSONConfig()
    doc_id = request.form['options']

    if doc_id != config.get_current_active():
        config.change_active(doc_id)
        msg = 'Documento padrão alterado com sucesso!'
        type = 'success'
    else:            
        msg = 'Escolha um documento diferente do atual para que a mudança possa ser realizada'
        type = 'warning'
    return redirect(url_for('alert_message', msg=msg, type=type, route=route))

@app.route('/change_doc_config/<doc_id>', methods=['GET','POST'])
def change_doc_config(doc_id:str):
    target_path = request.form['target_path']
    author_option = request.form['author_option']
    
    config = JSONConfig()
    is_valid = config.validate_save_directory(target_path)

    if is_valid:
        change_active = request.form.getlist('makeActive')
        try:
            if change_active[0] == 'on':
                config.change_active(doc_id)
                new_pattern = True
        except Exception:
            new_pattern = False
        
        new_format = config.change_author_format(doc_id, author_option)
        new_directory = config.change_save_directory(doc_id, target_path)
        type = 'success'

        if (new_directory and new_format and new_pattern):
            msg = 'Alterações realizadas com sucesso'                
        elif ((not new_directory) and (not new_pattern)) and new_format:
            msg = 'Formato do autor alterado com sucesso'                
        elif new_directory and ((not new_format) and (not new_pattern)):
            msg = 'Diretório de salvamento alterado com sucesso'
        elif new_pattern and ((not new_directory) and (not new_format)):
            msg = 'Documento padrão alterado com sucesso!'
        else:
            msg = 'As informações devem ser alteradas para o envio do formulário'
            type = 'warning'
    else:
        msg = 'ERRO: O diretório especificado não existe! Nenhuma modificação foi realizada'
        type = 'danger'
    return redirect(url_for('alert_message', msg=msg, type=type, route='configuration'))
        
@app.route('/delete/<doc_id>', methods=['GET'])
def delete(doc_id:str):
    config = JSONConfig()
    doc = config.docs[doc_id]
    doc_amount = config.get_amount_of_document(doc['name'])
    try:
        if doc_amount == 1:
            Path(doc["template_path"], doc['name']).unlink()
        config.remove(doc_id)
        msg = f'Documento {doc["name"]} removido com sucesso!'
        type = 'success'
    except Exception as error:
        msg = f'ERRO: {error}'
        type = 'danger'
    return redirect(url_for('alert_message', msg=msg, type=type, route='configuration'))

@app.route('/open_document/<document>', methods=['GET'])
def open_document(document:str):
    config = JSONConfig()
    doc_name = config.get_current_active()
    doc = config.docs[doc_name]

    filename = doc['save_directory'] + document
    webbrowser.open(filename)
    return redirect(url_for('success', document=document))



if __name__ == '__main__':
    # app.run(debug=True)
    ui.run()
    