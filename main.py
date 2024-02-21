import sqlite3 as sq

class BD:
    def new_bd_table(self, name_file: str, name_table: str):

        with sq.connect(f'{name_file}') as con:
            cur = con.cursor()
            cur.execute(f'''
            CREATE TABLE {name_table}(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sex INTEGER NOT NULL DEFAULT 1,
            skill INTEGER NOT NULL DEFAULT 0
            )
            ''')

class People:

    def __init__(self, name_file: str, name_table: str):
        print('Сейчас вы запишите в базу данных имя человека, его пол (0-девочка, 1-мальчик) и его скил по жизни.')
        print('Укажите имя человека:')
        name = input()
        print('Укажите пол человека:')
        sex = int(input())
        print('Укажите скил человека:')
        skill = int(input())

        with sq.connect(f'{name_file}') as con:
            cur = con.cursor()
            cur.execute(f'INSERT INTO {name_table}(name, sex, skill) VALUES(\'{name}\', {sex}, {skill})')



pep = People('people.db', 'user')





















