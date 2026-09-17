#!/usr/bin/env python3
# core.py - Основная логика (чтение IP)

import re

def read_unique_ips(filename):
    """Читает IP-адреса из файла и возвращает множество уникальных"""
    unique_ips = set()
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
                for ip in ips:
                    unique_ips.add(ip)
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл '{filename}' не найден")
        return None
    except PermissionError:
        print(f"❌ Ошибка: Нет прав на чтение файла '{filename}'")
        return None
    
    return unique_ips
