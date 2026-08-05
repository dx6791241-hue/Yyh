#!/usr/bin/env python3
"""
Henxi Quest CLI — Discord Auto Quest
"""
import os, sys, sqlite3, json, threading, time, random, base64, requests, re, traceback
from datetime import datetime, timezone
from pathlib import Path

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Dummy:
        def __getattr__(self, n): return ""
    Fore = Style = Dummy()


def rgb_to_ansi(r, g, b):
    return f"[38;2;{r};{g};{b}m"

def gradient_3(text):
    start = (0, 255, 0)
    end   = (0, 128, 255)
    result = ""
    for i, char in enumerate(text):
        t = i / (len(text) - 1 if len(text) > 1 else 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        result += rgb_to_ansi(r, g, b) + char
    return result + "[0m"

def gradient_2(text):
    start_color = (255, 87, 34)
    mid_color   = (255, 20, 147)
    end_color   = (255, 255, 0)
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
    return result + "[0m"

def gradient_1(text):
    start_color = (0, 128, 255)
    mid_color   = (0, 255, 255)
    end_color   = (255, 255, 255)
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
    return result + "[0m"


# ── Config ────────────────────────────────────────────────────────────────────
DB_PATH = Path("bot_data.db")
API_BASE = "https://discord.com/api/v9"
POLL_INTERVAL = 90
HEARTBEAT_INTERVAL = 20
VIDEO_SPEED = 7
AUTO_ACCEPT = True
DEBUG = False

SUPPORTED_TASKS = [
    "WATCH_VIDEO", "WATCH_VIDEO_ON_MOBILE",
    "PLAY_ON_DESKTOP", "PLAY_ON_DESKTOP_V2",
    "STREAM_ON_DESKTOP", "PLAY_ACTIVITY",
]

# ── Database ──────────────────────────────────────────────────────────────────
def get_conn():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL, username TEXT, added_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS quest_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL, quest_name TEXT, action TEXT NOT NULL, created_at TEXT NOT NULL
            );
        """)
        try:
            cols = [r[1] for r in conn.execute("PRAGMA table_info(quest_log)").fetchall()]
            if "username" not in cols:
                conn.execute("DROP TABLE IF EXISTS quest_log")
                conn.execute("""CREATE TABLE quest_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL,
                    quest_name TEXT, action TEXT NOT NULL, created_at TEXT NOT NULL)""")
        except Exception:
            pass
        conn.commit()

def add_account(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    try:
        r = requests.get(f"{API_BASE}/users/@me", headers=headers, timeout=15)
        if r.status_code != 200:
            return {"success": False, "error": "Token khong hop le."}
        u = r.json()
        user_id, username = u.get("id"), u.get("username", "Unknown")
        now = datetime.now(timezone.utc).isoformat()
        with get_conn() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO accounts (user_id, username, added_at) VALUES (?,?,?)",
                (user_id, username, now),
            )
            conn.commit()
        return {"success": True, "user_id": user_id, "username": username}
    except Exception as e:
        return {"success": False, "error": str(e)}

def log_quest(username, quest_name, action):
    try:
        now = datetime.now(timezone.utc).isoformat()
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO quest_log (username, quest_name, action, created_at) VALUES (?,?,?,?)",
                (username, quest_name, action, now),
            )
            conn.commit()
    except Exception:
        pass

# ── Helpers ───────────────────────────────────────────────────────────────────
def _get(d, *keys):
    if d is None: return None
    for k in keys:
        if k in d: return d[k]
    return None

def parse_iso(s):
    if not s: return None
    try:
        s = str(s).replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None

def fetch_latest_build_number():
    FALLBACK = 504649
    try:
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        r = requests.get("https://discord.com/app", headers={"User-Agent": ua}, timeout=15)
        if r.status_code != 200: return FALLBACK
        scripts = re.findall(r"/assets/([a-f0-9]+)\.js", r.text)
        if not scripts: return FALLBACK
        for asset_hash in scripts[-5:]:
            try:
                ar = requests.get(f"https://discord.com/assets/{asset_hash}.js", headers={"User-Agent": ua}, timeout=15)
                m = re.search(r'buildNumber["\s:]+["\s]*(\d{5,7})', ar.text)
                if m: return int(m.group(1))
            except Exception:
                continue
    except Exception:
        pass
    return FALLBACK

def make_super_properties(build_number):
    obj = {
        "os": "Windows", "browser": "Discord Client", "release_channel": "stable",
        "client_version": "1.0.9175", "os_version": "10.0.26100", "os_arch": "x64",
        "app_arch": "x64", "system_locale": "en-US",
        "browser_user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) discord/1.0.9175 Chrome/128.0.6613.186 "
            "Electron/32.2.7 Safari/537.36"
        ),
        "browser_version": "32.2.7",
        "client_build_number": build_number,
        "native_build_number": 59498,
        "client_event_source": None,
    }
    return base64.b64encode(json.dumps(obj, separators=(",", ":")).encode()).decode()

class WorkerAPI:
    def __init__(self, token):
        token = token.strip()
        if token.lower().startswith("bot "):
            token = token[4:].strip()
        self.token = token
        self.session = requests.Session()
        bn = fetch_latest_build_number()
        ua = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) discord/1.0.9175 Chrome/128.0.6613.186 "
            "Electron/32.2.7 Safari/537.36"
        )
        self.session.headers.update({
            "Authorization": token, "Content-Type": "application/json",
            "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": ua, "X-Super-Properties": make_super_properties(bn),
            "X-Discord-Locale": "en-US", "X-Discord-Timezone": "Asia/Ho_Chi_Minh",
            "Origin": "https://discord.com", "Referer": "https://discord.com/channels/@me",
        })

    def get(self, path, **kw):
        return self.session.get(f"{API_BASE}{path}", timeout=15, **kw)

    def post(self, path, payload=None, **kw):
        return self.session.post(f"{API_BASE}{path}", json=payload, timeout=15, **kw)

def get_task_config(quest):
    return _get(quest.get("config", {}), "taskConfig", "task_config", "taskConfigV2", "task_config_v2")

def get_quest_name(quest):
    cfg = quest.get("config", {})
    msgs = cfg.get("messages", {})
    name = _get(msgs, "questName", "quest_name")
    if name: return name.strip()
    game = _get(msgs, "gameTitle", "game_title")
    if game: return game.strip()
    app = cfg.get("application", {}).get("name")
    return app or f"Quest#{quest.get('id', '?')}"

def get_user_status(quest):
    us = _get(quest, "userStatus", "user_status")
    return us if isinstance(us, dict) else {}

def is_expired(quest):
    exp = parse_iso(_get(quest.get("config", {}), "expiresAt", "expires_at"))
    return exp is not None and datetime.now(timezone.utc) >= exp

def is_not_started(quest):
    st = parse_iso(_get(quest.get("config", {}), "startsAt", "starts_at"))
    return st is not None and datetime.now(timezone.utc) < st

def is_enrolled(quest):
    return bool(_get(get_user_status(quest), "enrolledAt", "enrolled_at"))

def is_completed(quest):
    return bool(_get(get_user_status(quest), "completedAt", "completed_at"))

def get_task_type(quest):
    tc = get_task_config(quest)
    if not tc or "tasks" not in tc: return None
    for t in SUPPORTED_TASKS:
        if tc["tasks"].get(t) is not None: return t
    return None

def is_completable(quest):
    if is_expired(quest) or is_not_started(quest): return False
    return get_task_type(quest) is not None

def get_seconds_needed(quest):
    tc, tt = get_task_config(quest), get_task_type(quest)
    if not tc or not tt: return 0
    return tc["tasks"][tt].get("target", 0)

def get_seconds_done(quest):
    tt = get_task_type(quest)
    if not tt: return 0
    return get_user_status(quest).get("progress", {}).get(tt, {}).get("value", 0) or 0

def get_app_id(quest):
    tc, tt = get_task_config(quest), get_task_type(quest)
    if tc and tt:
        apps = tc["tasks"][tt].get("applications") or []
        if apps: return apps[0].get("id")
    return _get(quest.get("config", {}).get("application", {}), "id")

# ── Worker ────────────────────────────────────────────────────────────────────
class QuestWorker(threading.Thread):
    def __init__(self, token, username):
        super().__init__(daemon=True)
        self.token, self.username = token, username
        self._stop = threading.Event()
        self._api = WorkerAPI(token)
        self.completed_ids, self.skipped_ids = set(), set()
        self.first_scan = True
        self._rate_until = 0
        self.session_done = 0

    def _log(self, msg, color=Fore.WHITE):
        t = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.CYAN}[{t}]{Style.RESET_ALL} {Fore.MAGENTA}[{self.username}]{Style.RESET_ALL} {color}{msg}{Style.RESET_ALL}")

    def _handle_429(self, r, context=""):
        try: delay = float(r.json().get("retry_after", 60))
        except Exception: delay = 60
        delay = max(delay, 5)
        mins = delay / 60
        if mins >= 1:
            self._log(f"Rate limit{context}. Doi ~{mins:.0f} phut ({delay:.0f}s).", Fore.RED)
        else:
            self._log(f"Rate limit{context}. Doi {delay:.0f}s...", Fore.RED)
        self._rate_until = time.time() + delay
        end = time.time() + delay
        while time.time() < end and not self._stop.is_set():
            time.sleep(1)

    def print_status_report(self, quests):
        total = len(quests)
        completed = expired = unsupported = pending = 0
        pending_names = []
        for q in quests:
            if is_completed(q) or q["id"] in self.completed_ids:
                completed += 1
            elif is_expired(q):
                expired += 1
            elif not get_task_type(q):
                unsupported += 1
            elif is_completable(q):
                pending += 1
                pending_names.append(get_quest_name(q))
            else:
                expired += 1

        line = "═" * 52
        print(f"\n{gradient_1(line)}")
        print(gradient_2("  ▸ BAO CAO TONG KET QUEST"))
        print(f"  Chao {Fore.CYAN}{Style.BRIGHT}{self.username}{Style.RESET_ALL}, he thong da quet xong!")
        print(gradient_1(line))
        print(f"  {Fore.WHITE}Tong quest{Style.RESET_ALL}          {total}")
        print(f"  {Fore.GREEN}Da hoan thanh{Style.RESET_ALL}       {completed}")
        print(f"  {Fore.RED}Het han / bo qua{Style.RESET_ALL}    {expired}")
        print(f"  {Fore.LIGHTBLACK_EX}Khong ho tro{Style.RESET_ALL}        {unsupported}")
        print(f"  {Fore.CYAN}Can lam lan nay{Style.RESET_ALL}     {pending}")
        if pending_names:
            print(f"\n  {Fore.CYAN}Se cay:{Style.RESET_ALL}")
            for n in pending_names[:12]:
                print(f"    ▸ {n}")
            if len(pending_names) > 12:
                print(f"    ... +{len(pending_names) - 12} quest")
        if pending == 0:
            print(f"\n  {Fore.LIGHTBLACK_EX}Khong co quest moi. Theo doi ngam...{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.CYAN}Bat dau cay {pending} quest...{Style.RESET_ALL}")
        print(f"{gradient_1(line)}\n")
        self.first_scan = False
        return pending

    def enroll(self, quest):
        name, qid = get_quest_name(quest), quest["id"]
        self._log(f"Dang nhan: {name}...", Fore.YELLOW)
        for attempt in range(1, 4):
            try:
                r = self._api.post(f"/quests/{qid}/enroll", {
                    "location": 11, "is_targeted": False,
                    "metadata_raw": None, "metadata_sealed": None,
                    "traffic_metadata_raw": quest.get("traffic_metadata_raw"),
                    "traffic_metadata_sealed": quest.get("traffic_metadata_sealed"),
                })
                if r.status_code == 429:
                    self._handle_429(r, f' nhan "{name}"'); continue
                if r.status_code in (200, 201, 204):
                    self._log(f"[OK] Nhan thanh cong: {name}", Fore.GREEN); return True
                if r.status_code == 404:
                    self._log(f"[X] '{name}' het han", Fore.LIGHTBLACK_EX)
                    self.skipped_ids.add(qid); return False
                try: msg = r.json().get("message") or r.text[:80]
                except Exception: msg = r.text[:80]
                if r.status_code == 400 and ("already" in msg.lower() or "enrolled" in msg.lower()):
                    self._log(f"[OK] Da nhan tu truoc: {name}", Fore.GREEN); return True
                self._log(f"[X] Khong nhan '{name}' ({r.status_code}) {msg}", Fore.RED)
                if attempt >= 3:
                    self.skipped_ids.add(qid); return False
                time.sleep(2)
            except Exception as e:
                self._log(f"Loi enroll '{name}': {e}", Fore.RED); return False
        return False

    def complete_video(self, quest):
        name, qid = get_quest_name(quest), quest["id"]
        needed, done = get_seconds_needed(quest), get_seconds_done(quest)
        enrolled_str = _get(get_user_status(quest), "enrolledAt", "enrolled_at")
        if enrolled_str:
            et = parse_iso(enrolled_str)
            enrolled_ts = et.timestamp() if et else time.time()
        else:
            enrolled_ts = time.time()

        self._log(f">> Video: {name} ({done:.0f}/{needed}s)", Fore.YELLOW)
        while done < needed and not self._stop.is_set() and time.time() >= self._rate_until:
            max_allowed = (time.time() - enrolled_ts) + 10
            if max_allowed - done < VIDEO_SPEED:
                time.sleep(1); continue
            timestamp = min(needed, done + VIDEO_SPEED)
            try:
                r = self._api.post(f"/quests/{qid}/video-progress",
                                   {"timestamp": timestamp + random.random() * 0.5})
                if r.status_code == 200:
                    body = r.json()
                    if body.get("completed_at"):
                        done = needed; break
                    done = timestamp
                elif r.status_code == 429:
                    self._handle_429(r, " video"); continue
            except Exception:
                pass
            if timestamp >= needed: break
            time.sleep(1)
        try:
            self._api.post(f"/quests/{qid}/video-progress", {"timestamp": needed})
        except Exception:
            pass
        self.completed_ids.add(qid)
        self.session_done += 1
        self._log(f"[DONE] Hoan thanh: {name}", Fore.GREEN)
        log_quest(self.username, name, "completed")

    def complete_heartbeat(self, quest):
        name, qid = get_quest_name(quest), quest["id"]
        tt = get_task_type(quest)
        needed, done = get_seconds_needed(quest), get_seconds_done(quest)
        app_id = get_app_id(quest)
        pid = random.randint(1000, 30000)
        remaining = max(0, needed - done)

        self._log(
            f">> {tt}: {name} (~{remaining // 60} phut) [pid={pid}]"
            + (f" [app={app_id}]" if app_id else ""),
            Fore.YELLOW,
        )
        last_log, retries = 0, 0
        while done < needed and not self._stop.is_set() and time.time() >= self._rate_until:
            try:
                payload = {"stream_key": f"call:0:{pid}", "terminal": False}
                if app_id and tt in ("PLAY_ON_DESKTOP", "PLAY_ON_DESKTOP_V2"):
                    payload["application_id"] = str(app_id)
                r = self._api.post(f"/quests/{qid}/heartbeat", payload)
                if r.status_code == 200:
                    body = r.json()
                    prog = body.get("progress", {})
                    if tt in prog and isinstance(prog[tt], dict):
                        done = prog[tt].get("value", done)
                    elif "stream_progress_seconds" in body:
                        done = body.get("stream_progress_seconds", done)
                    retries = 0
                    if done - last_log >= 60 or done >= needed:
                        pct = (done / needed * 100) if needed else 0
                        self._log(f"  ... {name}: {done:.0f}/{needed}s ({pct:.1f}%)", Fore.LIGHTBLACK_EX)
                        last_log = done
                    if body.get("completed_at") or done >= needed:
                        break
                elif r.status_code == 429:
                    self._handle_429(r, " heartbeat"); continue
                elif r.status_code == 401:
                    retries += 1
                    if "application_id" in payload and retries <= 2:
                        self._log("  401 -> thu lai chi stream_key...", Fore.YELLOW)
                        try:
                            r2 = self._api.post(f"/quests/{qid}/heartbeat",
                                                {"stream_key": f"call:0:{pid}", "terminal": False})
                            if r2.status_code == 200:
                                body = r2.json()
                                prog = body.get("progress", {})
                                if tt in prog:
                                    done = prog[tt].get("value", done)
                                retries = 0; continue
                        except Exception:
                            pass
                    if retries > 5:
                        self._log(f"[X] Heartbeat 401. PLAY can Discord Desktop. Bo: {name}", Fore.RED)
                        self.skipped_ids.add(qid); return
                else:
                    retries += 1
                    if retries <= 2:
                        try: err = r.json()
                        except Exception: err = r.text[:100]
                        self._log(f"  Heartbeat {r.status_code}: {err}", Fore.RED)
                    if retries > 5:
                        self._log(f"[X] Heartbeat loi, bo: {name}", Fore.RED)
                        self.skipped_ids.add(qid); return
            except Exception as e:
                retries += 1
                if retries <= 2:
                    self._log(f"  Exception: {e}", Fore.RED)
            time.sleep(HEARTBEAT_INTERVAL)

        try:
            self._api.post(f"/quests/{qid}/heartbeat",
                           {"stream_key": f"call:0:{pid}", "terminal": True})
        except Exception:
            pass
        if done >= needed:
            self.completed_ids.add(qid)
            self.session_done += 1
            self._log(f"[DONE] Hoan thanh: {name}", Fore.GREEN)
            log_quest(self.username, name, "completed")

    def process_quest(self, quest):
        if time.time() < self._rate_until: return
        qid = quest["id"]
        if qid in self.completed_ids or qid in self.skipped_ids: return
        if is_completed(quest) or is_expired(quest) or not is_completable(quest): return
        if not is_enrolled(quest):
            if not self.enroll(quest): return
            time.sleep(1)
        tt = get_task_type(quest)
        if tt in ("WATCH_VIDEO", "WATCH_VIDEO_ON_MOBILE"):
            self.complete_video(quest)
        elif tt in ("PLAY_ON_DESKTOP", "PLAY_ON_DESKTOP_V2", "STREAM_ON_DESKTOP", "PLAY_ACTIVITY"):
            self.complete_heartbeat(quest)

    def run(self):
        self._log("Bat dau auto quest...", Fore.GREEN)
        while not self._stop.is_set():
            if time.time() < self._rate_until:
                remain = self._rate_until - time.time()
                if remain > 10:
                    self._log(f"Cho rate limit (~{remain / 60:.0f} phut)...", Fore.YELLOW)
                while time.time() < self._rate_until and not self._stop.is_set():
                    time.sleep(1)
                continue
            try:
                r = self._api.get("/quests/@me")
                if r.status_code == 200:
                    data = r.json()
                    quests = data.get("quests", []) if isinstance(data, dict) else data
                    blocked = _get(data, "quest_enrollment_blocked_until") if isinstance(data, dict) else None
                    if blocked:
                        self._log(f"Enrollment bi chan den: {blocked}", Fore.YELLOW)
                    if not quests:
                        self._log("Khong co quest.", Fore.YELLOW)
                    else:
                        if self.first_scan:
                            self.print_status_report(quests)
                        enrolled_q, need_enroll = [], []
                        for q in quests:
                            qid = q["id"]
                            if qid in self.completed_ids or qid in self.skipped_ids: continue
                            if is_completed(q) or not is_completable(q): continue
                            if is_enrolled(q): enrolled_q.append(q)
                            else: need_enroll.append(q)
                        for q in enrolled_q:
                            if self._stop.is_set() or time.time() < self._rate_until: break
                            self.process_quest(q); time.sleep(1.5)
                        if AUTO_ACCEPT:
                            for q in need_enroll:
                                if self._stop.is_set() or time.time() < self._rate_until: break
                                self.process_quest(q); time.sleep(3)
                        if self.session_done > 0:
                            print(f"\n{Fore.GREEN}{Style.BRIGHT}  Session: hoan thanh {self.session_done} quest.{Style.RESET_ALL}")
                            print(f"{Fore.LIGHTBLACK_EX}  Cho quest moi (check {POLL_INTERVAL}s)...{Style.RESET_ALL}\n")
                        elif not enrolled_q and not need_enroll:
                            self._log("Tat ca quest (con han) da xong. Cho quest moi...", Fore.LIGHTBLACK_EX)
                elif r.status_code == 429:
                    self._handle_429(r, " lay danh sach")
                else:
                    self._log(f"Loi lay quest ({r.status_code})", Fore.RED)
            except Exception as e:
                self._log(f"Loi he thong: {e}", Fore.RED)
                if DEBUG: traceback.print_exc()
            for _ in range(POLL_INTERVAL):
                if self._stop.is_set(): break
                time.sleep(1)
        self._log("Da dung.", Fore.RED)

    def stop(self):
        self._stop.set()

# ── Banner & CLI ──────────────────────────────────────────────────────────────

def print_banner():
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
    [+] Tool      : Discord Quest Auto CLI
    [+] Chuc nang : Auto quet · Auto nhan · Auto hoan thanh quest
    [+] Version   : 4.0
    ═══════════════════════════════════════════════════════════════════
    """
    print(gradient_3(my_banner_text))
    print(gradient_2(my_info_text))


