# Бот для развития навыков счёта
# Версия 3, рабочее упражнения 'Сумма цифр'
#

import telebot
from telebot import types

from bot_constants import YOUR_TELEGRAM_TOKEN

import numpy as np
# Функции для упражнений
from calc_functions import det_m, r_sum

status = [0, 0]
# status[0]
# Определяет положение решающего в системе:
# 0 - находится в главном меню
# 10 - задаёт параметры задачи
# 11 - даёт ответ
# 12 - выбирает действие после ответа

# status[1]
# Содержит название задачи
# 'det_m' - Определитель квадратной матрицы
# 'r-sum' - Сумма ряда цифр


# Задание и ответ
task = ''
ans = 0
gen = ''

# task2 = ''
# ans2 = 0

# [task, ans] = det_m(0, 9, 3)
# print(task)
# print(ans)


bot = telebot.TeleBot(YOUR_TELEGRAM_TOKEN)


#
# Названия кнопок
#
btn1 = 'Определитель матрицы'
btn2 = 'Сумма цифр'

btn_pars = 'Задать новые параметры'
btn_main = 'Вернуться в главное меню'

#
# "Callback data" кнопок
btn1_cb = 'btn1_cb'
btn2_cb = 'btn2_cb'

    # Переход в главное меню
btn_pars_main = 'btn_pars_main'

    # btn1 - Определитель матрицы
btn_pars_det_m_repeat = 'btn_pars_det_m_repeat'
btn_pars_det_m = 'btn_pars_det_m'


    # btn2 - Сумма ряда
btn_pars_r_sum_repeat = 'btn_pars_r_sum_repeat'
btn_pars_r_sum = 'btn_pars_r_sum'



#
# Клавиатуры
#

# Главное меню
kb_main = types.InlineKeyboardMarkup(row_width = 1)
btn1_types = types.InlineKeyboardButton(text = btn1, callback_data = btn1_cb)
btn2_types = types.InlineKeyboardButton(text = btn2, callback_data = btn2_cb)
kb_main.add(btn1_types)
kb_main.add(btn2_types)

#
# Меню упраженения btn1 = 'Определитель матрицы'
kb_det_m = types.InlineKeyboardMarkup(row_width = 1)
btn1_det_m = types.InlineKeyboardButton(text = btn_pars, callback_data = btn_pars_det_m)
btn2_det_m = types.InlineKeyboardButton(text = btn_main, callback_data = btn_pars_main)
kb_det_m.add(btn1_det_m)
kb_det_m.add(btn2_det_m)

    # + "Повторить задание" (с новыми параметрами)
kb_det_m_ans = types.InlineKeyboardMarkup(row_width = 1)
btn0_det_m = types.InlineKeyboardButton(text = 'Ещё одну задачу', callback_data = btn_pars_det_m_repeat)
btn1_det_m = types.InlineKeyboardButton(text = btn_pars, callback_data = btn_pars_det_m)
btn2_det_m = types.InlineKeyboardButton(text = btn_main, callback_data = btn_pars_main)
kb_det_m_ans.add(btn0_det_m)
kb_det_m_ans.add(btn1_det_m)
kb_det_m_ans.add(btn2_det_m)

#
# Меню упраженения btn2 = 'Сумма цифр'
kb_r_sum = types.InlineKeyboardMarkup(row_width = 1)
btn1_r_sum = types.InlineKeyboardButton(text = btn_pars, callback_data = btn_pars_r_sum)
btn2_r_sum = types.InlineKeyboardButton(text = btn_main, callback_data = btn_pars_main)
kb_r_sum.add(btn1_r_sum)
kb_r_sum.add(btn2_r_sum)

    # + "Повторить задание" (с новыми параметрами)
kb_r_sum_ans = types.InlineKeyboardMarkup(row_width = 1)
btn0_r_sum_ans = types.InlineKeyboardButton(text = 'Ещё одну задачу', callback_data = btn_pars_r_sum_repeat)
btn1_r_sum_ans = types.InlineKeyboardButton(text = btn_pars, callback_data = btn_pars_r_sum)
btn2_r_sum_ans = types.InlineKeyboardButton(text = btn_main, callback_data = btn_pars_main)
kb_r_sum_ans.add(btn0_r_sum_ans)
kb_r_sum_ans.add(btn1_r_sum_ans)
kb_r_sum_ans.add(btn2_r_sum_ans)



#
# Действия при запуске бота
#
@bot.message_handler(commands = ['start'])

def start_message(message):
    # hello_msg = 'Приветствую!\nЭто чат для развития навыков счёта.\nНаберите /button, чтобы появилось меню с упражнениями.'
    hello_msg = 'Приветствую!\nЭто чат для развития навыков счёта.\nВыберите упражнение.'
    # bot.send_message(message.chat.id, hello_msg, markup = kb_main)
    bot.send_message(message.chat.id, hello_msg, reply_markup = kb_main)
    status[0] = 0
    status[1] = 0


# #
# # /button
# # Ещё один способ выйти в главное меню
# #
# @bot.message_handler(commands = ['button'])
#
# def button_message(message):
#     # btn1 = 'Определитель матрицы'
#     # btn2 = 'Сумма цифр'
#
#     markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
#     item1 = types.KeyboardButton(btn1)
#     markup.add(item1)
#     item2 = types.KeyboardButton(btn2)
#     markup.add(item2)
#     bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup = markup)


#
# Обработчик Кнопок меню
#

 # Функция callback_query_handler вносится один раз для обработки всех событий
