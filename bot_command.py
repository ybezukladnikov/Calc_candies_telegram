from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, CallbackContext
import logger
from math import gcd


first_question, answer_yes, exit_play, choose_num_can, choose_max_num,start_play,\
    create_name, step_first_pl, step_second_pl = range(9)
temp_list = []
list_name = []

def start(update, _):
    logger.my_log(update, CallbackContext, 'Зашел в программу')
    reply_keyboard = [['Да', 'Нет']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        f'Приветствую тебя уважаемый пользователь, {update.effective_user.first_name}!\n'
        'Хочешь ли ты посчитать рациональное выражение?\n'
        'Ты можешь завершить программу на любом этапе просто, нужно просто ввести команду:\n'
        '/cancel',
        reply_markup=markup_key,)

    return first_question


def answer_fq(update, _):
    if update.message.text == 'Нет':
        logger.my_log(update, CallbackContext, 'Не захотел считать.')
        update.message.reply_text(
            'Очень жаль, приходи в следующий раз!'
            'И скажи мне хотя бы Пока)',
            reply_markup=ReplyKeyboardRemove(),
        )
        return exit_play
    else:
        logger.my_log(update, CallbackContext, 'Захотел посчитать.')

        update.message.reply_text(
            f'{update.effective_user.first_name}\n'
            'Введите выражение, которое вы хотите посчитать.\n'
            'Выражение должно быть вида 1/2/3+4/5/6 где:\n'
            '1 и 4 - это целые части чисел (если их нет, то ставим "0")\n'
            '2 и 5 - это числители.\n'
            '3 и 6 - это знаменатели\n'
            'Доступны следующие операции:\n'
            'Сложение. Знак - "+"\n'
            'Вычитание. Знак - "-"\n'
            'Умножение. Знак - "*"\n'
            'Деление. Знак - ":"\n')
        return answer_yes

def choose_mod(update, _):
    expr_temp = (update.message.text).replace(' ', '')
    expr_temp = expr_temp.replace('\\','/')
    for i in expr_temp:
        if i.isalpha():
            update.message.reply_text(
                f'В вашем выражении есть буква. Напишите выражение заново без букв')
            return answer_yes
    list_dig = []
    list_operator = []
    list_one_num = []
    znak = 1

    if expr_temp[0] == '-':
        znak = -1
        expr = expr_temp[1:]
    else:
        expr = expr_temp

    dict_op = {'+': lambda x, y: x + y,
               '-': lambda x, y: x - y,
               '*': lambda x, y: x * y,
               ':': lambda x, y: x * y, # это деление. Просто с рациональными числами это по сути умножение перевернутой дроби.
               }

    for oper in dict_op:
        expr = expr.replace(oper, f'#{oper}#')

    temp = expr.split('#')
    print(temp)

    for i in range(len(temp)):
        list_one_num.append(temp[i]) if not i % 2 else list_operator.append(temp[i])


    print(list_one_num)
    print(list_operator)


    for i in list_one_num:
        try:
            list_temp = list(map(int, i.split("/")))
            list_dig.append([(list_temp[0] * list_temp[2] + list_temp[1]), list_temp[2]])
        except:
            update.message.reply_text(
                f'В вашем выражении число {i} не соответствует стандарту 1/2/3+1/2/3. Напишите выражение заново по стандарту')
            return answer_yes

    list_dig[0][0] *= znak

    temprory = 0
    while '*' in list_operator or ':' in list_operator:
        for i in range(len(list_operator)):
            if list_operator[i] == '*' or list_operator[i] == ':':
                if list_operator[i] == ':': temprory = 1
                new_chis = (dict_op[list_operator[i]])(list_dig[i][0], list_dig[i + 1][0 + temprory])
                new_znam = (dict_op[list_operator[i]])(list_dig[i][1], list_dig[i + 1][1 - temprory])
                temp_res = [new_chis, new_znam]
                list_dig.pop(i)
                list_dig.pop(i)
                list_dig.insert(i, temp_res)
                list_operator.pop(i)
                break

    while len(list_operator) != 0:
        znam_first = list_dig[0][1]
        znam_second = list_dig[1][1]

        list_dig[0][0] *= znam_second
        list_dig[0][1] *= znam_second

        list_dig[1][0] *= znam_first
        list_dig[1][1] *= znam_first

        new_chis = (dict_op[list_operator[0]])(list_dig[0][0], list_dig[1][0])
        temp_res = [new_chis, list_dig[0][1]]

        list_operator.pop(0)
        list_dig.pop(0)
        list_dig.pop(0)
        list_dig.insert(0, temp_res)

    nod = gcd(list_dig[0][0], list_dig[0][1])

    res_chis = int(list_dig[0][0] / nod)
    res_znam = int(list_dig[0][1] / nod)

    update.message.reply_text(f'Ответ: {res_chis}/{res_znam}') if res_chis < res_znam else \
        update.message.reply_text(
            f'Ответ: {res_chis}/{res_znam} или {res_chis // res_znam} целых и {res_chis - (res_chis // res_znam) * res_znam}/{res_znam}')

    reply_keyboard = [['Да', 'Нет']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
                f'{update.effective_user.first_name}, Хотите ли еще что-нибудь посчитать?',
                reply_markup=markup_key)


    return first_question


    # if update.message.text == 'Бот':
    #     logger.my_log(update, CallbackContext, 'Выбрал игру с ботом.')
    #     # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
    #     update.message.reply_text(
    #         'Отличный выбор!\n'
    #         'Приступаем к игре!\n'
    #         'Правила очень просты. Кто возмет последнюю конфету тот и выиграл!'
    #         'На первом этапе укажи сколько будет всего конфет!',
    #         reply_markup=ReplyKeyboardRemove(),
    #     )
    #     return choose_num_can
    # else:
    #     logger.my_log(update, CallbackContext, 'Выбрал игру с человеком.')
    #     update.message.reply_text(
    #         "Хорошо. Теперь введи через пробел имена двух игроков",
    #         reply_markup=ReplyKeyboardRemove(),
    #     )
    #     return create_name

