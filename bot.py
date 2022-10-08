from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json


bot = Bot("") #Telegram bot token
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    await bot.send_message(msg.from_user.id, "Для получения курса отправь любое сообщение мне.\nДля установки порога для сигнала отправь команду /signal 8 или /сигнал 8\n\И когда курс тенге к рублю будет 8 и более тебе придет сообщение.")


@dp.message_handler(commands=['сигнал', 'signal'])
async def read_signal(msg: types.Message):
    text = str(msg.text)
    if len(text.split(' ')) == 2:
        num = float(text.split(' ')[1].replace(',', '.'))
        with open('db.json', 'r') as file:
            db = json.load(file)

        db[f'{msg.from_user.id}'] = num

        with open('db.json', 'w') as file:
            json.dump(db, file)

        await bot.send_message(msg.from_user.id, f'сигнал на курс {num} записан.')

    else:
        await bot.send_message(msg.from_user.id, "ты ввел что-то не правильно.\nНужно воодить /signal 8 или /сигнал 8")


@dp.message_handler()
async def send_curs(msg: types.Message):
    with open('curs.json', 'r') as file:
        curs = json.load(file)

    await bot.send_message(msg.from_user.id, "Казахстанский тенге " + str(curs['Казахстанский тенге']))



if __name__ == '__main__':
    executor.start_polling(dp)
