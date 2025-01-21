import smtplib
from flask import Blueprint, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_blueprint = Blueprint('/email', __name__)

@email_blueprint.route('', methods=['GET'])
def enviar_email():
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_sender = "matheusveneski654@gmail.com"  # Seu e-mail
    email_destinatario = "matheusveneski654@gmail.com"  # Destinatário fixo
    email_password = "koyn eoxi xlmp oyzm"  # Sua senha de aplicativo
    subject = "Teste de envio de email"
    body = "Este é um teste de envio de e-mail utilizando Flask e smtplib."

    # Criando o conteúdo do e-mail
    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = email_destinatario
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Conectando ao servidor SMTP e enviando o e-mail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_destinatario, msg.as_string())
        server.quit()

        # Retornando sucesso
        return jsonify({"envio": "email enviado com sucesso"}), 200
    except Exception as e:
        # Tratando erros
        return jsonify({"error": f"Erro ao enviar e-mail: {e}"}), 500
