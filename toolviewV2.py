import aiohttp
import asyncio
import random
import requests
import re
import time
import secrets
import os
import signal
import sys
from hashlib import md5
from time import time as T
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CÁC HÀM TẠO MÀU GRADIENT TỪ FBTTC.PY ---
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


@dataclass
class DeviceInfo:
    model: str
    version: str
    api_level: int

class DeviceGenerator:
    DEVICES = [
        DeviceInfo("Pixel 4", "11", 30),
        DeviceInfo("Pixel 4a", "11", 30),
        DeviceInfo("Pixel 5", "11", 30),
        DeviceInfo("Pixel 5a", "12", 31),
        DeviceInfo("Pixel 6", "12", 31),
        DeviceInfo("Pixel 6a", "13", 33),
        DeviceInfo("Pixel 7", "13", 33),
        DeviceInfo("Pixel 7a", "14", 34),
        DeviceInfo("Pixel 8", "14", 34),
        DeviceInfo("Samsung Galaxy S20", "11", 30),
        DeviceInfo("Samsung Galaxy S21", "12", 31),
        DeviceInfo("Samsung Galaxy S21 FE", "13", 33),
        DeviceInfo("Samsung Galaxy S22", "13", 33),
        DeviceInfo("Samsung Galaxy S23", "14", 34),
        DeviceInfo("Samsung Galaxy A52", "12", 31),
        DeviceInfo("Samsung Galaxy A53", "13", 33),
        DeviceInfo("Samsung Galaxy A54", "14", 34),
        DeviceInfo("Xiaomi Mi 10", "11", 30),
        DeviceInfo("Xiaomi Mi 11", "12", 31),
        DeviceInfo("Xiaomi 11T", "12", 31),
        DeviceInfo("Xiaomi 12", "13", 33),
        DeviceInfo("Xiaomi 13", "14", 34),
        DeviceInfo("Redmi Note 10", "11", 30),
        DeviceInfo("Redmi Note 11", "12", 31),
        DeviceInfo("Redmi Note 12", "13", 33),
        DeviceInfo("Oppo Reno 6", "11", 30),
        DeviceInfo("Oppo Reno 7", "12", 31),
        DeviceInfo("Oppo Reno 8", "13", 33),
        DeviceInfo("Oppo Reno 10", "14", 34),
        DeviceInfo("Oppo A74", "11", 30),
        DeviceInfo("Oppo A96", "12", 31),
        DeviceInfo("Vivo Y20", "11", 30),
        DeviceInfo("Vivo Y33s", "12", 31),
        DeviceInfo("Vivo V25", "13", 33),
        DeviceInfo("Vivo V27", "14", 34),
        DeviceInfo("Realme 8", "11", 30),
        DeviceInfo("Realme 9 Pro", "12", 31),
        DeviceInfo("Realme GT Neo 3", "13", 33),
        DeviceInfo("Realme GT 5", "14", 34),
        DeviceInfo("OnePlus 8", "11", 30),
        DeviceInfo("OnePlus 9", "12", 31),
        DeviceInfo("OnePlus 10 Pro", "13", 33),
        DeviceInfo("OnePlus 11", "14", 34),
        DeviceInfo("Asus ROG Phone 5", "11", 30),
        DeviceInfo("Asus ROG Phone 6", "12", 31),
        DeviceInfo("Asus ROG Phone 7", "13", 33),
        DeviceInfo("Sony Xperia 5 II", "11", 30),
        DeviceInfo("Sony Xperia 1 III", "12", 31),
        DeviceInfo("Sony Xperia 1 V", "14", 34),
    ]
    
    @classmethod
    def random_device(cls) -> DeviceInfo:
        return random.choice(cls.DEVICES)

class Signature:
    KEY = [0xDF, 0x77, 0xB9, 0x40, 0xB9, 0x9B, 0x84, 0x83, 0xD1, 0xB9, 
           0xCB, 0xD1, 0xF7, 0xC2, 0xB9, 0x85, 0xC3, 0xD0, 0xFB, 0xC3]
    
    def __init__(self, params: str, data: str, cookies: str):
        self.params = params
        self.data = data
        self.cookies = cookies
    
    def _md5_hash(self, data: str) -> str:
        return md5(data.encode()).hexdigest()
    
    def _reverse_byte(self, n: int) -> int:
        return int(f"{n:02x}"[1:] + f"{n:02x}"[0], 16)
    
    def generate(self) -> Dict[str, str]:
        g = self._md5_hash(self.params)
        g += self._md5_hash(self.data) if self.data else "0" * 32
        g += self._md5_hash(self.cookies) if self.cookies else "0" * 32
        g += "0" * 32
        
        unix_timestamp = int(T())
        payload = []
        
        for i in range(0, 12, 4):
            chunk = g[8 * i:8 * (i + 1)]
            for j in range(4):
                payload.append(int(chunk[j * 2:(j + 1) * 2], 16))
        
        payload.extend([0x0, 0x6, 0xB, 0x1C])
        payload.extend([
            (unix_timestamp & 0xFF000000) >> 24,
            (unix_timestamp & 0x00FF0000) >> 16,
            (unix_timestamp & 0x0000FF00) >> 8,
            (unix_timestamp & 0x000000FF)
        ])
        
        encrypted = [a ^ b for a, b in zip(payload, self.KEY)]
        
        for i in range(0x14):
            C = self._reverse_byte(encrypted[i])
            D = encrypted[(i + 1) % 0x14]
            F = int(bin(C ^ D)[2:].zfill(8)[::-1], 2)
            H = ((F ^ 0xFFFFFFFF) ^ 0x14) & 0xFF
            encrypted[i] = H
        
        signature = "".join(f"{x:02x}" for x in encrypted)
        
        return {
            "X-Gorgon": "840280416000" + signature,
            "X-Khronos": str(unix_timestamp)
        }

