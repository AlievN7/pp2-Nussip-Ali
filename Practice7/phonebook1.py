from connect import connect
from config import load_config
import csv

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

#Добавление
def insert_contact(conn):
    name = input("Name: ")
    phone = input("Phone: ")
    with conn.cursor() as cur:
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print("Added.")

#вставка CSV
def insert_from_csv(conn, filename="contacts.csv"):
    users = []

    with open(filename, encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 2:
                print(f"Skipped invalid row: {row}")
                continue

            name = row[0].strip()
            phone = row[1].strip()

            users.append(f"{name},{phone}")

    if users:
        with conn.cursor() as cur:
            cur.execute("CALL bulk_upsert_contacts(%s)", (users,))
        conn.commit()
        print("CSV imported with validation.")
    else:
        print("No valid data found.")

#все контакты
def show_all(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM contacts ORDER BY id")
        for row in cur.fetchall():
            print(row)

#Поиск
def search_by_name(conn):
    name = input("Enter name or phone: ")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (name,))
        for row in cur.fetchall():
            print(row)

#Удаление имя
def delete_by_name(conn):
    name = input("Enter name: ")
    with conn.cursor() as cur:
        cur.execute("CALL delete_contact(p_name => %s)", (name,))
    conn.commit()
    print("Deleted.")
    
#Удаление номер
def delete_by_phone(conn):
    phone = input("Enter phone: ")
    with conn.cursor() as cur:
        cur.execute("CALL delete_contact(p_phone => %s)", (phone,))
    conn.commit()
    print("Deleted.")

#Обновление контакта
def update_contact(conn):
    contact_id = int(input("Enter contact ID to update: "))
    new_name = input("New name: ")
    new_phone = input("New phone: ")

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE contacts
            SET name = %s, phone = %s
            WHERE id = %s
        """, (new_name, new_phone, contact_id))

    conn.commit()
    print("Contact updated.")
    
#Фильтр
def filter_contacts(conn):
    name = input("Filter by name (Enter to skip): ")
    phone = input("Filter by phone (Enter to skip): ")

    query = "SELECT * FROM contacts WHERE 1=1"
    params = []

    if name:
        query += " AND name ILIKE %s"
        params.append(f"%{name}%")

    if phone:
        query += " AND phone ILIKE %s"
        params.append(f"%{phone}%")

    with conn.cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No results found.")
    
def menu():
    config = load_config()
    conn = connect(config)

    create_table(conn)


    while True:
        print("\n1 Add contact")
        print("2 Update contact")
        print("3 Show all")
        print("4 Search by name/phone")
        print("5 Delete by name")
        print("6 Delete by phone")
        print("7 Import CSV")
        print("8 Show by filter")
        print("0 Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_contact(conn)
        elif choice == "2":
            update_contact(conn)
        elif choice == "3":
            show_all(conn)
        elif choice == "4":
            search_by_name(conn)
        elif choice == "5":
            delete_by_name(conn)
        elif choice == "6":
            delete_by_phone(conn)
        elif choice == "7":
            insert_from_csv(conn)
        elif choice == "8":
            filter_contacts(conn)
        elif choice == "0":
            conn.close()
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()