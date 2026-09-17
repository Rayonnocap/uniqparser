#!/usr/bin/env python3
# bh_parser.py - Парсинг JSON-файлов BloodHound (поиск "name":"имя")

import re

def extract_users_from_bh_json(json_file):
    """
    Извлекает имена пользователей из JSON-файла BloodHound
    Ищет все вхождения "name":"имя_пользователя" и извлекает имя
    """
    users = set()
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ищем все вхождения "name":"что-то"
        # Учитываем, что могут быть пробелы: "name" : "имя"
        pattern = r'"name"\s*:\s*"([^"]+)"'
        matches = re.findall(pattern, content)
        
        for match in matches:
            # Если имя содержит @ (user@domain), берем часть до @
            if '@' in match:
                match = match.split('@')[0]
            users.add(match.strip())
        
        return sorted(users)
    
    except FileNotFoundError:
        print(f"❌ Файл '{json_file}' не найден")
        return None
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")
        return None
