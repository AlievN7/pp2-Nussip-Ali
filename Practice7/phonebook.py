from connect import connect
from config import load_config
import csv

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


def insert_contact(conn):
    name = input("Name: ")
    phone = input("Phone: ")

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
            (name, phone)
        )
    conn.commit()
    print("Added.")



def insert_from_csv(conn, filename="contacts.csv"):
    with open(filename, encoding="utf-8") as f:
        reader = csv.reader(f)
        with conn.cursor() as cur:
            for row in reader:
                cur.execute(
                    "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                    (row[0], row[1])
                )
    conn.commit()
    print("CSV imported.")


def show_all(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM contacts")
        for row in cur.fetchall():
            print(row)


def search_by_name(conn):
    name = input("Enter name: ")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM contacts WHERE name = %s", (name,))
        print(cur.fetchall())


def search_by_prefix(conn):
    prefix = input("Enter phone prefix: ")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM contacts WHERE phone LIKE %s", (prefix + "%",))
        print(cur.fetchall())

def update_name(conn):
    phone = input("Enter phone: ")
    new_name = input("New name: ")

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE contacts SET name = %s WHERE phone = %s",
            (new_name, phone)
        )
    conn.commit()
    print("Updated.")

def update_phone(conn):
    name = input("Enter name: ")
    new_phone = input("New phone: ")

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE contacts SET phone = %s WHERE name = %s",
            (new_phone, name)
        )
    conn.commit()
    print("Updated.")

def delete_by_name(conn):
    name = input("Enter name: ")

    with conn.cursor() as cur:
        cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
    conn.commit()
    print("Deleted.")


def delete_by_phone(conn):
    phone = input("Enter phone: ")

    with conn.cursor() as cur:
        cur.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
    conn.commit()
    print("Deleted.")


def menu():
    config = load_config()
    conn = connect(config)

    create_table(conn)

    while True:
        print("\n1 Add contact")
        print("2 Show all")
        print("3 Search by name")
        print("4 Search by prefix")
        print("5 Update name")
        print("6 Update phone")
        print("7 Delete by name")
        print("8 Delete by phone")
        print("9 Import CSV")
        print("0 Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_contact(conn)
        elif choice == "2":
            show_all(conn)
        elif choice == "3":
            search_by_name(conn)
        elif choice == "4":
            search_by_prefix(conn)
        elif choice == "5":
            update_name(conn)
        elif choice == "6":
            update_phone(conn)
        elif choice == "7":
            delete_by_name(conn)
        elif choice == "8":
            delete_by_phone(conn)
        elif choice == "9":
            insert_from_csv(conn)
        elif choice == "0":
            conn.close()
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()