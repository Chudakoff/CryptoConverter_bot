import telebot
from config import TOKEN, currencies
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в формате: \n <имя валюты> ' \
           '<в какую валюту перевести> <количество переводимой валюты>\n' \
           '(пример: "биткоин доллар 2")\n\nУвидеть ' \
           'список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for item in currencies.keys():
        text = '\n - '.join((text, item,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {round(total_base * float(amount),2)}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
