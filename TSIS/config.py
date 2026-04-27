from configparser import ConfigParser

# Загрузка конфигурации из database.ini
def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        for key, value in parser.items(section):
            config[key] = value
    else:
        raise Exception(f"Секция {section} не найдена в {filename}")

    return config


if __name__ == '__main__':
    # проверка
    print(load_config())
