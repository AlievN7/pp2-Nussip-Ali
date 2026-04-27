import json
import csv
from connect import connect


# показывает строки из БД

def print_rows(rows):
    if not rows:
        print("  (нет результатов)")
    else:
        for row in rows:
            print(" ", row)


# Иинициализация, читает schema.sql

def setup_schema():
    conn = connect()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            with open("schema.sql", "r", encoding="utf-8") as f:
                cur.execute(f.read())
        conn.commit()
        print("Схема готова.")
    except Exception as e:
        print("Ошибка при настройке схемы:", e)
    finally:
        conn.close()


def run_sql_file(filename):
    """
    Выполняет произвольный .sql файл.
    Используется для загрузки хранимых процедур из procedures.sql.
    CREATE OR REPLACE — безопасно запускать каждый раз при старте.
    """
    conn = connect()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            with open(filename, "r", encoding="utf-8") as f:
                cur.execute(f.read())
        conn.commit()
        print(f"{filename} загружен.")
    except Exception as e:
        print(f"Ошибка загрузки {filename}:", e)
    finally:
        conn.close()


# ДОБАВЛЕНИЕ КОНТАКТА (email, birthday, group)

def add_contact(username, email=None, birthday=None, group_name=None):
    conn = connect()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            # Находим group_id по названию группы
            group_id = None
            if group_name:
                cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                row = cur.fetchone()
                if row:
                    group_id = row[0]
                else:
                    print(f"Группа '{group_name}' не найдена. group_id будет NULL.")

            cur.execute("""
                INSERT INTO contacts (username, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (username) DO NOTHING
            """, (username, email, birthday, group_id))

        conn.commit()
        print(f"Контакт '{username}' добавлен.")
    except Exception as e:
        conn.rollback()
        print("Ошибка при добавлении контакта:", e)
    finally:
        conn.close()


# КРИТЕРИЙ 3.4 — ПРОЦЕДУРА add_phone

def add_phone(contact_name, phone, phone_type):
    """
    Вызывает хранимую процедуру add_phone(name, phone, type).
    Процедура находит контакт по имени и добавляет номер в таблицу phones.
    Если контакт не найден — процедура сама выбрасывает исключение.
    """
    conn = connect()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, phone_type))
        conn.commit()
        print(f"Телефон добавлен контакту '{contact_name}'.")
    except Exception as e:
        conn.rollback()
        print("Ошибка при добавлении телефона:", e)
    finally:
        conn.close()


# КРИТЕРИЙ 3.4 — ПРОЦЕДУРА move_to_group

def move_to_group(contact_name, group_name):
    """
    Вызывает хранимую процедуру move_to_group(name, group).
    Процедура создаёт группу если её нет, затем обновляет контакт.
    """
    conn = connect()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
        conn.commit()
        print(f"'{contact_name}' перемещён в группу '{group_name}'.")
    except Exception as e:
        conn.rollback()
        print("Ошибка при перемещении в группу:", e)
    finally:
        conn.close()


# КРИТЕРИЙ 3.4 — ФУНКЦИЯ search_contacts (поиск по имени, email, телефонам)

def search_contacts(query):
    """
    Вызывает SQL-функцию search_contacts(query).
    Функция ищет совпадения ILIKE по полям: username, email, phone.
    Возвращает все совпавшие строки (id, username, email, birthday, phone, type).
    """
    conn = connect()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            rows = cur.fetchall()
        print(f"\nРезультаты поиска по '{query}':")
        print_rows(rows)
    except Exception as e:
        print("Ошибка при поиске:", e)
    finally:
        conn.close()


# КРИТЕРИЙ 3.2 — ФИЛЬТР ПО ГРУППЕ

