import sqlite3 as sq

# Не очень хороший метод, так как если произойдет ошибка при работе с базой данных, она не закроется
#.................................................................
con = sq.connect('saper.db') # устанавливаем связь с базой данных
cur = con.cursor() # возвращает экземплял класса

cur.execute('''
''')

con.close() # закрываем БД
#.................................................................


#.................................................................
# Контекст менеджера автоматически закрывает БД, даже если произошла ошибка

with sq.connect("saper.db") as con:
   cur = con.cursor() # возвращает экземплял класса
   cur.execute('''DROP TABLE IF EXISTS users''')  # удаление таблицы
   # CREATE TABLE users говорим что нужно создать таблицу с именем users, а так же если она уже есть то не нужно
   # Затем в круглых скобках создаем структуру таблицы, говорим какие будут поля
   # указываем имя и какой будет тип данных
   # NOT NULL значит что поле должно быть заполнено
   # DEFAULT 1 по умолчанию, значение 1
   # PRIMARY KEY говорим что значение будет уникальным ключём
   # AUTOINCREMENT говорит что уникальное имя увеличивается на единицу
   cur.execute('''CREATE TABLE users (
   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT NOT NULL,
   sex INTEGER NOT NULL DEFAULT 1,
   old INTEGER,
   score INTEGER
   )''')
#.................................................................


#.................................................................
#INSERT добавление записи в таблицу

#with sq.connect('saper.db') as con:
   cur = con.cursor()
   cur.execute('INSERT INTO users VALUES(1, \'Игорь\', 1, 21, 1500)')
   cur.execute('INSERT INTO users (name, old, score) VALUES(\'Петя\', 21, 1400)') # В случае если по умолчанию есть данные в неиспользуемых столбцах
#.................................................................


#.................................................................
# BETWEEN число AND число - диапазон выборки

with sq.connect('saper.db') as con:
   cur = con.cursor()
   cur.execute('SELECT * FROM users WHERE score BETWEEN 0 AND 2000')
#.................................................................


#.................................................................
# Удаление таблицы

with sq.connect("saper.db") as con:
   cur = con.cursor() # возвращает экземплял класса
   cur.execute('''DROP TABLE users''') # удаление таблицы
#.................................................................


#.................................................................
# Доступ к БД, то есть можем прописывать команды SQL, а так же получать доступ к результату
# SELECT возвращает данные из таблицы
# SELECT name, old, score FROM users - Вернет имя, возраст, очки игроков
# ORDER BY выполняет сортировку по выбранному столбцу, если хотим сортировать по убыванию, то дописываем DESC.
# LIMIT 1, 2 - значит что пропускает 1 запись и выводит следующие 2
# LIMIT 1 - значит что выведет 1 запись

with sq.connect("saper.db") as con:
   cur = con.cursor() # возвращает экземплял класса
   cur.execute('SELECT * FROM users WHERE old > 0 ORDER BY old DESC LIMIT 1, 2') # Прописываем условие для выборки из таблицы
   #result = cur.fetchall()  #Записываем выборку в переменную
   #(result)
   # Или можем последвательно перебирать итерируемый обьект cur, что очень сильно экономит память компьютера
   for result in cur:
       print(result)

#.................................................................


#.................................................................
# Доступ к БД, и использование методов fetchmany b fetchone, если вызывать последовательно, то продолжит, а не начнет с начала
# fetchmany(size) возвращает число записей, не более чем size
# fetchone() возвращает первую запись

with sq.connect("saper.db") as con:
   cur = con.cursor() # возвращает экземплял класса
   cur.execute('SELECT * FROM users WHERE old > 0 ORDER BY old DESC LIMIT 1, 10') # Прописываем условие для выборки из таблицы
   result = cur.fetchone()
   result2 = cur.fetchmany(3)
   print(result)
   print(result2)
#.................................................................


#.................................................................
# Обнуление очков у пользователей, запись имеет вид:
# UPDATE имя_таблицы SET имя_столбца = новое значение WHERE условие

with sq.connect("saper.db") as con:
   cur = con.cursor() # возвращает экземплял класса
   cur.execute('UPDATE users SET score = 0')
#.................................................................


#.................................................................
# Обновляем данные если у игрока rowid = 1 или это девушка:
# UPDATE имя_таблицы SET имя_столбца = новое значение WHERE условие

with sq.connect("saper.db") as con:
   cur = con.cursor() # возвращает экземплял класса
   cur.execute('UPDATE users SET score = 1000 WHERE rowid = 1 OR sex = 2')
# .................................................................


