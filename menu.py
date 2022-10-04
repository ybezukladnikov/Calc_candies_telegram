from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, CallbackContext
import logger
from math import gcd


first_question, want_play, exit_play, choose_num_can, choose_max_num,start_play,\
    create_name, step_first_pl, step_second_pl, want_count = range(10)
temp_list = []
list_name = []

def start(update, _):
    logger.my_log(update, CallbackContext, 'Зашел в программу')
    reply_keyboard = [['Посчитать', 'Играть', 'Ничего']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        f'Приветствую тебя уважаемый пользователь, {update.effective_user.first_name}!\n'
        'В нашем боте ты можешь:\n'
        '1) Посчитать рациональное выражение?\n'
        '2) Сыграть в игру конфеты.\n'
        'P.S. Ты можешь завершить программу на любом этапе просто, нужно просто ввести команду:\n'
        '/cancel',
        reply_markup=markup_key,)

    return first_question


def answer_fq(update, _):
    if update.message.text == 'Ничего':
        logger.my_log(update, CallbackContext, 'Не захотел ничего делать.')
        update.message.reply_text(
            'Очень жаль, приходи в следующий раз!'
            'И скажи мне хотя бы Пока)',
            reply_markup=ReplyKeyboardRemove(),
        )
        return exit_play
    elif update.message.text == 'Посчитать':
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
        return want_count

    elif update.message.text == 'Играть':
        logger.my_log(update, CallbackContext, 'Захотел поиграть.')
        reply_keyboard = [['Бот', 'Человек']]
        # Создаем простую клавиатуру для ответа
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


        update.message.reply_text(
            f'{update.effective_user.first_name}\n'
            'Выбери с кем ты будешь играть! '
            ,
            reply_markup=markup_key,)
        return want_play