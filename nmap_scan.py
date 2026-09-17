#!/usr/bin/env python3
# nmap_scan.py - Nmap сканирование

import subprocess
import re

def scan_ip_with_nmap(ip, max_rate=1000):
    """
    Сканирует один IP через nmap -sn (ping scan)
    Возвращает True если хост жив, False если нет
    """
    try:
        cmd = ['nmap', '--max-rate', str(max_rate), '-n', '-sn', ip]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        # Nmap выводит "Host is up" в stdout если хост жив
        if "Host is up" in result.stdout:
            return True
        return False
    except subprocess.TimeoutExpired:
        print(f"⏰ Таймаут при сканировании {ip}")
        return False
    except Exception as e:
        print(f"❌ Ошибка при сканировании {ip}: {e}")
        return False

def scan_ips_with_nmap(ip_list, max_rate=1000, output_file=None):
    """
    Сканирует список IP через nmap
    Возвращает список живых хостов
    """
    alive_hosts = []
    total = len(ip_list)
    
    print(f"\n🔍 Запуск Nmap ping scan для {total} IP-адресов...\n")
    
    for idx, ip in enumerate(ip_list, 1):
        print(f"  [{idx}/{total}] Сканирую {ip}...", end=' ')
        if scan_ip_with_nmap(ip, max_rate):
            print("✅ ЖИВ")
            alive_hosts.append(ip)
        else:
            print("❌ Нет ответа")
    
    return alive_hosts
