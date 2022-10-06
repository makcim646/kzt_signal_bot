import telebot
import json

bot = telebot.TeleBot("")



@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
	bot.send_message(msg.from_user.id, "Для получения курса отправь любое сообщение мне.\n\
 Для установки порога для сигнала отправь команду /signal 8 или /сигнал 8\n\
 И когда курс тенге к рублю будет 8 и более тебе придет сообщение.")


@bot.message_handler(commands=['сигнал', 'signal'])
def send_signal(msg):
    text = str(msg.text)
    if len(text.split(' ')) == 2:
        num = float(text.split(' ')[1].replace(',', '.'))
        with open('db.json', 'r') as file:
            db = json.load(file)

        db[f'{msg.from_user.id}'] = num

        with open('db.json', 'w') as file:
            json.dump(db, file)

        bot.send_message(msg.from_user.id, f'сигнал на курс {num} записан.')

    else:
        bot.send_message(msg.from_user.id, "ты ввел что-то не правильно.\n\
 Нужно воодить /signal 8 или /сигнал 8")


@bot.message_handler(content_types=["text"])
def send_curs(msg):
    with open('curs.json', 'r') as file:
        curs = json.load(file)

    bot.send_message(msg.from_user.id, "Казахстанский тенге " + str(curs['Казахстанский тенге']))



bot.polling(none_stop=True, interval=0)