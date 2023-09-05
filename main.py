from telebot import TeleBot, types
import config
import imaplib
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re
from email import message_from_bytes
import smtplib
from email.mime.text import MIMEText  # Импортирование нужных библиотек
API_TOKEN = '5851371679:AAHi0cGLX0LAtRDfjZsX7b0LSH7MHrLJa_g' # Используем этот токен для доступа к HTTP API
bot =TeleBot(API_TOKEN)
class User: # Создание класса в котром хранитсья информация о пользователе
    def __init__(self, login): # Конструктор класса
        self.password = None
        self.login = login
        self.receiver = None
        self.theme = None
user_dict = {} # Словарь,который мы будем использовать в качестве базы данных 
@bot.message_handler(commands=['help', 'start']) # Команды на которые отвечате бот
def send_welcome(message: types.Message): # Стартовая функция, которая запускается сразу после входа в бот и которая осуществляет ввод логин пользователя
    bot.send_message(chat_id=message.chat.id, text="Приветствую.Введите логин(Для того чтобы начать с начала напишите /help)") 
    bot.register_next_step_handler(message, next1_step) # Переход к следующему шагу


def next1_step(message: types.Message): # Функция, которая запрашивает пароль у пользователя 
   chat_id = message.chat.id # ID нашего пользователя
   login = message.text # Логин нашего пользователя
   user = User(login) # Заносим информацию о пользователе в словарь, чтобы с помощью него запомнить нашего пользователя
   user_dict[chat_id] = user
   bot.send_message(chat_id=message.chat.id, text='Введите пароль для приложений от почты')
   bot.register_next_step_handler(message, next_step2) # Переход к следующему шагу


def next_step2(message: types.Message): # Функция, которая спрашивает пользователя, что он хочет сделать
   password = message.text # Пароль нашего пользователя
   chat_id = message.chat.id # ID нашего пользователя, используя его, мы с можем получить информацию о нашем пользователе из словаря
   user = user_dict[chat_id] # Находим нашего пользователя
   user.password=password # Пароль нашего пользователя
   bot.send_message(chat_id=message.chat.id, text='Введите 1 если хотите прочитать все непрочитанные сообщения,\n Введите 2 если хотите посмотреть непрочитанные сообщения,\n Введите 3 если хотите отправить сообщение')
   bot.register_next_step_handler(message, final_step) # Переход к следующему шагу

