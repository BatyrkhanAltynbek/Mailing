from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import time

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def send_message(data):
    message = """
Здравствуйте, {} {}!

Ваш логин: {}
Ваш пароль: {}
Ссылка на контест: https://codeforces.com/
Ссылка на инструкция по системе: 

Начало олимпиады: 10:00
Продолжительность: 2 часа

Ссылка на прокторинг: https://proct.iitu.edu.kz/
Ваш логин на прокторинг: {}
Ваш пароль на прокторинг: {}
Инструкция по проторинговой системе: 
Вам надо обязательно держать открытой вкладку сайта прокторинга и дать доступ на трансляцию своего экрана, камере и звуку.

С уважением,
Жюри олимпиады!
    """.format(
        data['name'],
        data['surname'],
        data['username'],
        data['password'],
        data['loginProct'],
        data['passwordProct']
    )
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = data['email']
    mimeMessage['subject'] = 'Олимпиада'    # название письма
    mimeMessage.attach(MIMEText(message, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    service.users().messages().send(userId='me', body={'raw': raw_string}).execute()


with open('data.csv', newline='', encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("Sending data:{}".format(row))
        send_message(data=row)
        print("Send!")
        time.sleep(1)
