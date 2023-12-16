import telebot
from telebot import types # для указания типов
import time
from datetime import datetime
from telefunc import tel_token, admin
from random import randint

class TaskSpo(object):

    def __init__(self, menu, var):
        self.menu = menu
        self.var = var

        self.task = {

            "kin": [
                "Зависимость координаты тела от времени описывается уравнением x=8∙t-t^2 (м). В какой момент времени скорость тела равна нулю?",
                "Мотоциклист и велосипедист одновременно начинают двигаться из состояния покоя. Ускорение мотоциклиста в 3 раза больше, чем велосипедиста. Во сколько раз скорость мото-циклиста больше скорости велосипедиста в один и тот же момент времени?",
                "Тело движется вертикально вверх с начальной скоростью, равной 20 м/с. Каков будет модуль скорости через 0,5 с после начала движения? Сопротивление воздуха не учитывать.",
                "Диск радиусом 20 см равномерно вращается вокруг своей оси. Скорость точки, находящейся на расстоянии 15 см от центра диска, равна 1,5 м/с. Скорость крайних точек диска равна: "

            ],

            "din": [
                "Тело подвешено на двух нитях и находится в равновесии. Угол между нитями равен 90°.Силы натяжения нитей равны 3 Н и 4 Н. Вес тела равен: ",
                "Тело массой 4 кг начинает двигаться под действием силы 8 Н. Какая скорость будет у тела через 4 с.",
                "Тело массой 5 кг с начальной скоростью 10 м/с двигается под действием силы 15 Н. Какая скорость будет у тела через 3 с.",
                "Тело массой 4 кг начинает двигаться под действием силы 8 Н. Какое растояние пройдёт тело через 4 с."

            ],

            "job": [
                "Движение материальной точки массой 3 кг описывается уравнением x(t)=25-10·t+2·t^2 м. Определите изменение импульса материальной точки за первые 8 с после начала движения.",
                "Мяч массой 1,5 кг, движущийся со скоростью 5,2 м/с перпендикулярно стенке, в результате удара отскакивает от стенки со скоростью 4,8 м/с. Во время удара на мяч действовал импульс силы (кг*м/с):",
                "На тележку массой 100 кг, движущуюся равномерно по гладкой горизонтальной поверхности со скоростью 3 м/с, вертикально падает груз массой 50 кг и не соскальзывает с тележки. С какой скоростью (м/с) будет двигаться тележка? ",
                "Стоящий на льду человек массой 49 кг ловит мяч массой 1 кг, который летит горизонтально со скоростью 10 м/с. На какое расстояние (м) откатился человек с мячом по горизонтальной поверхности льда, если коэффициент трения относительно льда равен 0,02?"

            ],

            "gas": [
                "Бутылку с подсолнечным маслом плотностью 920 кг/м^3, закрытую пробкой, перевернули. Определите среднюю силу (до десятых), с которой действует масло на пробку площадью 6 см^2, если высота масла над пробкой 20 см.",
                "Пластиковый пакет с водой объёмом 1 л полностью погрузили в воду, g=10 м/с^2. На него действует выталкивающая сила, равная:",
                "Аэростат объёмом 1000 м^3 заполнен гелием. Плотность гелия – 0,18 кг/м^3, плотность воздуха – 1,29 кг/м^3. На аэростат действует выталкивающая сила (в кН до десятых).",
                "Из цилиндрического сосуда диаметром 0,1 м с высотой столба 40 см перелили воду (плотность 1000 кг/м^3) в другой сосуд с диаметром в 2 раза больше. Чему равно давление, действующее на дно нового сосуда?"

            ]

        }

        self.cases = {
            "kin": ['4', '3', '15', '2'],
            "din": ['5', '8', '19', '16'],
            "job": ['96', '15', '2', '0,1'],
            "gas": ['1,1', '10', '11,1', '9,8']

        }

        self.phys = ["kin", "din", "job", "gas"]

    def testSPO(self):
        menu = self.menu
        var = self.var
        task = self.task[self.phys[menu]]
        cases = self.cases[self.phys[menu]]
        return task[var], cases[var]

token = tel_token()

bot = telebot.TeleBot(token)

test_data = {}

name_dict = {}

varTask = {}

@bot.message_handler(commands=['start']) # функция начала работы бота с регистрацией студента в БД
def send_welcome(message): #функция на команды
	msg = bot.reply_to(message, "Здравствуй, студент! Я думаю, что ты готов сдавать тест. Напиши свою фамилию имя отчество:")
	bot.register_next_step_handler(msg, group)
	name_dict.update({str(message.chat.id):[]})

