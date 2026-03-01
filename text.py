import os
import sys
import asyncio
import aiohttp
import time
import statistics
from time import sleep
from colorama import Fore, init

init(autoreset=True)

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')

    ban = r'''
                                                                           ,--.        
      ,--.'|                       ___                                         ,--.'|        
   ,--,  | :                     ,--.'|_                           ,---.   ,--,:  : |        
,---.'|  : '                     |  | :,'   ,---.    __  ,-.      /__./|,`--.'`|  ' :        
|   | : _' |                     :  : ' :  '   ,'\ ,' ,'/ /| ,---.;  ; ||   :  :  | |        
:   : |.'  |   ,---.     ,---. .;__,'  /  /   /   |'  | |' |/___/ \  | |:   |   \ | :        
|   ' '  ; :  /     \   /     \|  |   |  .   ; ,. :|  |   ,'\   ;  \ ' ||   : '  '; |        
'   |  .'. | /    /  | /    / ':__,'| :  '   | |: :'  :  /   \   \  \: |'   ' ;.    ;        
|   | :  | '.    ' / |.    ' /   '  : |__'   | .; :|  | '     ;   \  ' .|   | | \   |        
'   : |  : ;'   ;   /|'   ; :__  |  | '.'|   :    |;  : |      \   \   ''   : |  ; .'        
|   | '  ,/ '   |  / |'   | '.'| ;  :    ;\   \  / |  , ;       \   `  ;|   | '`--'          
;   : ;--'  |   :    ||   :    : |  ,   /  `----'   ---'         :   \ |'   : |              
|   ,/       \   \  /  \   \  /   ---`-'                          '---" ;   |.'              
'---'         `----'    `----'                                          '---'      
'''

    for char in ban:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.005)  

import requests, json, time, sys
from datetime import datetime, timedelta
from time import sleep
from concurrent.futures import ThreadPoolExecutor

# ===================== GET KEY - GIỮ NGUYÊN =====================
import base64

def encrypt_data(data: str) -> str:
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")

def decrypt_data(data: str) -> str:
    return base64.b64decode(data.encode("utf-8")).decode("utf-8")
def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        ip_address = ip_data['ip']
        return ip_address
    except Exception as e:
        print(f"Lỗi khi lấy địa chỉ IP: {e}")
        return None

def display_ip_address(ip_address):
    if ip_address:
        banner()
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;31mĐịa chỉ IP : {ip_address}")
    else:
        print("Không thể lấy địa chỉ IP của thiết bị.")

def luu_thong_tin_ip(ip, key, expiration_date):
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))

    with open('ip_key.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        data = json.loads(decrypt_data(encrypted_data))
        return data
    except FileNotFoundError:
        return None

def kiem_tra_ip(ip):
    data = tai_thong_tin_ip()
    if data and ip in data:
        expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
        if expiration_date > datetime.now():
            return data[ip]['key']
    return None

def generate_key_and_url(ip_address):
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'HECTORVN{key1}{ip_numbers}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://deltagetkey.blogspot.com/2026/02/get-key.html?ma={key}'
    return url, key, expiration_date

def da_qua_gio_moi():
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return now >= midnight

def get_shortened_link_phu(url):
    try:
        token = "6989d7bcd70a74263103abab"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"status": "error", "message": "Không thể kết nối đến dịch vụ rút gọn URL."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi rút gọn URL: {e}"}

def main():
    ip_address = get_ip_address()
    display_ip_address(ip_address)

    if ip_address:
        existing_key = kiem_tra_ip(ip_address)
        if existing_key:
            print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;35mTool còn hạn, mời bạn dùng tool...")
            time.sleep(2)
        else:
            if da_qua_gio_moi():
                print("\033[1;33mQuá giờ sử dụng tool !!!")
                sys.exit()

            url, key, expiration_date = generate_key_and_url(ip_address)

            with ThreadPoolExecutor(max_workers=2) as executor:
                print("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;32mNhập 1 Để Lấy Key \033[1;33m( Free )")

                while True:
                    choice = input("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;34mNhập lựa chọn: ")
                    print("\033[97m════════════════════════════════════════════════")
                    if choice == "1":
                        yeumoney_data = executor.submit(get_shortened_link_phu, url).result()
                        if yeumoney_data.get('status') == "error":
                            print(yeumoney_data.get('message'))
                            sys.exit()

                        link_key = yeumoney_data.get('shortenedUrl')
                        print('\033[1;35mLink Để Vượt Key:', link_key)

                        while True:
                            keynhap = input('\033[1;33mKey Đã Vượt Là: ')
                            ADMIN_KEY = "hectoradminskibidi123"

                            if keynhap == key or keynhap == ADMIN_KEY:
                                print('Key Đúng Mời Bạn Dùng Tool')
                                sleep(2)
                                luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                                return
                            else:
                                print('Key Sai, Vượt Lại:', link_key)

# ===================== CÁC HÀM LOAD TEST =====================

def percentile(data, p):
    if not data:
        return 0
    k = (len(data)-1) * (p/100)
    f = int(k)
    c = f + 1
    if c >= len(data):
        return data[f]
    return data[f] + (data[c]-data[f]) * (k-f)


async def worker(name, session, url, rate, results, stop_time):
    interval = 1 / rate

    while time.time() < stop_time:
        start = time.time()

        try:
            async with session.get(url) as r:
                elapsed = time.time() - start
                results["success"] += 1
                results["times"].append(elapsed)

        except asyncio.TimeoutError:
            results["timeout"] += 1
        except aiohttp.ClientError:
            results["connection_error"] += 1

        await asyncio.sleep(interval)


async def monitor(results, start):
    while True:
        await asyncio.sleep(2)
        elapsed = time.time() - start
        total = results["success"] + results["timeout"] + results["connection_error"]

        print(Fore.CYAN +
              f"[LIVE] {elapsed:.1f}s | total={total} | success={results['success']} | timeout={results['timeout']} | conn_err={results['connection_error']}")


async def load_test():

    url = input("[?] URL: ")
    users = int(input("[?] Concurrent users: "))
    rate = float(input("[?] Request / giây mỗi user: "))
    duration = int(input("[?] Test bao nhiêu giây: "))

    timeout = aiohttp.ClientTimeout(total=10)

    results = {
        "success": 0,
        "timeout": 0,
        "connection_error": 0,
        "times": []
    }

    stop_time = time.time() + duration
    start = time.time()

    connector = aiohttp.TCPConnector(limit=users * 2)

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:

        tasks = [
            worker(i, session, url, rate, results, stop_time)
            for i in range(users)
        ]

        tasks.append(monitor(results, start))

        print(Fore.YELLOW + "\n[⚡] Đang test...\n")

        await asyncio.gather(*tasks, return_exceptions=True)

    total = results["success"] + results["timeout"] + results["connection_error"]
    times = sorted(results["times"])

    print(Fore.YELLOW + "\n===== KẾT QUẢ =====")
    print(f"Tổng request: {total}")
    print(f"Success: {results['success']}")
    print(f"Timeout: {results['timeout']}")
    print(f"Connection error: {results['connection_error']}")

    if times:
        print("\n--- LATENCY ---")
        print(f"Min: {min(times):.3f}s")
        print(f"Avg: {statistics.mean(times):.3f}s")
        print(f"P50: {percentile(times,50):.3f}s")
        print(f"P90: {percentile(times,90):.3f}s")
        print(f"P99: {percentile(times,99):.3f}s")
        print(f"Max: {max(times):.3f}s")


# ===================== MAIN RUN =====================

if __name__ == "__main__":
    main()
    asyncio.run(load_test())
