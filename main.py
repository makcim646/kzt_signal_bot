import requests
from bs4 import BeautifulSoup
import subprocess
import json
import telebot
from time import sleep

def get_curs():
    url = 'https://mironline.ru/support/list/kursy_mir/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    p_list = soup.find_all('p')
    p_list = p_list[3:25]

    curs = {}
    for n in range(0,22,2):
        num = float(p_list[n+1].text.strip().replace(',', '.'))
        coin = p_list[n].text.strip()

        if num < 1:
            num = round(1 / num, 2)
        else:
            num = round(num, 2)

        curs[coin] = num

    with open('curs.json', 'w') as file:
        json.dump(curs, file)




def send_call():
    bot = telebot.TeleBot("")
    with open('curs.json', 'r') as file:
        curs = json.load(file)
    num = curs['Казахстанский тенге']


    with open('db.json', 'r') as file:
        db = json.load(file)

    for user, user_num in db.items():
        if user_num <= num:
            bot.send_message(int(user), f'Курс {num}')



if __name__ == '__main__':
    proc = subprocess.Popen('python3 bot.py', shell=True)
    while True:
        get_curs()
        send_call()
        sleep(60*60)