class OptimizedTikTokViewBot:
    def __init__(self):
        self.count = 0
        self.start_time = 0
        self.is_running = False
        self.session = None
        self.successful_requests = 0
        self.failed_requests = 0
        self.peak_speed = 0
        
    async def init_session(self):
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(
            limit=0,
            limit_per_host=0,
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={'User-Agent': 'com.ss.android.ugc.trill/400304'},
            cookie_jar=aiohttp.DummyCookieJar()
        )
    
    async def close_session(self):
        if self.session:
            await self.session.close()
    
    def get_video_id(self, url: str) -> Optional[str]:
        try:
            patterns_url = [
                r'/video/(\d+)',
                r'tiktok\.com/@[^/]+/(\d+)',
                r'(\d{18,19})'
            ]
            
            for pattern in patterns_url:
                match = re.search(pattern, url)
                if match:
                    video_id = match.group(1)
                    logger.info(f" Found Video ID from URL: {video_id}")
                    return video_id
            
            response = requests.get(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            match = re.search(r'/video/(\d+)', response.url)
            if match:
                video_id = match.group(1)
                logger.info(f" Found Video ID from Redirect URL: {video_id}")
                return video_id
        except Exception as e:
            logger.error(f" Failed to get video ID: {e}")
        return None

    def generate_request_data(self, video_id: str) -> Tuple[str, Dict, Dict, Dict]:
        device = DeviceGenerator.random_device()
        fp = secrets.token_hex(16)
        iid = str(random.randint(7000000000000000000, 7400000000000000000))
        did = str(random.randint(7000000000000000000, 7400000000000000000))
        
        url = (
            f"https://api16-core-c-useast1a.tiktokv.com/aweme/v1/aweme/stats/?"
            f"action_time={int(time.time())}&a_version=1.2.3&channel=googleplay&"
            f"device_type={device.model.replace(' ', '%20')}&device_platform=android&"
            f"os_version={device.version}&version_code=400304&app_name=trill&"
            f"device_id={did}&install_id={iid}&aid=1180&update_version_code=400304&"
            f"chrome_version=42.0.2311.135&os_api={device.api_level}&"
            f"manifest_version_code=400304&fp={fp}&current_region=US&"
            f"import_item_id={video_id}"
        )
        data = {
            "item_id": video_id,
            "play_delta": 1,
            "action_time": int(time.time())
        }
        cookies = {"sessionid": secrets.token_hex(16)}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "com.ss.android.ugc.trill/400304",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive"
        }
        return url, data, cookies, headers

    async def send_view_request(self, video_id: str, semaphore: asyncio.Semaphore) -> bool:
        async with semaphore:
            for attempt in range(2):
                try:
                    url, data, cookies, base_headers = self.generate_request_data(video_id)
                    sig = Signature(url.split('?')[1], str(data), str(cookies)).generate()
                    headers = {**base_headers, **sig}
                    async with self.session.post(
                        url, data=data, headers=headers, cookies=cookies, ssl=False
                    ) as response:
                        if response.status == 200:
                            self.count += 1
                            self.successful_requests += 1
                            return True
                        else:
                            if attempt == 0:
                                await asyncio.sleep(0.01)
                                continue
                            self.failed_requests += 1
                            return False
                except Exception as e:
                    if attempt == 0:
                        await asyncio.sleep(0.01)
                        continue
                    self.failed_requests += 1
                    return False

    async def view_sender(self, video_id: str, task_id: int, semaphore: asyncio.Semaphore):
        consecutive_success = 0
        base_delay = 0.001
        while self.is_running:
            success = await self.send_view_request(video_id, semaphore)
            if success:
                consecutive_success += 1
                if consecutive_success > 100:
                    delay = base_delay * 0.5
                elif consecutive_success > 50:
                    delay = base_delay * 0.7
                else:
                    delay = base_delay
            else:
                consecutive_success = 0
                delay = base_delay * 2
                
            current_speed = self.calculate_stats()["views_per_second"]
            if current_speed > 500:
                delay *= 1.5
            elif current_speed > 1000:
                delay *= 2
            await asyncio.sleep(delay + random.uniform(0, 0.002))

    def calculate_stats(self) -> Dict[str, float]:
        elapsed = time.time() - self.start_time
        views_per_second = self.count / elapsed if elapsed > 0 else 0
        if views_per_second > self.peak_speed:
            self.peak_speed = views_per_second
            
        return {
            "total_views": self.count,
            "views_per_second": views_per_second,
            "peak_speed": self.peak_speed,
            "success_rate": (self.successful_requests / (self.successful_requests + self.failed_requests)) * 100 if (self.successful_requests + self.failed_requests) > 0 else 100,
            "elapsed_time": elapsed
        }

    def display_stats(self):
        stats = self.calculate_stats()
        print("\n" + "═" * 60)
        print("📊 BOT SESSION STATS")
        print("═" * 60)
        print(f" Total Views Sent : {stats['total_views']:,}")
        print(f" Total Time Spend : {stats['elapsed_time']:.1f}s")
        print(f" Average Speed    : {stats['views_per_second']:.1f} views/s")
        print(f" Peak Speed       : {stats['peak_speed']:.1f} views/s")
        print(f" Success Rate     : {stats['success_rate']:.1f}%")

    async def run_optimized(self, video_url: str):
        video_id = self.get_video_id(video_url)
        if not video_id:
            print("❌ Invalid TikTok Video URL or could not extract Video ID!")
            return
            
        print(f"\n🚀 Bot initialising...")
        print(f"📌 Video ID Target: {video_id}")
        
        cpu_count = os.cpu_count() or 4
        optimal_workers = min(3000, cpu_count * 250)
        print(f"⚡ System Performance Tuning: Multi-threaded async task for your device {optimal_workers:,}")
        await asyncio.sleep(2)
        
        await self.init_session()
        self.is_running = True
        self.start_time = time.time()
        
        semaphore = asyncio.Semaphore(min(1000, optimal_workers // 3))
        tasks = []
        try:
            for i in range(optimal_workers):
                task = asyncio.create_task(self.view_sender(video_id, i, semaphore))
                tasks.append(task)
            logger.info(f" {len(tasks):,} tasks initiated successfully")
            
            last_display = 0
            while self.is_running:
                await asyncio.sleep(0.5)
                current_time = time.time()
                if current_time - last_display >= 2:
                    stats = self.calculate_stats()
                    print(
                        f"\r Spend: {stats['total_views']:,} | "
                        f"Speed: {stats['views_per_second']:.1f} view/s | "
                        f"Peak: {stats['peak_speed']:.1f} view/s | "
                        f"Nice: {stats['success_rate']:.1f}% | "
                        f"Time: {stats['elapsed_time']:.1f}s", end="", flush=True
                    )
                    last_display = current_time
        except KeyboardInterrupt:
            print("\n\nStop requested by user")
        except Exception as e:
            logger.error(f" Run error: {e}")
        finally:
            self.is_running = False
            logger.info("stopping tasks...")
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            await self.close_session()
            self.display_stats()

def signal_handler(sig, frame):
    print("\n\nStop requested!")
    sys.exit(0)

# --- THAY THẾ BANNER CŨ BẰNG BANNER MỚI TỪ FBTTC.PY ---
def display_banner():
    os.system("cls" if os.name == "nt" else "clear")
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

def get_user_input() -> Optional[str]:
    video_url = input("🔗 Please enter TikTok Video URL: ").strip()
    if not video_url:
        print(" ❌ URL cannot be empty!")
        return None
    if not video_url.startswith(('http://', 'https://')):
        print(" ❌ Invalid URL format! Please include http:// or https://")
        return None
    
    print("\nChecking internet connection...", end="")
    try:
        requests.get("https://www.google.com", timeout=5)
        print("  Connected")
    except:
        print("  No internet connection!")
        return None
    return video_url

async def main_optimized():
    display_banner()
    signal.signal(signal.SIGINT, signal_handler)
    video_url = get_user_input()
    if not video_url:
        return
    print("\nHi!.")
    bot = OptimizedTikTokViewBot()
    try:
        await bot.run_optimized(video_url)
    except Exception as e:
        logger.error(f" Bot execution error: {e}")
        print(f"\n error occurred: {e}")
    finally:
        await bot.close_session()
    print("\n" + "═" * 60)
    print("🎉 BOT SESSION COMPLETED")
    print("═" * 60)
    print("Thank you for using Service")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main_optimized())