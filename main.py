import telebot
from telebot import types

API_TOKEN = '7281868191:AAHXEuPq52p-PHrvYERSCIynhnaqHqnAVhQ'
YOUR_TARGET_CHAT_ID = '-1002302826608'
bot = telebot.TeleBot(API_TOKEN)

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Зберу сам")
    button2 = types.KeyboardButton("Замовлення пiд ключ")
    markup.add(button1, button2)

    bot.send_message(message.chat.id, "Виберіть опцію:", reply_markup=markup)


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@bot.message_handler(func=lambda message: message.text == "Зберу сам")
def handle_zberu_sam(message):
    user_data[message.chat.id] = {'order_type': 'Зберу сам', 'additional_info': [], 'files': []}
    msg = bot.send_message(
        message.chat.id,
        "Введіть додаткову інформацію або прикріпіть файл. Надішліть /done, коли завершите:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, collect_additional_info)

def collect_additional_info(message):
    if message.text == "/done":
        ask_full_name(message)
    else:
        if message.chat.id not in user_data:
            user_data[message.chat.id] = {'additional_info': [], 'files': []}

        if 'files' not in user_data[message.chat.id]:
            user_data[message.chat.id]['files'] = []

        if 'additional_info' not in user_data[message.chat.id]:
            user_data[message.chat.id]['additional_info'] = []

        if message.content_type == 'text':
            user_data[message.chat.id]['additional_info'].append(message.text)
        elif message.content_type == 'document':
            user_data[message.chat.id]['files'].append(message.document.file_id)
            user_data[message.chat.id]['additional_info'].append(f"Файл: {message.document.file_name}")

        msg = bot.send_message(message.chat.id, "Додайте ще інформацію або надішліть /done, коли закінчите.")
        bot.register_next_step_handler(msg, collect_additional_info)

def ask_full_name(message):
    msg = bot.send_message(message.chat.id, "Введіть ваше ім'я та прізвище:")
    bot.register_next_step_handler(msg, ask_phone_number)

def ask_phone_number(message):
    user_data[message.chat.id]['full_name'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = types.KeyboardButton("Поділитися телефоном", request_contact=True)
    markup.add(contact_button)

    msg = bot.send_message(
        message.chat.id,
        "Надішліть ваш номер телефону, натиснувши кнопку нижче:",
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, process_contact)

@bot.message_handler(content_types=['contact'])
def process_contact(message):
    if message.contact is not None:
        user_data[message.chat.id]['contact_info'] = message.contact.phone_number
        bot.send_message(
            message.chat.id,
            send_results(message),
            "Дякуємо! Ваші дані було передано. /start для новой заявки",
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        msg = bot.send_message(message.chat.id, "Будь ласка, використовуйте кнопку для надсилання номера телефону.")
        bot.register_next_step_handler(msg, ask_phone_number)

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@bot.message_handler(func=lambda message: message.text == "Замовлення пiд ключ")
def handle_zamovlennia_pid_klyuch(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("кухня")
    button2 = types.KeyboardButton("шафа")
    button3 = types.KeyboardButton("iнше")
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Оберіть категорію:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "кухня")
def handle_kitchen(message):
    user_data[message.chat.id] = {'type_of_work': 'Кухня', 'order_type': 'Замовлення пiд ключ'}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Фарбований МДФ")
    button2 = types.KeyboardButton("Ламіноване ДСП")
    button3 = types.KeyboardButton("Акриловий МДФ")
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Оберіть тип фасаду для кухні:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_kitchen_facade)

@bot.message_handler(func=lambda message: message.text == "шафа")
def handle_closet(message):
    user_data[message.chat.id] = {'type_of_work': 'Шафа', 'order_type': 'Замовлення пiд ключ'}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Фарбований МДФ")
    button2 = types.KeyboardButton("Ламіноване ДСП")
    button3 = types.KeyboardButton("Дверi Купе")
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Оберіть тип фасаду для шафи:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_closet_facade)

@bot.message_handler(func=lambda message: message.text == "iнше")
def handle_other(message):
    bot.send_message(message.chat.id, "Введіть деталі замовлення або прикріпіть файл:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, save_additional_info, "Замовлення пiд ключ")

@bot.message_handler(func=lambda message: message.text == "Замовлення пiд ключ")
def handle_zamovlennia_pid_klyuch(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("кухня")
    button2 = types.KeyboardButton("шафа")
    button3 = types.KeyboardButton("iнше")
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Оберіть категорію:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "кухня")
def handle_kitchen(message):
    user_data[message.chat.id] = {'type_of_work': 'Кухня', 'order_type': 'Замовлення пiд ключ'}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Фарбований МДФ")
    button2 = types.KeyboardButton("Ламіноване ДСП")
    button3 = types.KeyboardButton("Акриловий МДФ")
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Оберіть тип фасаду для кухні:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_kitchen_facade)

@bot.message_handler(func=lambda message: message.text == "шафа")
def handle_closet(message):
    user_data[message.chat.id] = {'type_of_work': 'Шафа', 'order_type': 'Замовлення пiд ключ'}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Фарбований МДФ")
    button2 = types.KeyboardButton("Ламіноване ДСП")
    button3 = types.KeyboardButton("Дверi Купе")
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Оберіть тип фасаду для шафи:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_closet_facade)