#.................................................................
# Присвиваем 1500 очков если игрока зовут Федя
# LIKE возвращает true если поле name совпадает с тем, что мы написали (Ресурсозатратная операция)
# UPDATE имя_таблицы SET имя_столбца = новое значение WHERE условие

with sq.connect("saper.db") as con:
   cur = con.cursor() # возвращает экземплял класса
   cur.execute('UPDATE users SET score = 1500 WHERE name LIKE \'Федя\'')
#.................................................................


#.................................................................
# К score прибавляем 2000 очков, если имя начинается на В
# % - любое продолжение строки, _ - любой символ (один текущий)

with sq.connect("saper.db") as con:
   cur = con.cursor()
   cur.execute('UPDATE users SET score = score + 2000 WHERE name LIKE \'В%\'')
#.................................................................


#.................................................................
# DELETE FROM имя_таблицы WHERE условие (условие нужно прописывать очень строгим, чтобы не удалить лишние данные)

with sq.connect("saper.db") as con:
   cur = con.cursor()
   cur.execute('DELETE FROM users WHERE rowid IN(2, 5)') # удаляем записи у которых rowid = 2 и =5
#.................................................................


#.................................................................
# Агрегирующие функции

# count(имя_столбца) - вычисляет количество записей, которые попали в нашу выборку
# count() - также вычислит кол-во записей, которые попали в выборку
# В SQL выведет поле с именем count(user_id), что некрасиво,
# поэтому есть возможность поменять имя поля, если дописать count() as count
# Помимо count(), можно использовать агрегирующие функции:
# sum() - подсчет суммы указанного поля по всем записям выборки
# avg() - вычисляет среднее арифметическое указанного поля
# min() - нахождение минимального значения для указанного поля
# max() - нахождение максимального значения для указанного поля

with sq.connect("saper.db") as con:
   cur = con.cursor()
   #cur.execute('SELECT count(user_id) FROM games WHERE user_id = 1')
   cur.execute('SELECT count(user_id) FROM games WHERE user_id = 1')
   for res in cur:
       print(res)
#.................................................................


#.................................................................
# Агрегирующие функции

# DISTINCT - позволяет выбрать поля с уникальными значениями, записывается перед полем которое мы выбираем
# count(DISTINCT имя_столбца) - подсчитает количество уникальных значений
with sq.connect("saper.db") as con:
   cur = con.cursor()
   #cur.execute('SELECT count(user_id) FROM games WHERE user_id = 1')
   cur.execute('SELECT count(DISTINCT user_id) FROM games')
   for res in cur:
       print(res)
#.................................................................


#.................................................................
# Группировка записей

# В данном примере будет производиться группировка записей по user_id
# GROUP BY имя_поля
# GROUP BY user_id - группируем записи по user_id
# ORDER BY sum DESC - сортируем по убыванию столбец sum

with sq.connect("saper.db") as con:
   cur = con.cursor()
   cur.execute('''SELECT user_id, sum(score) as sum
               FROM games
               GROUP BY user_id
               ORDER BY sum DESC
               ''')

   for res in cur:
       print(res)

#.................................................................


#.................................................................
# JOIN - Создание сводных таблиц (указывает какую таблицу будем связывать,
# объединяет записи, если есть совпадения в таблицах)
# LEFT JOIN - Создание сводных таблиц (указывает какую таблицу будем связывать,
# даже если нет совпадения с другой таблицей, создаст запись с пустыми значениями,
# которые должны были из нее браться)
# games.score - Явно указываем что берем значение score из таблицы games,
# так как в таблице users так же есть поле score
# после ключевого слова ON задается условие связывания
# games.user_id = users.rowid - указываем что айди пользователя должен совпадать с уникальным именем

with sq.connect("saper.db") as con:
   cur = con.cursor()
   cur.execute('''SELECT name, sex, games.score FROM games
                   JOIN users ON games.user_id = users.rowid''')
   for res in cur:
       print(res)
#.................................................................


#.................................................................
# Сводная таблица без JOIN

with sq.connect("saper.db") as con:
   cur = con.cursor()
   cur.execute('''SELECT name, sex, games.score FROM users, games''')
   for res in cur:
       print(res)
#.................................................................


#.................................................................
# Групируем записи, объединяем таблицы, выводим сумму всех игр каждого игрока

with sq.connect("saper.db") as con:
   cur = con.cursor()
   cur.execute('''SELECT name, sum(games.score) as score
                   FROM games
                   JOIN users ON games.user_id = users.user_id
                   GROUP BY games.user_id
                   ORDER BY score DESC''')
   for res in cur:
       print(res)
