import telebot

from config import TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

keys = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
}


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n' \
           'Увидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    message_text = '\n'.join(keys.keys())
    bot.reply_to(message, text + message_text)


@bot.message_handler(content_types=['text'])
def handle_convert(message: telebot.types.Message):
    try:
        user_input = message.text.split(' ')
        if len(user_input) != 3:
            raise APIException("Ожидается ввод трех значений через пробел")

        quote, base, amount = user_input

        if quote == base:
            raise APIException("Недопустим ввод одинаковых валют")

        ticker_from = keys.get(quote)
        ticker_to = keys.get(base)

        if not ticker_from or not ticker_to:
            raise APIException("Введена неизвестная валюта, список доступных валют: /values")

        try:
            amount = int(amount)
        except ValueError:
            raise APIException("Неправильный формат числа")

        try:
            result = Converter.get_price(ticker_from, ticker_to, amount)
        except:
            raise APIException("Ошибка сервиса API")

        bot.send_message(message.chat.id, result * amount)
    except APIException as e:
        bot.send_message(message.chat.id, e.args[0])


bot.polling()
