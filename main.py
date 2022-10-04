import logging
import module_candies as bt
import rational as rt
import menu
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from config import TOKEN

def cancel(update, _):
    update.message.reply_text(
        'Если будет скучно, заходи.',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, menu.start)],

        states={
            bt.first_question: [MessageHandler(Filters.regex('^(Посчитать|Играть|Ничего)$'), menu.answer_fq)],
            menu.want_count:[MessageHandler(Filters.text, rt.get_rational)],

            bt.want_play:[MessageHandler(Filters.regex('^(Бот|Человек)$'), bt.choose_mod)],
            bt.choose_num_can:[MessageHandler(Filters.text, bt.check_num_can)],
            bt.choose_max_num:[MessageHandler(Filters.text, bt.check_max_can)],
            bt.start_play:[MessageHandler(Filters.text, bt.main_func)],
            bt.create_name:[MessageHandler(Filters.text, bt.check_name)],
            bt.step_first_pl:[MessageHandler(Filters.text, bt.main_step_first)],
            bt.step_second_pl:[MessageHandler(Filters.text, bt.main_step_second)],


            bt.exit_play: [MessageHandler(Filters.text, cancel)]
        },

        fallbacks=[CommandHandler('cancel', cancel)],
    )





dispatcher.add_handler(conv_handler)



print('server started')
updater.start_polling()
updater.idle()

