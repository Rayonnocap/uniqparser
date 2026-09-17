#!/usr/bin/env python3
# main.py - Точка входа

import argparse
import sys
from banner import print_banner
from core import read_unique_ips
from nmap_scan import scan_ips_with_nmap
from bh_parser import extract_users_from_bh_json
from email_parser import extract_emails_from_json
from mail_parser import extract_emails_from_file

def main():
    # Печатаем баннер
    print_banner()
    
    # Настройка парсера аргументов
    parser = argparse.ArgumentParser(
        description='Утилита для работы с IP-адресами и BloodHound данными',
        usage='python3 uniqparser.py -f /path/to/file'
    )
    
    parser.add_argument('-f', '--file', 
                        help='Путь к файлу с IP-адресами')
    
    parser.add_argument('-s', '--sort', 
                        action='store_true', 
                        help='Сортировать IP-адреса по возрастанию')
    
    parser.add_argument('-o', '--output', 
                        help='Сохранить результат в указанный файл')
    
    parser.add_argument('--nmap', 
                        action='store_true',
                        help='Запустить Nmap ping scan для всех IP (определить живые хосты)')
    
    parser.add_argument('--max-rate', 
                        type=int,
                        default=1000,
                        help='Максимальная скорость Nmap (пакетов/сек), по умолчанию 1000')
    
    parser.add_argument('--bh-json', 
                        metavar='FILE',
                        help='Извлечь имена пользователей из JSON-файла BloodHound (укажите путь к .json)')
    
    parser.add_argument('--bh-output',
                        metavar='FILE',
                        help='Сохранить список пользователей в файл')
    parser.add_argument('--email-json',
                        metavar='FILE',
                        nargs='+',
                        help='Извлечь email из JSON-файла(ов) Hunter.io / DeHashed (можно указать несколько файлов через пробел)')
    
    parser.add_argument('--email-output',
                        metavar='FILE',
                        help='Сохранить список email в файл')

    parser.add_argument('--mail',
                        metavar='FILE',
                        nargs='+',
                        help='Извлечь email из любого файла(ов) через regex (можно указать несколько файлов)')
    
    parser.add_argument('--mail-output',
                        metavar='FILE',
                        help='Сохранить список email в файл (для --mail)')

    parser.add_argument('--mail-end',
                        metavar='DOMAIN',
                        nargs='+',
                        help='Фильтр по домену (например: yandex.ru mail.ru). Оставить только email с указанными доменами')

    # Если аргументов нет — показать help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    # --- Режим BloodHound ---
    if args.bh_json:
        users = extract_users_from_bh_json(args.bh_json)
        
        if users is None:
            sys.exit(1)
        
        if not users:
            print("⚠️ Пользователи не найдены в JSON-файле")
            sys.exit(0)
        
        print(f"\n✅ Найдено пользователей: {len(users)}")
        print("\n📋 Список пользователей:")
        print("─" * 40)
        for user in users:
            print(f"{user}")
        print("─" * 40)
        
        if args.bh_output:
            try:
                with open(args.bh_output, 'w') as f:
                    for user in users:
                        f.write(user + '\n')
                print(f"\n💾 Результат сохранён в файл: {args.bh_output}")
            except Exception as e:
                print(f"❌ Ошибка при сохранении: {e}")
        
        return  # <- внутри функции main() это допустимо
        
        
    # --- Режим Mail (regex по любому файлу) ---
    if args.mail:
        all_emails = set()
        
        for file_path in args.mail:
            print(f"📄 Обработка: {file_path}")
            emails = extract_emails_from_file(file_path)
            
            if emails is None:
                continue
            
            if not emails:
                print(f"  ⚠️ Email не найдены в {file_path}")
                continue
            
            print(f"  ✅ Найдено: {len(emails)}")
            all_emails.update(emails)
        
        if not all_emails:
            print("\n⚠️ Email не найдены ни в одном файле")
            sys.exit(0)
        
        # --- Фильтрация по домену (--mail-end) ---
        if args.mail_end:
            # Нормализуем домены: нижний регистр, убираем @ если есть
            domains = set()
            for d in args.mail_end:
                d = d.strip().lower().lstrip('@')
                domains.add(d)
            
            filtered = set()
            for email in all_emails:
                # Берём домен после @
                if '@' in email:
                    email_domain = email.rsplit('@', 1)[1]
                    if email_domain in domains:
                        filtered.add(email)
            
            print(f"\n🔍 Фильтр по доменам: {', '.join(sorted(domains))}")
            print(f"   До фильтрации: {len(all_emails)}")
            print(f"   После фильтрации: {len(filtered)}")
            
            all_emails = filtered
            
            if not all_emails:
                print("\n⚠️ После фильтрации не осталось ни одного email")
                sys.exit(0)
        
        sorted_emails = sorted(all_emails)
        
        print(f"\n✅ Всего уникальных email: {len(sorted_emails)}")
        print("\n📧 Список email:")
        print("─" * 40)
        for email in sorted_emails:
            print(f"{email}")
        print("─" * 40)
        
        if args.mail_output:
            try:
                with open(args.mail_output, 'w') as f:
                    for email in sorted_emails:
                        f.write(email + '\n')
                print(f"\n💾 Результат сохранён в файл: {args.mail_output}")
            except Exception as e:
                print(f"❌ Ошибка при сохранении: {e}")
        
        return
    
    # --- Режим Email (Hunter.io / DeHashed) ---
    if args.email_json:
        all_emails = set()
        
        for json_file in args.email_json:
            print(f"📄 Обработка: {json_file}")
            emails = extract_emails_from_json(json_file)
            
            if emails is None:
                continue
            
            if not emails:
                print(f"  ⚠️ Email не найдены в {json_file}")
                continue
            
            print(f"  ✅ Найдено: {len(emails)}")
            all_emails.update(emails)
        
        if not all_emails:
            print("\n⚠️ Email не найдены ни в одном файле")
            sys.exit(0)
        
        sorted_emails = sorted(all_emails)
        
        print(f"\n✅ Всего уникальных email: {len(sorted_emails)}")
        print("\n📧 Список email:")
        print("─" * 40)
        for email in sorted_emails:
            print(f"{email}")
        print("─" * 40)
        
        if args.email_output:
            try:
                with open(args.email_output, 'w') as f:
                    for email in sorted_emails:
                        f.write(email + '\n')
                print(f"\n💾 Результат сохранён в файл: {args.email_output}")
            except Exception as e:
                print(f"❌ Ошибка при сохранении: {e}")
        
        return
    
    # --- Режим IP (без BloodHound) ---
    if not args.file:
        print("Укажите файл с IP-адресами через -f или используйте --bh-json / --email-json / --mail")
        sys.exit(1)
    
    # Читаем уникальные IP
    unique_ips = read_unique_ips(args.file)
    
    if unique_ips is None:
        sys.exit(1)
    
    if not unique_ips:
        print("⚠️ Файл пуст или не содержит IP-адресов")
        sys.exit(0)
    
    # Сортируем IP
    sorted_ips = sorted(unique_ips, key=lambda ip: tuple(map(int, ip.split('.'))))
    
    # --- Режим Nmap ---
    if args.nmap:
        alive_hosts = scan_ips_with_nmap(sorted_ips, args.max_rate)
        
        print(f"\n📊 Результаты Nmap сканирования:")
        print("─" * 40)
        print(f"  Всего IP: {len(sorted_ips)}")
        print(f"  Живых хостов: {len(alive_hosts)}")
        print("─" * 40)
        
        if alive_hosts:
            print("\n✅ Живые хосты:")
            for ip in alive_hosts:
                print(f"{ip}")
        else:
            print("\n❌ Живых хостов не найдено.")
        
        if args.output:
            try:
                with open(args.output, 'w') as f:
                    for ip in alive_hosts:
                        f.write(ip + '\n')
                print(f"\n💾 Результат сохранён в файл: {args.output}")
            except Exception as e:
                print(f"❌ Ошибка при сохранении: {e}")
        
        return  # внутри функции
    
    # --- Обычный режим (без Nmap) ---
    print(f"✅ Найдено уникальных IP-адресов: {len(sorted_ips)}")
    print("\n📋 Список уникальных IP-адресов:")
    print("─" * 40)
    for ip in sorted_ips:
        print(f"{ip}")
    print("─" * 40)
    
    if args.output:
        try:
            with open(args.output, 'w') as f:
                for ip in sorted_ips:
                    f.write(ip + '\n')
            print(f"\n💾 Результат сохранён в файл: {args.output}")
        except Exception as e:
            print(f"❌ Ошибка при сохранении файла: {e}")

if __name__ == "__main__":
    main()
