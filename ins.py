import requests, os, platform, sys, time, json, pyautogui, webbrowser, pyperclip, traceback, threading, random, subprocess, hashlib, re, base64, uuid, shutil
from urllib.parse import urljoin
from colorama import init, Fore, Back, Style
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue

init(autoreset=True)

# --- CÁC HÀM TẠO MÀU GRADIENT TỪ TOOLVIEWV2.PY ---
def gradient_3(text):
    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    start = (0, 255, 0)   # xanh lá
    end   = (0, 128, 255) # xanh biển

    result = ""
    for i, char in enumerate(text):
        t = i / (len(text) - 1 if len(text) > 1 else 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        result += rgb_to_ansi(r, g, b) + char
    return result + "\033[0m"

def gradient_2(text):
    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    start_color = (255, 87, 34)     # 🧡 Cam đất
    mid_color   = (255, 20, 147)    # 💖 Hồng đậm neon
    end_color   = (255, 255, 0)     # 💛 Vàng sáng

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

def xaibo_dep_trai(text, start_color, end_color=None):
    if end_color is None:
        end_color = (255, 255, 255)
    result = ""
    length = len(text)
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / max(1, length-1))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / max(1, length-1))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / max(1, length-1))
        result += f"\033[38;2;{r};{g};{b}m{char}"
    return result + "\033[0m"

xaibo_vang = (255, 255, 0)
xaibo_menu = (255, 255, 0)
xaibo_success = (0, 255, 0)
xaibo_error = (255, 0, 0)
xaibo_warning = (255, 0, 255)
xaibo_info = (0, 255, 255)
xaibo_coin = (255, 255, 0)
xaibo_link = (0, 255, 255)
xaibo_input = (255, 255, 255)
xaibo_coord = (255, 0, 255)
xaibo_account = (0, 255, 0)
xaibo_job = (255, 255, 0)
xaibo_timer = (255, 165, 0)
xaibo_action = (255, 0, 255)
xaibo_stats = (0, 255, 255)
xaibo_comment = (0, 0, 255)
xaibo_cookie = (255, 165, 0)
xaibo_delay = (255, 165, 0)

xaibo_file = "user.cfg"
xaibo_session = requests.Session()
xaibo_stop = False
xaibo_threads = []
xaibo_lock = threading.Lock()
xaibo_displays = {}
xaibo_order = []
xaibo_cache = {}
xaibo_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
]

def xaibo_thoi_gian(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours} giờ {minutes} phút {secs} giây"
    elif minutes > 0:
        return f"{minutes} phút {secs} giây"
    return f"{secs} giây"

# --- BANNER THAY THẾ TỪ TOOLVIEWV2.PY ---
def xaibo_hien_thi():
    my_banner_text = r"""
      ,--.'|                       ___                                         ,--.'|        
   ,--,  | :                     ,--.'|_                           ,---.   ,--,:  : |        
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

    my_info_text = f"""
    ═══════════════════════════════════════════════════════════════════
    [+] Dev       : Deltatrash09 (Duong Khoi)
    [+] SDT       : 0949557645
    ═══════════════════════════════════════════════════════════════════
    """
    print(gradient_3(my_banner_text))
    print(gradient_2(my_info_text))

xaibo_cuoi = 0

def xaibo_lam_moi():
    global xaibo_cuoi
    current_time = time.time()
    if current_time - xaibo_cuoi < 0.2:
        return
    with xaibo_lock:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        my_banner_text = r"""
      ,--.'|                       ___                                         ,--.'|        
   ,--,  | :                     ,--.'|_                           ,---.   ,--,:  : |        
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

        my_info_text = f"""
        ═══════════════════════════════════════════════════════════════════
        [+] Dev       : Deltatrash09 (Duong Khoi)
        [+] SDT       : 0949557645
        ═══════════════════════════════════════════════════════════════════
        """
        print(gradient_3(my_banner_text))
        print(gradient_2(my_info_text))
        for account_name in xaibo_order:
            if account_name in xaibo_displays:
                display_info = xaibo_displays[account_name]
                if 'start_time' in display_info:
                    elapsed = time.time() - display_info['start_time']
                    time_str = xaibo_thoi_gian(elapsed)
                else:
                    time_str = "0 giây"
                job_count = display_info.get('job_count', 0)
                action = display_info.get('current_action', '')
                link = display_info.get('current_link', '')
                total_earned = display_info.get('total_earned', 0)
                if link and len(link) > 40:
                    link = link[:37] + "..."
                if 'delay_message' in display_info:
                    line = f"[{account_name}] | {time_str} - {job_count} jobs | {display_info['delay_message']}"
                    color = xaibo_delay
                elif action:
                    if 'thành công' in action.lower() or '+' in action:
                        line = f"[{account_name}] | {time_str} - {job_count} jobs | {action} | {link} (= {total_earned}đ)"
                        color = xaibo_success
                    elif 'đang' in action.lower() or 'chờ' in action.lower():
                        line = f"[{account_name}] | {time_str} - {job_count} jobs | {action} | {link} (= {total_earned}đ)"
                        color = xaibo_timer if 'chờ' in action.lower() else xaibo_action
                    elif 'thất bại' in action.lower() or 'lỗi' in action.lower():
                        line = f"[{account_name}] | {time_str} - {job_count} jobs | {action} | {link} (= {total_earned}đ)"
                        color = xaibo_error
                    else:
                        line = f"[{account_name}] | {time_str} - {job_count} jobs | {action} (= {total_earned}đ)"
                        color = xaibo_info
                else:
                    line = f"[{account_name}] | {time_str} - {job_count} jobs"
                    color = xaibo_info
                print(xaibo_dep_trai(line, color))
            else:
                print(xaibo_dep_trai(f"[{account_name}] | đang khởi tạo...", xaibo_info))
        print("")
        print(xaibo_dep_trai("─" * 80, xaibo_menu))
        sys.stdout.flush()
        xaibo_cuoi = current_time

def xaibo_cap_nhat(account_name, action="", link="", job_type="", job_count=None, reward=0, total_earned=0, is_delay_message=False):
    global xaibo_displays, xaibo_order
    with xaibo_lock:
        if account_name not in xaibo_displays:
            xaibo_displays[account_name] = {'start_time': time.time(), 'job_count': 0, 'total_earned': 0, 'current_action': '', 'current_link': '', 'current_type': ''}
            if account_name not in xaibo_order:
                xaibo_order.append(account_name)
        display_info = xaibo_displays[account_name]
        if is_delay_message:
            display_info['delay_message'] = action
            if 'start_time' in display_info:
                del display_info['start_time']
            display_info['job_count'] = 0
            display_info['total_earned'] = 0
            display_info['current_action'] = ''
            display_info['current_link'] = ''
            display_info['current_type'] = ''
        else:
            if 'delay_message' in display_info:
                del display_info['delay_message']
            if 'start_time' not in display_info:
                display_info['start_time'] = time.time()
            if job_count is not None:
                display_info['job_count'] = job_count
            if total_earned > 0:
                display_info['total_earned'] = total_earned
            display_info['current_action'] = action
            display_info['current_link'] = link
    xaibo_lam_moi()

def xaibo_agent(account_username):
    if account_username in xaibo_cache:
        return xaibo_cache[account_username]
    user_agent = random.choice(xaibo_agents)
    xaibo_cache[account_username] = user_agent
    return user_agent

def xaibo_session_moi(user_agent):
    session = requests.Session()
    headers = {'User-Agent': user_agent, 'Accept': '*/*', 'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive', 'Host': 'www.instagram.com', 'Origin': 'https://www.instagram.com', 'Referer': 'https://www.instagram.com/', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'X-ASBD-ID': '198387', 'X-IG-App-ID': '936619743392459', 'X-IG-WWW-Claim': '0', 'X-Requested-With': 'XMLHttpRequest'}
    session.headers.update(headers)
    ig_did = str(uuid.uuid4()).upper()
    mid = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=26))
    datr = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_', k=43))
    session.cookies.set('ig_did', ig_did, domain='.instagram.com')
    session.cookies.set('mid', mid, domain='.instagram.com')
    session.cookies.set('datr', datr, domain='.instagram.com')
    session.cookies.set('dpr', '1.25', domain='.instagram.com')
    session.cookies.set('wd', '1536x738', domain='.instagram.com')
    return session

