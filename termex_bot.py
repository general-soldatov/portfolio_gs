import telebot
from telebot import types # для указания типов
from mysql.connector import connect


def user_sql(user_id): #регистрация пользователя в списке рассылок
    with connect(
        host="GS.mysql.pythonanywhere-services.com",
        user='GS',
        password='$Ff_kdfkbf3A',
        database='GS$ter_mex',
    ) as connection:
        print(connection)

        show_db_query = "INSERT INTO teldata (user_id, active) VALUES (%s, %s)"
        data_tg = [(user_id, 1)]
        with connection.cursor() as cursor:
            cursor.executemany(show_db_query, data_tg)
            connection.commit()
            print("id append")

def user_select(message):  # подпрограмма рассылки пользователям сообщений
    with connect(
        host="GS.mysql.pythonanywhere-services.com",
        user='GS',
        password='$Ff_kdfkbf3A',
        database='GS$ter_mex',
    ) as connection:
        print(connection)

        show_select = "SELECT user_id FROM teldata"
        with connection.cursor() as cursor:
            cursor.execute(show_select)
            for result in cursor.fetchall():
                bot.copy_message(chat_id = result, from_chat_id=message.chat.id,         
                    message_id=message.message_id)

def user_sql_reg(user_id, username, group, surname, name, aftername, study): #регистрация студента в базе данных
    with connect(
        host="GS.mysql.pythonanywhere-services.com",
        user='GS',
        password='$Ff_kdfkbf3A',
        database='GS$ter_mex',
    ) as connection:
        print(connection)

        show_db_query = "INSERT INTO namedata (user_id, user_name, user_group, syrname, name, aftername, study) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data_tg = [(user_id, username, group, surname, name, aftername, study)]
        with connection.cursor() as cursor:
            cursor.executemany(show_db_query, data_tg)
            connection.commit()
            print("user registered")




token = "token"

HELP = """
В меню встроенной клавиатуры ты можешь найти пособия для самостоятельной работы, учебник.
Также возможно найти свой вариант, студенческий рейтинг, расписание преподавателя.
/help - вывести список доступных команд
/menu - вызов встроенной клавиатуры
"""

bot = telebot.TeleBot(token)

name_data = []
message_data = []

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)




def button_default():  #кнопки по умолчанию
    app1 = types.KeyboardButton("🔑 Вариант")
    app2 = types.KeyboardButton("📈 Топ")
    app3 = types.KeyboardButton("📒 Методички")
    app4 = types.KeyboardButton("📖 Учебник")
    app5 = types.KeyboardButton("📆 Расписание преподавателя")
    app6 = types.KeyboardButton("📞 Контакты преподавателя")
    markup.add(app3, app4, app1, app2, app5, app6)


@bot.message_handler(commands=['start']) # функция начала работы бота с регистрацией студента в БД
def send_welcome(message): #функция на команды
	msg = bot.reply_to(message, "Приветствую! Я твой телеграм-помощник в области теоретической механики. Давайте познакомимся, напиши свою фамилию:")
	user_sql(message.from_user.id)
	bot.register_next_step_handler(msg, surname)


def surname(message):
    text = message.text
    name_data.append(text)
    msg = bot.send_message(message.chat.id, "Напиши имя:")
    bot.register_next_step_handler(msg, name)

