import string
import random
import concurrent.futures
import threading
import itertools
import time
import sys
import os
import requests
import json
from datetime import datetime, timedelta
from time import sleep
import base64

# ===================== BANNER =====================
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

# ===================== KEY SYSTEM =====================
def encrypt_data(data: str) -> str:
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")

def decrypt_data(data: str) -> str:
    return base64.b64decode(data.encode("utf-8")).decode("utf-8")

def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return None

def display_ip_address(ip_address):
    banner()
    if ip_address:
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;31mĐịa chỉ IP : {ip_address}")
    else:
        print("Không thể lấy địa chỉ IP của thiết bị.")

def luu_thong_tin_ip(ip, key, expiration_date):
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    with open('ip_key.json', 'w') as file:
        file.write(encrypt_data(json.dumps(data)))

def tai_thong_tin_ip():
    try:
        with open('ip_key.json', 'r') as file:
            return json.loads(decrypt_data(file.read()))
    except:
        return None

def kiem_tra_ip(ip):
    data = tai_thong_tin_ip()
    if data and ip in data:
        try:
            expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
            if expiration_date > datetime.now():
                return data[ip]['key']
        except:
            pass
    return None

def generate_key_and_url(ip_address):
    ngay = datetime.now().day
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'HECTORVN{key1}{ip_numbers}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://deltagetkey.blogspot.com/2026/02/get-key.html?ma={key}'
    return url, key, expiration_date

def get_shortened_link_phu(url):
    try:
        token = "6989d7bcd70a74263103abab"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"
        response = requests.get(api_url, timeout=8)
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "message": "Không thể kết nối dịch vụ rút gọn."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi rút gọn URL: {e}"}

# ===================== PROXY SCANNER =====================
def getls():
    urls = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    ]
    proxy_list = []
    session = requests.Session()
    for url in urls:
        try:
            r = session.get(url, timeout=10)
            if r.status_code == 200:
                proxy_list.extend(r.text.splitlines())
        except:
            pass
    return list(set(proxy_list))

def check_proxy(proxy):
    try:
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        r = requests.get("http://www.google.com", proxies=proxies, timeout=3)
        return proxy if r.status_code == 200 else None
    except:
        return None

# ===================== MAIN =====================
def main():
    ip_address = get_ip_address()
    display_ip_address(ip_address)

    if not ip_address:
        print("\033[1;31mKhông lấy được IP, thoát tool!")
        sys.exit()

    existing_key = kiem_tra_ip(ip_address)
    if existing_key:
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;35mTool còn hạn, mời bạn dùng tool...")
        sleep(2)
    else:
        if datetime.now().hour >= 23 and datetime.now().minute >= 59:  # đơn giản hóa
            print("\033[1;33mĐã quá giờ sử dụng tool hôm nay !!!")
            sys.exit()

        url, key, expiration_date = generate_key_and_url(ip_address)

        print("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;32mNhập 1 Để Lấy Key \033[1;33m(Free)")
        while True:
            choice = input("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;34mNhập lựa chọn: ")
            print("\033[97m════════════════════════════════════════════════")
            if choice == "1":
                print("Đang tạo link lấy key...")
                yeumoney_data = get_shortened_link_phu(url)
                if yeumoney_data.get('status') == "error":
                    print(yeumoney_data.get('message'))
                    sys.exit()

                link_key = yeumoney_data.get('shortenedUrl')
                print(f'\033[1;35mLink Để Vượt Key: {link_key}')

                while True:
                    keynhap = input('\033[1;33mKey Đã Vượt Là: ')
                    ADMIN_KEY = "hectoradminskibidi123"

                    if keynhap == key or keynhap == ADMIN_KEY:
                        print('\033[1;32mKey Đúng! Mời bạn dùng Tool')
                        sleep(2)
                        luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                        break
                    else:
                        print(f'Key Sai! Vui lòng vượt lại: {link_key}')
                break  # Thoát vòng lặp lấy key

    # ===================== BẮT ĐẦU SCAN PROXY =====================
    print("\n\033[1;36mĐang lấy danh sách proxy...\033[0m")
    proxy_list = getls()
    total = len(proxy_list)
    print(f"\033[1;97mTổng proxy lấy được: \033[1;33m{total}\033[0m")

    live_proxies = []
    start_time = time.time()
    checked = 0

    chibi_frames = ["(≧◡≦)", "(≧◡≦)ゞ", "(≧◡≦)ﾉ", "(≧◡≦)…", "(≧◡≦)💦", "(≧◡≦)✨"]
    spinner = itertools.cycle(chibi_frames)
    print_lock = threading.Lock()

    def worker(proxy):
        nonlocal checked
        result = check_proxy(proxy)

        with print_lock:
            checked += 1
            elapsed = time.time() - start_time
            avg_time = elapsed / checked if checked > 0 else 0
            remaining = (total - checked) * avg_time
            mins, secs = divmod(int(remaining), 60)

            chibi = next(spinner)
            print(
                f"\r{chibi} Đã scan {checked}/{total} proxy | Còn lại: {mins:02d}:{secs:02d}",
                end="", flush=True
            )
        return result

    print("\n\033[1;32mBắt đầu kiểm tra proxy...\033[0m")
    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
        results = executor.map(worker, proxy_list)
        for proxy in results:
            if proxy:
                live_proxies.append(proxy)

    # Lưu file
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"live_{timestamp}_{random_str}.txt"

    with open(file_name, "w", encoding="utf-8") as f:
        for proxy in live_proxies:
            f.write(proxy + "\n")

    print(f"\n\n\033[1;32m✓ Hoàn thành! {len(live_proxies)} proxy live đã được lưu vào file: \033[1;33m{file_name}\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[1;31mTool đã bị dừng bởi người dùng.\033[0m")
    except Exception as e:
        print(f"\n\033[1;31mLỗi không mong muốn: {e}\033[0m")
    finally:
        print("\n\033[1;35mDev: KhanhZ9 (TangHuchi)\033[0m")
