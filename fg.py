import os
import sys
import json
import base64
import requests
import threading
import time
from datetime import datetime, timedelta
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from colorama import init

# Khởi tạo colorama
init(autoreset=True,convert=True)

# ===================== PHẦN OPENING (ĐÃ FIX LỖI) =====================

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

# ===================== CHẠY GET KEY TRƯỚC =====================

if __name__ == "__main__":
    main()

# ===================== PHẦN CÔNG CỤ (WEB TOOL) =====================

class WebToolPro:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def load_test_pro(self):
        url = input(f"{Fore.CYAN}[?] Nhập URL website của bạn: ")
        num_threads = int(input(f"{Fore.CYAN}[?] Bao nhiêu luồng (threads): "))
        req_per_thread = int(input(f"{Fore.CYAN}[?] Mỗi luồng gửi bao nhiêu request: "))
        
        print(f"{Fore.MAGENTA}\n[*] Đang bắt đầu Load Test mạnh mẽ...\n")
        
        success, fail = 0, 0
        lock = threading.Lock()
        start_time = time.time()

        def worker(tid):
            nonlocal success, fail
            with requests.Session() as session:
                for i in range(req_per_thread):
                    try:
                        r = session.get(url, headers=self.headers, timeout=5)
                        with lock: success += 1
                        print(f"{Fore.GREEN}[Thread {tid}] Req {i+1} OK -> {r.status_code}")
                    except:
                        with lock: fail += 1
                        print(f"{Fore.RED}[Thread {tid}] Req {i+1} FAIL")

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for t in range(num_threads): executor.submit(worker, t + 1)

        print(Fore.YELLOW + f"\n[✅] Xong! Thành công: {success} | Thất bại: {fail} | {round(time.time()-start_time, 2)}s")

# ===================== CHẠY CHƯƠNG TRÌNH =====================

def main():
    # 1. Hiện Banner ngay lập tức
    banner()
    
    # 2. Lấy IP ngầm (không để treo banner)
    print(f"{Fore.WHITE}[*] Đang kiểm tra hệ thống...")
    ip_address = get_ip_address()
    
    if ip_address == "Unknown":
        print(Fore.RED + "[-] Lỗi kết nối mạng!")
        return

    print(f"{Fore.WHITE}[{Fore.RED}<>{Fore.WHITE}] {Fore.RED}Địa chỉ IP : {ip_address}")
    
    # 3. Kiểm tra Key
    existing_key = kiem_tra_ip(ip_address)
    if existing_key:
        print(f"{Fore.MAGENTA}[+] Tool còn hạn. Đang mở Menu...")
        sleep(1)
    else:
        url, key, expiration_date = generate_key_and_url(ip_address)
        print(f"{Fore.GREEN}[1] Lấy Key Free")
        choice = input(f"{Fore.BLUE}[?] Lựa chọn: ")
        
        if choice == "1":
            data = get_shortened_link_phu(url)
            if data.get('status') == "error":
                print(Fore.RED + "[-] Lỗi server key!"); return
            
            print(f"{Fore.MAGENTA}[!] Link Key: {Fore.WHITE}{data.get('shortenedUrl')}")
            
            while True:
                kn = input(f"{Fore.YELLOW}[?] Nhập Key: ")
                if kn == key or kn == "hectoradminskibidi123":
                    print(Fore.GREEN + "[+] Key đúng!"); luu_thong_tin_ip(ip_address, kn, expiration_date)
                    break
                else:
                    print(Fore.RED + "[-] Key sai!")

    # 4. Vào Menu chính
    tool = WebToolPro()
    while True:
        print(f"\n{Fore.WHITE}--- MENU ---")
        print(f"{Fore.CYAN}[1] Load Test Website")
        print(f"{Fore.RED}[0] Thoát")
        c = input(f"{Fore.YELLOW}[?] Chọn: ")
        if c == "1": tool.load_test_pro()
        elif c == "0": break

# ===================== PHẦN LOAD TEST (GIỮ NGUYÊN CLASS) =====================

