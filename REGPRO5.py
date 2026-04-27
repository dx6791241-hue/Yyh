import os
import sys
import requests
import json
import time
import random
import re
import base64
from datetime import datetime, timedelta
from time import sleep
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor

# ================== GIAO DIỆN & TIỆN ÍCH ==================
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    ban = r'''
     ,--.'|                        ___                                         ,--.'|       
   ,--,  | :                     ,--.'|_                             ,---.   ,--,:  : |        
,---.'|  : '                     |  | :,'   ,---.    __  ,-.      /__./|,`--.'`|  ' :        
|   | : _' |                     :  : ' :  '   ,'\ ,' ,'/ /| ,---.;  ; ||   :  :  | |        
:   : |.'  |   ,---.     ,---. .;__,'  /  /   /   |'  | |' |/___/ \  | |:   |   \ | :        
|   ' '  ; :  /     \   /     \|  |   |  .   ; ,. :|  |  ,'\   ;  \ ' ||   : '  '; |        
'   |  .'. | /    /  | /    / ':__,'| :  '   | |: :'  :  /   \   \  \: |'   ' ;.    ;        
|   | :  | '.    ' / |.    ' /   '  : |__'   | .; :|  | '     ;   \  ' .|   | | \   |        
'   : |  : ;'   ;   /|'   ; :__  |  | '.'|   :    |;  : |      \   \  ''   : |  ; .'        
|   | '  ,/ '   |  / |'   | '.'| ;  :    ;\   \  / |  , ;       \   `  ;|   | '`--'          
;   : ;--'  |   :    ||   :    : |  ,   /  `----'   ---'         :   \ |'   : |              
|   ,/       \   \  /  \   \  /   ---`-'                           '---" ;   |.'              
'---'         `----'    `----'                                         '---'       
    '''
    for char in ban:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.002)

# ================== HÀM MÃ HÓA / GIẢI MÃ / AUTH ==================
def encrypt_data(data: str) -> str:
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")

def decrypt_data(data: str) -> str:
    return base64.b64decode(data.encode("utf-8")).decode("utf-8")

def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except Exception as e:
        print(f"Lỗi khi lấy địa chỉ IP: {e}")
        return None