def name(message):
    text = message.text
    name_data.append(text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Нет отчества")
    markup.add(btn1)
    msg = bot.send_message(message.chat.id, "Напиши отчество, если его нет, нажми кнопку:", reply_markup=markup)
    bot.register_next_step_handler(msg, aftername)


def aftername(message):
    text = message.text
    name_data.append(text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("очное")
    btn2 = types.KeyboardButton("заочное")
    markup.add(btn1, btn2)
    msg = bot.send_message(message.chat.id, "Выбери форму обучения с помощью кнопок:", reply_markup=markup)
    bot.register_next_step_handler(msg, study)

def study(message):
    text = message.text
    name_data.append(text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Тм 1-1")
    btn2 = types.KeyboardButton("Тм 1-2")
    btn3 = types.KeyboardButton("НТТС 2-9")
    btn4 = types.KeyboardButton("НТТС 2-10")
    markup.add(btn1, btn2, btn3, btn4)
    msg = bot.send_message(message.chat.id, "Выбери группу с помощью кнопок:", reply_markup=markup)
    bot.register_next_step_handler(msg, group)



def group(message):
    text = message.text
    name_data.append(text)
    user_id = message.from_user.id
    surname = name_data[0]
    name = name_data[1]
    aftername = name_data[2]
    study = name_data[3]
    group = name_data[4]
    if aftername == "Нет отчества":
        username = surname + " " + name
    else:
        username = surname + " " + name + " " + aftername
    user_sql_reg(user_id, username, group, surname, name, aftername, study)
    name_data.clear()
    button_default()
    bot.send_message(message.chat.id, "Приятно познакомиться! Теперь ты можешь пользоваться кнопками на телеграм-клавиатуре.", reply_markup=markup)

@bot.message_handler(commands=['menu']) #вывод клавиатуры
def menu(message):
    bot.send_message(message.chat.id, 'Загрузка ⚙️', reply_markup=types.ReplyKeyboardRemove())
    button_default()
    bot.send_message(message.chat.id, 'Клавиатура выведена ⌨️', reply_markup=markup)


@bot.message_handler(commands=['del']) #удаление меню
def del_row(message):
    bot.send_message(message.chat.id, 'Удаление ⚙️', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['help']) #вывод справки
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=['prog']) #вывод справки
def prog(message):
    msg = bot.send_message(message.chat.id, 'Напиши код')
    bot.register_next_step_handler(msg, coder)

def coder(message):
    ar = compile (message.text, '', 'exec')
    ex = eval(ar)
    df = str(ex).split('\n')
    print(df)
    if ex == 0:
        bot.send_message(message.chat.id, 'Задание выполнено')
    else:
        bot.send_message(message.chat.id, 'Задание не выполнено')


@bot.message_handler(commands=['sendall'])  #команда рассылки сообщения пользователям
def sendall(message):
    if message.from_user.id == 980314213:
        msg = bot.send_message(message.chat.id, "Напиши сообщение для рассылки!")
        bot.register_next_step_handler(msg, mailling)


def mailling(message):
    user_select(message)


@bot.message_handler(content_types = ["text"]) #обработчик текстовых сообщений пользователя
def echo(message): #функция ответа на сообщения
    string = message.text
    markup_inl = types.InlineKeyboardMarkup()
    if string == "🔑 Вариант":
        button1 = types.InlineKeyboardButton("Актуальные варианты", url='https://drive.google.com/file/d/17FIeGJSOMbaHVG1sxeFEaxKIovgdftIJ/view?usp=sharing')
        markup_inl.add(button1)
        bot.send_message(message.chat.id, 'Свой вариант можно найти в файле', reply_markup=markup_inl)

    elif string == "📈 Топ":
        button1 = types.InlineKeyboardButton("Рейтинг студентов", url='https://drive.google.com/file/d/17H105tExHL_ZZjmNGhy5yhqfOBsexuvv/view?usp=sharing')
        markup_inl.add(button1)
        bot.send_message(message.chat.id, 'Рейтинг студентов в файле по ссылке:', reply_markup=markup_inl)

    elif string == "📒 Методички":
        button1 = types.InlineKeyboardButton("Статика", url='https://drive.google.com/file/d/172EuTxLjZlYR0GYi03wdbzu70kae4RdC/view?usp=sharing')
        button2 = types.InlineKeyboardButton("Кинематика", url='https://drive.google.com/file/d/1i23gh8Kcsu-R5OkyHfdbp7SFUW2c73kx/view?usp=sharing')
        button3 = types.InlineKeyboardButton("Динамика", url='https://drive.google.com/file/d/1wrluEFNR18gYT1wFe-oLsmar9pxSB8ZH/view?usp=sharing')
        markup_inl.add(button1, button2, button3)
        bot.send_message(message.chat.id, 'Ссылки на методические указания:', reply_markup=markup_inl)

    elif string == "📖 Учебник":
        button1 = types.InlineKeyboardButton("Учебник", url='https://drive.google.com/file/d/17OhsVDAaPVkdBEMbjl3wR0Scj7WjeMYo/view?usp=drive_link')
        markup_inl.add(button1)
        bot.send_message(message.chat.id, 'Ссылка на учебник: "Краткий курс теоретической механики"', reply_markup=markup_inl)

    elif string == "📆 Расписание преподавателя":
        button1 = types.InlineKeyboardButton("Расписание", url='https://drive.google.com/file/d/17JUNCEKttgoa4HwPY63l0RB3CGJITdyU/view?usp=sharing')
        markup_inl.add(button1)
        bot.send_message(message.chat.id, 'Расписание преподавателя можете найти по ссылке ниже', reply_markup=markup_inl)

    elif string == "📞 Контакты преподавателя":
        button1 = types.InlineKeyboardButton("Telegram", url='https://t.me/general_soldatov')
        button2 = types.InlineKeyboardButton("ВК", url='https://vk.com/general_soldatov')
        markup_inl.add(button1, button2)
        bot.send_message(message.chat.id, 'Контакты преподавателя можете найти по ссылке ниже', reply_markup=markup_inl)

    else:
        bot.send_message(message.chat.id, 'Пока что я вас не понимаю... 🤷‍♂')



#Постоянно обращается к серверу телеграм
bot.polling(none_stop=True, interval=0)