#.................................................................


#.................................................................
# Работа с оператором объединения UNION

# поля score и val, from и type совпадают по типу данных, что позволяет объединить таблицы
# `from` записывается, чтобы не было совпадения с оператором FROM
# оператор UNION при объединении записей оставляет только уникальные значения

with sq.connect("test_union.db") as con:
   cur = con.cursor() # возвращает экземплял класса
   cur.execute('''SELECT score, `from` FROM tab1
   UNION SELECT val, type FROM tab2''')
   for res in cur:
       print(res)
#....................................................... ..........


#.................................................................
# Вложенные SQL-запросы

with sq.connect("students_marks_table.db") as con:
   cur = con.cursor()
   cur.execute("""SELECT name, subject, mark FROM marks
   JOIN students ON students.rowid = marks.id
   WHERE mark > (SELECT avg(mark) FROM marks
   WHERE id = 2)
   AND subject LIKE ('Си') """)
   for res in cur:
       print(res)

#.................................................................


#.................................................................
# Запись из одной таблицы в другую по условию

with sq.connect("students_marks_table.db") as con:
   cur = con.cursor() # возвращает экземплял класса
   cur.execute('''INSERT INTO femaly
                   SELECT * FROM students WHERE sex = 2''')
   for res in cur:
       print(res)
#.................................................................


#.................................................................
# Обнуляем строки по условию, для всех, если их оценка меньше либо равна оценке выбранного индекса

with sq.connect("students_marks_table.db") as con:
   cur = con.cursor() # возвращает экземплял класса
   cur.execute('''UPDATE marks SET mark = 0
   WHERE mark <= (SELECT min(mark) FROM marks WHERE id = 1)''')
   for res in cur:
       print(res)
#.................................................................


#.................................................................
# Работа с python, с шаблонами

# VALUES(NULL, ?, ?) - шаблон, вместо вопросительных знаков будет подставлено первое значение
# первого кортежа, так как у нас указано cars[0] и второе значение ппервого кортежа

# Вместо перебора циклом for лучше использовать метод executemany:
# cur.executemany(" INSERT INTO cars VALUES(NULL, ?, ?)", cars)

# Именованные параметры (:Price)
# cur. execute("UPDATE cars SET price =:Price WHERE model LIKE 'A%'", {'Price': 0})
# Значение ключа подставится вместо ключа, таким образом мы для всех автомобилей, которые начинаются с A цену поставим 0

# ; - выполняем несколько команд, но есть ограничение, нельзя использовать шаблоны
# cur.executescript("""DELETE FROM cars WHERE model LIKE 'A%';
#     UPDATE cars SET price = price + 1000
#     """)

cars = [
   ('AUDI', 52642),
   ('Mersedes', 57127),
   ('Skoda', 9000),
   ('Volvo', 29000),
   ('Bentley', 350000)
]

with sq.connect("cars.db") as con:
   cur = con.cursor()

   cur.execute("""CREATE TABLE IF NOT EXISTS cars(
   car_id INTEGER PRIMARY KEY AUTOINCREMENT,
   model TEXT,
   price INTEGER)""")
    for car in cars:
       cur.execute("INSERT INTO cars VALUES(NULL, ?, ?)", car)

    cur.executemany(" INSERT INTO cars VALUES(NULL, ?, ?)", cars)

    cur. execute("UPDATE cars SET price =:Price WHERE model LIKE 'A%'", {'Price': 0})

   cur.executescript("""DELETE FROM cars WHERE model LIKE 'A%';
   UPDATE cars SET price = price + 1000
   """)
#.................................................................


#.................................................................
# если при работе с БД появляется ошибка, мы пишем об этом в терминал
# BEGIN - метка к которой мы возвращаемся, если произошла ошибка

cars = [
   ('AUDI', 52642),
   ('Mersedes', 57127),
   ('Skoda', 9000),
   ('Volvo', 29000),
   ('Bentley', 350000)
]
con = None
try:
   con = sq.connect("cars.db")
   cur = con.cursor()

   cur.executescript("""CREATE TABLE IF NOT EXISTS cars(
   car_id INTEGER PRIMARY KEY AUTOINCREMENT,
   model TEXT,
   price INTEGER
   );
   BEGIN;
   INSERT INTO cars VALUES(NULL, 'AUDI', 52642);
   INSERT INTO cars VALUES(NULL, 'Mersedes', 57127);
   INSERT INTO cars VALUES(NULL, 'Skoda', 9000);
   INSERT INTO cars VALUES(NULL, 'Volvo', 29000);
   INSERT INTO cars VALUES(NULL, 'Bentley', 350000)
   """)

   con.commit() # Сохраняет изменения в БД