def display_ip_address(ip_address):
    if ip_address:
        banner()
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;31mĐịa chỉ IP : {ip_address}\033[0m")
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
        return json.loads(decrypt_data(encrypted_data))
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
            return response.json()
        else:
            return {"status": "error", "message": "Không thể kết nối đến dịch vụ rút gọn URL."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi rút gọn URL: {e}"}

# ================== CORE REG PAGE PRO5 ==================
class CookieHandler:
    @staticmethod
    def to_dict(cookie_str: str) -> Dict[str, str]:
        return {k.strip(): v.strip() for item in cookie_str.split(";") 
                if "=" in item for k, v in [item.split("=", 1)]}

class NumberEncoder:
    @staticmethod
    def to_base36(num: int) -> str:
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        if num == 0: return "0"
        result = ""
        while num:
            num, remainder = divmod(num, 36)
            result = chars[remainder] + result
        return result

class HTMLExtractor:
    @staticmethod
    def find_pattern(html: str, pattern: str) -> Optional[str]:
        match = re.search(pattern, html)
        return match.group(1) if match else None
    
    @staticmethod
    def extract_token(html: str) -> Optional[str]:
        patterns = [r'DTSGInitialData".*?"token":"([^"]+)"', r'"token":"([^"]+)"']
        for pattern in patterns:
            result = HTMLExtractor.find_pattern(html, pattern)
            if result: return result
        return None

    @staticmethod
    def extract_lsd(html: str) -> Optional[str]:
        patterns = [r'LSD".*?"token":"([^"]+)"', r'"token":"([^"]+)"']
        for pattern in patterns:
            result = HTMLExtractor.find_pattern(html, pattern)
            if result: return result
        return None

    @staticmethod
    def extract_user_id(html: str) -> Optional[str]:
        patterns = [r'"actorID":"(\d+)"', r'"USER_ID":"(\d+)"', r'c_user=(\d+)']
        for pattern in patterns:
            result = HTMLExtractor.find_pattern(html, pattern)
            if result: return result
        return None
    
    @staticmethod
    def extract_revision(html: str) -> Optional[str]:
        return HTMLExtractor.find_pattern(html, r'client_revision["\s:]+(\d+)')
    
    @staticmethod
    def extract_jazoest(html: str) -> Optional[str]:
        return HTMLExtractor.find_pattern(html, r'jazoest=(\d+)')

class FacebookSession:
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.token = None
        self.user_id = None
        self.revision = None
        self.jazoest = None
        self.lsd = None

    def authenticate(self) -> bool:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(
                "https://www.facebook.com/",
                headers=headers,
                cookies=CookieHandler.to_dict(self.cookie),
                timeout=30
            )
            html = response.text
            self.token = HTMLExtractor.extract_token(html)
            self.user_id = HTMLExtractor.extract_user_id(html)
            self.revision = HTMLExtractor.extract_revision(html) or "1000000"
            self.jazoest = HTMLExtractor.extract_jazoest(html) or "0"
            self.lsd = HTMLExtractor.extract_lsd(html) or "0"
            
            if not self.token or not self.user_id:
                return False
                
            return {
                "token": self.token,
                "user_id": self.user_id,
                "revision": self.revision,
                "jazoest": self.jazoest,
                "lsd" : self.lsd,
            }
        except Exception:
            return False

class GenData:
    def __init__(self, session: FacebookSession):
        self.session = session
        self.request_counter = 0
    
    def build(self, bio: str, name: str) -> Dict[str, Any]:
        self.request_counter += 1   
        category_id = [169421023103905, 2347428775505624, 192614304101075, 145118935550090, 1350536325044173, 471120789926333, 180410821995109, 357645644269220, 2705]
        category = random.choice(category_id) 
        payload = {
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'AdditionalProfilePlusCreationMutation',
            'server_timestamps': 'true',
            "fb_dtsg": self.session.token,
            "jazoest": self.session.jazoest,
            "__a": "1",
            "__user": self.session.user_id,
            "__req": NumberEncoder.to_base36(self.request_counter),
            "__rev": self.session.revision,
            "av": self.session.user_id,
            "lsd" : self.session.lsd,
            'variables': '{"input":{"bio":"'+bio+'","categories":["'+str(category)+'"],"creation_source":"comet","name":"'+name+'","off_platform_creator_reachout_id":null,"page_referrer":"launch_point","actor_id":"'+self.session.user_id+'","client_mutation_id":"1"}}',
            'doc_id' : '9868446276528106'
        }
        return payload

class REGPRO5:
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.session = FacebookSession(cookie)
        self.payload_builder = None
        self.ready = False
        
    def login(self) -> bool:
        self.info = self.session.authenticate()
        if self.info:
            self.payload_builder = GenData(self.session)
            self.ready = True
            return True
        return False
       
    def REG(self, bio: str, name: str) -> tuple:
        if not self.ready:
            return False, "Not logged in"

        payload = self.payload_builder.build(bio, name)
        headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.facebook.com",
            "referer": "https://www.facebook.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "x-fb-lsd": self.session.lsd,
            "x-fb-friendly-name": "AdditionalProfilePlusCreationMutation",
            "cookie": self.cookie,
        }

        try:
            response = requests.post(
                'https://www.facebook.com/api/graphql/', 
                headers=headers, 
                data=payload,
                timeout=30
            )

            print(f"\033[1;33m[DEBUG] Status Code: {response.status_code}\033[0m")
            print(f"\033[1;33m[DEBUG] Response Length: {len(response.text)} bytes\033[0m")
            
            # In ra 300 ký tự đầu để xem lỗi
            preview = response.text[:300].replace('\n', ' ')
            print(f"\033[1;31m[DEBUG] Response Preview: {preview}...\033[0m")

            # Nếu không phải JSON (HTML hoặc rỗng)
            if not response.text.strip().startswith('{'):
                return False, f"Không phải JSON. Có thể bị block hoặc cookie die. Status: {response.status_code}"

            res_json = response.json()
            
            # Debug đầy đủ data
            print(f"\033[1;34m[DEBUG] Full JSON keys: {list(res_json.keys()) if isinstance(res_json, dict) else 'Not dict'}\033[0m")

            error_msg = res_json.get('data', {}).get('additional_profile_plus_create', {}).get('error_message')
            if error_msg:
                return False, error_msg

            page_id = res_json.get('data', {}).get('additional_profile_plus_create', {}).get('additional_profile', {}).get('id')
            if page_id:
                return True, page_id

            return False, "Không lấy được ID Page (có thể mutation lỗi)"

        except requests.exceptions.JSONDecodeError as e:
            return False, f"JSON Decode Error: {str(e)} - Response không phải JSON"
        except Exception as e:
            return False, f"Lỗi exception: {str(e)}"

# ================== MAIN LUỒNG HOẠT ĐỘNG ==================
def main_get_key() -> bool:
    ip_address = get_ip_address()
    display_ip_address(ip_address)
    
    if not ip_address:
        sys.exit()

    existing_key = kiem_tra_ip(ip_address)
    if existing_key:
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;35mTool còn hạn, mời bạn dùng tool...\033[0m")
        time.sleep(2)
        return True
    
    if da_qua_gio_moi():
        print("\033[1;33mQuá giờ sử dụng tool !!!\033[0m")
        sys.exit()

    url, key, expiration_date = generate_key_and_url(ip_address)
    ADMIN_KEY = "hectoradminskibidi123" # Admin key của bạn

    with ThreadPoolExecutor(max_workers=2) as executor:
        print("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;32mNhập 1 Để Lấy Key \033[1;33m( Free )\033[0m")
        while True:
            choice = input("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;34mNhập lựa chọn: \033[0m").strip()
            print("\033[97m════════════════════════════════════════════════\033[0m")
            
            if choice == "1":
                yeumoney_data = executor.submit(get_shortened_link_phu, url).result()
                if isinstance(yeumoney_data, dict) and yeumoney_data.get('status') == "error":
                    print(yeumoney_data.get('message'))
                    sys.exit()
                
                link_key = yeumoney_data.get('shortenedUrl') if isinstance(yeumoney_data, dict) else url
                print(f'\033[1;35mLink Để Vượt Key: {link_key}\033[0m')
                
                # Bọc vòng lặp nhập key ở đây, sai thì hỏi lại
                while True:
                    keynhap = input('\033[1;33mKey Đã Vượt Là: \033[0m').strip()
                    if keynhap == key or keynhap == ADMIN_KEY:
                        print('\033[1;32m[+] Key Đúng! Mời Bạn Dùng Tool.\033[0m')
                        sleep(2)
                        # Dù dùng Admin Key nhưng mình vẫn lưu Key gốc vào file để các lần mở lại tool nhận dạng IP đúng
                        luu_thong_tin_ip(ip_address, key, expiration_date)
                        return True
                    else:
                        print(f'\033[1;91m[-] Key Sai, Vui lòng nhập lại hoặc vượt link: {link_key}\033[0m')
            else:
                print("\033[1;91m[-] Lựa chọn không hợp lệ. Vui lòng nhập 1.\033[0m")

def main():
    # Chạy hàm get key trước
    main_get_key()

    # Bắt đầu Tool Reg
    print("\n\033[1;35m" + "="*40 + "\033[0m")
    cookie_input = input("\033[1;97m[>] Nhập Cookie Nick: \033[1;32m").strip()
    page_name = input("\033[1;97m[>] Nhập Tên Page: \033[1;32m").strip()
    page_bio = input("\033[1;97m[>] Nhập Tiểu Sử: \033[1;32m").strip()
    print("\033[1;35m" + "="*40 + "\033[0m")

    print("\033[1;33m[!] Đang khởi tạo luồng đăng nhập...\033[0m")
    tool = REGPRO5(cookie_input)
    
    if tool.login():
        print("\033[1;32m[+] Cập nhật Token & Data thành công! Đang request tạo Page...\033[0m")
        success, result = tool.REG(page_bio, page_name)
        
        if success:
            print(f"\033[1;32m[+] Tạo Page PRO5 Thành Công! ID Page: {result}\033[0m")
        else:
            print(f"\033[1;91m[-] Lỗi Tạo Page: {result}\033[0m")
    else:
        print("\033[1;91m[-] Đăng nhập thất bại. Cookie có thể đã die hoặc lỗi Get Token!\033[0m")

if __name__ == "__main__":
    main()
