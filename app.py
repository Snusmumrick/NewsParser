from flask import Flask
import sqlite3
from flask import jsonify
from flask import request
from apscheduler.schedulers.background import BackgroundScheduler
from load import loadData,generateDB


app = Flask(__name__)

# Глобальные переменные
DB = "news.db"  #Название базы данных
MAX_COUNT = 30 #Максимальное число записей
LIMIT = 5 # Значение LIMIT по умолчанию
OFFSET = 0 # Значение OFFSET по умолчанию
ORDER = "id" # Значение поля для сортировки
MINUTES = 15 # Время для периодического опрашивания сайта новостей

def checkParams(order,limit,offset):
    """
    Функция проверяющая корректность параметров для выборки
    :param order:
    :param limit:
    :param offset:
    :return:
    """
    if order not in ['id','title','url','created','-id','-title','-url','-created']:
        raise Exception("Wrong order param")
    try:
        limit = int(limit)
        if limit<0 or limit>MAX_COUNT:
            raise Exception("Limit should be in 0 - {}".format(MAX_COUNT))
    except ValueError:
        raise Exception("Limit should be integer")
    try:
        offset = int(offset)
    except:
        raise Exception("Offset should be integer")
    return True


def dictFactory(cursor, row):
    """
    Функция для преобразования результатов запроса в словарь, для перевода затем в JSON
    :param cursor:
    :param row:
    :return:
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route("/posts", methods=["GET"])
def posts():
    """
    Основная функция API. В ней формируется запрос к базе данных и возвращается результат данного запроса.
    :return:
    """
    req = "SELECT * FROM news ORDER BY {} {} LIMIT {} OFFSET {} "
    limit = request.args.get("limit",5)
    offset = request.args.get("offset",0)
    order = request.args.get("order","id")
    order_p = 'ASC'
    if order[0]=='-':
        order_p = 'DESC'
        order = order[1:]
    try:
        checkParams(order,limit,offset)
        con = sqlite3.connect(DB)
        con.row_factory = dictFactory
        cur = con.cursor()
        return jsonify(cur.execute(req.format(order,order_p, limit,offset)).fetchall())
    except Exception as e:
        return jsonify({"error":str(e)})


@app.route("/update",methods=["POST"])
def update():
    """
    Метод API позволяющий обновить БД не по таймеру, а принудительно
    :return:
    """
    loadData()

# Создание процесса фонового обновления БД
scheduler = BackgroundScheduler()
scheduler.add_job(func=loadData, trigger="interval", seconds = MINUTES*60)
scheduler.start()

# Инициализация и запуск
if __name__ == "__main__":
    generateDB()
    loadData()
    app.run(host="0.0.0.0")

