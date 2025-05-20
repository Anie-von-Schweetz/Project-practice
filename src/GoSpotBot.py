import telebot
from DataBot import calculate_result
from DataBot import QUESTIONS
from DataBot import SPORT_INFO
from telebot import types


bot = telebot.TeleBot('7711818193:AAFbgLcy9n11H8eif-gSX4eHtvZQVsvS3qo')
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.set_my_commands([
        types.BotCommand("/start", "Перезапустить бота"),
        types.BotCommand("/reset", "Пройти тест заново")])

    kb = types.InlineKeyboardMarkup(row_width=1)
    bt1 = types.InlineKeyboardButton(text="Сайт GoSpot", url='https://timely-rabanadas-f0fcfa.netlify.app/')
    bt2 = types.InlineKeyboardButton(text="Пройти тест", callback_data='start_test')
    kb.add(bt1, bt2)

    bot.send_message(message.chat.id,
        "🏄‍♂️ *Добро пожаловать в GoSpot Bot!*\n\n"
        "Я помогу подобрать идеальный водный вид спорта для вас.\n",
        #"Используйте меню команд или кнопки ниже:",
        reply_markup=kb,
        parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == 'start_test')
def start_test_call(call):
    chat_id = call.message.chat.id
    user_data[chat_id] = {'answers': {}, 'current_question': 0}
    bot.send_message(call.message.chat.id, text='Отлично, давай начнем!')
    send_question(chat_id)

def send_question(chat_id):
    question_data = QUESTIONS[user_data[chat_id]['current_question']]
    kb = types.InlineKeyboardMarkup()
    for i, option in enumerate(question_data['options']):
        kb.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f"q{user_data[chat_id]['current_question']}_a{i}"))
    bot.send_message(chat_id, question_data['text'], reply_markup=kb)



@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    chat_id = call.message.chat.id
    question_index = user_data[chat_id]['current_question']
    user_data[chat_id]['answers'][question_index] = call.data

    if question_index < len(QUESTIONS)-1:
        user_data[chat_id]['current_question'] += 1
        send_question(chat_id)

    else:
        final_results = calculate_result(user_data[chat_id]['answers'])
        formatted_results = ", ".join(final_results)  # Преобразуем список в строку

        kb = types.InlineKeyboardMarkup(row_width=1)
        bt1 = types.InlineKeyboardButton(text="GoSpot", url='https://timely-rabanadas-f0fcfa.netlify.app/')
        kb.add(bt1)

        bot.send_message(chat_id, f"Отлично, тест завершён!🌟\n\nВам подходят: {formatted_results}")

        sport_info = ''
        for sport in final_results:
            sport_info += format_sport_info(sport)
            sport_info += '\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n'

        bot.send_message(chat_id, text = sport_info, parse_mode='Markdown')
        bot.send_message(chat_id,'👉Узнать подробнее об этих видах водного спорта, '
                                 'а так же найти место для занятий ты сможешь на нашем сайте GoSpot!\n\n'
                                 '⚡Если хочешь пройти тест еще раз, отправь команду /reset', reply_markup=kb)
def format_sport_info(sport):
    info = SPORT_INFO[sport]
    message = f"{info['emoji']} *{sport}*\n\n{info['description']}\n\n"
    message += "🔹 *Основные параметры:*\n" + "\n".join(f"- {k}: {v}" for k, v in info['key_features'].items())
    message += "\n\n✅ *Польза:*\n" + "\n".join(info['benefits'])
    message += f"\n\n🎯 *Советы новичкам:*\n" + "\n".join(info['training_tips'])
    message += f"\n\n💡 *Интересный факт:* {info['fact']}"
    return message

@bot.message_handler(commands=['reset'])
def reset_test(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}

    kb = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Пройти тест", callback_data='start_test')
    kb.add(button)

    bot.send_message(message.chat.id,'Давай пройдем тест заново!', reply_markup=kb)

bot.polling()