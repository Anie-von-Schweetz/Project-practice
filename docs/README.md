# Документация к проектной практике    

## Оглавление
1. [Базовая часть задания. Создание статического веб-сайта](#базовая-часть-задания.-создание-статического-веб-сайта)
2. [Вариативная часть задания](#вариативная-часть-задания)
3. [Исследование предметной области](#исследование-предметной-области)
4. [Пошаговое руководство](#пошаговое-руководство)
5. [Модификации и расширения](#модификации-и-расширения)
6. [Этапы работы над проектом](#этапы-работы-над-проектом)
   
## 1. Базовая часть задания. Создание статического веб-сайта


## 2. Вариативная часть задания. Реализация технологии "Создание телеграм-бота с помощью языка программирования Python"
### Исследование предметной области
#### 1. Анализ водных видов спорта
Для создания базы знаний нашего бота была использована информация о водных видах спорта, которая собиралась в рамках проекта "Водный спорт" по дисциплине "Проетная деятельность". Было отобрано 12 популярных водных видов спорта, и определены их требований к:
- Уровню физической подготовки
- Необходимому оборудованию
- Бюджету для начала занятий
- Рискам и мерам безопасности

#### 2. Определение ключевых параметров
Были выделены 6 ключевых характеристик для классификации:
1. Уровень активности
2. Физическая подготовка
3. Комфорт в воде
4. Предпочитаемая локация
5. Цели занятий
6. Бюджет

### Пошаговое руководство
#### 1. Получение токена бота
Для создания и настройки нового необходимо обратиться к другому телеграм-боту @BotFather. Запускаем его и через команду /newbot и, следуя инструкции, уснавливаем имя и юзернейм для бота. На выходе получаем токен, который будем использовать для аунтефикации нашего бота и предоставления ему доступа к Telegram API.

<img src="https://github.com/user-attachments/assets/26fe901c-1ca8-4986-b997-df1da0ecb75e" alt="Описание изображения" width="300" height="600">

#### 2. Настройка окружения
Для создания телеграм-бота была использована библиотека TeleBot. Перед написанием кода, необходимо установить её на свой компьтер с помощью определённой команды в командной строке.
```
# Установка необходимых библиотек
pip install pyTelegramBotAPI
```

#### 3. Создание базовой структуры бота
Научим бот обрабатывать команду /start
```python
import telebot #импорт библиотеки TeleBot в проект
from telebot import types

bot = telebot.TeleBot('YOUR_TOKEN') #уснанавливаем связь с ботом через токен
user_data = {} #словарь для хранения ответов пользователя на тест

#обработчик команды /start
@bot.message_handler(commands=['start']) 
def start(message):

    #инициализация кнопок под сообщением
    kb = types.InlineKeyboardMarkup(row_width=1)
    bt1 = types.InlineKeyboardButton(text="Сайт GoSpot", url='https://timely-rabanadas-f0fcfa.netlify.app/')
    bt2 = types.InlineKeyboardButton(text="Пройти тест", callback_data='start_test')
    kb.add(bt1, bt2)

    #сообщение, которое бот будет отправлять при запуске
    bot.send_message(message.chat.id,
        "🏄‍♂️ *Добро пожаловать в GoSpot Bot!*\n\n"
        "Я помогу подобрать идеальный водный вид спорта для вас.\n", reply_markup=kb, parse_mode='Markdown')

bot.polling()
```

#### 4. Реализация теста
Создаём в проекте файл `DataBot.py`, и в списке `QUESTIONS` записываем все вопросы нашего теста и варианты ответов на них.
```python
QUESTIONS = [
    {
        "text": "Какую активность вы предпочитаете?",
        "options": [
            "Спокойные занятия",
            "Умеренные нагрузки",
            "Экстремальные виды"
        ]
    },
    # ... другие вопросы
]
```

#### 5. Алгоритм рекомендаций
В файле `DataBot.py` реализуем функцию `calculate_result` для вычисления итога теста. Словарь scores хранит баллы каждого вида спорта. Через ветвление if-elif-else в зависимости ответа на каждый вопрос тому или иному виду спотру начисляются баллы.
```python
def calculate_result(answers):
    scores = {
        'Кайтсерфинг': 0,
        'Плавание': 0,
        # ... другие виды
    }
    
    # Процесс подсчета баллов
    # Блок 1: Уровень активности
    if answers[0] == "q0_a0":
        scores['Плавание'] += 3
        scores['Аквааэробика'] += 2
        scores['САП-серфинг'] += 2

    elif answers[0] == "q0_a1":
        scores['Каякинг'] += 2
        scores['Гребля на байдарках'] += 3
        scores['Водное поло'] += 2

    elif answers[0] == "q0_a2":
        scores['Виндсерфинг'] += 2
        scores['Водное поло'] += 3
        scores['Дайвинг'] += 1

    elif answers[0] == "q0_a3":
        scores['Кайтсерфинг'] += 3
        scores['Вейкбординг'] += 3
        scores['Рафтинг'] += 2
      #....другие вопросы
    
    # Сортируем результаты
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = [sport for sport, score in sorted_scores[:3] if score > 0]

    return top_3 if top_3 else ["Плавание"]  # Дефолтный вариант
```

#### 6. Система тестирования
Для запуска теста и отправки вопров реализуем функции `start_test_call`, `send_question`. 
```python
#ловит нажатие кнопки с callback_data='start_test'
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
            callback_data=f"q{user_data[chat_id]['current_question']}_a{i}"))#форматирует полученный ответ в формат qX_aY, где х-номер вопроса, а у-номер ответа
    bot.send_message(chat_id, question_data['text'], reply_markup=kb)
```

Для записи ответов и перехода к следующему вопросу или завершению теста создадим функцию `handle_answer`.

```python
@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    chat_id = call.message.chat.id
    question_index = user_data[chat_id]['current_question']
    user_data[chat_id]['answers'][question_index] = call.data

    #если ещё остались вопросы - отправляем следующий
    if question_index < len(QUESTIONS)-1:
        user_data[chat_id]['current_question'] += 1
        send_question(chat_id)

    #иначе - отправляем результат
    else:
        final_results = calculate_result(user_data[chat_id]['answers'])
        formatted_results = ", ".join(final_results)  # Преобразуем список в строку

        kb = types.InlineKeyboardMarkup(row_width=1)
        bt1 = types.InlineKeyboardButton(text="GoSpot", url='https://timely-rabanadas-f0fcfa.netlify.app/')
        kb.add(bt1)

        bot.send_message(chat_id, f"Отлично, тест завершён!\n\nВам подходят: {formatted_results}\n\nУзнать подробнее об этих видах водного спорта, "
                                  f"а так же найти место для занятий ты сможешь на нашем сайте GoSpot!", reply_markup=kb)
        bot.send_message(chat_id,'Если хочешь пройти тест еще раз, отправь команду /reset')
        user_data[chat_id] = {}
```

Внедрим команду /reset для прохождения теста заново. 
```python
#обработчик команды /reset
@bot.message_handler(commands=['reset'])
def reset_test(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}

    kb = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Пройти тест", callback_data='start_test')
    kb.add(button)

    bot.send_message(message.chat.id,'Давай пройдем тест заново!', reply_markup=kb)
```
#### 7. Промежуточный итог
На данном этапе работы телеграм-бота выглядит так: 

<img src="https://github.com/user-attachments/assets/78f8e5ac-796a-4387-a205-e1093c543fca" alt="Описание изображения" width="200" height="450">
<img src="https://github.com/user-attachments/assets/9538eddf-00f1-45db-b0d8-e55b3281e204" alt="Описание изображения" width="200" height="450">
<img src="https://github.com/user-attachments/assets/c6b925d5-3355-42bc-b1db-5b9bcedd5091" alt="Описание изображения" width="200" height="450">
<img src="https://github.com/user-attachments/assets/75bd3a2f-4e96-408b-9357-ddb700a20116" alt="Описание изображения" width="200" height="450">

### Модификации и расширения
Для большей заинтересованности пользователей создадим базу знаний о водных видах спорта. После получения результатов теста будет присылаться сообщение со сведениями о подходящих видах спорта. Также для удобства добавим меню команд.
#### 1. Добавление меню команд
Модифицируем обработчик команды /start, чтобы пользователю вседа было доступно меню с имеющимися командами.
```python
@bot.message_handler(commands=['start'])
def start(message):
    #меню команд
    bot.set_my_commands([
        types.BotCommand("/start", "Перезапустить бота"),
        types.BotCommand("/reset", "Пройти тест заново"),
        types.BotCommand("/sports", "Список всех видов спорта"),])

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
}
```
#### 1. Добавление описаний видов спорта
Дополним файл `DataBot.py`. Создадим словарь `SPORT_INFO` для хранения информации о видах водного спорта
```python
SPORT_INFO = {
    'Плавание': {
        'description': "Гармония движений в воде, сочетающая силу и расслабление. Дарит ощущение невесомости и всесторонне развивает тело.",
        'category': "Оздоровительный/Соревновательный",
        'activity_level': "Любой (от низкого до высокого)",
        'budget': "Минимальный (абонемент от 1000 руб/мес)",
        'difficulty': "Начальный/Продвинутый",
        'locations': "Бассейны, открытые водоёмы",
        'emoji': "🏊‍♂️",
        'key_features': {
            'Кроль': "Самый быстрый стиль с попеременными гребками",
            'Брасс': "Плавные 'лягушачьи' движения",
            'Баттерфляй': "Мощный синхронный гребок с волнообразным телом",
            'На спине': "Расслабленное плавание с минимальной нагрузкой"
        },
        'benefits': [
            "💪 Укрепляет все группы мышц без нагрузки на суставы",
            "🧠 Снижает стресс через ритмичные движения",
            "🫀 Улучшает работу сердечно-сосудистой системы",
            "🌊 Доступно в любом возрасте и уровне подготовки"
        ],
        'fact': "Всего 30 минут плавания сжигают до 400 калорий",
        'training_tips': [
            "1. Освойте дыхательные упражнения",
            "2. Отточите базовые движения",
            "3. Соблюдайть регулярность"
        ]
    },
    # ... другие виды
}
```

#### 2. Показ детальной информации вместе с результатами теста
```python
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

        #для каждого полученного вида спорта составим описание
        sport_info = ''
        for sport in final_results:
            sport_info += format_sport_info(sport)
            sport_info += '\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n'

        bot.send_message(chat_id, text = sport_info, parse_mode='Markdown')
        bot.send_message(chat_id,'👉Узнать подробнее об этих видах водного спорта, '
                                 'а так же найти место для занятий ты сможешь на нашем сайте GoSpot!\n\n'
                                 '⚡Если хочешь пройти тест еще раз, отправь команду /reset', reply_markup=kb)

#форматированный вывод информации из словаря SPORT_INFO
def format_sport_info(sport):
    info = SPORT_INFO[sport]
    message = f"{info['emoji']} *{sport}*\n\n{info['description']}\n\n"
    message += "🔹 *Основные параметры:*\n" + "\n".join(f"- {k}: {v}" for k, v in info['key_features'].items())
    message += "\n\n✅ *Польза:*\n" + "\n".join(info['benefits'])
    message += f"\n\n🎯 *Советы новичкам:*\n" + "\n".join(info['training_tips'])
    message += f"\n\n💡 *Интересный факт:* {info['fact']}"
    return message
```

#### 3. Пример работы финальной версии телеграм-бота

<img src="https://github.com/user-attachments/assets/df9ca38d-4263-43ff-bec6-0c5689199025" alt="Описание изображения" width="200" height="450">
<img src="https://github.com/user-attachments/assets/8105c611-792f-450d-816f-73a58f9b8c97" alt="Описание изображения" width="200" height="450">
<img src="https://github.com/user-attachments/assets/e86dd70b-ccee-47f1-857e-c2b28210d0ea" alt="Описание изображения" width="200" height="450">

#### 4. Видео презентация выполненной работы
Смотрите видео в файле [practice_report_template.docx](practice_report_template.docx).

## 3. Этапы работы над проектом
