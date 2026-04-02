import os
import sys
from time import sleep
import requests
import json
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import base64

# ================== BANNER ==================
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    ban = r'''
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

# ================== HÀM MÃ HÓA / GIẢI MÃ ==================
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

def main_get_key():
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
                        ADMIN_KEY = "hectoradminskibidi123"
                        while True:
                            keynhap = input('\033[1;33mKey Đã Vượt Là: ').strip()
                            if keynhap == key or keynhap == ADMIN_KEY:
                                print('Key Đúng Mời Bạn Dùng Tool')
                                sleep(2)
                                luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                                return
                            else:
                                print('Key Sai, Vượt Lại:', link_key)

# ================== KIỂM TRA KEY TRƯỚC KHI VÀO TOOL ==================
if __name__ == "__main__":
    main_get_key()

# ================== MENU CHÍNH ==================
banner()
print("Dev:Deltatrash09(Duong Khoi)")
print("SDT:0949557645")
print("___________________________________________________________")

print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;32mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.1\033[1;31m] \033[1;32m SPAMSMS BETA \033[1;33m[\033[1;31mV1\033[1;33m]")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;32mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.2\033[1;31m] \033[1;32mTDS TIKTOK \033[1;33m[\033[1;31mV2\033[1;33m]")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;32mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.3\033[1;31m] \033[1;32mTOOL TDS FACEBOOK")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;32mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.5\033[1;31m] \033[1;32mTOOL DOSS WEB V1")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;32mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.6\033[1;31m] \033[1;32mTOOL ĐÀO PROXY ")
print("_____________________________________DỊCH VỤ _____________________________________________")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;32mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.7\033[1;31m] \033[1;32m TẠO MAIL ẢO")
print("\033[1;31m[\033[1;37m<>\033[1;31m] \033[1;37m=> \033[1;32mNhập\033[1;36m Số \033[1;31m[\033[1;33m1.8\033[1;31m] \033[1;32m LỌC PROXY LIVE")

chon = input("\033[1;32mNhập lựa chọn: ").strip()
print(f"\033[1;35m[DEBUG] Bạn đã chọn: {chon}")

# ================== HÀM EXEC AN TOÀN ==================
def safe_exec(url, tool_name):
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            print(f"\033[1;31mKhông tải được {tool_name}: HTTP {resp.status_code}")
            return
        code = resp.text
        if len(code) < 100:
            print(f"\033[1;31mNội dung {tool_name} quá ngắn, có thể bị lỗi URL.")
            return
        # Thực thi code trong không gian riêng
        exec_globals = {'__name__': '__main__'}
        exec(code, exec_globals)
    except SyntaxError as se:
        print(f"\033[1;31mLỗi cú pháp trong {tool_name}: {se}")
        print(f"\033[1;33mDòng lỗi: {se.text}")
    except Exception as e:
        print(f"\033[1;31mLỗi khi chạy {tool_name}: {e}")

# ================== CHẠY TOOL ĐƯỢC CHỌN ==================
if chon == '1.1':
    safe_exec('https://raw.githubusercontent.com/dx6791241-hue/Yyh/refs/heads/main/spamsms1.py', 'SPAMSMS BETA')
elif chon == '1.2':
    safe_exec('https://raw.githubusercontent.com/dx6791241-hue/Yyh/refs/heads/main/tiktok.py', 'TDS TIKTOK')
elif chon == '1.3':
    safe_exec('https://raw.githubusercontent.com/dx6791241-hue/Yyh/refs/heads/main/facebook_tds.py', 'TOOL TDS FACEBOOK')
elif chon == '1.5':
    safe_exec('https://raw.githubusercontent.com/dx6791241-hue/Yyh/refs/heads/main/text.py', 'TOOL DOSS WEB V1')
elif chon == '1.6':
    safe_exec('https://raw.githubusercontent.com/dx6791241-hue/Yyh/refs/heads/main/view_deobf.py', 'TOOL ĐÀO PROXY')
elif chon == '1.7':
    safe_exec('https://raw.githubusercontent.com/dx6791241-hue/Yyh/main/getmail.py', 'TẠO MAIL ẢO')
elif chon == '1.8':
    safe_exec('https://raw.githubusercontent.com/dx6791241-hue/Yyh/refs/heads/main/check_proxy.py', 'LỌC PROXY LIVE')
else:
    print("\033[1;31mLựa chọn không hợp lệ!")
























