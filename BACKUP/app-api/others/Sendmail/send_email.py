import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações do e-mail
smtp_server = "smtp.gmail.com"  # Servidor SMTP (exemplo: Gmail)
smtp_port = 587  # Porta SMTP (587 para TLS)

email_sender = "matheusveneski654@gmail.com"
email_password = "tfaz ovlq rgnb sskq"  # Use uma senha de aplicativo, se necessário

email_receiver = "matheusveneski654@gmail.com"

# Criação da mensagem
subject = "Assunto do e-mail"
body = "Este é o corpo do e-mail."

# Monta o e-mail
msg = MIMEMultipart()
msg["From"] = email_sender
msg["To"] = email_receiver
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

try:
    # Conexão com o servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Ativa o modo TLS
    server.login(email_sender, email_password)
    
    # Envia o e-mail
    server.sendmail(email_sender, email_receiver, msg.as_string())
    print("E-mail enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar e-mail: {e}")
finally:
    server.quit()
