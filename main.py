import telebot
from telebot import types
from src.message_encryptor import MessageEncrypter

bot = telebot.TeleBot("6912342529:AAG4G05ojSErXM2Sa9Fez__KIsoQXkNzkB8")

stats = {}

def InputBot(message, text):
    a = ''
    def ret(message):
        nonlocal a
        a = message.text
        return False

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, ret)
    while not a:
        pass
    return a

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/help'), types.KeyboardButton('/register'))
    bot.send_message(message.chat.id, 'Привет, я бот-шифрователь. \nЯ могу зашифровать твое сообщение методом Цезаря или методом Виженера', reply_markup=markup)

@bot.message_handler(commands=['help'])
def hlp(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/start'), types.KeyboardButton('/register'), types.KeyboardButton('/stats'), types.KeyboardButton('/encrypt'), types.KeyboardButton('/decrypt'))
    bot.send_message(message.chat.id, '/start - начать работу с ботом\n/help - описание команд\n/register - зарегистрировать пользователя' +
                     '\n/stats - получить статистику по пользователям\n/encrypt - зашифровать сообщение методом Цезаря или Виженера' +
                     '\n/decrypt - расшифровать сообщение методом Цезаря или Виженера', reply_markup=markup)

@bot.message_handler(commands=['register'])
def register(message):
    if message.from_user.username not in stats:
        stats[message.from_user.username] = 0
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован')

@bot.message_handler(commands=['stats'])
def stats_(message):
    ans: str = 'Статистика по пользователям:'
    lst = [ans]
    for person, value in stats.items():
        lst.append(f'{person}: {value} запросов шифрования и дешифрования')
    bot.send_message(message.chat.id, '\n'.join(lst))

@bot.message_handler(commands=['encrypt'])
def encrypt(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Цезарь'), types.KeyboardButton('Виженер'))
    bot.send_message(message.chat.id, 'Выберите метод шифрования:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Цезарь', 'Виженер'])
def encrypt_method(message):
    if message.text == 'Цезарь':
        inpt = InputBot(message, "Введите данные для шифрования [строка] [сдвиг]")
        inpt, key = inpt.split(' ')
        enc = MessageEncrypter(inpt)
        bot.send_message(message.chat.id, enc.caesar_encrypt(int(key)))
    else:
        inpt = InputBot(message, "Введите данные для шифрования [строка] [ключ-пароль]")
        inpt, key = inpt.split(' ')
        enc = MessageEncrypter(inpt)
        bot.send_message(message.chat.id, enc.vigenere_encrypt((key)))
    if message.from_user.username in stats:
        stats[message.from_user.username] += 1
    main_menu(message)

@bot.message_handler(commands=['decrypt'])
def decrypt(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Цезaрь'), types.KeyboardButton('Виженеp'))
    bot.send_message(message.chat.id, 'Выберите способ дешифрования:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Цезaрь', 'Виженеp'])
def decrypt_method(message):
    if message.text == 'Цезaрь':
        inpt = InputBot(message, "Введите данные для дешифрования [шифр] [сдвиг]")
        inpt, key = inpt.split(' ')
        enc = MessageEncrypter(inpt)
        bot.send_message(message.chat.id, enc.caesar_decrypt(int(key)))
    else:
        inpt = InputBot(message, "Введите данные для дешифрования [шифр] [ключ-пароль]")
        inpt, key = inpt.split(' ')
        enc = MessageEncrypter(inpt)
        bot.send_message(message.chat.id, enc.vigenere_decrypt(key))
    if message.from_user.username in stats:
        stats[message.from_user.username] += 1
    main_menu(message)
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/help'), types.KeyboardButton('/register'), types.KeyboardButton('/stats'), types.KeyboardButton('/encrypt'), types.KeyboardButton('/decrypt'))
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=markup)

bot.infinity_polling()
