#!/usr/bin/env python3
# mail_parser.py - Извлечение email из любого текстового файла через regex

import re

# Универсальный regex для email:
# - локальная часть: буквы, цифры, . _ % + -
# - домен: буквы, цифры, . -
# - TLD: минимум 2 буквы
EMAIL_REGEX = re.compile(
    r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
)

def extract_emails_from_file(file_path):
    """
    Извлекает все email из любого текстового файла через regex.
    Возвращает отсортированный список уникальных email в нижнем регистре.
    """
    emails = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Файл '{file_path}' не найден")
        return None
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")
        return None
    
    for match in EMAIL_REGEX.findall(content):
        emails.add(match.strip().lower())
    
    return sorted(emails)