def group(message):
    text = message.text
    name_dict[str(message.chat.id)].append(text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Агроном")
    btn2 = types.KeyboardButton("Геодезист")
    markup.add(btn1, btn2)
    msg = bot.send_message(message.chat.id, "Выбери профиль:", reply_markup=markup)
    bot.register_next_step_handler(msg, test)
    varTask.update({str(message.chat.id): []})

def test(message):
    text = message.text
    name_dict[str(message.chat.id)].append(text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать тест")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Нажми при готовности!", reply_markup=markup)
    test_data.update({str(message.chat.id):[]})

@bot.message_handler(content_types = ["text"]) #обработчик текстовых сообщений пользователя
def echo(message): #функция ответа на сообщения
    if message.text == "Начать тест":
        rast = 0
        test_data[str(message.chat.id)].clear()
        varTask[str(message.chat.id)].clear()
        for num in range(4):
            s = randint(0, 3)
            varTask[str(message.chat.id)].append(s)
        var = varTask[str(message.chat.id)][rast]
        task, cases = TaskSpo(rast, var).testSPO()
        msg = bot.send_message(message.chat.id, f"Задача №{rast + 1}: {task}", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, din)

    elif message.text == "Привет":
        bot.send_message(message.chat.id, f"Приветик, {message.from_user.first_name}!")

def din(message):
    rast = 0
    var = varTask[str(message.chat.id)][rast]
    task, cases = TaskSpo(rast, var).testSPO()
    if message.text == cases:
        bot.send_message(message.chat.id, "Правильно")
        test_data[str(message.chat.id)].append(1)
    else:
        bot.send_message(message.chat.id, "Неправильно")
        test_data[str(message.chat.id)].append(0)
    rast = 1
    var = varTask[str(message.chat.id)][rast]
    task, cases = TaskSpo(rast, var).testSPO()
    msg = bot.send_message(message.chat.id, f"Задача №{rast+1}: {task}")
    bot.register_next_step_handler(msg, job)

def job(message):
    rast = 1
    var = varTask[str(message.chat.id)][rast]
    task, cases = TaskSpo(rast, var).testSPO()
    if message.text == cases:
        bot.send_message(message.chat.id, "Правильно")
        test_data[str(message.chat.id)].append(1)
    else:
        bot.send_message(message.chat.id, "Неправильно")
        test_data[str(message.chat.id)].append(0)
    rast = 2
    var = varTask[str(message.chat.id)][rast]
    task, cases = TaskSpo(rast, var).testSPO()
    msg = bot.send_message(message.chat.id, f"Задача №{rast+1}: {task}")
    bot.register_next_step_handler(msg, gas)

def gas(message):
    rast = 2
    var = varTask[str(message.chat.id)][rast]
    task, cases = TaskSpo(rast, var).testSPO()
    if message.text == cases:
        bot.send_message(message.chat.id, "Правильно")
        test_data[str(message.chat.id)].append(1)
    else:
        bot.send_message(message.chat.id, "Неправильно")
        test_data[str(message.chat.id)].append(0)
    rast = 3
    var = varTask[str(message.chat.id)][rast]
    task, cases = TaskSpo(rast, var).testSPO()
    msg = bot.send_message(message.chat.id, f"Задача №{rast+1}: {task}")
    bot.register_next_step_handler(msg, res)

def res(message):
    rast = 3
    var = varTask[str(message.chat.id)][rast]
    task, cases = TaskSpo(rast, var).testSPO()
    if message.text == cases:
        bot.send_message(message.chat.id, "Правильно")
        test_data[str(message.chat.id)].append(1)
    else:
        bot.send_message(message.chat.id, "Неправильно")
        test_data[str(message.chat.id)].append(0)

    testRes = 0
    for im in range(4):
        testRes += test_data[str(message.chat.id)][im]
    testRes = testRes * 25
    bot.send_message(message.chat.id, f"Задачи решены на {testRes} %")
    text = f"Обучающийся профиля {name_dict[str(message.chat.id)][1]}: {name_dict[str(message.chat.id)][0]} (id: {message.chat.id}) решил задачи на {testRes} %"
    bot.send_message(admin(), text)

import logging
import sys

print(datetime.now()) #вывод даты и времени сервера в момент запуска

while True: #проверка связи с сервером
    try:
      bot.polling(none_stop=True, interval=1)
    except:
      print('upalo ' + str(datetime.now()))
      logging.error('error: {}'.format(sys.exc_info()[0]))
      time.sleep(5)
