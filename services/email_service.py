import smtplib
from email.message import EmailMessage
import config
import os


def send_email_with_attachment(recipients, subject, body, attachment_path):
    if not recipients:
        return False, 'Nenhum destinatário informado'
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = config.SMTP_USER or 'no-reply@example.com'
    msg['To'] = ', '.join(recipients)
    msg.set_content(body)

    # Attach file
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            data = f.read()
        maintype = 'application'
        subtype = 'pdf'
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=os.path.basename(attachment_path))

    try:
        if config.SMTP_USE_TLS:
            server = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT)
        if config.SMTP_USER and config.SMTP_PASSWORD:
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True, None
    except Exception as e:
        return False, str(e)
