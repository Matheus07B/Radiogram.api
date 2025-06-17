import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(email_destinatario, codigo):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_sender = os.getenv('EMAIL_SENDER')
    email_password = os.getenv("EMAIL_KEY")

    subject = "🔑 Seu Código de Recuperação - Radiogram"
    
    # Versão HTML do e-mail
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #ccc; background-color: #211f21; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background-color: rgb(16,16,16); color: #eee; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
            <h2 style="margin: 0;">Recuperação de Senha</h2>
        </div>
        <div style="padding: 20px; background-color: #2a2a2d; border-radius: 0 0 8px 8px; border: 1px solid #333;">
            <div style="text-align: center; margin-bottom: 20px;">
                <img style="width: 100px;" src="https://web.radiogram.shop/Radiogram.png" alt="Radiogram Logo">
            </div>
            <p style="color: #fff;">Olá,</p>
            <p style="color: #fff;">Recebemos uma solicitação para redefinir sua senha. Use o código abaixo para continuar:</p>

            <div style="font-size: 24px; font-weight: bold; color: #fff; background-color: #333; text-align: center; margin: 20px 0; padding: 15px; border-radius: 5px; letter-spacing: 3px;">
                {codigo}
            </div>

            <p style="color: #fff;">Este código é válido por 15 minutos. Se você não solicitou isso, por favor ignore este e-mail.</p>
            <p style="color: #fff;">Atenciosamente,<br>Equipe Radiogram</p>
        </div>
        <div style="margin-top: 20px; font-size: 12px; color: #555; text-align: center;">
            <p style="color: #555;">© {datetime.datetime.now().year} Radiogram. Todos os direitos reservados.</p>
            <p style="color: #555;">Este é um e-mail automático, por favor não responda.</p>
        </div>
    </body>
    </html>
    """
    
    msg = MIMEMultipart("alternative")
    msg["From"] = email_sender
    msg["To"] = email_destinatario
    msg["Subject"] = subject
    
    # Anexe ambas as versões (texto e HTML)
    # msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_destinatario, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False