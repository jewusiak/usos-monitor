import email
import smtplib
import ssl
import datetime

import credentials


def send_email(places):
    body = "<ol>"

    for x in places:
        if x['status'] == 'new':
            body += "<li style='margin: 10px 0'>"
            body += f"<b>Nowa grupa</b>: {x['subject_name']} ({x['subject_id']}, gr. {x['group']}) - zajętość: {x['registered']}/{x['max']}. {x['time']}, {x['teacher']}"
            body += '</li>'
        elif x['diff'] > 0:
            body += "<li style='margin: 10px 0'>"
            body += f"<b>Wolne miejsca</b>: {x['subject_name']} ({x['subject_id']}, gr. {x['group']}) - zajętość: {x['registered']}/{x['max']}. {x['time']}, {x['teacher']}"
            body += '</li>'
        elif x['diff'] < 0:
            body += "<li style='margin: 10px 0'>"
            body += f"Zajęto wolne miejsca: {x['subject_name']} ({x['subject_id']}, gr. {x['group']}) - zajętość: {x['registered']}/{x['max']}. {x['time']}, {x['teacher']}"
            body += '</li>'
        else:
            pass
    body += "</ol>"

    message = email.message.EmailMessage()

    message["Subject"] = "Nowe miejsca na WF"

    message["From"] = credentials.mail_from
    message["To"] = credentials.mail_to_address
    html = f"<html><body>{body}</body></html>"
    message.set_content(html, subtype='html')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(credentials.mail_smtp_address, credentials.mail_smtp_port, context=context) as server:
        server.login(credentials.mail_login, credentials.mail_password)
        server.send_message(message)
    print("Wysłano o {}".format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
