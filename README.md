# UNIQPARSER

This tool you can use for parsing some kind of files to get users/emails list (and get IP`s from any file)
 
OS Version: Linux, Win, MacOS Requirements: Python 3.14.6

---

## Installation steps

### Clone this repo:
```
git clone https://github.com/Rayonnocap/uniqparser.git
cd uniqparser
```

### Usage

_Hint: Use -h flag to see /help option_
```
python3 uniqparser -h
```

---

<img width="1100" height="588" alt="изображение" src="https://github.com/user-attachments/assets/69a37774-4d05-4754-8578-a35a18b71c35" />

---
### Usage examples

Parsing **ANY type of files contains Email** addresses with output option:
```
python3 uniqparser.py --mail ~/path/to/raw_file_with_emails --mail-output ~/path/to/output_file
```

Parsing **BLOODHOUND JSON** file to get users:
```
python3 uniqparser.py --bh-json ~/path/to/users.json --bh-output ~/path/to/output_file       
```

Parsing **ANY type of files contains Email addresses sorting ONLY @EXAMPLE.DOMAIN.COM** option
```
python3 uniqparser.py --mail ~/path/to/raw_file_with_emails --mail-end domain.com --mail-output ~/path/to/output_file  
```

---

**Sorting** only **UNIQUE IP-addresses** with -f -s -o flags
```
python3 uniqparser.py -f ~/path/to/file -s -o ~/path/to/output 
```

**Sorting** and **ping-SCANNING** only **UNIQUE IP-addresses** with -f -s -o flags to get IP list you can access
```
python3 uniqparser.py -f ~/path/to/file -s -o --nmap ~/path/to/output 
```

---

P.S ts is vibecoded

**[by Ultimate Lizzard]**