class WebToolPro:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def check_status(self):
        url = input(f"{Fore.CYAN}[?] Nhập URL: ")
        try:
            r = requests.get(url, headers=self.headers, timeout=5)
            print(f"{Fore.GREEN}[+] {url} → Status: {r.status_code} | Time: {r.elapsed.total_seconds()}s")
        except Exception as e:
            print(f"{Fore.RED}[-] Lỗi: {e}")

    def fast_ping(self):
        host = input(f"{Fore.CYAN}[?] Nhập Host/IP: ")
        param = "-n" if os.name == "nt" else "-c"
        os.system(f"ping {param} 4 {host}")

    def load_test_pro(self):
        url = input(f"{Fore.CYAN}[?] Nhập URL website của bạn: ")
        num_threads = int(input(f"{Fore.CYAN}[?] Bao nhiêu luồng (threads): "))
        req_per_thread = int(input(f"{Fore.CYAN}[?] Mỗi luồng gửi bao nhiêu request: "))
        
        print(f"{Fore.MAGENTA}\n[*] Đang bắt đầu Load Test... Vui lòng đợi.\n")
        
        success, fail = 0, 0
        lock = threading.Lock()
        start_time = time.time()

        def worker(tid):
            nonlocal success, fail
            with requests.Session() as session:
                for i in range(req_per_thread):
                    try:
                        r = session.get(url, headers=self.headers, timeout=5)
                        with lock:
                            success += 1
                        print(f"{Fore.GREEN}[Thread {tid}] Request {i+1}/{req_per_thread} → {r.status_code}")
                    except:
                        with lock:
                            fail += 1
                        print(f"{Fore.RED}[Thread {tid}] Request {i+1}/{req_per_thread} FAILED")

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for t in range(num_threads):
                executor.submit(worker, t + 1)

        end_time = time.time()
        print(Fore.YELLOW + f"\n[✅] Hoàn tất! Thành công: {success} | Thất bại: {fail} | Thời gian: {round(end_time-start_time, 2)}s\n")

# ===================== KẾT NỐI VÀ CHẠY CHƯƠNG TRÌNH =====================

def run_tool():
    tool = WebToolPro()
    while True:
        banner()
        print(f"{Fore.WHITE}════════════════════ MENU TOOL ════════════════════")
        print(f"{Fore.CYAN}[1] Kiểm tra trạng thái Website (Status Code)")
        print(f"{Fore.CYAN}[2] Ping Host/IP")
        print(f"{Fore.CYAN}[3] Load Test Website (Mạnh mẽ)")
        print(f"{Fore.RED}[0] Thoát")
        print(f"{Fore.WHITE}═══════════════════════════════════════════════════")
        
        choice = input(f"{Fore.YELLOW}Nhập lựa chọn của bạn: ")
        
        if choice == "1":
            tool.check_status()
            input("\nNhấn Enter để quay lại menu...")
        elif choice == "2":
            tool.fast_ping()
            input("\nNhấn Enter để quay lại menu...")
        elif choice == "3":
            tool.load_test_pro()
            input("\nNhấn Enter để quay lại menu...")
        elif choice == "0":
            print(Fore.RED + "Đang thoát...")
            break
        else:
            print(Fore.RED + "Lựa chọn không hợp lệ!")
            sleep(1)

def main_key_system():
    ip_address = get_ip_address()
    banner()
    
    if ip_address:
        print(f"{Fore.WHITE}[{Fore.RED}<>{Fore.WHITE}] {Fore.RED}Địa chỉ IP : {ip_address}")
        existing_key = kiem_tra_ip(ip_address)
        
        if existing_key:
            print(f"{Fore.WHITE}[{Fore.RED}<>{Fore.WHITE}] {Fore.MAGENTA}Tool còn hạn, mời bạn dùng tool...")
            sleep(2)
            run_tool()
        else:
            url, key, expiration_date = generate_key_and_url(ip_address)
            print(f"{Fore.WHITE}[{Fore.RED}<>{Fore.WHITE}] {Fore.GREEN}Nhập 1 Để Lấy Key {Fore.YELLOW}( Free )")
            
            choice = input(f"{Fore.WHITE}[{Fore.RED}<>{Fore.WHITE}] {Fore.BLUE}Nhập lựa chọn: ")
            if choice == "1":
                yeumoney_data = get_shortened_link_phu(url)
                if yeumoney_data.get('status') == "error":
                    print(yeumoney_data.get('message'))
                    sys.exit()

                link_key = yeumoney_data.get('shortenedUrl')
                print(f'{Fore.MAGENTA}Link Để Vượt Key: {Fore.WHITE}{link_key}')

                while True:
                    keynhap = input(f'{Fore.YELLOW}Key Đã Vượt Là: ')
                    ADMIN_KEY = "hectoradminskibidi123"

                    if keynhap == key or keynhap == ADMIN_KEY:
                        print(f'{Fore.GREEN}Key Đúng Mời Bạn Dùng Tool')
                        luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                        sleep(2)
                        run_tool()
                        break
                    else:
                        print(f'{Fore.RED}Key Sai, Vượt Lại: {link_key}')
    else:
        print(Fore.RED + "Không thể lấy địa chỉ IP của thiết bị.")


