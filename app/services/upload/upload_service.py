from flask import Blueprint, request, render_template, send_from_directory, redirect, url_for, abort
from werkzeug.utils import secure_filename
import os
import uuid
import hashlib

upload_blueprint = Blueprint('upload', __name__, template_folder='templates/')

# Tamanho máximo de 2 GB (em bytes)
MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024  # 2 GB

# Caminho fixo para a pasta onde os arquivos serão salvos
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_blueprint.before_request
def limit_file_size():
    if request.content_length is not None and request.content_length > MAX_CONTENT_LENGTH:
        abort(413, description="Arquivo excede o limite de 2 GB.")

# def generate_unique_filename(filename):
#     """Gera um nome único baseado em UUID + hash"""
#     ext = os.path.splitext(filename)[1]  # Pega a extensão original
#     unique_id = str(uuid.uuid4())  # Gera um UUID único
#     hash_part = hashlib.sha256(unique_id.encode()).hexdigest()[:16]  # Hash de 16 caracteres
#     return f"{unique_id}_{hash_part}{ext}"  # Ex: 550e8400-e29b-41d4-a716_4f3c2a8e9b1d.jpg"

@upload_blueprint.route('/')
def index():
    return render_template('index.html')

@upload_blueprint.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return "Nenhum arquivo enviado", 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nome do arquivo inválido"}), 400

    # filename = secure_filename(file.filename)
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    print(url_for('upload.download_link', filename=filename, _external=True))
    return redirect(url_for('upload.download_link', filename=filename))

@upload_blueprint.route('/listFiles', methods=['GET'])
def list_files():
    try:
        files = os.listdir(UPLOAD_FOLDER)  # Lista todos os arquivos na pasta
        files = [f for f in files if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]  # Garante que são arquivos

        if not files:
            return "<p>Nenhum arquivo encontrado.</p><a href='/'>Voltar</a>"

        links = ''.join(
            f'<li><a href="/upload/download/{filename}" download>{filename}</a></li>' for filename in files
        )

        return f"""
        <h3>Arquivos disponíveis para download:</h3>
        <ul>{links}</ul>
        <br><a href="/">Voltar</a>
        """
    except Exception as e:
        return f"Erro ao listar arquivos: {str(e)}", 500

@upload_blueprint.route('/download/<filename>', methods=['GET'])
def download_link(filename):
    print("Teste Dow")
    return send_from_directory(UPLOAD_FOLDER, filename)

@upload_blueprint.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

'''
    return jsonify({
        "message": "Arquivo enviado com sucesso!",
        "filename": unique_filename,
        "url": f"https://cloud-personal.onrender.com/files/{unique_filename}"
    })
'''