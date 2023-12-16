# ТелеграмБОТ контрольной для СПО

Телеграм бот работает на библиотеке `pytelegramBotAPI`. Код находится на сервере и через API взаимодействует с мессенджером. В код программы вставляются задачи и ответы к ним. И благодаря модулю `random` подбирается индивидуальный вариант контрольной для каждого студента. Индивидуальность контрольной зависит от количества задач в разделах. Результат в процентном соотношении присылается студенту и админу бота.

## Как пользоваться

В мессенджере находим интересующего бота, регистрируем ФИО и профиль. Нажимаем кнопку `Начать тест` и пользователю сообщением присылаются задачи. В тексте сообщения студент пишет ответ в численном виде, которая преобразуется в строку и сверяется с эталоном. После решения всех задач бот выдаёт количество решённых задач в процентнос соотношении.