# импорт необходимых библиотек
import logging
import sqlite3


# Функция для создания базы данных
def create_db():
    connection = sqlite3.connect("sqlite3.db")  # Устанавливаем соединение с базой данных
    connection.close()  # Закрываем соединение
    logging.info("База данных успешно создана")  # Выводим сообщение в лог о том, что база данных создана


# Функция для обработки запросов к базе данных
def process_query(query, params):
    connection = sqlite3.connect("sqlite3.db")  # Устанавливаем соединение с базой данных
    connection.row_factory = sqlite3.Row  # Устанавливаем формат возвращаемых данных
    cur = connection.cursor()
    if not params:
        if 'SELECT' in query:
            result = cur.execute(query)
            return result
        cur.execute(query)
    else:
        if 'SELECT' in query:
            result = cur.execute(query, tuple(params))
            return list(result)
        cur.execute(query, tuple(params))
    connection.commit()  # Сохраняем изменения в базе данных
    connection.close()  # Закрываем соединение


# Функция для создания таблицы prompts
def create_prompts_table():
    query = '''
    CREATE TABLE IF NOT EXISTS prompts(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    role INTEGER,
    text TEXT DEFAULT " ",
    tokens INTEGER DEFAULT 0,
    session_id INTEGER DEFAULT 0);'''
    process_query(query, None)


# Функция для создания таблицы settings
def create_settings_table():
    query = '''
       CREATE TABLE IF NOT EXISTS settings(
       id INTEGER PRIMARY KEY,
       user_id INTEGER UNIQUE,
       genre TEXT DEFAULT "",
       character TEXT DEFAULT "",
       place TEXT DEFAULT "",
       additional_info TEXT DEFAULT "",
       processing_answer INTEGER DEFAULT 0) ;'''
    process_query(query, None)


# Функция для добавления пользователя в базу данных
def add_user_to_database(table_name, user_id):
    query = f'''INSERT INTO {table_name} (user_id) VALUES (?);'''
    process_query(query, [user_id])
    logging.info(f"Пользователь с user_id = {user_id} успешно добавлен в базу данных")


# Функция для поиска данных пользователя в базе данных
def find_user_data(table_name, user_id):
    query = f'''SELECT * FROM {table_name} WHERE user_id = ?;'''
    result = process_query(query, [user_id])
    if result:
        logging.info(f"Данные пользователя с user_id {user_id} успешно найдены.")
        return result[0]
    logging.error("Не получилось собрать данные пользователя.")
    return result


# Функция для обновления данных пользователя в базе данных
def update_user_data(table_name, user_id, column_name, value):
    query = f'''UPDATE {table_name} SET {column_name} = ? WHERE user_id = ?;'''
    process_query(query, [value, user_id])
    logging.info(f"база данных успешно обновлена, таблица: {table_name}, колонка: {column_name}, user_id: {user_id}")


# Функция для подсчета количества пользователей в базе данных
def count_users():
    query = "SELECT COUNT(DISTINCT user_id) FROM prompts"
    counter = list(process_query(query, None))
    logging.info(f"Успешно подсчитано количество пользователей {counter[0][0]}")
    return counter[0][0]


# Функция для поиска текущей сессии пользователя в базе данных
def find_current_session(user_id):
    query = f'''SELECT COUNT(DISTINCT session_id) FROM prompts WHERE user_id = ?;'''
    counter = process_query(query, [user_id])
    logging.info(f"Текущая сессия для пользователя с user_id: {user_id} успешно найдена: {counter[0][0]}.")
    return counter[0][0]


# Функция для поиска промптов пользователя в текущей сессии в базе данных
def find_prompts_by_session(user_id, session_id):
    query = "SELECT role, text FROM prompts WHERE user_id = ? and session_id = ?"
    prompts = process_query(query, [user_id, session_id])
    logging.info(f"Промпты пользователя с user_id: {user_id} в сессии {session_id} успешно найдены")
    return prompts


# Функция для поиска ответа нейросети для пользователя в текущей сессии в базе данных
def find_assistant_text_by_session(user_id, session_id):
    query = '''
    SELECT text 
    FROM prompts
    WHERE user_id = ? and session_id = ? and role = "assistant" 
    ORDER BY id DESC 
    LIMIT 1'''
    content = process_query(query, [user_id, session_id])
    if content:
        content = content[0]["text"]
        logging.info(f"Ответ нейросети для пользователя с user_id: {user_id} в сессии {session_id} успешно найден.")
    else:
        logging.info(f"Не удалось получить ответ нейросети для пользователя с user_id: {user_id} в сессии {session_id}")
    return content


# Функция для поиска текста промпта пользователя по роли и user_id в базе данных
def find_text_by_role_and_user_id(user_id, role):
    query = '''
       SELECT text 
       FROM prompts
       WHERE user_id = ? and role = ?
       ORDER BY id DESC 
       LIMIT 1'''
    content = process_query(query, [user_id, role])
    if content:
        content = content[0]["text"]
        logging.info(f"Контент для пользователя с user_id: {user_id} от роли: {role} успешно найден.")
    else:
        logging.info(f"Не удалось получить контент для пользователя с user_id: {user_id} от роли: {role}")
    return content


# Функция для добавления промпта в базу данных
def add_prompt_to_database(user_id, role, text, tokens, session_id):
    query = '''INSERT INTO prompts (user_id, role, text, tokens, session_id) VALUES(?, ?, ?, ?, ?)'''
    values = [user_id, role, text, tokens, session_id]
    process_query(query, values)
    logging.info(f"Промпт от пользователя с user_id: {user_id} в сессии {session_id} успешно добавлен в базу данных")


# Функция для поиска последнего промпта
def find_latest_prompt(user_id):
    query = f"SELECT * FROM prompts WHERE user_id = ? ORDER BY id DESC LIMIT 1"
    prompt_data = process_query(query, [user_id])
    if prompt_data:
        logging.info(f"Последний промпт пользователя с user_id: {user_id} успешно найден")
        prompt_data = prompt_data[0]
    else:
        logging.info(f"Не удалось получить последний промпт пользователя с user_id: {user_id} успешно найден")
    return prompt_data


def delete_settings(user_id):
    query = f"DELETE FROM settings WHERE user_id = ?"
    process_query(query, [user_id])
    logging.info(f"Настройки пользователя с user_id = {user_id} успешно удалены из базы данных")


def delete_process_answer():
    query = "UPDATE settings SET processing_answer = 0"
    process_query(query, None)
    logging.info(f"Ошибка взаимодействия с нейросетью успешно исправлена")