def final_step(message): # Функция, Выполняет команды пользователя
        chat_id = message.chat.id # ID нашего пользователя, используя его, мы с можем получить информацию о нашем пользователе из словаря
        user = user_dict[chat_id] # Находим нашего пользователя
        if(message.text=='1'): # Введите 1 если хотите прочитать все непрочитанные сообщения
         imap_server='imap.gmail.com' # Указывае сервер с почтой gmail
         email=user.login # Получаем логин нашего пользователя
         password=user.password # Получаем пароль нашего пользователя
         imap=imaplib.IMAP4_SSL(imap_server) # Протокол для поиска нашей электроннной почты
         imap.login(email,password) # Вход в почту пользователя
         imap.select('Inbox') # Переходим к ящику с письмами пользователя
         num_of_mes=imap.search(None,"UNSEEN")  # Определяем количество непрочитанных писем 
         result, data = imap.uid('search', None, "UNSEEN") # Получаем информацию о наших письмах
         if result == 'OK': # Проверка правильности испольнения команды выше
            for num in data[0].split(): # цикл в котором мы выводим письма
               result, data = imap.uid('fetch', num, '(RFC822)') # Делаем запросы с помощью fetch
               if result == 'OK': # Проверка правильности испольнения команды выше
                  messagee = message_from_bytes(data[0][1]) # Получаем информацию о i письме
                  print((f"Message Number: {num}"))
         imap.close() # конец работы
         bot.send_message(chat_id=message.chat.id, text='Введите 1 если хотите прочитать все непрочитанные сообщения,\n Введите 2 если хотите посмотреть непрочитанные сообщения,\n Введите 3 если хотите отправить сообщение')
         bot.register_next_step_handler(message, final_step) # Переход к следующему шагу

        elif(message.text=='2'): # Введите 2 если хотите посмотреть непрочитанные сообщения
         imap_server='imap.gmail.com' # Указывае сервер с почтой gmail
         email=user.login # Получаем логин нашего пользователя
         password=user.password # Получаем пароль нашего пользователя
         imap=imaplib.IMAP4_SSL(imap_server) # Протокол для поиска нашей электроннной почт
         imap.login(email,password) # Вход в почту пользователя
         imap.select('Inbox') # Переходим к ящику с письмами пользователя
         num_of_mes=imap.search(None,"UNSEEN") # Определяем количество непрочитанных писем
         result, data = imap.uid('search', None, "UNSEEN") # Получаем информацию о наших письмах
         if result == 'OK': # Проверка правильности испольнения команды выше
            for num in data[0].split(): # цикл в котором мы выводим письма
               result, data = imap.uid('fetch', num, '(RFC822)')  # Делаем запросы с помощью fetch
               if result == 'OK':  # Проверка правильности испольнения команды выше
                  messagee = message_from_bytes(data[0][1])  # Ниже в области действия if бот выводит информацию о письме
                  bot.send_message(chat_id=message.chat.id,text=(f"Message Number: {num}")) # Вывод номера письма
                  bot.send_message(chat_id=message.chat.id,text=(f"From: {messagee.get('From')}")) # Вывод от кого письмо
                  bot.send_message(chat_id=message.chat.id,text=(f"To: {messagee.get('To')}-"))  # Вывод кому письмо
                  bot.send_message(chat_id=message.chat.id,text=(f"Date: {messagee.get('Date')}")) # Вывод даты, когда пришло письмо
                  bot.send_message(chat_id=message.chat.id,text=("Content: ")) # Выводим содержимое письма если это текст или файл
                  for part in messagee.walk():
                     if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain': # проверка что содержимое письма текст
                        bot.send_message(chat_id=message.chat.id,text=(base64.b64decode(part.get_payload()).decode())) # вывод текста
                     if part.get_content_disposition() == 'attachment': # проверка что содержимое письма файл
                        bot.send_message(chat_id=message.chat.id,text=(decode_header(part.get_filename())[0][0].decode())); # вывод имени файла
         imap.close() # конец работы
         bot.send_message(chat_id=message.chat.id, text='Введите 1 если хотите прочитать все непрочитанные сообщения,\n Введите 2 если хотите посмотреть непрочитанные сообщения,\n Введите 3 если хотите отправить сообщение')
         bot.register_next_step_handler(message, final_step)
        elif(message.text=='3'): # Введите 3 если хотите отправить сообщение
            bot.send_message(chat_id=message.chat.id, text='Кому будем отправлять сообщение')
            bot.register_next_step_handler(message, next_step3) # Переход к следующему шагу
def next_step3(message: types.Message): # Функция, которая спрашивает пользователя кому он хочет отправить сообщение
   receiver = message.text # Почта, на которую мы планируем отправить письмо
   chat_id = message.chat.id # ID нашего пользователя, используя его, мы с можем получить информацию о нашем пользователе из словаря
   user = user_dict[chat_id] # Находим нашего пользователя
   user.receiver=receiver # Заносим информацию о получателе в класс
   bot.send_message(chat_id=message.chat.id, text='Тема сообщения')
   bot.register_next_step_handler(message, next_step4) # Переход к следующему шагу
def next_step4(message: types.Message):
   theme = message.text # Тема нашего сообщения
   chat_id = message.chat.id # ID нашего пользователя, используя его, мы с можем получить информацию о нашем пользователе из словаря
   user = user_dict[chat_id] # Находим нашего пользовател
   user.theme=theme # Заносим информацию о теме в класс
   bot.send_message(chat_id=message.chat.id, text='Введите текст сообщения')
   bot.register_next_step_handler(message, next_step5) # Переход к следующему шагу
def next_step5(message: types.Message):
   msg = MIMEText(message.text) # Текст нашего сообщения
   chat_id = message.chat.id # ID нашего пользователя, используя его, мы с можем получить информацию о нашем пользователе из словаря
   user = user_dict[chat_id] # Находим нашего пользовател
   msg['Subject']=user.theme # Вводим тему нашего сообщения
   server = smtplib.SMTP("smtp.gmail.com", 587) # Определяет объект сеанса пользоватедля SMTP, который можно использовать для отправки писем
   server.starttls() # Шифрование
   server.login(user.login,user.password) # Взод в почту
   server.sendmail(user.login,user.receiver,msg.as_string()) # Отправка письма
   bot.send_message(chat_id=message.chat.id, text='Введите 1 если хотите прочитать все непрочитанные сообщения,\n Введите 2 если хотите посмотреть непрочитанные сообщения,\n Введите 3 если хотите отправить сообщение')
   bot.register_next_step_handler(message, final_step) # Переход к следующему шагу
bot.infinity_polling(skip_pending=True)







