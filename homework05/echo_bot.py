import telebot
import config

telebot.apihelper.proxy = config.proxy
access_token = config.access_token
bot = telebot.TeleBot(access_token)


@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
