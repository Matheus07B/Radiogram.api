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
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #ccc;
                background-color: #211f21;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #25282d;
                color: #eee;
                padding: 20px;
                text-align: center;
                border-radius: 8px 8px 0 0;
            }}
            .content {{
                padding: 20px;
                background-color: #2a2a2d;
                border-radius: 0 0 8px 8px;
                border: 1px solid #333;
            }}
            .code {{
                font-size: 24px;
                font-weight: bold;
                color: #fff;
                background-color: #333;
                text-align: center;
                margin: 20px 0;
                padding: 15px;
                border-radius: 5px;
                letter-spacing: 3px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #555;
                text-align: center;
            }}
            .logo {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .logo img {{
                height: 200px;
            }}
            a {{
                color: #4a90e2;
                text-decoration: none;
            }}
            p {{
                color: #fff
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>Recuperação de Senha</h2>
        </div>
        <div class="content">
            <div class="logo">
                <img src="https://web.radiogram.shop/Radiogram.png" alt="Radiogram Logo">
            </div>
            <p>Olá,</p>
            <p>Recebemos uma solicitação para redefinir sua senha. Use o código abaixo para continuar:</p>
            
            <div class="code">{codigo}</div>
            
            <p>Este código é válido por 15 minutos. Se você não solicitou isso, por favor ignore este e-mail.</p>
            <p>Atenciosamente,<br>Equipe Radiogram</p>
        </div>
        <div class="footer">
            <p>© {datetime.datetime.now().year} Radiogram. Todos os direitos reservados.</p>
            <p>Este é um e-mail automático, por favor não responda.</p>
        </div>
    </body>
    </html>
    """
    
    # Versão em texto simples para clientes que não suportam HTML
    text = f"""
    Recuperação de Senha - Radiogram
    -------------------------------
    
    Olá,
    
    Recebemos uma solicitação para redefinir sua senha. Use o código abaixo para continuar:
    
    Código: {codigo}
    
    Este código é válido por 15 minutos. Se você não solicitou isso, por favor ignore este e-mail.
    
    Atenciosamente,
    Equipe Radiogram
    
    © {datetime.datetime.now().year} Radiogram. Todos os direitos reservados.
    """
    
    msg = MIMEMultipart("alternative")
    msg["From"] = email_sender
    msg["To"] = email_destinatario
    msg["Subject"] = subject
    
    # Anexe ambas as versões (texto e HTML)
    msg.attach(MIMEText(text, "plain"))
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