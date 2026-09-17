#!/usr/bin/env python3
# email_parser.py - Парсинг email из JSON-файлов Hunter.io и DeHashed

import re

def extract_emails_from_json(json_file):
    """
    Извлекает email из JSON-файла. Поддерживает два формата:
    
    1. Hunter.io:
       "emails": [{"value": "example@mail.ru", "type": "personal"}, ...]
    
    2. DeHashed:
       "email": ["example@mail.ru", "another@mail.ru"]
    
    Возвращает отсортированный список уникальных email в нижнем регистре.
    """
    emails = set()
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Файл '{json_file}' не найден")
        return None
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")
        return None
    
    # --- Формат 1: Hunter.io ---
    # "emails": [{"value": "example@mail.ru", "type": "personal"}, ...]
    hunter_blocks = re.findall(r'"emails"\s*:\s*\[(.*?)\]', content, re.DOTALL)
    for block in hunter_blocks:
        for value in re.findall(r'"value"\s*:\s*"([^"]+)"', block):
            value = value.strip().lower()
            if '@' in value:
                emails.add(value)
    
    # --- Формат 2: DeHashed ---
    # "email": ["example@mail.ru", "another@mail.ru"]
    dehashed_blocks = re.findall(r'"email"\s*:\s*\[(.*?)\]', content, re.DOTALL)
    for block in dehashed_blocks:
        for value in re.findall(r'"([^"]+)"', block):
            value = value.strip().lower()
            if '@' in value:
                emails.add(value)
    
    # --- Дополнительный fallback: поиск всех email-подобных строк ---
    # На случай, если структура немного другая
    if not emails:
        fallback = re.findall(
            r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
            content
        )
        for value in fallback:
            emails.add(value.strip().lower())
    
    return sorted(emails)
