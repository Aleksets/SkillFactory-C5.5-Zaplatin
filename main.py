import telebot
from config import keys, TOKEN
from extensions import APIException, GetPrice, Out

# подключение к боту
bot = telebot.TeleBot(TOKEN)


# предоставление пользователю информации о корректной работе с ботом
# при получении команд "/start" или "/help"
@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду боту в следующем формате: " \
           "<имя валюты, цену которой надо узнать> " \
           "<имя валюты, в которой надо узнать цену первой валюты> " \
           "<количество первой валюты>" \
           "\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


# предоставление пользователю информации о доступных валютах
# при получении команды "/values"
@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


# предоставление пользователю информации о проведённой конвертации валют
# при вводе пользователем текста (с проверкой исключений и минимизацией ошибок ввода)
@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Введите 3 параметра в заданном формате!")
        base, quote, amount = values
        base, quote, amount = base.lower(), quote.lower(), amount.replace(",", ".")
        total_base = GetPrice.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Вы ошиблись при вводе.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        text = f"{amount} {Out.correct(base)} = {total_base:.4f} {Out.correct(quote)}"
        bot.send_message(message.chat.id, text)


# обеспечение периодического опроса серверов Telegram на появление новых сообщений
bot.polling()
