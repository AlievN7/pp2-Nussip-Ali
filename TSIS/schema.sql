-- ТАБЛИЦА ГРУПП 
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Стандартные группы. ON CONFLICT DO NOTHING — не падает при повторном запуске.
INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
-- Если такая запись уже существует то пропускает
ON CONFLICT DO NOTHING;


-- ТАБЛИЦА КОНТАКТОВ
-- Если таблица уже существует CREATE пропускается
CREATE TABLE IF NOT EXISTS contacts (
    id         SERIAL PRIMARY KEY,
    username   VARCHAR(100) NOT NULL UNIQUE,
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Если UNIQUE ограничение на username отсутствует добавляем его.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conrelid = 'contacts'::regclass AND contype = 'u' AND conkey = ARRAY(
              SELECT attnum FROM pg_attribute
              WHERE attrelid = 'contacts'::regclass AND attname = 'username'
          )
    ) THEN
        ALTER TABLE contacts ADD CONSTRAINT contacts_username_key UNIQUE (username);
    END IF;
END $$;

-- 'name' вместо 'username'.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'contacts' AND column_name = 'name'
    ) THEN
        ALTER TABLE contacts RENAME COLUMN name TO username;
    END IF;
END $$;

-- добавляем новые поля к существующей таблице contacts.
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email      VARCHAR(100);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS birthday   DATE;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS group_id   INTEGER REFERENCES groups(id);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();


-- ТАБЛИЦА ТЕЛЕФОНОВ
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);