@bot.callback_query_handler(func=lambda call: True)
def answer(call):

    global ans
    global task
    global gen

    # Главное меню
    if call.data == btn_pars_main:
        hello_msg = 'Приветствую!\nЭто чат для развития навыков счёта.\nВыберите упражнение'
        bot.send_message(call.message.chat.id, hello_msg, reply_markup=kb_main)
        status[0] = 0
        status[1] = 0

    #
    # Упражнение btn1 = 'Определитель матрицы'
    #
    elif call.data == btn1_cb:
        task1 = f'Вы выбрали упражнение "{btn1}"'
        task1_info = f'\nЗадайте величину целых чисел и размер матрицы в виде:\ndet-m a b n\nНа пример: det-m 0 9 2\nСоздаёт матрицу 2х2 из чисел от 0 до 9'
        bot.send_message(call.message.chat.id, task1 + task1_info, reply_markup = kb_det_m)
        status[0] = 10
        status[1] = 'det-m'

    # Задать параметры упражнения det-m
    elif call.data == btn_pars_det_m:
        # task1 = f'Вы выбрали упражнение "{btn1}"'
        task1_info = f'\nЗадайте величину целых чисел и размер матрицы в виде:\ndet-m a b n\nНа пример: det-m 0 9 2\nСоздаёт матрицу 2х2 из чисел от 0 до 9'
        bot.send_message(call.message.chat.id, task1_info, reply_markup=kb_det_m)
        status[0] = 10
        # status[1] = 'det-m'

    # Повторить упражнение det-m
    elif call.data == btn_pars_det_m_repeat:
        # print('\nbtn callback')
        [task, ans] = det_m(int(gen[1]), int(gen[2]), int(gen[3]))
        bot.send_message(call.message.chat.id, str(task), reply_markup=kb_det_m_ans)
        status[0] = 11
        # status[1] = 'det-m'



    #
    # Упражнение btn2 = 'Сумма цифр'
    #
    elif call.data == btn2_cb:
        task2 = f'Вы выбрали упражнение "{btn2}"'
        task2_info = '\nЗадайте диапазон значений и количество чисел в виде:\nr-sum a b n\nНа пример: r-sum 0 9 8\nСоздаёт строку из 8 цифр от 0 до 9'
        bot.send_message(call.message.chat.id, task2 + task2_info, reply_markup=kb_r_sum)
        status[0] = 10
        status[1] = 'r_sum'

    # Задать параметры упражнения r_sum
    elif call.data == btn_pars_r_sum:
        task2_info = '\nЗадайте диапазон значений и количество чисел в виде:\nr-sum a b n\nНа пример: r-sum 0 9 8\nСоздаёт строку из 8 цифр от 0 до 9'
        bot.send_message(call.message.chat.id, task2_info, reply_markup=kb_r_sum)
        status[0] = 10

    # Повторить упражнение r_sum
    elif call.data == btn_pars_r_sum_repeat:
        [task, ans] = r_sum(int(gen[1]), int(gen[2]), int(gen[3]))
        bot.send_message(call.message.chat.id, task, reply_markup=kb_r_sum_ans)
        status[0] = 11


#
# Обработка текстовых ответов
@bot.message_handler(content_types = 'text')
def message_reply(message):

    global task
    global ans
    global gen

    if message.text == '/main':

        hello_msg = 'Приветствую!\nЭто чат для развития навыков счёта.\nВыберите упражнение'
        bot.send_message(message.chat.id, hello_msg, reply_markup = kb_main)
        status[0] = 0
        status[1] = 0

    # Ввод условий задачи
    elif status[0] == 10:
        # строка с параметрами задачи
        gen = message.text.split()

        if gen[0] == 'det-m':
            # print('\nВход в det-m')
            # print(int(gen[1]), int(gen[2]), int(gen[3]))
            # Формирование матрицы и ответа
            [task, ans] = det_m(int(gen[1]), int(gen[2]), int(gen[3]))
            # print('ans', ans)

            # Отправляет задание в
            # print(task)
            # bot.send_message(message.chat.id, 'Задание: ' + str(task), reply_markup = kb_det_m)
            bot.send_message(message.chat.id, str(task), reply_markup=kb_det_m)
            status[0] = 11
            status[1] = 'det-m'


        elif gen[0] == 'r-sum':
            # print('\nВход в r-sum')
            # print(int(gen[1]), int(gen[2]), int(gen[3]))
            # Формирование строки и ответа
            [task, ans] = r_sum(int(gen[1]), int(gen[2]), int(gen[3]))
            # print('ans', ans)

            bot.send_message(message.chat.id, task, reply_markup=kb_r_sum)
            status[0] = 11
            status[1] = 'r-sum'


        else:
            bot.send_message(message.chat.id, 'Что-то пошло не так.\nВыберите упражнение ещё раз', reply_markup=kb_main)

    # Решение задачи. Обработка ответа
    elif status[0] == 11:
        print('\nВход в status == 11')
        usr_ans = int(message.text)
        # ans2 = round(np.linalg.det(task2))
        # print('usr_ans', usr_ans)
        # print('ans', ans)

        # Выбор клавиатуры к заданию
        kb_ans = ''
        if status[1] == 'det-m':
            kb_ans = kb_det_m_ans

        elif status[1] == 'r-sum':
            kb_ans = kb_r_sum_ans

        # Сообщение о результатах
        if int(message.text) == ans:
            # print('Верно!')

            bot.send_message(message.chat.id, 'Верно!', reply_markup=kb_ans)
            status[0] == 12

        else:
            # print(f'Правильный ответ: {ans}')
            bot.send_message(message.chat.id, f'Правильный ответ: {ans}', reply_markup=kb_ans)
            status[0] == 12


    # Не предусмотренные ситуации
    else:
        bot.send_message(message.from_user.id, "Что-то не понятное. Напишите '/main'")


if __name__ == '__main__':
    # schedule.every().day.at('22:11').do(send_message)
    # Thread(target=schedule_checker).start()
    bot.polling(none_stop=True)