except sq.Error as e:
   if con:
       con.rollback() # Откатывает БД к исходное состояние
   print("Ошибка выполнения запроса!")
finally:
   if con:
       con.close()
#.................................................................


#.................................................................
# lastrowid - будет содержать id последней записи

with sq.connect("cars.db") as con:
    cur = con.cursor()

    cur.executescript("""CREATE TABLE IF NOT EXISTS cars(
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT,
    price INTEGER);
    CREATE TABLE IF NOT EXISTS cust(name TEXT, tr_in INTEGER, buy INTEGER)
    """)

    cur.execute("INSERT INTO cars VALUES(NULL, 'Запарожец', 1000)")
    last_row_id = cur.lastrowid
    buy_car_id = 2
    cur.execute("INSERT INTO cust VALUES('Федор', ?, ?)", (last_row_id, buy_car_id))
#.................................................................


#.................................................................
#  con.row_factory = sq.Row - делаем так, чтобы возвращался словарь

cars = [
   ('AUDI', 52642),
   ('Mersedes', 57127),
   ('Skoda', 9000),
   ('Volvo', 29000),
   ('Bentley', 350000)
]

with sq.connect("cars.db") as con:
    con.row_factory = sq.Row
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT,
    price INTEGER
    )
    """)
    cur.execute("SELECT * FROM cars")
    for cr in cur:
        print(cr['model'], cr['price'])
#.................................................................


#.................................................................
# Сохранение изображения в БД
# BLOB - хранится в бинарном виде, то есть записываются так, как есть
def readAva(n):
    try:
        with open(f"avas/{n}.png", "rb") as f:
            return f.read()
    except IOError as e:
        print(e)
        return False

with sq.connect("cars.db") as con:
    con.row_factory = sq.Row
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    ava BLOB,
    score INTEGER
    )
    """)
    img = readAva(1)
    if img:
        binary = sq.Binary(img) # Преобразуем бинарный обьект в специальный бинарный обьект модуля SQlite
        cur.execute("INSERT INTO users VALUES ('Николай', ?, 1000)", (binary,))
#.................................................................


#.................................................................
# Чтение изображения из БД и сохранение его в каталог

def readAva(n):
    try:
        with open(f"avas/{n}.png", "rb") as f:
            return f.read()
    except IOError as e:
        print(e)
        return False

def writeAva(name, data): # Передаем имя файла и данные
    try:
        with open(name, "wb") as f: # Открываем фаил в бинарном режиме
            f.write(data) # Записываем данные
    except IOError as e:
        print(e)
        return False

    return True

with sq.connect("cars.db") as con:
    con.row_factory = sq.Row
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    ava BLOB,
    score INTEGER
    )
    """)
    cur.execute("SELECT ava FROM users LIMIT 1")
    img = cur.fetchone()['ava'] # Читаем бинарные данные, с помощью метода fetchone(), обращаемся через имя, благодаря строчке: ava con.row_factory = sq.Row

    writeAva("but.png", img) # Создаем фаил и записываем в него данные, которые мы прочитали
#.................................................................


#.................................................................
# iterdump - возвращает sql запрос, что позволяет создать такую же БД, как и та, которую мы считываем
#
with sq.connect("cars.db") as con:
    cur = con.cursor()

    for sql in con.iterdump():
        print(sql)
#.................................................................


#.................................................................
# Запись QSL запроса для создания копии БД в фаил

# iterdump - возвращает sql запрос, что позволяет создать такую же БД, как и та, которую мы считываем

with sq.connect("cars.db") as con:
    cur = con.cursor()

    with open("sql_damp.sql", "w") as f: # Открываем фаил на запись и записываем в этот фаил
        for sql in con.iterdump():
            f.write(sql)
#.................................................................


#.................................................................
# Хранение БД не на диске, а в памяти компьютера

data = [("car", "машина"), ("house", "дом"), ("tree", "дерево"), ("color", "цвет"), ]

con = sq.connect(':memory:') # Чтобы создать БД не на диске, а в памяти
with con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS dict(
    eng TEXT,
    rus TEXT)""")

    cur.executemany("INSERT INTO dict VALUES(?, ?)", data)

    cur.execute("SELECT rus FROM dict WHERE eng LIKE 'c%'")

    print(cur.fetchall()) # Вывод в консоль
#.................................................................