def xaibo_csrf(session):
    try:
        response = session.head('https://www.instagram.com/', timeout=3, allow_redirects=True)
        csrftoken = session.cookies.get('csrftoken', '')
        if not csrftoken:
            response = session.get('https://www.instagram.com/', timeout=3)
            csrftoken = session.cookies.get('csrftoken', '')
            if not csrftoken:
                match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if match:
                    csrftoken = match.group(1)
                    session.cookies.set('csrftoken', csrftoken, domain='.instagram.com')
        if csrftoken:
            session.headers.update({'X-CSRFToken': csrftoken})
        return csrftoken
    except:
        return None

def xaibo_xoa_man():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def xaibo_doc_cfg():
    if os.path.exists(xaibo_file):
        try:
            with open(xaibo_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def xaibo_ghi_cfg(config):
    with open(xaibo_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def xaibo_format_cookie(cookies_dict):
    cookie_parts = []
    for key, value in cookies_dict.items():
        if key == 'rur' and value and not value.startswith('"'):
            value = f'"{value}"'
        cookie_parts.append(f"{key}={value}")
    return '; '.join(cookie_parts)

def xaibo_hien_thi_cookie(cookies_dict, account_username):
    print(xaibo_dep_trai(f"\n{'='*80}", xaibo_cookie))
    print(xaibo_dep_trai(f"🍪 COOKIES CHO TÀI KHOẢN: {account_username}", xaibo_cookie))
    print(xaibo_dep_trai(f"{'='*80}", xaibo_cookie))
    cookie_string = xaibo_format_cookie(cookies_dict)
    print(xaibo_dep_trai(cookie_string, xaibo_cookie))
    print(xaibo_dep_trai(f"{'='*80}", xaibo_cookie))
    print(xaibo_dep_trai(f"📊 TỔNG SỐ COOKIES: {len(cookies_dict)}", xaibo_success))
    user_agent = cookies_dict.get('useragent', 'Chưa có')
    if user_agent != 'Chưa có':
        try:
            decoded_ua = base64.b64decode(user_agent).decode('utf-8')
            print(xaibo_dep_trai(f"🔑 USER AGENT: {decoded_ua[:80]}...", xaibo_info))
        except:
            print(xaibo_dep_trai(f"🔑 USER AGENT: {user_agent[:80]}...", xaibo_info))
    print(xaibo_dep_trai(f"{'='*80}\n", xaibo_cookie))
    for i in range(3, 0, -1):
        print(xaibo_dep_trai(f"⏳ TIẾP TỤC SAU {i} GIÂY...", xaibo_warning), end='\r')
        time.sleep(1 + random.uniform(0, 0.002))
    print(' ' * 50, end='\r')
    print("")

def xaibo_api_data(auth_token, t_param):
    url = urljoin("https://gateway.golike.net/", "api/users/me")
    headers = {"Authorization": f"Bearer {auth_token.replace('Bearer ', '')}", "T": t_param, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Content-Type": "application/json"}
    try:
        response = xaibo_session.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        print(xaibo_dep_trai(f"❌ Lỗi API: {response.status_code} - {response.text}", xaibo_error))
        return None
    except Exception as e:
        print(xaibo_dep_trai(f"❌ Lỗi kết nối: {str(e)}", xaibo_error))
        return None

def xaibo_dang_nhap(username, password):
    try:
        user_agent = xaibo_agent(username)
        print(xaibo_dep_trai(f"[{username}] Đang lấy cookies...", xaibo_menu, xaibo_success))
        ig_session = xaibo_session_moi(user_agent)
        csrftoken = xaibo_csrf(ig_session)
        if not csrftoken:
            print(xaibo_dep_trai(f"[{username}] ❌ KHÔNG THỂ LẤY CSRF TOKEN", xaibo_error))
            return None
        login_data = {'username': username, 'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}', 'queryParams': '{}', 'optIntoOneTap': 'false', 'stopDeletionNonce': '', 'trustedDeviceRecords': '{}', 'device_id': ig_session.cookies.get('ig_did', '')}
        login_headers = {'User-Agent': user_agent, 'Accept': '*/*', 'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7', 'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': csrftoken, 'X-Instagram-AJAX': str(random.randint(1000000000, 9999999999)), 'X-IG-App-ID': '936619743392459', 'X-IG-WWW-Claim': '0', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://www.instagram.com', 'Referer': 'https://www.instagram.com/', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin'}
        time.sleep(random.uniform(2, 4))
        login_response = ig_session.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', data=login_data, headers=login_headers, allow_redirects=False, timeout=10)
        if login_response.status_code == 200:
            response_data = login_response.json()
            if response_data.get('authenticated'):
                print(xaibo_dep_trai(f"[{username}] Lấy Cookies thành công!", xaibo_success))
                user_id = response_data.get('userId', '')
                time.sleep(1 + random.uniform(0, 0.002))
                cookies_dict = {}
                for cookie in ig_session.cookies:
                    cookies_dict[cookie.name] = cookie.value
                if 'rur' in cookies_dict:
                    rur_value = cookies_dict['rur']
                    if not rur_value.startswith('"'):
                        cookies_dict['rur'] = f'"{rur_value}"'
                else:
                    timestamp = int(time.time()) + 86400 * 7
                    random_hash = hashlib.sha256(f"{username}{timestamp}{random.random()}".encode()).hexdigest()[:32]
                    cookies_dict['rur'] = f'"PRN\\054{user_id}\\054{timestamp}:{random_hash}"'
                cookies_dict['ds_user_id'] = user_id
                cookies_dict['useragent'] = base64.b64encode(user_agent.encode()).decode()
                default_cookies = {'dpr': '1.25', 'wd': '1536x738', 'ps_l': '1', 'ps_n': '1'}
                for key, value in default_cookies.items():
                    if key not in cookies_dict:
                        cookies_dict[key] = value
                required_cookies = ['csrftoken', 'sessionid', 'ds_user_id', 'rur']
                missing = [c for c in required_cookies if c not in cookies_dict]
                if missing:
                    print(xaibo_dep_trai(f"[{username}] Thiếu Cookie: {', '.join(missing)}", xaibo_error))
                    print(xaibo_dep_trai(f"[{username}] Cookies: {list(cookies_dict.keys())}", xaibo_warning))
                    return None
                return dict(sorted(cookies_dict.items()))
            else:
                error_msg = response_data.get('message', 'Đăng nhập thất bại')
                if 'checkpoint' in response_data:
                    print(xaibo_dep_trai(f"[{username}] Tài khoản yêu cầu xác minh", xaibo_error))
                else:
                    print(xaibo_dep_trai(f"[{username}] Lấy cookies thất bại {error_msg}", xaibo_error))
                time.sleep(2 + random.uniform(0, 0.002))
                return None
        else:
            print(xaibo_dep_trai(f"[{username}] Lỗi HTTP: {login_response.status_code}", xaibo_error))
            return None
    except Exception as e:
        print(xaibo_dep_trai(f"[{username}] Lỗi lấy cookies: {str(e)}", xaibo_error))
        traceback.print_exc()
        time.sleep(2 + random.uniform(0, 0.002))
        return None

def xaibo_luu_account(account_username, password, cookies):
    config = xaibo_doc_cfg()
    if 'accounts' not in config:
        config['accounts'] = {}
    config['accounts'][account_username] = {'password': password, 'cookies': cookies.copy(), 'cookie_string': xaibo_format_cookie(cookies), 'last_login': datetime.now().isoformat()}
    xaibo_ghi_cfg(config)
    return True

def xaibo_lay_account(account_username):
    config = xaibo_doc_cfg()
    if 'accounts' in config and account_username in config['accounts']:
        return config['accounts'][account_username]
    return None

def xaibo_kiem_tra_cookie(cookies):
    try:
        user_agent = cookies.get('useragent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15')
        try:
            if len(user_agent) > 50 and '=' in user_agent:
                decoded_ua = base64.b64decode(user_agent).decode('utf-8')
                user_agent = decoded_ua
        except:
            pass
        headers = {'User-Agent': user_agent, 'Accept': 'application/json, text/plain, */*', 'x-ig-app-id': '936619743392459'}
        response = xaibo_session.get('https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram', headers=headers, cookies=cookies, timeout=5)
        return response.status_code == 200
    except:
        return False

def xaibo_refresh_cookie(account_username):
    saved_account = xaibo_lay_account(account_username)
    if saved_account and saved_account.get('password'):
        print(xaibo_dep_trai(f"[{account_username}] 🔄 ĐANG LÀM MỚI COOKIES...", xaibo_info))
        new_cookies = xaibo_dang_nhap(account_username, saved_account['password'])
        if new_cookies:
            xaibo_luu_account(account_username, saved_account['password'], new_cookies)
            return new_cookies
    return None

def xaibo_lay_user_id(username, cookies):
    try:
        user_agent = cookies.get('useragent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        try:
            if len(user_agent) > 50 and '=' in user_agent:
                decoded_ua = base64.b64decode(user_agent).decode('utf-8')
                user_agent = decoded_ua
        except:
            pass
        headers = {'User-Agent': user_agent, 'Accept': '*/*', 'Accept-Language': 'vi,en;q=0.9'}
        response = requests.get(f"https://www.instagram.com/{username}/", headers=headers, cookies=cookies, timeout=10)
        patterns = [r'"user_id":"(\d+)"', r'"id":"(\d+)"', r'"pk":\s*"?(\d+)"?', r'"user":\{"id":"(\d+)"', r'"profilePage_(\d+)"', r'"owner":\{"id":"(\d+)"']
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                return match.group(1)
        return None
    except:
        return None

def xaibo_lay_fb_lsd(username, cookies):
    try:
        user_agent = cookies.get('useragent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        try:
            if len(user_agent) > 50 and '=' in user_agent:
                decoded_ua = base64.b64decode(user_agent).decode('utf-8')
                user_agent = decoded_ua
        except:
            pass
        headers = {'User-Agent': user_agent, 'Accept': '*/*'}
        response = requests.get(f"https://www.instagram.com/{username}/", headers=headers, cookies=cookies, timeout=10)
        fb_dtsg_match = re.search(r'"fb_dtsg":"([^"]+)"', response.text)
        lsd_match = re.search(r'"lsd":"([^"]+)"', response.text)
        return (fb_dtsg_match.group(1) if fb_dtsg_match else None), (lsd_match.group(1) if lsd_match else None)
    except:
        return None, None

def xaibo_follow(cookies, target_username, account_username=None):
    try:
        if 'sessionid' not in cookies or 'ds_user_id' not in cookies:
            return False
        user_agent = cookies.get('useragent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        try:
            if len(user_agent) > 50 and '=' in user_agent:
                decoded_ua = base64.b64decode(user_agent).decode('utf-8')
                user_agent = decoded_ua
        except:
            pass
        target_user_id = xaibo_lay_user_id(target_username, cookies)
        if not target_user_id:
            return False
        fb_dtsg, lsd = xaibo_lay_fb_lsd(target_username, cookies)
        headers = {'accept': '*/*', 'accept-language': 'vi,en;q=0.9', 'cache-control': 'no-cache', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://www.instagram.com', 'pragma': 'no-cache', 'priority': 'u=1, i', 'referer': f'https://www.instagram.com/{target_username}/', 'sec-ch-prefers-color-scheme': 'dark', 'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"', 'sec-ch-ua-full-version-list': '"Not:A-Brand";v="99.0.0.0", "Google Chrome";v="145.0.7632.160", "Chromium";v="145.0.7632.160"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua-platform-version': '"10.0.0"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': user_agent, 'x-asbd-id': '359341', 'x-bloks-version-id': '61fc9465e13b77eaa110f317859102ba7fb93a0a2bcc08c46473da6713640739', 'x-fb-friendly-name': 'usePolarisFollowMutation', 'x-ig-app-id': '936619743392459', 'x-root-field-name': 'xdt_create_friendship', 'x-csrftoken': cookies.get('csrftoken', '')}
        if fb_dtsg:
            headers['x-fb-dtsg'] = fb_dtsg
        if lsd:
            headers['x-fb-lsd'] = lsd
        av = f"178414{cookies.get('ds_user_id', '')}"
        data = {'av': av, '__d': 'www', '__user': '0', '__a': '1', '__req': '1j', '__hs': '20519.HYP:instagram_web_pkg.2.1...0', 'dpr': '1', '__ccg': 'EXCELLENT', '__rev': '1034708364', '__s': 'cywslo:ltqg37:glm7el', '__hsi': str(int(time.time() * 1000)), '__dyn': '7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0DU2wx609vCwjE1EE2Cw8G11wBz81s8hwGxu786a3a1YwBgao6C0Mo2swlo8od8-U2zxe2GewGw9a361qwuEjUlwhEe87q0oa2-azqwt8d-2u2J0bS1LwTwKG1pg2fwxyo6O1FwlA3a3zhAq4rwIxeUnAwCAxW1oxe6U5q0EoKmUhw4rwXyEcE4y16wAwj8', '__csr': 'ggT9sahcIAIAcgzblhtR2mRl44TdvNiaLmXnFlmHiBKmnroCK4_gJaAjiAiWHz2Kp5AKKiQBBx6BU8VoKiVJaeKayXlQql4SdAGT8mgxqGhDCzoy9mbBpFEXRG2jCy8KimVUGifBV9p4imA8yGjGayQih_yrXCy9Q9hVdJ5qDKbyEO58hDBABAyFp968CUaUK5UeUdU0x20vWaK01BHw04d8wWAAwOKC0k20Ak1dB80pu4Eak0f4wmFU13U8EduV98kgnQ0PVm0e3g0CCp06aAw1bS1fwtu1xxmEkokweqc8vwtywa10qhoGbUmzQ485SdeEkhohpRwk9A14w5Zwioy9gOgE5m0Bju0E8bUmBt2VQew14C4C6o9p8W4ER0ncxoBgE0jS07IU0o6G07pU0lYw1AS02XW', '__hsdp': 'go55M8i142Bl9dd4YIesGqkbJkFb5Qhijtlp91jlz9kpiarGsgd8Pk4o9GldEfIIs5Z7wxe9g5Fp1MG1qC8axi3S78e4dxufzogym5t2pUiyi3UlG1vggfwkUG6GwXxO5U9Uf8fUkxW5omzElwCx64Edo2gG5obE7W1nw-Lwso0zq0hKfw2jES0Z82rg0we0fdxe0NQ1AzE3Uw5AU1s8co2Hw3SE14Q0Wo24wQ8787O1gwc60FE7y', '__hblp': '0p8twlEtw_wSx2idCwyG78b89EuxGdxjwHwoE8ouho-Q32agiwg84equbG2p24UcFVaHxaczV8gQV8jwh8nAwZx28UqQaKu2i79ECq4olxy2e4U8Ey5bx3Dxm5HgC5qxyax64FEbE662WESu2Wm1NCwlaw-Lx21wwGwcO0jW0hKfw9q0FU13UNU3Nw9J0be0RUDo4K7o2Ox23m1Bw2rojzU7e13gc8-2eewl82wGbxK7E5S0A8tw63wNw862C09uw5awMwf2291iaw8S2yeK0x8uxkxolgy1PxW361sx-12U6K2Odwu8', '__sjsp': 'go55M8i142Bl9dd4YIesGWkj6JkFb5Qhijtlhp1jlx96haCWx-7oaljq2UIIs5WDwza9g5Fp1M6V0bd0', '__comet_req': '7', 'jazoest': '26738', '__spin_r': '1034708364', '__spin_b': 'trunk', '__spin_t': '1772902434', '__crn': 'comet.igweb.PolarisProfilePostsTabRoute', 'fb_api_caller_class': 'RelayModern', 'fb_api_req_friendly_name': 'usePolarisFollowMutation', 'server_timestamps': 'true', 'variables': json.dumps({'target_user_id': target_user_id, 'container_module': 'profile', 'nav_chain': f'PolarisProfilePostsTabRoot:profilePage:1:via_cold_start,PolarisProfilePostsTabRoot:profilePage:3:unexpected'}), 'doc_id': '9740159112729312'}
        if fb_dtsg:
            data['fb_dtsg'] = fb_dtsg
        if lsd:
            data['lsd'] = lsd
        follow_session = requests.Session()
        follow_session.cookies.update(cookies)
        response = follow_session.post('https://www.instagram.com/graphql/query', headers=headers, data=data, timeout=15, allow_redirects=False)
        if response.status_code == 200:
            try:
                result = response.json()
                if 'data' in result and result.get('data'):
                    return True
                elif 'errors' in result:
                    error_msg = result['errors'][0].get('message', 'Unknown error')
                    if 'already' in error_msg.lower() or 'following' in error_msg.lower():
                        return True
                    return False
                return True
            except:
                return True
        return False
    except:
        return False

def xaibo_like(cookies, media_id):
    user_agent = cookies.get('useragent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    try:
        if len(user_agent) > 50 and '=' in user_agent:
            decoded_ua = base64.b64decode(user_agent).decode('utf-8')
            user_agent = decoded_ua
    except:
        pass
    headers = {'User-Agent': user_agent, 'Accept': '*/*', 'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8', 'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': cookies.get('csrftoken', ''), 'X-Requested-With': 'XMLHttpRequest', 'X-Instagram-AJAX': '1', 'Origin': 'https://www.instagram.com', 'Referer': f'https://www.instagram.com/p/{media_id}/', 'Connection': 'keep-alive'}
    try:
        like_session = requests.Session()
        like_session.cookies.update(cookies)
        response = like_session.post(f'https://www.instagram.com/api/v1/web/likes/{media_id}/like/', headers=headers, timeout=10)
        return response.status_code == 200
    except:
        return False

def xaibo_cookie_lay(account_username):
    saved_account = xaibo_lay_account(account_username)
    return saved_account.get('cookies', {}) if saved_account else {}

def xaibo_cookie_luu(account_username, cookie_dict):
    config = xaibo_doc_cfg()
    if 'accounts' in config and account_username in config['accounts']:
        config['accounts'][account_username]['cookies'] = cookie_dict
        config['accounts'][account_username]['cookie_string'] = xaibo_format_cookie(cookie_dict)
        config['accounts'][account_username]['last_login'] = datetime.now().isoformat()
        xaibo_ghi_cfg(config)
        return True
    return False

def xaibo_instagram_accounts(auth_token, t_param):
    url = urljoin("https://gateway.golike.net/", "api/instagram-account")
    headers = {"Authorization": f"Bearer {auth_token.replace('Bearer ', '')}", "T": t_param, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Content-Type": "application/json"}
    try:
        response = xaibo_session.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        print(xaibo_dep_trai(f"❌ Lỗi API: {response.status_code} - {response.text}", xaibo_error))
        return None
    except Exception as e:
        print(xaibo_dep_trai(f"❌ Lỗi kết nối: {str(e)}", xaibo_error))
        return None

def xaibo_quan_ly_menu(accounts):
    xaibo_xoa_man()
    xaibo_hien_thi()
    print(xaibo_dep_trai(" ╭───────────────────────────────────────────╮", xaibo_menu))
    print(xaibo_dep_trai(" │" + " "*14 + "QUẢN LÝ TÀI KHOẢN" + " "*14 + "│", xaibo_menu))
    print(xaibo_dep_trai(" │───────────────────────────────────────────│", xaibo_menu))
    config = xaibo_doc_cfg()
    saved_accounts = list(config['accounts'].keys()) if 'accounts' in config else []
    if not saved_accounts:
        print(xaibo_dep_trai("     CHƯA CÓ TÀI KHOẢN NÀO ĐƯỢC LƯU", xaibo_error))
    else:
        for index, username in enumerate(saved_accounts, 1):
            account_info = config['accounts'][username]
            last_login = account_info.get('last_login', 'Không rõ')
            cookies_exist = "✓" if account_info.get('cookies') else "✗"
            cookie_count = len(account_info.get('cookies', {})) if account_info.get('cookies') else 0
            print(xaibo_dep_trai(f"│ {index:2d}. {username.ljust(20)} │ Cookies: {cookies_exist} ({cookie_count}) │ Lần cuối: {last_login[:10]} │", xaibo_account))
    print(xaibo_dep_trai("╰─────────────────────────────────────────────────╯", xaibo_menu))
    print(xaibo_dep_trai("\n[ 0 ] QUAY LẠI", xaibo_info))
    print(xaibo_dep_trai("[ 1 ] XÓA TÀI KHOẢN", xaibo_warning))
    print(xaibo_dep_trai("[ 2 ] HIỂN THỊ COOKIES ĐÃ LƯU", xaibo_cookie))
    choice = input(xaibo_dep_trai("[ => ] CHỌN: ", xaibo_success)).strip()
    if choice == '1' and saved_accounts:
        del_choice = input(xaibo_dep_trai("NHẬP SỐ THỨ TỰ TÀI KHOẢN CẦN XÓA: ", xaibo_warning)).strip()
        try:
            idx = int(del_choice) - 1
            if 0 <= idx < len(saved_accounts):
                username = saved_accounts[idx]
                del config['accounts'][username]
                if username in xaibo_cache:
                    del xaibo_cache[username]
                xaibo_ghi_cfg(config)
                print(xaibo_dep_trai(f"✅ ĐÃ XÓA TÀI KHOẢN {username}", xaibo_success))
                time.sleep(1 + random.uniform(0, 0.002))
        except:
            pass
    elif choice == '2' and saved_accounts:
        view_choice = input(xaibo_dep_trai("NHẬP SỐ THỨ TỰ TÀI KHOẢN CẦN XEM COOKIES: ", xaibo_cookie)).strip()
        try:
            idx = int(view_choice) - 1
            if 0 <= idx < len(saved_accounts):
                username = saved_accounts[idx]
                cookies = config['accounts'][username].get('cookies', {})
                if cookies:
                    xaibo_hien_thi_cookie(cookies, username)
                else:
                    print(xaibo_dep_trai(f"❌ TÀI KHOẢN {username} KHÔNG CÓ COOKIES", xaibo_error))
                input(xaibo_dep_trai("\nNHẤN ENTER ĐỂ TIẾP TỤC...", xaibo_info))
        except:
            pass
    time.sleep(1 + random.uniform(0, 0.002))

def xaibo_hien_thi_accounts(accounts_data):
    if not accounts_data or 'data' not in accounts_data or not accounts_data['data']:
        print(xaibo_dep_trai("⚠️ Không có tài khoản Instagram nào được tìm thấy", xaibo_warning))
        return None
    print(xaibo_dep_trai("╭────────────────────────────────────╮", xaibo_menu))
    print(xaibo_dep_trai("│" + " "*2 + "STT" + " "*2 + "│" + " "*8 + "TÊN INSTAGRAM" + " "*7 + "│", xaibo_menu))
    print(xaibo_dep_trai("│───────│─────────────────────────────", xaibo_menu))
    for index, account in enumerate(accounts_data['data'], 1):
        print(xaibo_dep_trai("│ " + " "*2 + f"{str(index).ljust(4)}" + "│" + " "*10 + f"{str(account.get('instagram_username', '')).ljust(24)}" + " ", xaibo_menu))
    print(xaibo_dep_trai("╰" + "─"*7 + "─" + "─"*28 + "╯", xaibo_menu))
    return accounts_data['data']

def xaibo_chon_account(accounts):
    while True:
        try:
            print()
            print(xaibo_dep_trai("─"*50, xaibo_success))
            print(xaibo_dep_trai("[ 0 ] QUẢN LÝ TÀI KHOẢN", xaibo_info))
            choice = input(xaibo_dep_trai("> Nhập tài khoản chạy (VD: 1,2,3 hoặc ALL): ", xaibo_success)).strip().lower()
            time.sleep(0.5 + random.uniform(0, 0.002))
            if choice == '0':
                xaibo_quan_ly_menu(accounts)
                return None
            if choice == 'q':
                return None
            if choice == 'all':
                return accounts.copy()
            selected_indexes = []
            for c in choice.split(','):
                c = c.strip()
                if not c:
                    continue
                index = int(c)
                if 1 <= index <= len(accounts):
                    selected_indexes.append(index-1)
                else:
                    print(xaibo_dep_trai(f"[ :< ] SỐ {index} KHÔNG HỢP LỆ!", xaibo_warning))
            if selected_indexes:
                selected_indexes = list(dict.fromkeys(selected_indexes))
                return [accounts[i] for i in selected_indexes]
            print(xaibo_dep_trai(f"[ :< ] VUI LÒNG NHẬP TỪ 1 -> {len(accounts)} (HOẶC 'Q' ĐỂ THOÁT)", xaibo_warning))
        except ValueError:
            print("")
            print(xaibo_dep_trai("[ :< ] SỐ BẠN VỪA NHẬP KHÔNG HỢP LỆ!", xaibo_warning))

def xaibo_job_delay():
    while True:
        delay_input = input(xaibo_dep_trai(f"\n Nhập delay (enter để 10): ", xaibo_link)).strip()
        if not delay_input:
            return 10
        if ',' in delay_input:
            try:
                parts = delay_input.split(',')
                if len(parts) != 2:
                    raise ValueError
                min_delay = int(parts[0].strip())
                max_delay = int(parts[1].strip())
                if min_delay <= 0 or max_delay <= 0:
                    print(xaibo_dep_trai("[ :< ] THỜI GIAN PHẢI LỚN HƠN 0!", xaibo_warning))
                    continue
                if min_delay > max_delay:
                    min_delay, max_delay = max_delay, min_delay
                print(xaibo_dep_trai(f"\n[ :> ] ĐÃ ĐẶT THỜI GIAN DELAY RANDOM: {min_delay}s - {max_delay}s", xaibo_success))
                return f"{min_delay},{max_delay}"
            except ValueError:
                print(xaibo_dep_trai("[ :< ] ĐỊNH DẠNG KHÔNG HỢP LỆ!", xaibo_warning))
                continue
        else:
            try:
                delay = int(delay_input)
                if delay <= 0:
                    print(xaibo_dep_trai("[ :< ] THỜI GIAN PHẢI LỚN HƠN 0!", xaibo_warning))
                    continue
                print(xaibo_dep_trai(f"\n[ :> ] ĐÃ ĐẶT THỜI GIAN DELAY LÀ {delay}s", xaibo_success))
                return delay
            except ValueError:
                print(xaibo_dep_trai("[ :< ] VUI LÒNG NHẬP SỐ NGUYÊN DƯƠNG!", xaibo_warning))
                continue

def xaibo_account_delay():
    while True:
        delay_input = input(xaibo_dep_trai(f"\n> Nhập delay giữa các tài khoản (ENTER để mặc định 5-10s): ", xaibo_link)).strip()
        if not delay_input:
            return "5,10"
        if ',' in delay_input:
            try:
                parts = delay_input.split(',')
                if len(parts) != 2:
                    raise ValueError
                min_delay = int(parts[0].strip())
                max_delay = int(parts[1].strip())
                if min_delay <= 0 or max_delay <= 0:
                    print(xaibo_dep_trai("[ :< ] THỜI GIAN PHẢI LỚN HƠN 0!", xaibo_warning))
                    continue
                if min_delay > max_delay:
                    min_delay, max_delay = max_delay, min_delay
                return f"{min_delay},{max_delay}"
            except ValueError:
                print(xaibo_dep_trai("[ :< ] ĐỊNH DẠNG KHÔNG HỢP LỆ!", xaibo_warning))
                continue
        else:
            try:
                delay = int(delay_input)
                if delay <= 0:
                    print(xaibo_dep_trai("[ :< ] THỜI GIAN PHẢI LỚN HƠN 0!", xaibo_warning))
                    continue
                return f"{delay},{delay}"
            except ValueError:
                print(xaibo_dep_trai("[ :< ] VUI LÒNG NHẬP SỐ NGUYÊN DƯƠNG!", xaibo_warning))
                continue

def xaibo_get_jobs(auth_token, t_param, account_id):
    url = urljoin("https://gateway.golike.net/", "api/advertising/publishers/instagram/jobs")
    headers = {"Authorization": f"Bearer {auth_token.replace('Bearer ', '')}", "T": t_param, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Content-Type": "application/json;charset=utf-8", "Accept": "application/json, text/plain, */*", "Connection": "keep-alive", "Accept-Encoding": "gzip, deflate"}
    params = {"instagram_account_id": account_id, "data": "null", "_": int(time.time() * 1000)}
    try:
        response = xaibo_session.get(url, headers=headers, params=params, timeout=3)
        if response.status_code == 200:
            job_data = response.json()
            if isinstance(job_data, dict) and job_data.get('message'):
                message = job_data.get('message', '').lower()
                if 'khóa' in message or 'banned' in message or 'block' in message or 'cấm' in message:
                    return "account_banned"
                if 'chưa có jobs mới' in message or 'nghỉ tay' in message or 'quay lại sau' in message:
                    time_match = re.search(r'(\d+)\s*(phút|p)', message)
                    if time_match:
                        return f"no_jobs_{time_match.group(1)}"
                    return "no_jobs_30"
                return "no_jobs"
            if isinstance(job_data, dict) and job_data.get('data'):
                data = job_data['data']
                if data and isinstance(data, dict) and data.get('id'):
                    return {'id': str(data.get('id', '')), 'type': data.get('type', ''), 'coin': int(data.get('coin', 0)), 'price_per_after_cost': int(data.get('price_per_after_cost', 0)), 'link': data.get('link', ''), 'created_at': data.get('created_at', ''), 'object_id': data.get('object_id', ''), 'comment_text': data.get('comment_text', '') if data.get('type') == 'comment' else None}
                return "no_jobs"
            return "no_jobs"
        if response.status_code == 400:
            try:
                error_data = response.json()
                if error_data.get('message'):
                    message = error_data['message'].lower()
                    if 'khóa' in message or 'banned' in message:
                        return "account_banned"
                    if "Hệ thống đang tính toán jobs" in message:
                        return "calculating_jobs"
                    if 'chưa có jobs mới' in message or 'nghỉ tay' in message:
                        return "no_jobs_30"
            except:
                pass
            return "no_jobs"
        return "no_jobs"
    except:
        return "no_jobs"

def xaibo_complete_job(auth_token, t_param, job_id, account_id):
    url = urljoin("https://gateway.golike.net/", "api/advertising/publishers/instagram/complete-jobs")
    headers = {"Authorization": f"Bearer {auth_token.replace('Bearer ', '')}", "T": t_param, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Content-Type": "application/json;charset=UTF-8", "Accept": "application/json, text/plain, */*"}
    json_data = {"instagram_users_advertising_id": int(job_id), "instagram_account_id": int(account_id), "async": True, "data": None}
    try:
        response = xaibo_session.post(url, headers=headers, json=json_data, timeout=3)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                coin_earned = result.get('coin', 0)
                if 'data' in result and 'prices' in result['data']:
                    coin_earned = result['data']['prices']
                return True, coin_earned
        return False, 0
    except:
        return False, 0

def xaibo_skip_job(auth_token, t_param, job_id, account_id, job_type, object_id=None):
    url = urljoin("https://gateway.golike.net/", "api/advertising/publishers/instagram/skip-jobs")
    headers = {"Authorization": f"Bearer {auth_token.replace('Bearer ', '')}", "T": t_param, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Content-Type": "application/json;charset=UTF-8", "Accept": "application/json, text/plain, */*", "X-Requested-With": "XMLHttpRequest", "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"', "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"', "Referer": ""}
    json_data = {"ads_id": int(job_id), "account_id": int(account_id), "type": job_type}
    if object_id and job_type in ['follow', 'like', 'comment', 'share']:
        json_data["object_id"] = object_id
    try:
        response = xaibo_session.post(url, headers=headers, json=json_data, timeout=8)
        return response.status_code == 200 and response.json().get('success', False)
    except:
        return False

def xaibo_prepare(auth_token, t_param, selected_accounts):
    prepared_accounts = []
    for i, account in enumerate(selected_accounts, 1):
        account_username = account.get('instagram_username', '')
        account_id = account.get('id', '')
        print(xaibo_dep_trai(f"[{i}/{len(selected_accounts)}]──────────────────> {account_username} <──────────────────", xaibo_error, xaibo_menu))
        saved_account = xaibo_lay_account(account_username)
        cookies = None
        if saved_account:
            current_cookies = saved_account.get('cookies', {})
            if current_cookies and xaibo_kiem_tra_cookie(current_cookies):
                print(xaibo_dep_trai(f"\n[{account_username}] Cookies hiện tại còn dùng được ({len(current_cookies)} cookies)", xaibo_success))
                cookies = current_cookies
                print(xaibo_dep_trai(f"\n Cookies của ", xaibo_menu) + xaibo_dep_trai(f"{account_username}:", xaibo_cookie))
                cookie_string = xaibo_format_cookie(cookies)
                for j in range(0, len(cookie_string), 150):
                    print(xaibo_dep_trai(cookie_string[j:j+150], xaibo_cookie))
                print("")
            else:
                print(xaibo_dep_trai(f"[{account_username}] Cookies hết hiệu lực, cần RESET", xaibo_input, xaibo_error))
                if saved_account.get('password'):
                    new_cookies = xaibo_dang_nhap(account_username, saved_account['password'])
                    if new_cookies:
                        cookies = new_cookies
                        xaibo_luu_account(account_username, saved_account['password'], new_cookies)
                        print(xaibo_dep_trai(f"\n Cookies của {account_username}:", xaibo_cookie))
                        cookie_string = xaibo_format_cookie(cookies)
                        for j in range(0, len(cookie_string), 150):
                            print(xaibo_dep_trai(cookie_string[j:j+150], xaibo_cookie))
                        print("")
        if not cookies:
            password = input(xaibo_dep_trai(f"[{account_username}] > Nhập mật khẩu: ", xaibo_input, xaibo_menu)).strip()
            if not password:
                print(xaibo_dep_trai(f"[{account_username}] Không có mật khẩu, tự bỏ qua...", xaibo_error))
                continue
            cookies = xaibo_dang_nhap(account_username, password)
            if not cookies:
                print(xaibo_dep_trai(f"[{account_username}] Lấy cookies thất bại, tự bỏ tài khoản này!", xaibo_error))
                continue
            print(xaibo_dep_trai(f"\n Cookies: {account_username}:", xaibo_cookie))
            cookie_string = xaibo_format_cookie(cookies)
            for j in range(0, len(cookie_string), 150):
                print(xaibo_dep_trai(cookie_string[j:j+150], xaibo_cookie))
            print("")
            xaibo_luu_account(account_username, password, cookies)
            time.sleep(2 + random.uniform(0, 0.002))
        prepared_accounts.append({'id': account_id, 'instagram_username': account_username, 'cookies': cookies})
        if i == len(selected_accounts) and len(selected_accounts) > 1:
            print(xaibo_dep_trai(f"\n[!] Đã có đầy đủ cookies cần thiết", xaibo_input, xaibo_error))
            for s in range(3, 0, -1):
                print(xaibo_dep_trai(f"[!] Vui lòng chờ {s:2d}s để setup xong ", xaibo_info, xaibo_error), end='\r')
                time.sleep(1 + random.uniform(0, 0.002))
            print(' ' * 30, end='\r')
            print("")
    return prepared_accounts

def xaibo_worker(auth_token, t_param, account, job_delay, account_index, total_accounts):
    global xaibo_stop
    account_id = account.get('id', '')
    account_username = account.get('instagram_username', '')
    cookies = account.get('cookies', {})
    xaibo_cap_nhat(account_username, "đang lấy job...", "", "", 0, 0, 0)
    running = True
    consecutive_errors = 0
    job_count = 0
    total_earned = 0
    last_cookie_check = time.time()
    cookie_check_interval = 300
    calculating_count = 0
    follow_fail_count = 0
    no_job_count = 0
    banned = False
    wait_until = 0
    jobs_since_last_nurture = 0
    nurture_threshold = random.randint(3, 5)
    while running and not xaibo_stop and not banned:
        try:
            if wait_until > time.time():
                remaining = int(wait_until - time.time())
                minutes = remaining // 60
                seconds = remaining % 60
                if minutes > 0:
                    xaibo_cap_nhat(account_username, f'hết job, chờ {minutes} phút {seconds} giây...', "", "", job_count, 0, total_earned)
                else:
                    xaibo_cap_nhat(account_username, f'hết job, chờ {seconds} giây...', "", "", job_count, 0, total_earned)
                time.sleep(5 + random.uniform(0, 0.002))
                continue
            if time.time() - last_cookie_check > cookie_check_interval:
                if not xaibo_kiem_tra_cookie(cookies):
                    new_cookies = xaibo_refresh_cookie(account_username)
                    if new_cookies:
                        cookies = new_cookies
                        account['cookies'] = new_cookies
                last_cookie_check = time.time()
            job = xaibo_get_jobs(auth_token, t_param, account_id)
            if job == "account_banned":
                banned = True
                xaibo_cap_nhat(account_username, "❌ TÀI KHOẢN BỊ KHÓA/CẤM", "", "", job_count, 0, total_earned, is_delay_message=True)
                break
            if isinstance(job, str) and job.startswith("no_jobs_"):
                try:
                    minutes = int(job.split('_')[2])
                    wait_until = time.time() + (minutes * 60)
                    xaibo_cap_nhat(account_username, f'hết job, chờ {minutes} phút...', "", "", job_count, 0, total_earned)
                except:
                    wait_until = time.time() + (30 * 60)
                    xaibo_cap_nhat(account_username, 'hết job, chờ 30 phút...', "", "", job_count, 0, total_earned)
                continue
            if job == "calculating_jobs":
                calculating_count += 1
                if calculating_count == 1:
                    xaibo_cap_nhat(account_username, "đang tính toán jobs...", "", "", job_count, 0, total_earned)
                time.sleep(2 + random.uniform(0, 0.002))
                continue
            if job == "no_jobs":
                no_job_count += 1
                if no_job_count % 6 == 0:
                    xaibo_cap_nhat(account_username, "không có job, đang chờ...", "", "", job_count, 0, total_earned)
                time.sleep(5 + random.uniform(0, 0.002))
                continue
            if not job or not isinstance(job, dict):
                time.sleep(2 + random.uniform(0, 0.002))
                continue
            no_job_count = 0
            calculating_count = 0
            if job.get('type') == 'comment':
                xaibo_skip_job(auth_token, t_param, job['id'], account_id, job['type'], job.get('object_id'))
                time.sleep(1 + random.uniform(0, 0.002))
                continue
            job_count += 1
            jobs_since_last_nurture += 1
            if jobs_since_last_nurture >= nurture_threshold:
                nurture_duration = random.randint(30, 45)
                xaibo_cap_nhat(account_username, f' Tiến hành NUÔI ({nurture_duration}s)...', '', '', job_count, 0, total_earned)
                posts_viewed = xaibo_scroll_feed(cookies, nurture_duration)
                xaibo_cap_nhat(account_username, f'Nuôi xong ({posts_viewed} bài viết)', '', '', job_count, 0, total_earned)
                jobs_since_last_nurture = 0
                nurture_threshold = random.randint(3, 5)
                time.sleep(random.uniform(1, 2))
            is_random_delay = isinstance(job_delay, str) and ',' in job_delay
            if is_random_delay:
                min_d, max_d = map(int, job_delay.split(','))
                current_delay = random.randint(min_d, max_d)
            else:
                current_delay = job_delay
            job_type = job.get('type', 'unknown')
            job_reward = job.get('price_per_after_cost', 0)
            object_id = job.get('object_id', '')
            job_link = job.get('link', '')
            xaibo_cap_nhat(account_username, f'đang {job_type}', job_link, '', job_count, job_reward, total_earned)
            action_success = False
            if job_type == 'follow' and object_id:
                target_username = None
                if not object_id.isdigit():
                    target_username = object_id
                else:
                    if job_link and 'instagram.com/' in job_link:
                        match = re.search(r'instagram\.com/([^/?]+)', job_link)
                        if match:
                            target_username = match.group(1)
                if target_username:
                    action_success = xaibo_follow(cookies, target_username, account_username)
                    if action_success:
                        follow_fail_count = 0
                        xaibo_cap_nhat(account_username, f'follow {target_username} thành công', job_link, '', job_count, job_reward, total_earned)
                    else:
                        follow_fail_count += 1
                        xaibo_cap_nhat(account_username, f'follow thất bại', job_link, '', job_count, job_reward, total_earned)
                else:
                    action_success = False
            elif job_type == 'like' and object_id:
                action_success = xaibo_like(cookies, object_id)
                if action_success:
                    xaibo_cap_nhat(account_username, 'like thành công', job_link, '', job_count, job_reward, total_earned)
                else:
                    xaibo_cap_nhat(account_username, 'like thất bại', job_link, '', job_count, job_reward, total_earned)
            if not action_success:
                xaibo_skip_job(auth_token, t_param, job['id'], account_id, job_type, object_id)
                consecutive_errors += 1
                if consecutive_errors >= 3:
                    xaibo_cap_nhat(account_username, '3 lỗi liên tiếp, tạm dừng 5s', "", "", job_count, 0, total_earned)
                    time.sleep(5 + random.uniform(0, 0.002))
                    consecutive_errors = 0
                continue
            else:
                consecutive_errors = 0
            if current_delay > 0:
                for remaining in range(current_delay, 0, -1):
                    if xaibo_stop:
                        break
                    xaibo_cap_nhat(account_username, f'chờ {remaining}s', job_link, '', job_count, job_reward, total_earned)
                    time.sleep(1 + random.uniform(0, 0.002)) # Add toolviewV2 style random delay here
            time.sleep(random.uniform(2, 4))
            success, earned = xaibo_complete_job(auth_token, t_param, job['id'], account_id)
            if success:
                total_earned += earned
                xaibo_cap_nhat(account_username, f'+{earned}đ', job_link, '', job_count, earned, total_earned)
            time.sleep(1 + random.uniform(0, 0.002))
        except Exception as e:
            traceback.print_exc()
            consecutive_errors += 1
            if consecutive_errors >= 3:
                time.sleep(5 + random.uniform(0, 0.002))
                consecutive_errors = 0
            time.sleep(1 + random.uniform(0, 0.002))
    if banned:
        xaibo_cap_nhat(account_username, '❌ ĐÃ DỪNG - TÀI KHOẢN BỊ KHÓA', "", "", job_count, 0, total_earned, is_delay_message=True)
    else:
        xaibo_cap_nhat(account_username, f'đã dừng | tổng: {total_earned}đ', "", "", job_count, 0, total_earned)
    return True

def xaibo_chay_nhieu(auth_token, t_param, prepared_accounts, job_delay, account_delay):
    global xaibo_stop, xaibo_threads, xaibo_displays, xaibo_order
    xaibo_stop = False
    xaibo_threads = []
    xaibo_displays = {}
    xaibo_order = []
    if ',' in account_delay:
        min_d, max_d = map(int, account_delay.split(','))
        is_random = True
    else:
        min_d = max_d = int(account_delay)
        is_random = False
    xaibo_xoa_man()
    xaibo_hien_thi()
    for i, account in enumerate(prepared_accounts):
        account_username = account.get('instagram_username', '')
        xaibo_order.append(account_username)
        if i == 0:
            xaibo_displays[account_username] = {'start_time': time.time(), 'job_count': 0, 'total_earned': 0, 'current_action': 'đang lấy job...', 'current_link': '', 'current_type': ''}
            print(xaibo_dep_trai(f"[{account_username}] | 0 giây - 0 jobs | đang lấy job...", xaibo_action))
        else:
            delay_text = f'chờ {min_d}-{max_d}s trước khi bắt đầu' if is_random else f'chờ {min_d}s trước khi bắt đầu'
            xaibo_displays[account_username] = {'delay_message': delay_text}
            print(xaibo_dep_trai(f"[{account_username}] | {delay_text}", xaibo_delay))
    print("")
    print(xaibo_dep_trai("─" * 80, xaibo_menu))
    print(xaibo_dep_trai(" Enter để tạm dừng", xaibo_info))
    sys.stdout.flush()
    def check_global_stop():
        global xaibo_stop
        input()
        xaibo_stop = True
        sys.stdout.write("\033[2K")
        sys.stdout.write("\r")
        print(xaibo_dep_trai(" Đang dừng all tài khoản", xaibo_warning))
        sys.stdout.flush()
    stop_thread = threading.Thread(target=check_global_stop)
    stop_thread.daemon = True
    stop_thread.start()
    thread = threading.Thread(target=xaibo_worker, args=(auth_token, t_param, prepared_accounts[0], job_delay, 1, len(prepared_accounts)))
    thread.daemon = True
    thread.start()
    xaibo_threads.append(thread)
    for i in range(1, len(prepared_accounts)):
        if xaibo_stop:
            break
        account = prepared_accounts[i]
        account_username = account.get('instagram_username', '')
        current_delay = random.randint(min_d, max_d) if is_random else min_d
        def start_with_delay(acc, delay, idx):
            account_username = acc.get('instagram_username', '')
            for remaining in range(delay, 0, -1):
                if xaibo_stop:
                    return
                with xaibo_lock:
                    if account_username in xaibo_displays:
                        xaibo_displays[account_username]['delay_message'] = f'chờ {remaining}s trước khi bắt đầu'
                        line_number = xaibo_order.index(account_username) + 9
                        sys.stdout.write("\033[s")
                        sys.stdout.write(f"\033[{line_number};0H")
                        sys.stdout.write("\033[K")
                        print(xaibo_dep_trai(f"[{account_username}] | chờ {remaining}s trước khi bắt đầu", xaibo_delay))
                        sys.stdout.write("\033[u")
                        sys.stdout.flush()
                time.sleep(1 + random.uniform(0, 0.002))
            if xaibo_stop:
                return
            with xaibo_lock:
                if account_username in xaibo_displays:
                    if 'delay_message' in xaibo_displays[account_username]:
                        del xaibo_displays[account_username]['delay_message']
                    xaibo_displays[account_username].update({'start_time': time.time(), 'job_count': 0, 'total_earned': 0, 'current_action': 'đang lấy job...', 'current_link': '', 'current_type': ''})
                    line_number = xaibo_order.index(account_username) + 9
                    sys.stdout.write("\033[s")
                    sys.stdout.write(f"\033[{line_number};0H")
                    sys.stdout.write("\033[K")
                    print(xaibo_dep_trai(f"[{account_username}] | 0 giây - 0 jobs | đang lấy job...", xaibo_action))
                    sys.stdout.write("\033[u")
                    sys.stdout.flush()
            t = threading.Thread(target=xaibo_worker, args=(auth_token, t_param, acc, job_delay, idx+1, len(prepared_accounts)))
            t.daemon = True
            t.start()
            xaibo_threads.append(t)
        delay_thread = threading.Thread(target=start_with_delay, args=(account, current_delay, i))
        delay_thread.daemon = True
        delay_thread.start()
    for thread in xaibo_threads:
        thread.join()

def xaibo_scroll_feed(cookies, scroll_duration=30):
    try:
        user_agent = cookies.get('useragent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        try:
            if len(user_agent) > 50 and '=' in user_agent:
                decoded_ua = base64.b64decode(user_agent).decode('utf-8')
                user_agent = decoded_ua
        except:
            pass
        headers = {'User-Agent': user_agent, 'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': cookies.get('csrftoken', ''), 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://www.instagram.com/'}
        scroll_session = requests.Session()
        scroll_session.cookies.update(cookies)
        scroll_start_time = time.time()
        posts_viewed = 0
        while time.time() - scroll_start_time < scroll_duration:
            data = {'route_urls[0]': '/', 'routing_namespace': 'igx_www', '__a': '1', '__d': 'www', '__user': '0', '__req': str(random.randint(1, 9)), '__hs': '20521.HYP:instagram_web_pkg.2.1...0'}
            fb_dtsg = cookies.get('fb_dtsg', '')
            lsd = cookies.get('lsd', '')
            if fb_dtsg:
                data['fb_dtsg'] = fb_dtsg
            if lsd:
                data['lsd'] = lsd
            try:
                response = scroll_session.post('https://www.instagram.com/ajax/bulk-route-definitions/', headers=headers, data=data, timeout=5)
                if response.status_code == 200:
                    posts_viewed += 1
                    time.sleep(random.uniform(0.7, 1.4))
            except:
                time.sleep(random.uniform(1, 2))
        return posts_viewed
    except Exception as e:
        print(xaibo_dep_trai(f"[SCROLL FEED] ❌ LỖI: {str(e)}", xaibo_error))
        return 0

def xaibo_main():
    config = xaibo_doc_cfg()
    while True:
        try:
            xaibo_xoa_man()
            xaibo_hien_thi()
            auth_token = config.get('auth_token', '').strip()
            if not auth_token:
                print(xaibo_dep_trai("[ :> ] NHẬP AUTH TOKEN CỦA BẠN: ", xaibo_input))
                auth_token = input().strip()
                if not auth_token:
                    print(xaibo_dep_trai("[ :< ] AUTH TOKEN KHÔNG ĐƯỢC ĐỂ TRỐNG!", xaibo_error))
                    time.sleep(2 + random.uniform(0, 0.002))
                    continue
                config['auth_token'] = auth_token
                xaibo_ghi_cfg(config)
            t_param = config.get('t_param', '').strip()
            if not t_param:
                print(xaibo_dep_trai("[ :> ] NHẬP T PARAM CỦA BẠN: ", xaibo_input))
                t_param = input().strip()
                if not t_param:
                    print(xaibo_dep_trai("[ :< ] T PARAM KHÔNG ĐƯỢC ĐỂ TRỐNG!", xaibo_error))
                    time.sleep(2 + random.uniform(0, 0.002))
                    continue
                config['t_param'] = t_param
                xaibo_ghi_cfg(config)
            account_data = xaibo_api_data(auth_token, t_param)
            if not account_data or 'data' not in account_data:
                print(xaibo_dep_trai("[ :< ] KHÔNG THỂ LẤY THÔNG TIN TÀI KHOẢN!", xaibo_error))
                time.sleep(2 + random.uniform(0, 0.002))
                continue
            user_data = account_data['data']
            user_name = user_data.get('name', '')
            user_coin = user_data.get('coin', 0)
            print(xaibo_dep_trai("\n╭────────────────────────────────────╮", xaibo_menu))
            print(xaibo_dep_trai("│" + " "*14 + "TÀI KHOẢN" + " "*13 + "│", xaibo_menu))
            print(xaibo_dep_trai("│────────────────────────────────────│", xaibo_menu))
            print("")
            print(xaibo_dep_trai("[ <3 ] Tài khoản: " + f"{user_name}", xaibo_info))
            print(xaibo_dep_trai("[ <3 ] Số coin: " + f"{user_coin} VNĐ", xaibo_coin))
            print("")
            print(xaibo_dep_trai("╰───────────────────────────────────╯", xaibo_menu))
            accounts_data = xaibo_instagram_accounts(auth_token, t_param)
            if not accounts_data:
                print(xaibo_dep_trai("[ :< ] KHÔNG THỂ LẤY DANH SÁCH TÀI KHOẢN INSTAGRAM!", xaibo_error))
                time.sleep(2 + random.uniform(0, 0.002))
                continue
            accounts = xaibo_hien_thi_accounts(accounts_data)
            if not accounts:
                print(xaibo_dep_trai("[ :< ] KHÔNG CÓ TÀI KHOẢN INSTAGRAM NÀO ĐỂ LÀM VIỆC!", xaibo_error))
                time.sleep(2 + random.uniform(0, 0.002))
                continue
            selected_accounts = xaibo_chon_account(accounts)
            if not selected_accounts:
                continue
            job_delay = xaibo_job_delay()
            prepared_accounts = xaibo_prepare(auth_token, t_param, selected_accounts)
            if not prepared_accounts:
                print(xaibo_dep_trai("\n❌ KHÔNG CÓ TÀI KHOẢN NÀO SẴN SÀNG ĐỂ XỬ LÝ!", xaibo_error))
                time.sleep(2 + random.uniform(0, 0.002))
                continue
            account_delay = None
            if len(prepared_accounts) > 1:
                account_delay = xaibo_account_delay()
            while True:
                xaibo_xoa_man()
                xaibo_hien_thi()
                if len(prepared_accounts) == 1:
                    account = prepared_accounts[0]
                    account_username = account.get('instagram_username', '')
                    global xaibo_displays, xaibo_order, xaibo_stop
                    xaibo_displays = {}
                    xaibo_order = []
                    xaibo_stop = False
                    def run_single():
                        xaibo_worker(auth_token, t_param, account, job_delay, 1, 1)
                    thread = threading.Thread(target=run_single)
                    thread.daemon = True
                    thread.start()
                    print(xaibo_dep_trai("💡 NHẤN ENTER LẦN 1 ĐỂ DỪNG", xaibo_info))
                    print(xaibo_dep_trai("💡 NHẤN ENTER LẦN 2 ĐỂ CHẠY LẠI", xaibo_info))
                    print("")
                    input()
                    xaibo_stop = True
                    thread.join()
                    print(xaibo_dep_trai("\n✅ ĐÃ DỪNG XỬ LÝ", xaibo_success))
                    print(xaibo_dep_trai("🔄 NHẤN ENTER ĐỂ CHẠY LẠI, 'Q' ĐỂ QUAY LẠI MENU CHÍNH: ", xaibo_info))
                    choice = input().strip().lower()
                    if choice == 'q':
                        break
                    else:
                        continue
                elif len(prepared_accounts) > 1:
                    while True:
                        xaibo_chay_nhieu(auth_token, t_param, prepared_accounts, job_delay, account_delay)
                        print(xaibo_dep_trai("Enter để tiếp tục, hoặc 'q' để thoát: ", xaibo_info))
                        choice = input().strip().lower()
                        if choice == 'q':
                            break
                    else:
                        continue
        except KeyboardInterrupt:
            print(xaibo_dep_trai("\n[ :< ] ĐÃ DỪNG CHƯƠNG TRÌNH!", xaibo_warning))
            break
        except Exception as e:
            print(xaibo_dep_trai(f"[ :< ] LỖI: {str(e)}", xaibo_error))
            traceback.print_exc()
            time.sleep(3 + random.uniform(0, 0.002))

if __name__ == "__main__":
    xaibo_main()