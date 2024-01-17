import logging
import sys
import telebot
from telebot import types # для указания типов
import time
import gspread
import pandas as pd
from datetime import datetime
from telefunc import tel_token, sql_base_read_, admin
from speaker import download_file, recognize_speech


token = tel_token()
bot = telebot.TeleBot(token)

butList = (
    "🔑 Вариант",
    "📈 Топ",
    "📒 Методички",
    "📖 Учебник",
    "📆 Расписание преподавателя",
    "📞 Контакты преподавателя"
)

butAdmin = (
    "📩 Рассылка",
    "🗂 Список пользователей",
    "📲 Отправить контингент",
    "❌ Выход"
)


def user_sql(user_id): #регистрация пользователя в списке рассылок
    with sql_base_read_() as connection:
        print(connection)
        show_db_query = "INSERT INTO teldata (user_id, active) VALUES (%s, %s)"
        data_tg = [(user_id, 1)]
        with connection.cursor() as cursor:
            cursor.executemany(show_db_query, data_tg)
            connection.commit()
            print("id append")

def user_select(message):  # подпрограмма рассылки пользователям сообщений
    with sql_base_read_() as connection:
        print(connection)
        show_select = "SELECT user_id FROM data_user"
        with connection.cursor() as cursor:
            cursor.execute(show_select)
            for result in cursor.fetchall():
                bot.copy_message(chat_id = result, from_chat_id=message.chat.id, message_id=message.message_id)

def user_sql_reg(user_id, username, group, surname, name, aftername, study): #регистрация студента в базе данных
    with sql_base_read_() as connection:
        print(connection)
        show_db_query = "INSERT INTO namedata (user_id, user_name, user_group, syrname, name, aftername, study) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data_tg = [(user_id, username, group, surname, name, aftername, study)]
        with connection.cursor() as cursor:
            cursor.executemany(show_db_query, data_tg)
            connection.commit()
            print("user registered")

def user_reg(user_id, name, profile, name_group, section, variant, variant_D1): #регистрация студента в базе данных
    with sql_base_read_() as connection:
        #print(connection)
        show_db_query = "INSERT INTO data_user (user_id, name, profile, name_group, section, variant, variant_D1) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data_tg = [(user_id, name, profile, name_group, section, variant, variant_D1)]
        with connection.cursor() as cursor:
            cursor.executemany(show_db_query, data_tg)
            connection.commit()
            print("user registered")

def var(user_id):
    try:
        with sql_base_read_() as connection:
            #print(connection)
            show_select = f"SELECT name, variant, variant_D1 FROM data_user WHERE user_id = {user_id}"
            with connection.cursor() as cursor:
                cursor.execute(show_select)
                res = cursor.fetchall()
                text = f'Обучающийся {res[0][0]}: \nВариант №{res[0][1]}, для Д1 №{res[0][2]}'
                return text

    except:
        return "Вариант не найден"


