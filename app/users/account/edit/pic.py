import os

from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask import request, jsonify, url_for

from app.utils.decorators import token_required
from app.models.database import get_db_connection

from . import edit_blueprint

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')

@edit_blueprint.route('/profilePic', methods=['POST'])
@token_required
def update_profile_pic():
    conn = None
    try:
        user_uuid = request.form.get('userUUID')
        file = request.files.get('file')

        if not user_uuid:
            return jsonify({'error': 'UUID do usuário não fornecido'}), 400
            
        if not file or file.filename == '':
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400

        # Conexão com o banco para pegar a imagem antiga
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT pic FROM usuarios WHERE userUUID = ?', (user_uuid,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return jsonify({'error': 'Usuário não encontrado'}), 404

        old_pic_url = user['pic']

        # Deleta a imagem antiga (se for local)
        if old_pic_url and old_pic_url.startswith('http'):
            filename_in_url = old_pic_url.split('/')[-1]
            old_filepath = os.path.join(UPLOAD_FOLDER, filename_in_url)
            if os.path.exists(old_filepath):
                try:
                    os.remove(old_filepath)
                    print(f"[🗑️] Imagem antiga removida: {filename_in_url}")
                except Exception as e:
                    print(f"[⚠️] Falha ao remover imagem antiga: {str(e)}")

        # Salva a nova imagem
        filename = f"{user_uuid}_{secure_filename(file.filename)}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(filepath)

        print("AQUI PORRA")

        # Atualiza URL no banco
        file_url = url_for('upload.serve_file', filename=filename, _external=True).replace('http://', 'https://')
        print(file_url)

        cursor.execute(
            'UPDATE usuarios SET pic = ? WHERE userUUID = ?', 
            (file_url, user_uuid)
        )
        conn.commit()

        return jsonify({
            'success': True,
            'url': file_url,
            'message': 'Foto de perfil atualizada com sucesso'
        })

    except Exception as e:
        print(f"Erro ao atualizar foto: {str(e)}")
        return jsonify({'error': 'Erro interno no servidor'}), 500

    finally:
        if conn:
            conn.close()