def filter_by_group(group_name):
    """
    Выводит контакты, принадлежащие указанной группе.
    JOIN с таблицей groups по group_id.
    ILIKE — регистронезависимое сравнение (можно писать 'family' или 'Family').
    """
    conn = connect()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.username, c.email, c.birthday, g.name
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                WHERE g.name ILIKE %s
                ORDER BY c.username
            """, (group_name,))
            rows = cur.fetchall()
        print(f"\nКонтакты в группе '{group_name}':")
        print_rows(rows)
    except Exception as e:
        print("Ошибка при фильтрации по группе:", e)
    finally:
        conn.close()


# КРИТЕРИЙ 3.2 — ПОИСК ПО EMAIL

def search_by_email(email_pattern):
    """
    Ищет контакты по частичному совпадению email.
    Пример: 'gmail' найдёт все адреса @gmail.com
    %...% — подстрока в любом месте строки.
    """
    conn = connect()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, email, birthday
                FROM contacts
                WHERE email ILIKE %s
            """, (f"%{email_pattern}%",))
            rows = cur.fetchall()
        print(f"\nКонтакты с email похожим на '{email_pattern}':")
        print_rows(rows)
    except Exception as e:
        print("Ошибка при поиске по email:", e)
    finally:
        conn.close()


# КРИТЕРИЙ 3.2 — ПОКАЗАТЬ ВСЕ КОНТАКТЫ С СОРТИРОВКОЙ

def show_all_contacts(sort_by="username"):
    """
    Показывает все контакты с JOIN на groups.
    Сортировка по: username / birthday / created_at.
    Используем allowlist для защиты от SQL-инъекций через f-строку.
    """
    # Белый список допустимых полей для ORDER BY
    allowed = {"username", "birthday", "created_at"}
    if sort_by not in allowed:
        sort_by = "username"

    conn = connect()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            # f-строка безопасна здесь, потому что sort_by прошёл через allowlist выше
            cur.execute(f"""
                SELECT c.id, c.username, c.email, c.birthday, g.name
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                ORDER BY c.{sort_by}
            """)
            rows = cur.fetchall()
        print(f"\nВсе контакты (сортировка: {sort_by}):")
        print_rows(rows)
    except Exception as e:
        print("Ошибка при отображении контактов:", e)
    finally:
        conn.close()


# КРИТЕРИЙ 3.2 — ПАГИНАЦИЯ (навигация по страницам)

def paginated_navigation():
    """
    Листает контакты постранично используя SQL-функцию get_contacts_paginated(limit, offset).
    Команды: n = следующая страница, p = предыдущая, q = выход.

    ИСПРАВЛЕНО: убран лишний conn.close() из блока except.
    finally всегда выполняется (даже после return), поэтому conn.close()
    должен быть только там — иначе был бы двойной вызов и ошибка.
    """
    limit = 3   # сколько контактов показывать на одной странице
    offset = 0  # начинаем с первой записи

    while True:
        conn = connect()
        if not conn:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_paginated(%s, %s)",
                    (limit, offset)
                )
                rows = cur.fetchall()
        except Exception as e:
            print("Ошибка пагинации:", e)
            # ИСПРАВЛЕНИЕ: НЕ вызываем conn.close() здесь —
            # блок finally выполнится автоматически после return
            return
        finally:
            # finally выполняется ВСЕГДА: и при нормальном выходе, и при return в except
            conn.close()

        print(f"\n--- Страница (offset={offset}) ---")
        if not rows:
            print("  Больше нет контактов.")
        else:
            print_rows(rows)

        print("  [n] Следующая  [p] Предыдущая  [q] Выход")
        choice = input("  Выбор: ").strip().lower()

        if choice == "n":
            if rows:
                offset += limit
            else:
                print("  Вы уже на последней странице.")
        elif choice == "p":
            offset = max(0, offset - limit)  # не уходим в отрицательный offset
        elif choice == "q":
            break


# УДАЛЕНИЕ КОНТАКТА

def delete_contact(username):
    """
    Удаляет контакт по username.
    Связанные телефоны удаляются автоматически через ON DELETE CASCADE в schema.sql.
    """
    conn = connect()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM contacts WHERE username = %s", (username,))
            if cur.rowcount == 0:
                print("Контакт не найден.")
            else:
                print(f"Контакт '{username}' удалён.")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Ошибка при удалении:", e)
    finally:
        conn.close()


# КРИТЕРИЙ 3.3 — ЭКСПОРТ В JSON

