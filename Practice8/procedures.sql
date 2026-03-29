--вставка, обновление
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

--Bulk insert и провепрка
CREATE OR REPLACE PROCEDURE bulk_upsert_contacts(users TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    u TEXT;
    name_part TEXT;
    phone_part TEXT;
BEGIN
    FOREACH u IN ARRAY users LOOP
        name_part := split_part(u, ',', 1);
        phone_part := split_part(u, ',', 2);

        --проверка телефона
        IF phone_part ~ '^[0-9\-]+$' THEN
            CALL upsert_contact(name_part, phone_part);
        ELSE
            RAISE NOTICE 'Invalid phone for %: %', name_part, phone_part;
        END IF;
    END LOOP;
END;
$$;

--Удаление,имя или телефон
CREATE OR REPLACE PROCEDURE delete_contact(p_name VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE (p_name IS NOT NULL AND name = p_name)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;