#
# def check_name(update, _):
#     global list_name
#     text_m = update.message.text
#     try:
#         name_first, name_second = text_m.split()
#         if name_first == name_second:
#             update.message.reply_text('Хитрый) Но я хитрее)) мы добавим первому имени 1, а второму 2))')
#             name_first+='-1'
#             name_second+='-2'
#
#     except:
#         update.message.reply_text('Вы ввели имена некорректно, попробуйте еще!')
#         return create_name
#
#     random_num = randint(0, 1)
#     if random_num:
#         list_name.append(name_first)
#         list_name.append(name_second)
#     else:
#         list_name.append(name_second)
#         list_name.append(name_first)
#     logger.my_log(update, CallbackContext, f'Пользователь задал два имени {list_name[0]} и {list_name[1]} ')
#     update.message.reply_text(f'Отличные имена!\n'
#         f'Первым будет ходить {list_name[0]}'
#         f'Приступаем к игре!\n'
#         f'Правила очень просты. Кто возьмет последнюю конфету тот и выиграл!'
#         f'На первом этапе укажи сколько будет всего конфет!')
#
#     return  choose_num_can
#
#
# def check_num_can(update, _):
#
#     global temp_list
#     temp_list = []
#     try:
#         num = int(update.message.text)
#         if num <= 2:
#             update.message.reply_text('Число конфет должно быть больше 2')
#             return choose_num_can
#         temp_list.append(num)
#
#         update.message.reply_text('Все отлично. Продолжаем.\n'
#                                   'Теперь напишите по сколько конфет будете брать')
#         logger.my_log(update, CallbackContext, f'Для игры было выбрано {num} конфет')
#         return choose_max_num
#
#     except ValueError:
#         update.message.reply_text('Вы ввели некорректное число, попробуйте снова!')
#         return choose_num_can
#
# def check_max_can(update, _):
#     global temp_list
#     global list_name
#     try:
#         num = int(update.message.text)
#         if num >temp_list[0] :
#             update.message.reply_text(f'Число больше чем общее число конфет. Укажите меньшее {temp_list[0]}')
#             return choose_max_num
#         if num <= 1:
#             update.message.reply_text('Число конефет не может быть меньше 2')
#             return choose_max_num
#         if not temp_list[0] % (num + 1) and len(list_name)==0:
#             update.message.reply_text('По техническим причинам просим изменить максимальное кол. конфет, которые можно брать')
#             return choose_max_num
#         logger.my_log(update, CallbackContext, f'Установлено максимальное кол. конфет = {num}')
#         temp_list.append(num)
#         if len(list_name)==0:
#             update.message.reply_text('Все верно. Бот ходит первым.')
#             if temp_list[0] <= temp_list[1]:
#                 num_cand_first_player = temp_list[0]
#                 logger.my_log(update, CallbackContext, f'Бот взял {num_cand_first_player} конфет')
#             else:
#                 num_cand_first_player = temp_list[0] - (temp_list[1] + 1) * (temp_list[0] // (temp_list[1] + 1))
#                 logger.my_log(update, CallbackContext, f'Бот взял {num_cand_first_player} конфет')
#             update.message.reply_text(f'Bot взял {num_cand_first_player}')
#             temp_list[0]-=num_cand_first_player
#             update.message.reply_text(f'Осталось конфет => {temp_list[0]}, взять можно до {temp_list[1]} конфет. Сколько вы возьмете?')
#             return start_play
#         else:
#             update.message.reply_text(f'Отлично! Начинаем игру!\n'
#                                       f'Сейчас конфет осталось => {temp_list[0]},\n'
#                                       f'взять можно до {temp_list[1]} конфет.\n'
#                                       f'{list_name[0]}, Сколько вы возьмете?')
#             return step_first_pl
#     except ValueError:
#         update.message.reply_text('Вы ввели некорректное число, попробуйте снова!')
#         return choose_max_num
#
# def main_func(update, _):
#     global temp_list
#     try:
#         num = int(update.message.text)
#         if num > temp_list[1]:
#             update.message.reply_text('Число конфет больше разрешонного. Попробуйте еще. ')
#             return start_play
#         if num < 1:
#             update.message.reply_text('Число конфет меньше 1 попробуйте еще. ')
#             return start_play
#         if temp_list[0]-num <0:
#             update.message.reply_text('Конфет осталось меньше, попробуйте еще. ')
#             return start_play
#
#     except ValueError:
#         update.message.reply_text('Вы ввели некорректное число. Пробуйте еще.  ')
#         return start_play
#     logger.my_log(update, CallbackContext, f'Пользователь взял {num} конфет')
#     if temp_list[0]-num <=temp_list[1]:
#         update.message.reply_text(f'Осталось конфет => {temp_list[0]-num} Bot забирает последние {temp_list[0]-num}')
#         update.message.reply_text('К сожалению, вы проиграли.')
#         logger.my_log(update, CallbackContext, f'Пользователь проиграл')
#         temp_list = []
#         reply_keyboard = [['Да', 'Нет']]
#         markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#         update.message.reply_text(
#             f'{update.effective_user.first_name}, Хотите ли еще раз\n'
#             'попытать свое счастье?)',
#             reply_markup=markup_key, )
#
#
#         return first_question
#
#     else:
#         temp_list[0]-=num
#
#
#         num_cand_first_player = temp_list[0] - (temp_list[1] + 1) * (temp_list[0] // (temp_list[1] + 1))
#
#         update.message.reply_text(f'Осталось конфет => {temp_list[0]} Bot взял {num_cand_first_player}')
#         logger.my_log(update, CallbackContext, f'Бот взял {num_cand_first_player} конфет')
#         temp_list[0] -= num_cand_first_player
#
#         update.message.reply_text(
#             f'Осталось конфет => {temp_list[0]}, взять можно до {temp_list[1]} конфет. Сколько вы возьмете?')
#         return start_play
#
# def main_step_first(update, _):
#     global temp_list
#     global list_name
#     try:
#         num = int(update.message.text)
#         if num > temp_list[1]:
#             update.message.reply_text('Число конфет больше разрешонного. Попробуйте еще. ')
#             return step_first_pl
#         if num < 1:
#             update.message.reply_text('Число конфет меньше 1 попробуйте еще. ')
#             return step_first_pl
#         if temp_list[0]-num <0:
#             update.message.reply_text('Конфет осталось меньше, попробуйте еще. ')
#             return step_first_pl
#
#     except ValueError:
#         update.message.reply_text('Вы ввели некорректное число. Пробуйте еще. ')
#         return step_first_pl
#     logger.my_log(update, CallbackContext, f'Первый игрок взял {num} конфет')
#     if temp_list[0] - num ==0:
#         update.message.reply_text(f'Ура! Поздравляем {list_name[0]}, вы забрали последние конфеты\n'
#                                   f'А это значит, что вы выиграли!!!')
#         temp_list = []
#         list_name = []
#         reply_keyboard = [['Да', 'Нет']]
#         markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#         update.message.reply_text(
#             f'{update.effective_user.first_name}, Хотите ли еще раз\n'
#             'сыграть в нашу игру?)',
#             reply_markup=markup_key, )
#         logger.my_log(update, CallbackContext, f'Выиграл первый игрок')
#         return first_question
#
#     temp_list[0]-=num
#     update.message.reply_text(f'{list_name[0]} взял {num}')
#     update.message.reply_text(
#         f'Осталось конфет => {temp_list[0]}, взять можно до {temp_list[1]} конфет. {list_name[1]}, Cколько вы возьмете?')
#     return step_second_pl
#
# def main_step_second(update, _):
#     global temp_list
#     global list_name
#     try:
#         num = int(update.message.text)
#         if num > temp_list[1]:
#             update.message.reply_text('Число конфет больше разрешонного. Попробуйте еще. ')
#             return step_first_pl
#         if num < 1:
#             update.message.reply_text('Число конфет меньше 1 попробуйте еще. ')
#             return step_first_pl
#         if temp_list[0] - num < 0:
#             update.message.reply_text('Конфет осталось меньше, попробуйте еще. ')
#             return step_first_pl
#
#     except ValueError:
#         update.message.reply_text('Вы ввели некорректное число. Пробуйте еще. ')
#         return step_first_pl
#     logger.my_log(update, CallbackContext, f'Второй игрок взял {num} конфет')
#     if temp_list[0] - num == 0:
#         update.message.reply_text(f'Ура! Поздравляем {list_name[1]}, вы забрали последние конфеты\n'
#                                   f'А это значит, что вы выиграли!!!')
#         logger.my_log(update, CallbackContext, f'Выиграл второй игрок')
#         temp_list = []
#         list_name = []
#         reply_keyboard = [['Да', 'Нет']]
#         markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#         update.message.reply_text(
#             f'{update.effective_user.first_name}, Хотите ли еще раз\n'
#             'сыграть в нашу игру?)',
#             reply_markup=markup_key, )
#         return first_question
#
#     temp_list[0] -= num
#     update.message.reply_text(f'{list_name[1]} взял {num}')
#     update.message.reply_text(
#         f'Осталось конфет => {temp_list[0]}, взять можно до {temp_list[1]} конфет. {list_name[0]}, Cколько вы возьмете?')
#     return step_first_pl