def export_to_json(filename="contacts.json"):
    """
    Экспортирует все контакты в JSON-файл.
    Для каждого контакта отдельным запросом подгружаются его телефоны из таблицы phones.
    birthday приводится к строке через ::TEXT чтобы JSON мог его сериализовать.
    """
    conn = connect()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            # Получаем все контакты вместе с названием группы
            cur.execute("""
                SELECT c.username, c.email, c.birthday::TEXT, g.name AS grp
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
            """)
            contacts = cur.fetchall()

            result = []
            for (username, email, birthday, grp) in contacts:
                # Для каждого контакта получаем список его телефонов
                cur.execute("""
                    SELECT p.phone, p.type
                    FROM phones p
                    JOIN contacts c ON c.id = p.contact_id
                    WHERE c.username = %s
                """, (username,))
                phones = [{"phone": ph, "type": tp} for ph, tp in cur.fetchall()]

                result.append({
                    "username": username,
                    "email": email,
                    "birthday": birthday,
                    "group": grp,
                    "phones": phones
                })

        # Записываем в файл с отступами для читаемости
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Экспортировано {len(result)} контактов в '{filename}'.")
    except Exception as e:
        print("Ошибка при экспорте:", e)
    finally:
        conn.close()


# КРИТЕРИЙ 3.3 — ИМПОРТ ИЗ JSON (с обработкой дубликатов)

