import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email_codigo(email_destinatario, codigo):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    email_sender = "matheusveneski654@gmail.com"
    email_password = "tfaz ovlq rgnb sskq"

    email_destinatario ="matheusveneski654@gmail.com"

    subject = "Código de Recuperação de Senha"
    body = f"Seu código de recuperação é: {codigo}"

    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = email_destinatario
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_destinatario, msg.as_string())
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
    finally:
        server.quit()