def main():
    init_db()
    print_banner()
    print(f"  {Fore.GREEN}▸ Nhap Token Discord{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}  (Chuot phai de dan, Enter){Style.RESET_ALL}")
    print(f"  {Fore.RED}  !!! Khong share token / khong dan len chat!{Style.RESET_ALL}")

    if len(sys.argv) > 1:
        token = sys.argv[1].strip()
    elif Path(".token").exists():
        token = Path(".token").read_text().strip()
        print(f"  {Fore.CYAN}Doc token tu file .token{Style.RESET_ALL}")
    else:
        token = input(f"\n  {Fore.YELLOW}Token: {Style.RESET_ALL}").strip()

    if not token:
        print(f"  {Fore.RED}Chua nhap token.{Style.RESET_ALL}")
        time.sleep(2); return

    print(f"\n  {Fore.CYAN}Dang kiem tra token...{Style.RESET_ALL}")
    acc = add_account(token)
    if not acc["success"]:
        print(f"  {Fore.RED}Loi: {acc['error']}{Style.RESET_ALL}")
        input("\n  Enter de thoat..."); return

    print(f"  {Fore.GREEN}Dang nhap: {Style.BRIGHT}{acc['username']}{Style.RESET_ALL}\n")
    worker = QuestWorker(token, acc["username"])
    worker.start()
    print(f"  {Fore.YELLOW}Ctrl+C de dung.{Style.RESET_ALL}")
    print(gradient_1("  " + "─" * 50))

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n  {Fore.RED}Dang dung...{Style.RESET_ALL}")
        worker.stop(); worker.join(timeout=3)
        print(f"  {Fore.GREEN}Da thoat!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
