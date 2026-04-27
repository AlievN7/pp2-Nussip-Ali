
-- add_phone
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
AS $$
DECLARE
    v_contact_id INT;  -- переменная для хранения найденного id
BEGIN
    -- ищем контакт по имени
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE username = p_contact_name;

    -- если SELECT ничего не нашёл, SELECT INTO оставит переменную NULL
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Контакт % не найден', p_contact_name;
    END IF;

    -- вставляем телефон
    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$ LANGUAGE plpgsql;


-- move_to_group
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
AS $$
DECLARE
    v_group_id INT;  -- id группы. если такой нет то создаем новую
BEGIN
    -- ищем группу по названию
    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    -- если группы нет создаём и получаем её id через RETURNING
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name)
        VALUES (p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    -- обновляем контакт
    UPDATE contacts
    SET group_id = v_group_id
    WHERE username = p_contact_name;

    -- NOT FOUND истина если UPDATE не затронул ни одной строки
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Контакт % не найден', p_contact_name;
    END IF;
END;
$$ LANGUAGE plpgsql;


-- search_contacts
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id       INT,
    username VARCHAR,
    email    VARCHAR,
    birthday DATE,
    phone    VARCHAR,
    type     VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.username,
        c.email,
        c.birthday,
        p.phone,
        p.type
    FROM contacts c
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.username ILIKE '%' || p_query || '%'   -- поиск по имени
       OR c.email    ILIKE '%' || p_query || '%'   -- поиск по email
       OR p.phone    ILIKE '%' || p_query || '%';  -- поиск по телефону
END;
$$ LANGUAGE plpgsql;


-- get_contacts_paginated
DROP FUNCTION IF EXISTS get_contacts_paginated(integer, integer);


-- продолжение
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(
    id       INT,
    username VARCHAR,
    email    VARCHAR,
    birthday DATE,
    grp      VARCHAR   -- название группы 
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.username,
        c.email,
        c.birthday,
        g.name           -- название группы из JOIN
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    ORDER BY c.id        -- стабильный порядок для корректной пагинации
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