def import_from_json(filename="contacts.json"):
    """
    Импортирует контакты из JSON-файла.
    При дубликате (same username) спрашивает пользователя: пропустить или перезаписать.
    Каждый контакт коммитится отдельно — чтобы ошибка одного не отменяла остальных.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("Ошибка чтения файла:", e)
        return

    conn = connect()
    if not conn:
        return

    try:
        for item in data:
            username = item.get("username")
            email    = item.get("email")
            birthday = item.get("birthday")
            grp      = item.get("group")
            phones   = item.get("phones", [])

            with conn.cursor() as cur:
                # Проверяем существование контакта
                cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
                existing = cur.fetchone()

                if existing:
                    choice = input(
                        f"Контакт '{username}' уже существует. Перезаписать? (y/n): "
                    ).strip().lower()
                    if choice != "y":
                        print(f"  Пропущен '{username}'.")
                        continue
                    else:
                        # Удаляем старый (телефоны удалятся каскадно)
                        cur.execute("DELETE FROM contacts WHERE username = %s", (username,))

                # Находим group_id
                group_id = None
                if grp:
                    cur.execute("SELECT id FROM groups WHERE name = %s", (grp,))
                    row = cur.fetchone()
                    if row:
                        group_id = row[0]

                # Вставляем контакт
                cur.execute("""
                    INSERT INTO contacts (username, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (username, email, birthday, group_id))
                contact_id = cur.fetchone()[0]

                # Вставляем телефоны
                for p in phones:
                    cur.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s)
                    """, (contact_id, p.get("phone"), p.get("type")))

            conn.commit()
            print(f"  Импортирован '{username}'.")

    except Exception as e:
        conn.rollback()
        print("Ошибка при импорте:", e)
    finally:
        conn.close()


# КРИТЕРИЙ 3.3 — РАСШИРЕННЫЙ CSV ИМПОРТ

def import_from_csv(filename="contacts.csv"):
    """
    Импортирует контакты из CSV с расширенными полями:
      username, email, birthday, group, phone, phone_type

    Контакт вставляется через UPSERT (ON CONFLICT DO UPDATE).
    Телефон добавляется только если такого номера ещё нет у этого контакта —
    ИСПРАВЛЕНО: убрано дублирование телефонов при повторном запуске импорта.
    """
    conn = connect()
    if not conn:
        return
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            with conn.cursor() as cur:
                for row in reader:
                    username   = row.get("username", "").strip()
                    email      = row.get("email", "").strip() or None
                    birthday   = row.get("birthday", "").strip() or None
                    grp        = row.get("group", "").strip() or None
                    phone      = row.get("phone", "").strip() or None
                    phone_type = row.get("phone_type", "mobile").strip()

                    if not username:
                        continue  # пропускаем пустые строки

                    # Находим group_id по названию
                    group_id = None
                    if grp:
                        cur.execute("SELECT id FROM groups WHERE name = %s", (grp,))
                        r = cur.fetchone()
                        if r:
                            group_id = r[0]

                    # UPSERT контакта: обновляем email/birthday/group если уже существует
                    cur.execute("""
                        INSERT INTO contacts (username, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (username)
                        DO UPDATE SET
                            email    = EXCLUDED.email,
                            birthday = EXCLUDED.birthday,
                            group_id = EXCLUDED.group_id
                        RETURNING id
                    """, (username, email, birthday, group_id))
                    contact_id = cur.fetchone()[0]

                    # ИСПРАВЛЕНИЕ: проверяем, не существует ли уже такой телефон
                    # чтобы избежать дублирования при повторном запуске CSV-импорта
                    if phone:
                        cur.execute(
                            "SELECT 1 FROM phones WHERE contact_id = %s AND phone = %s",
                            (contact_id, phone)
                        )
                        if not cur.fetchone():
                            cur.execute("""
                                INSERT INTO phones (contact_id, phone, type)
                                VALUES (%s, %s, %s)
                            """, (contact_id, phone, phone_type))

            conn.commit()
        print(f"CSV '{filename}' успешно импортирован.")
    except Exception as e:
        conn.rollback()
        print("Ошибка при импорте CSV:", e)
    finally:
        conn.close()


# ГЛАВНОЕ МЕНЮ

def menu():
    """
    Консольное меню приложения.
    При старте: создаёт таблицы (schema.sql) и загружает процедуры (procedures.sql).
    """
    print("Инициализация...")
    setup_schema()        # создать таблицы если не существуют
    run_sql_file("procedures.sql")  # загрузить/обновить хранимые процедуры

    while True:
        print("\n===== PHONEBOOK =====")
        print("1.  Добавить контакт")
        print("2.  Добавить телефон к контакту")
        print("3.  Переместить контакт в группу")
        print("4.  Поиск (имя / email / телефон)")
        print("5.  Фильтр по группе")
        print("6.  Поиск по email")
        print("7.  Показать все контакты")
        print("8.  Листать страницы")
        print("9.  Удалить контакт")
        print("10. Экспорт в JSON")
        print("11. Импорт из JSON")
        print("12. Импорт из CSV")
        print("0.  Выход")

        choice = input("\nВыбор: ").strip()

        if choice == "1":
            username   = input("Username: ").strip()
            email      = input("Email (необязательно): ").strip() or None
            birthday   = input("День рождения ГГГГ-ММ-ДД (необязательно): ").strip() or None
            group_name = input("Группа (Family/Work/Friend/Other): ").strip() or None
            add_contact(username, email, birthday, group_name)

        elif choice == "2":
            name  = input("Username контакта: ").strip()
            phone = input("Телефон: ").strip()

            # ИСПРАВЛЕНИЕ: валидация типа телефона до вызова процедуры.
            # Если ввести 'cell' вместо 'mobile' — БД выбросит ошибку CHECK constraint.
            # Теперь пользователь получает понятное сообщение сразу.
            ptype = input("Тип (home/work/mobile): ").strip().lower()
            if ptype not in ("home", "work", "mobile"):
                print("Ошибка: тип должен быть home, work или mobile.")
            else:
                add_phone(name, phone, ptype)

        elif choice == "3":
            name  = input("Username контакта: ").strip()
            group = input("Название группы: ").strip()
            move_to_group(name, group)

        elif choice == "4":
            query = input("Поисковый запрос: ").strip()
            search_contacts(query)

        elif choice == "5":
            group = input("Название группы: ").strip()
            filter_by_group(group)

        elif choice == "6":
            pattern = input("Часть email: ").strip()
            search_by_email(pattern)

        elif choice == "7":
            print("Сортировать по: 1) username  2) birthday  3) created_at")
            s = input("Выбор: ").strip()
            sort_map = {"1": "username", "2": "birthday", "3": "created_at"}
            sort_by = sort_map.get(s, "username")
            show_all_contacts(sort_by)

        elif choice == "8":
            paginated_navigation()

        elif choice == "9":
            username = input("Username для удаления: ").strip()
            delete_contact(username)

        elif choice == "10":
            fname = input("Имя файла (по умолч. contacts.json): ").strip() or "contacts.json"
            export_to_json(fname)

        elif choice == "11":
            fname = input("Имя файла (по умолч. contacts.json): ").strip() or "contacts.json"
            import_from_json(fname)

        elif choice == "12":
            fname = input("CSV файл (по умолч. contacts.csv): ").strip() or "contacts.csv"
            import_from_csv(fname)

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    menu()