class ComandBot(object):

    def __init__(self, message, bot=bot):
        self.message = message
        self.bot = bot

    def welcome(self):
        msg = bot.reply_to(self.message,
                           "Приветствую! Я твой телеграм-помощник в области теоретической механики. Давайте познакомимся, напиши свою фамилию имя отчество:")
        user_sql(self.message.from_user.id)
        name_dict.update({str(self.message.chat.id): []})
        return msg

    def name_search(self):
        text = self.message.text
        df = pd.read_excel('Контингент.xlsx')
        name_dict[str(self.message.chat.id)].append(df.loc[df['name'] == text.title()]['name'].values[0])
        name_dict[str(self.message.chat.id)].append(
            df.loc[df['name'] == name_dict[str(self.message.chat.id)][0]]['profile'].values[0])
        name_dict[str(self.message.chat.id)].append(
            str(df.loc[df['name'] == name_dict[str(self.message.chat.id)][0]]['group'].values[0]))
        name_dict[str(self.message.chat.id)].append(
            df.loc[df['name'] == name_dict[str(self.message.chat.id)][0]]['section'].values[0])
        name_dict[str(self.message.chat.id)].append(
            str(df.loc[df['name'] == name_dict[str(self.message.chat.id)][0]]['variant'].values[0]))
        name_dict[str(self.message.chat.id)].append(
            str(df.loc[df['name'] == name_dict[str(self.message.chat.id)][0]]['variant_D1'].values[0]))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Нет")
        btn2 = types.KeyboardButton("Да")
        markup.add(btn1, btn2)
        msg = bot.send_message(self.message.chat.id,
                               f'Подтвердите личность: {name_dict[str(self.message.chat.id)][0]}, направление {name_dict[str(self.message.chat.id)][1]}, группа {name_dict[str(self.message.chat.id)][2]}, подгруппа {name_dict[str(self.message.chat.id)][3]}',
                               reply_markup=markup)
        return msg

    def button_default(self):  # кнопки по умолчанию
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but = (types.KeyboardButton(bs) for bs in butList)
        markup.add(*but)
        return markup

    def app_user(self):
        user_reg(str(self.message.chat.id), name_dict[str(self.message.chat.id)][0], name_dict[str(self.message.chat.id)][1],
                 name_dict[str(self.message.chat.id)][2], name_dict[str(self.message.chat.id)][3],
                 name_dict[str(self.message.chat.id)][4], name_dict[str(self.message.chat.id)][5])
        bot.send_message(admin(),
                         f'Добавлен пользователь: \n{name_dict[str(self.message.chat.id)][0]} направление {name_dict[str(self.message.chat.id)][1]}, группа {name_dict[str(self.message.chat.id)][2]}, подгруппа {name_dict[str(self.message.chat.id)][3]}')
        name_dict[str(self.message.chat.id)].clear()
        bot.send_message(self.message.chat.id,
                         "Приятно познакомиться! Теперь ты можешь пользоваться кнопками на телеграм-клавиатуре.",
                         reply_markup=self.button_default())

    def menu(self):
        bot.send_message(self.message.chat.id, 'Загрузка ⚙️', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(self.message.chat.id, 'Клавиатура выведена ⌨️',
                         reply_markup=self.button_default())

    def del_menu(self):
        bot.send_message(self.message.chat.id, 'Удаление ⚙️', reply_markup=types.ReplyKeyboardRemove())

    def help_bot(self):
        HELP = """
Привет! Я твой робот-помощник в освоении предмета "Теоретическая механика".
В меню встроенной клавиатуры ты можешь найти пособия для самостоятельной работы, учебник.
Также возможно найти свой вариант, студенческий рейтинг, расписание преподавателя.
Список доступных команд:
/help - вывести справку по чат-боту
/menu - вызов встроенной клавиатуры
/mic - расшифровка голосовых сообщений
Разработчик © Юрий Солдатов
        """
        bot.send_message(self.message.chat.id, HELP)

class ButtonBot(object):

    def __init__(self, message, bot=bot):
        self.message = message
        self.inl = types.InlineKeyboardMarkup()

    def top_stud(self):
        button1 = types.InlineKeyboardButton("Рейтинг студентов",
                                             url='https://drive.google.com/file/d/17H105tExHL_ZZjmNGhy5yhqfOBsexuvv/view?usp=sharing')
        self.inl.add(button1)
        bot.send_message(self.message.chat.id, 'Рейтинг студентов в файле по ссылке:', reply_markup=self.inl)

    def metod(self):
        button1 = types.InlineKeyboardButton("Статика",
                                             url='https://drive.google.com/file/d/172EuTxLjZlYR0GYi03wdbzu70kae4RdC/view?usp=sharing')
        button2 = types.InlineKeyboardButton("Кинематика",
                                             url='https://drive.google.com/file/d/1i23gh8Kcsu-R5OkyHfdbp7SFUW2c73kx/view?usp=sharing')
        button3 = types.InlineKeyboardButton("Динамика",
                                             url='https://drive.google.com/file/d/1wrluEFNR18gYT1wFe-oLsmar9pxSB8ZH/view?usp=sharing')
        self.inl.add(button1, button2, button3)
        bot.send_message(self.message.chat.id, 'Ссылки на методические указания:', reply_markup=self.inl)

    def study(self):
        button1 = types.InlineKeyboardButton("Учебник",
                                             url='https://drive.google.com/file/d/17OhsVDAaPVkdBEMbjl3wR0Scj7WjeMYo/view?usp=drive_link')
        self.inl.add(button1)
        bot.send_message(self.message.chat.id, 'Ссылка на учебник: "Краткий курс теоретической механики"',
                         reply_markup=self.inl)

    def shedule(self):
        button1 = types.InlineKeyboardButton("Расписание",
                                             url='https://drive.google.com/file/d/17JUNCEKttgoa4HwPY63l0RB3CGJITdyU/view?usp=sharing')
        self.inl.add(button1)
        bot.send_message(self.message.chat.id, 'Расписание преподавателя можете найти по ссылке ниже',
                         reply_markup=self.inl)

    def contact(self):
        button1 = types.InlineKeyboardButton("Telegram", url='https://t.me/general_soldatov')
        button2 = types.InlineKeyboardButton("ВК", url='https://vk.com/general_soldatov')
        self.inl.add(button1, button2)
        bot.send_message(self.message.chat.id, 'Контакты преподавателя можете найти по ссылке ниже',
                         reply_markup=self.inl)


class AdminBot(object):

    def __init__(self, message, bot=bot):
        self.message = message

    def adminButton(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but = (types.KeyboardButton(bs) for bs in butAdmin)
        markup.add(*but)
        return markup



test_data = {}

name_dict = {}

varTask = {}

@bot.message_handler(commands=['start']) # функция начала работы бота с регистрацией студента в БД
def send_welcome(message): #функция на команды
	msg = ComandBot(message).welcome()
	bot.register_next_step_handler(msg, namered)


def namered(message):
    try:
        msg = ComandBot(message).name_search()
        bot.register_next_step_handler(msg, appUser)
    except Exception as e:
        msg = bot.send_message(message.chat.id, "Проверьте правильность ввода данных.")
        bot.register_next_step_handler(msg, namered)
        print(e)

def appUser(message):
    text = message.text
    if text == "Нет":
        msg = bot.send_message(message.chat.id, "Введи свою фамилию имя отчество.")
        bot.register_next_step_handler(msg, namered)
    else:
        ComandBot(message).app_user()

@bot.message_handler(commands=['menu']) #вывод клавиатуры
def menu(message): ComandBot(message).menu()

@bot.message_handler(commands=['del']) #удаление меню
def delMenu(message): ComandBot(message).del_menu()

@bot.message_handler(commands=['help']) #вывод справки
def helpBot(message): ComandBot(message).help_bot()

@bot.message_handler(commands=['mic']) #расшифровка голосовых
def mic(message):
    msg = bot.send_message(message.chat.id, 'Отправьте голосовое сообщение.')
    bot.register_next_step_handler(msg, transcripter)

def transcripter(message):
    try:
        filename = download_file(bot, message.voice.file_id)
        text = recognize_speech(filename)
        bot.send_message(message.chat.id, text)
    except Exception as e:
        bot.send.message(message.chat.id, f'Возникла ошибка {e}')

@bot.message_handler(commands=['admin']) #панель управления администратора
def adminBot(message):
    if message.from_user.id == admin():
        bot.send_message(message.from_user.id,
                         "Добро пожаловать в панель управления! Выбери команду в меню ниже",
                         reply_markup=AdminBot(message).adminButton())

    else:
        bot.send_message(message.from_user.id, "Некорректная команда")


@bot.message_handler(func=lambda m: m.text == "📈 Топ")
def topStudy(message): ButtonBot(message).top_stud()

@bot.message_handler(func=lambda m: m.text == "📒 Методички")
def metodick(message): ButtonBot(message).metod()

@bot.message_handler(func=lambda m: m.text == "📖 Учебник")
def textbook(message): ButtonBot(message).study()

@bot.message_handler(func=lambda m: m.text == "📆 Расписание преподавателя")
def shedule(message): ButtonBot(message).shedule()

@bot.message_handler(func=lambda m: m.text == "📞 Контакты преподавателя")
def contPrep(message): ButtonBot(message).contact()

@bot.message_handler(func=lambda m: m.text == "🔑 Вариант")
def varez(message):
    bot.send_message(message.chat.id, var(str(message.chat.id)))

@bot.message_handler(func=lambda m: (m.text == "📩 Рассылка" and m.chat.id == admin()))
def sendall(message):
    msg = bot.send_message(message.chat.id, "Напиши сообщение для рассылки!")
    bot.register_next_step_handler(msg, mailer)

def mailer(message):
    user_select(message)

@bot.message_handler(func=lambda m: (m.text == "🗂 Список пользователей" and m.chat.id == admin()))
def listUser(message):
    with sql_base_read_() as connection:
        show_select = "SELECT ROW_NUMBER() OVER(ORDER BY name), name, profile, variant, variant_D1 FROM data_user"
        with connection.cursor() as cursor:
            cursor.execute(show_select)
            text = '\n'.join((f'{res[0]}. {res[1]}, {res[2]}, {res[3]}, {res[4]}') for res in cursor.fetchall())
            bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda m: (m.text == "📲 Отправить контингент" and m.chat.id == admin()))
def readStud(message):
    bot.send_message(message.chat.id, "Загружен процесс выгрузки данных из базы данных. Пожалуйста подождите.")
    bot.send_message(message.chat.id, "⌛️")
    gc = gspread.service_account(filename='termex-bot-0ea77baf201b.json') # Указываем путь к JSON
    sh = gc.open("Термех 2/2024") #Открываем тестовую таблицу
    worksheet = sh.worksheet("termex_bot")
    try:
        with sql_base_read_() as connection:
            show_select = "SELECT ROW_NUMBER() OVER(ORDER BY name), id, user_id, name, variant, variant_D1 FROM data_user"
            with connection.cursor() as cursor:
                cursor.execute(show_select)
                headerTab = ["№", 'base_id', 'user_id', 'name', 'variant', 'variant_D1']
                for ht in range(len(headerTab)):
                    worksheet.update_cell(1, ht+1, headerTab[ht])

                for res in cursor.fetchall():
                    for its in range(6):
                        worksheet.update_cell(int(res[0]+1), its+1, res[its])
                        time.sleep(1)

        bot.send_message(message.chat.id, "Процесс обновления данных завершён")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Произошла ошибка {e}")


@bot.message_handler(func=lambda m: (m.text == "❌ Выход" and m.chat.id == admin()))
def exitBot(message):
    bot.send_message(message.chat.id, "Вы вышли из панели управления.",
                     reply_markup=ComandBot(message).button_default())

@bot.message_handler(content_types=['text'])
def texter(message):
    ComandBot(message).help_bot()


print(datetime.now()) #вывод даты и времени сервера в момент запуска

while True: #проверка связи с сервером
    try:
      bot.polling(none_stop=True, interval=1)
    except:
      print('upalo ' + str(datetime.now()))
      logging.error('error: {}'.format(sys.exc_info()[0]))
      time.sleep(5)