@bot.message_handler(func=lambda message: message.text == "iнше")
def handle_other(message):
    bot.send_message(message.chat.id, "Введіть деталі замовлення або прикріпіть файл:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, save_additional_info, "Замовлення пiд ключ")

def handle_kitchen_facade(message):
    user_data[message.chat.id]['selected_facade'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("HPL")
    button2 = types.KeyboardButton("Акрилова")
    button3 = types.KeyboardButton("Кварцова")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Оберіть тип стільниці:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_kitchen_table_type)

def handle_closet_facade(message):
    user_data[message.chat.id]['selected_facade'] = message.text
    ask_question_sequence(message, "Розміри (в метрах)", "size_closet", handle_closet_size)

def handle_kitchen_table_type(message):
    user_data[message.chat.id]['selected_table_type'] = message.text
    ask_question_sequence(message, "Довжина кухні (в метрах)", "kitchen_length", handle_kitchen_length)

def handle_kitchen_length(message):
    user_data[message.chat.id]['kitchen_length'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Економ")
    button2 = types.KeyboardButton("Стандарт")
    button3 = types.KeyboardButton("Преміум")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Оберіть якість фурнітури:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_kitchen_furniture_quality)

def handle_kitchen_furniture_quality(message):
    selected_quality = message.text
    if selected_quality in ['Економ', 'Стандарт', 'Преміум']:
        user_data[message.chat.id]['furniture_quality'] = selected_quality
        bot.send_message(message.chat.id, f'Ви обрали {selected_quality} якість.')
        ask_question_sequence(message, "Коли потрібна кухня (дата)", "delivery_date", handle_delivery_date)
    else:
        bot.send_message(message.chat.id, "Будь ласка, оберіть коректну якість фурнітури.")
        handle_kitchen_length(message)

def handle_closet_furniture_quality(message):
    selected_quality = message.text
    if selected_quality in ['Економ', 'Стандарт', 'Преміум']:
        user_data[message.chat.id]['furniture_quality'] = selected_quality
        bot.send_message(message.chat.id, f'Ви обрали {selected_quality} якість.')
        ask_question_sequence(message, "Коли потрібна кухня (дата)", "delivery_date", handle_delivery_date)
    else:
        bot.send_message(message.chat.id, "Будь ласка, оберіть коректну якість фурнітури.")
        handle_kitchen_length(message)

def handle_closet_size(message):
    user_data[message.chat.id]['size_closet'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Економ")
    button2 = types.KeyboardButton("Стандарт")
    button3 = types.KeyboardButton("Преміум")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Оберіть якість фурнітури:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_closet_furniture_quality)

def handle_closet_furniture_quality(message):
    selected_quality = message.text
    if selected_quality in ['Економ', 'Стандарт', 'Преміум']:
        user_data[message.chat.id]['furniture_quality'] = selected_quality
        bot.send_message(message.chat.id, f'Ви обрали {selected_quality} якість.')
        ask_question_sequence(message, "Коли потрібна шафа (дата)", "delivery_date", handle_delivery_date)
    else:
        bot.send_message(message.chat.id, "Будь ласка, оберіть коректну якість фурнітури.")
        handle_closet_size(message)

def handle_delivery_date(message):
    user_data[message.chat.id]['delivery_date'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Знижка 20%")
    button2 = types.KeyboardButton("Підсвітка")
    button3 = types.KeyboardButton("Безкоштовна доставка")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Виберіть подарунок:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_closet_gift_selection)

def handle_kitchen_gift_selection(message):
    user_data[message.chat.id]['gift_selection'] = message.text
    bot.send_message(message.chat.id,
                     "Введіть додаткову інформацію або прикріпіть файл. Надішліть /done, коли завершите:",
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, collect_additional_info)

def handle_closet_gift_selection(message):
    user_data[message.chat.id]['gift_selection'] = message.text
    bot.send_message(message.chat.id,
                     "Введіть додаткову інформацію або прикріпіть файл. Надішліть /done, коли завершите:",
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, collect_additional_info)


def ask_question_sequence(message, question, key, next_handler):
    msg = bot.send_message(message.chat.id, question)
    bot.register_next_step_handler(msg, lambda m: save_answer_and_continue(m, key, next_handler))

def save_answer_and_continue(message, key, next_handler):
    user_data[message.chat.id][key] = message.text
    next_handler(message)

def save_additional_info(message, order_type):
    user_data[message.chat.id]['additional_info'] = message.text
    send_results(message)

def send_results(message):
    data = user_data.get(message.chat.id, {})
    if data.get('order_type') == 'Зберу сам':
        result = (
            f"Результати анкети:\n\n"
            f"Ім'я та прізвище: {data.get('full_name', 'Не вказано')}\n"
            f"Контакт: {data.get('contact_info', 'Не вказано')}\n"
            f"Додаткова інформація: {data.get('additional_info', 'Немає')}\n"
        )
    elif data.get('type_of_work') == 'Кухня':
        result = (
            f"Результати анкети:\n\n"
            f"Тип замовлення: {data.get('order_type', 'Не вказано')}\n"
            f"Мебель: {data.get('type_of_work', 'Не вказано')}\n"
            f"Ім'я та прізвище: {data.get('full_name', 'Не вказано')}\n"
            f"Контакт: {data.get('contact_info', 'Не вказано')}\n"
            f"Тип фасаду: {data.get('selected_facade', 'Не вказано')}\n"
            f"Тип стільниці: {data.get('selected_table_type', 'Не вказано')}\n"
            f"Довжина кухні: {data.get('kitchen_length', 'Не вказано')} м\n"
            f"Якість фурнітури: {data.get('furniture_quality', 'Не вказано')}\n"
            f"Час доставки: {data.get('delivery_date', 'Не вказано')}\n"
            f"Обраний подарунок: {data.get('gift_selection', 'Не обрано')}\n"
            f"Додаткова інформація: {data.get('additional_info', 'Немає')}\n"
        )
    elif data.get('type_of_work') == 'Шафа':
        result = (
            f"Результати анкети:\n\n"
            f"Тип замовлення: {data.get('order_type', 'Не вказано')}\n"
            f"Мебель: {data.get('type_of_work', 'Не вказано')}\n"
            f"Ім'я та прізвище: {data.get('full_name', 'Не вказано')}\n"
            f"Контакт: {data.get('contact_info', 'Не вказано')}\n"
            f"Тип фасаду: {data.get('selected_facade', 'Не вказано')}\n"
            f"Розмiри: {data.get('size_closet', 'Не вказано')} м\n"
            f"Якість фурнітури: {data.get('furniture_quality', 'Не вказано')}\n"
            f"Час доставки: {data.get('delivery_date', 'Не вказано')}\n"
            f"Обраний подарунок: {data.get('gift_selection', 'Не обрано')}\n"
            f"Додаткова інформація: {data.get('additional_info', 'Немає')}\n"
        )


    bot.send_message(YOUR_TARGET_CHAT_ID, result)

    # Send each file stored in the 'files' list
    for file_id in data.get('files', []):
        bot.send_document(YOUR_TARGET_CHAT_ID, file_id)

    separator = '-' * 100
    bot.send_message(chat_id=YOUR_TARGET_CHAT_ID, text=separator)

    bot.send_message(message.chat.id, "Дякуємо! Ваші дані було передано. /start для новой заявки")


bot.polling(none_stop=True)