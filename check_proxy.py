# -*- coding: utf-8 -*-
import string
import random
import concurrent
import threading
import itertools
import time
import sys
import os
import sys
from time import sleep
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    ban = r'''
   
░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░░▒▓████████▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░    ░▒▓██▓▒░  
   ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░   ░▒▓██▓▒░    
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██▓▒░      
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ 
                                                                                                               
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
# ===================== CHẠY GET KEY TRƯỚC =====================
if __name__ == "__main__":
    main()
print("Dev:KhanhZ9(TangHuchi)")

# ====================== TOOL CHECK PROXY LIVE - PHIÊN BẢN KỸ + NHANH =====================
from concurrent.futures import ThreadPoolExecutor, as_completed

# ====================== CẤU HÌNH ======================
OUTPUT_FILE = "live_proxies.txt"
TIMEOUT = 18
MAX_WORKERS = 70
TEST_URLS = [
    "http://httpbin.org/ip",
    "https://httpbin.org/ip"
]
RETRIES = 2
# =====================================================

def check_proxy(proxy):
    for attempt in range(RETRIES + 1):
        for url in TEST_URLS:
            start = time.time()
            try:
                proxies_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
                r = requests.get(url, proxies=proxies_dict, timeout=TIMEOUT, allow_redirects=True)
                
                if r.status_code in [200, 302]:
                    latency = round((time.time() - start) * 1000)
                    return proxy, True, latency
            except:
                pass
        if attempt < RETRIES:
            time.sleep(1)  # chờ nhẹ trước khi retry
    
    return proxy, False, None

def proxy_main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Tool Check Proxy Live - Kỹ Càng & Nhanh\n")
    
    while True:
        print("📁 Nhập tên file proxy (.txt) - phải nằm cùng thư mục:")
        input_file = input("> ").strip()
        if not input_file.lower().endswith(".txt"):
            input_file += ".txt"
        if os.path.exists(input_file):
            print(f"✅ Tìm thấy file: {input_file}")
            break
        else:
            print(f"❌ Không tìm thấy file '{input_file}' ! Hãy kiểm tra lại.\n")

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except Exception as e:
        print(f"❌ Lỗi đọc file: {e}")
        return

    print(f"📋 Tổng proxy cần check: {len(proxies)}\n")
    
    live_proxies = []
    total_start = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_proxy = {executor.submit(check_proxy, p): p for p in proxies}
        
        for i, future in enumerate(as_completed(future_to_proxy), 1):
            proxy, is_live, latency = future.result()
            status = "✅ LIVE" if is_live else "❌ DIE"
            speed = f"{latency}ms" if is_live else "—"
            
            print(f"[{i:3d}/{len(proxies)}] {status} {speed:>7} → {proxy}")
            
            if is_live:
                live_proxies.append(f"{proxy} | {latency}ms")

    if live_proxies:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for line in live_proxies:
                f.write(line + "\n")
        print(f"\n🎉 HOÀN THÀNH!")
        print(f"✅ Live: {len(live_proxies)}/{len(proxies)} proxy")
        print(f"📁 Đã lưu vào: {OUTPUT_FILE} (có kèm latency)")
    else:
        print("\n😢 Không có proxy live nào!")

    total_time = round(time.time() - total_start, 2)
    print(f"⏱️  Tổng thời gian: {total_time} giây")

# ====================== CHẠY TOOL PROXY =====================
proxy_main()
