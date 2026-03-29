from connect import connect
from config import load_config
import csv
import re

#Создание таблицы
def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
        """)
    conn.commit()

#Загрузка SQL-файлов
def execute_sql_file(conn, filename):
    with conn.cursor() as cur:
        with open(filename, 'r', encoding='utf-8') as f:
            cur.execute(f.read())
    conn.commit()

#Добавление/обновление
def insert_contact(conn):
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()

    if not re.fullmatch(r'[0-9\-]+', phone):
        print(f"Invalid phone: {phone}")
        return

    with conn.cursor() as cur:
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print("Added or updated.")

#импорт из CSV
def insert_from_csv(conn, filename="contacts.csv"):
    users = []
    with open(filename, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            # Проверяем, что строка имеет хотя бы 2 колонки
            if len(row) >= 2:
                name = row[0].strip()
                phone = row[1].strip()
                users.append(f"{name},{phone}")
            else:
                print(f"Skipped invalid row: {row}")

    if users:
        with conn.cursor() as cur:
            cur.execute("CALL bulk_upsert_contacts(%s)", (users,))
        conn.commit()
        print("CSV imported with validation.")
    else:
        print("No valid contacts found in CSV.")

#Показ всех контактов
def show_all(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, phone FROM contacts ORDER BY id")
        for row in cur.fetchall():
            print(row)

#Поиск по шаблону
def search_by_name(conn):
    pattern = input("Enter name or phone: ").strip()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No matching contacts found.")

#Пагинация
def show_paginated(conn):
    try:
        limit = int(input("Limit: "))
        offset = int(input("Offset: "))
    except ValueError:
        print("Invalid input. Enter integer numbers.")
        return

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts in this page.")

#Удаление
def delete_by_name(conn):
    name = input("Enter name: ").strip()
    with conn.cursor() as cur:
        cur.execute("CALL delete_contact(p_name => %s)", (name,))
    conn.commit()
    print("Deleted.")

def delete_by_phone(conn):
    phone = input("Enter phone: ").strip()
    with conn.cursor() as cur:
        cur.execute("CALL delete_contact(p_phone => %s)", (phone,))
    conn.commit()
    print("Deleted.")

#Меню
def menu():
    config = load_config()
    conn = connect(config)

    create_table(conn)

    #Загрузка функции и процедуры
    execute_sql_file(conn, 'functions.sql')
    execute_sql_file(conn, 'procedures.sql')

    while True:
        print("\n1 Add contact")
        print("2 Show all")
        print("3 Search by name/phone")
        print("4 Show paginated")
        print("5 Delete by name")
        print("6 Delete by phone")
        print("7 Import CSV")
        print("0 Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_contact(conn)
        elif choice == "2":
            show_all(conn)
        elif choice == "3":
            search_by_name(conn)
        elif choice == "4":
            show_paginated(conn)
        elif choice == "5":
            delete_by_name(conn)
        elif choice == "6":
            delete_by_phone(conn)
        elif choice == "7":
            insert_from_csv(conn)
        elif choice == "0":
            conn.close()
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()