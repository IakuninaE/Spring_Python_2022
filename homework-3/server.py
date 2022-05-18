# save this as app.py

from datetime import datetime
import time
import json
import flask
from flask import Flask, abort

app = Flask(__name__)
db = []
db_names = []

def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def eurovision(*args):
    spisok = {1: 'Urkaine: Kalush Orchestra - Stefania', 2: 'United Kingdom: Sam Ryder - SPACE MAN', 3: 'Spain: Chanel - SloMo',
            4: 'Sweden: Cornelia Jakobs - Hold Me Closer', 5: 'Konstrakta - In Corpore Sano', 6: \
                'Italy: Mahmood & Blanco - Brividi', 7: 'Moldova: Zdob şi Zdub & Advahov Brothers - Trenulețul',
            8: 'Greece: Amanda Georgiadi Tenfjord - Die Together', 9: 'Portugal: MARO - Saudade Saudade',
            10: 'Norway: Subwoolfer - Give That Wolf A Banana', 11: 'Netherlands: S10 - De Diepte',
            12: 'Poland: Ochman - River', 13: 'Estonia: Stefan - Hope', 14: 'Lithuania: Monika Liu - Sentimentai',
            15: 'Australia: Sheldon Riley - Not The Same', 16: 'Azerbaijan: Nadir Rustamli - Fade To Black',
            17: 'Switzerland: Marius Bear - Boys Do Cry', 18: 'Romania: WRS - Llámame', 19: \
                'Belgium: Jérémie Makiese - Miss You', 20: 'Armenia: Rosa Linn - Snap', 21: \
                'Finland: The Rasmus - Jezebel', 22: 'Czech Republic: We Are Domi - Lights Off',
            23: 'Iceland: Systur - Með Hækkandi', 24: 'Alvan & Ahez - Fulenn', 25: 'Germany: Malik Harris - Rockstars'}
    if args:
        return spisok.get(*args)
    else:
        return spisok

    
@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/send", methods= ['POST'])
def send_message():
    '''
    функция для отправки нового сообщения пользователем
    :return:
    '''
    # TODO
    # проверить, является ли присланное пользователем правильным json-объектом
    # проверить, есть ли там имя и текст
    # Добавить сообщение в базу данных db
    data = flask.request.json
    if not isinstance(data, dict):
        return abort(400)

    if 'name' not in data or 'text' not in data:
        return abort(400)

    if not isinstance(data['name'], str) or not isinstance(data['text'], str) or \
        len(data['name']) == 0 or len(data['text']) == 0:
        return abort(400)

    text = data['text']
    name = data['name']
    message = {
        'text': text,
        'name': name,
        'time': time.time()
    }
    db.append(message)
    return {'ok': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(flask.request.args['after'])
    except:
        abort(400)
    db_after = []
    for message in db:

        words = message['text'].split(' ')
        com = words[0]

        if message['time'] > after:
            """
            тут возможность отправлять анонимное сообщение
            """
            if com == '!anon':
                message['name'] = 'Анонимный пользователь'
                message['text'] = ' '.join(words[1:])
                db_after.append(message)
            else:
                db_after.append(message)

        """
        тут чат-бот, который дает узнать итоги прошедшего евровидения.
        если ввести просто команду !euro, то выведется весь список стран с их конкурсантами по местам.
        если после команды !euro ввести через пробел натуральное число от 1 до 25, то выведется страна и ее конкурсант, 
        который занял соответсвующее введенному числу место. 
        """

        if com[:5] == '!euro' and message['time'] > after:
            error = {
                'text': 'Команда !euro работает самостоятельно или принимает одно целое число от 1 до 25 через пробел',
                'name': 'Eurobot',
                'time': time.time()
            }
            # проверка, что не написано !euro6, !eurovision и т.п.
            if com != com[:5]:
                db_after.append(error)
            else:
                # проверка, что команда либо без аргумента, либо с одним
                if len(words) > 2:
                    db_after.append(error)
                # выводим весь список финалистов с занятыми ими местами в порядке возрастания мест
                elif len(words) == 1:
                    answer = {
                        'text': eurovision(),
                        'name': 'Eurobot',
                        'time': time.time()
                    }
                    db_after.append(answer)
                # выводим, кто конкретно занял место, указываемое в аргументе около команды
                elif len(words) == 2:
                    # проверяем, что аргумент у команды можно преобразовать в int
                    if is_int(words[1]) == True:
                        n = int(words[1])
                        # проверяем, находится ли поданное число в диапазоне мест
                        if n >= 1 and n <= 25:
                            answer = {
                                    'text': eurovision(n),
                                    'name': 'Eurobot',
                                    'time': time.time()
                                }
                            db_after.append(answer)
                        else:
                            db_after.append(error)
                    else:
                        db_after.append(error)

    return {'messages': db_after}


@app.route("/status")
def print_status():
    for message in db:
        if message['name'] not in set(db_names) and message['name'] != 'Анонимный пользователь':
            db_names.append(message['name'])
    t = time.time()
    dt = datetime.fromtimestamp(t)
    status = {
        'Текущие дата и время': dt.strftime('%Y-%m-%d %H:%M:%S'),
        'Пользователи': db_names,
        'Количество пользователей': len(db_names),
        'Количество сообщений': len(db)
    }
    return json.dumps(status, ensure_ascii=False)



app.run()
