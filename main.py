import telebot
from config import currency, TOKEN
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Здравствуйте Вас приветствует Бот для конвертации валют.\n\
Чтобы начать работу введите команду боту в следующем формате:\n<Валюта>\
<В какую валюту перевести> <Количество переводимой валюты>\n\
Увидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ощибка пользователя\n {e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\n {e}')
    else:
        text = f' Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()



