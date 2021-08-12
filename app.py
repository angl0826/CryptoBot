import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):  # эта функция отвечает на команды 'start', 'help'
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты> \
<имя валюты в которой нужно узнать цену первой валюты> \
<количество первой валюты>\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):  # эта функция отвечает на команды 'start', 'help'
    text = ''
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        values = list(map(str.lower, values))

        if len(values) > 3:
            raise APIException('Слишком много параметров')

        if len(values) < 3:
            raise APIException('Слишком мало параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

        if int(amount) < 100000:
            pass
        else:
            bot.send_message(message.chat.id, 'Вы уверены что настолько богаты? Ну ладно, во всяком случае вот')

    except APIException as e:
        bot.reply_to(message, f'Ошибка ползователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()  # запуск бота
