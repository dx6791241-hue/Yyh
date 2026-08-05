#!/usr/bin/env python3
"""
Henxi NextDNS — Auto dang ky tai khoan + lay API Key
"""
import sys, io, os
os.system("")
import time, random, string, re, argparse, asyncio, logging, traceback
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict
import warnings
import requests

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
    )

from rich.console import Console
from rich.progress import (
    Progress, SpinnerColumn, TextColumn, BarColumn,
    TaskProgressColumn, TimeRemainingColumn,
)
from rich.panel import Panel
from rich.table import Table
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

warnings.filterfilters = getattr(warnings, "filterwarnings")
warnings.filterwarnings("ignore", category=ResourceWarning)

def _suppress_unraisable(unraisable):
    msg = str(unraisable.exc_value) if unraisable.exc_value else ""
    if any(x in msg for x in ["I/O operation on closed pipe", "unclosed transport"]):
        return
    sys.__unraisablehook__(unraisable)

sys.unraisablehook = _suppress_unraisable

# ── Gradient tu fbttc.py ──────────────────────────────────────────────────────
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

# ── Cau hinh ──────────────────────────────────────────────────────────────────
NEXTDNS_WEB_URL = "https://my.nextdns.io"
TINYHOST_BASE_URL = "https://tinyhost.shop"
TINYHOST_RANDOM_DOMAINS_URL = f"{TINYHOST_BASE_URL}/api/random-domains/"
OUTPUT_FILE = "api_keys.txt"
LOG_FILE = "nextdns_tool.log"

def setup_logger(name: str = "nextdns_tool", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logger.handlers:
        return logger
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

log = setup_logger()
console = Console(safe_box=True, legacy_windows=True)

# ── Tinyhost ──────────────────────────────────────────────────────────────────
class TinyhostClient:
    def __init__(self, proxy: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/html, */*",
            "Accept-Language": "en-US,en;q=0.9",
        })
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}
        self._available_domains: Optional[List[str]] = None

    def _get_random_user(self, length: int = 12) -> str:
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def get_available_domains(self, limit: int = 30) -> List[str]:
        try:
            resp = self.session.get(TINYHOST_RANDOM_DOMAINS_URL, params={"limit": limit}, timeout=15)
            resp.raise_for_status()
            domains = resp.json().get("domains", [])
            if domains:
                log.info(f"  [Tinyhost] Tim thay {len(domains)} domain")
                return domains
            return []
        except Exception as e:
            log.error(f"  [Tinyhost] Loi lay domain: {e}")
            return []

    def generate_email(self) -> Tuple[str, str, str]:
        if not self._available_domains:
            self._available_domains = self.get_available_domains(30)
            if not self._available_domains:
                self._available_domains = [
                    "fhost.shop", "onepices.shop", "gwsop.shop", "shopzgi.shop",
                    "jngpfy.shop", "gopagb.shop", "onxea.shop", "mhostz.shop",
                    "hostpda.shop", "tempmail.shop", "tmpmail.shop", "mailn.shop",
                ]
                log.warning("  [Tinyhost] Dung domain du phong")
        candidates = [d for d in self._available_domains if d != "tinyhost.shop"] or self._available_domains
        domain = random.choice(candidates)
        user = self._get_random_user(12)
        full_email = f"{user}@{domain}"
        log.info(f"  [Tinyhost] Tao email: {full_email}")
        return full_email, domain, user

# ── NextDNS Engine ────────────────────────────────────────────────────────────
@dataclass
class NextDNSResult:
    success: bool
    email: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    profile_id: Optional[str] = None
    error: Optional[str] = None
    cookies: Optional[Dict] = None
    created_at: Optional[str] = None

class NextDNSEngine:
    def __init__(self, email: str, password: str, headless: bool = True, timeout: int = 90):
        self.email = email
        self.password = password
        self.headless = headless
        self.timeout = timeout
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def _launch(self) -> bool:
        try:
            pw = await async_playwright().start()
            self.browser = await pw.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-gpu",
                ],
            )
            self.context = await self.browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            self.page = await self.context.new_page()
            return True
        except Exception as e:
            log.error(f"  [NextDNS] Loi mo trinh duyet: {e}")
            return False

    async def _cleanup(self):
        try:
            if self.page: await self.page.close()
            if self.context: await self.context.close()
            if self.browser: await self.browser.close()
        except Exception:
            pass

    async def _fill_and_submit_signup(self) -> Tuple[bool, Optional[str]]:
        try:
            await self.page.goto(f"{NEXTDNS_WEB_URL}/signup", wait_until="domcontentloaded", timeout=30000)
            await self.page.wait_for_timeout(2000)
            email_input = await self.page.query_selector("input[type='email']")
            if not email_input:
                return False, None
            await email_input.fill(self.email)
            pass_input = await self.page.query_selector("input[type='password']")
            if not pass_input:
                return False, None
            await pass_input.fill(self.password)
            submit_btn = await self.page.query_selector("button[type='submit']")
            if submit_btn:
                await submit_btn.click()
            else:
                await self.page.keyboard.press("Enter")
            await self.page.wait_for_url(
                lambda url: "/setup" in url or "/account" in url, timeout=60000
            )
            await self.page.wait_for_timeout(2000)
            match = re.search(r"/([a-f0-9]{6,})/setup", self.page.url)
            return True, (match.group(1) if match else None)
        except Exception as e:
            log.error(f"  [NextDNS] Loi dang ky: {e}")
            return False, None

    async def _generate_api_key(self) -> Optional[str]:
        try:
            await self.page.goto(f"{NEXTDNS_WEB_URL}/account", wait_until="networkidle", timeout=20000)
            await self.page.wait_for_timeout(2000)
            generate_btn = await self.page.query_selector("button:has-text('Generate')")
            if not generate_btn:
                log.error("  [NextDNS] Khong tim thay nut Generate API Key")
                return None
            await generate_btn.click()
            await self.page.wait_for_timeout(3000)
            page_text = await self.page.inner_text("body")
            matches = re.findall(r"\b([a-f0-9]{40})\b", page_text)
            for match in matches:
                return match
            html = await self.page.content()
            matches = re.findall(r"\b([a-f0-9]{40})\b", html)
            for match in matches:
                idx = html.find(match)
                ctx = html[max(0, idx - 150): idx + 150].lower()
                if any(kw in ctx for kw in ["api", "key", "generate", "secret"]):
                    return match
            return None
        except Exception as e:
            log.error(f"  [NextDNS] Loi tao API key: {e}")
            return None

    async def register(self) -> NextDNSResult:
        if not await self._launch():
            return NextDNSResult(success=False, error="loi_mo_trinh_duyet")
        try:
            ok, profile_id = await self._fill_and_submit_signup()
            if not ok:
                return NextDNSResult(success=False, error="dang_ky_that_bai")
            log.info(f"  [NextDNS] Dang ky OK! Profile: {profile_id}")
            api_key = await self._generate_api_key()
            if not api_key:
                return NextDNSResult(
                    success=True, email=self.email, password=self.password,
                    api_key="KHONG_TIM_THAY", profile_id=profile_id,
                    error="khong_tim_thay_api_key",
                    created_at=datetime.now(timezone.utc).isoformat(),
                )
            log.info(f"  [NextDNS] API Key: {api_key}")
            cookies_list = await self.context.cookies()
            cookies = {c["name"]: c["value"] for c in cookies_list}
            return NextDNSResult(
                success=True, email=self.email, password=self.password,
                api_key=api_key, profile_id=profile_id, cookies=cookies,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
        finally:
            await self._cleanup()

# ── Batch ─────────────────────────────────────────────────────────────────────
def save_result(result: NextDNSResult):
    if not result.success:
        return
    timestamp = result.created_at or ""
    line = f"{result.email}|{result.password}|{result.api_key}|{result.profile_id or 'N/A'}|{timestamp}"
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    log.info(f"  [File] Da luu vao {OUTPUT_FILE}")

async def register_single(
    tinyhost: TinyhostClient, visible: bool = False, password: Optional[str] = None
) -> Optional[NextDNSResult]:
    email, domain, user = tinyhost.generate_email()
    pwd = password if password else "".join(
        random.choices(string.ascii_letters + string.digits, k=14)
    )
    log.info(f"  [NextDNS] Dang ky: {email}")
    try:
        engine = NextDNSEngine(email=email, password=pwd, headless=not visible)
        result = await engine.register()
        if result.success and result.api_key and result.api_key != "KHONG_TIM_THAY":
            save_result(result)
        return result
    except Exception as e:
        log.error(f"  [NextDNS] Loi bat ngo: {e}")
        log.debug(traceback.format_exc())
        return None

async def run_batch(count: int, output_file: str, visible: bool, password: Optional[str]):
    global OUTPUT_FILE
    OUTPUT_FILE = output_file
    if not os.path.exists(OUTPUT_FILE):
        open(OUTPUT_FILE, "w", encoding="utf-8").close()

    # Chi Panel thong tin — KHONG in banner lan 2
    console.print(Panel.fit(
        f"[bold cyan]NextDNS Auto-Register[/bold cyan]  |  "
        f"[dim]Made by Deltatrash[/dim]",
        border_style="cyan",
    ))

    results: List[NextDNSResult] = []
    failures = 0
    not_found = 0
    tinyhost = TinyhostClient()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=False,
    ) as progress:
        main_task = progress.add_task("[cyan]Dang bat dau...", total=count)
        for i in range(count):
            progress.update(
                main_task,
                description=(
                    f"[cyan]Tai khoan {i + 1}/{count} — "
                    f"[green]ok: {len(results)}[/green] / "
                    f"[yellow]chua_tim_key: {not_found}[/yellow] / "
                    f"[red]loi: {failures}[/red]"
                ),
            )
            result = await register_single(tinyhost, visible, password)
            if result:
                if result.success:
                    if result.api_key == "KHONG_TIM_THAY":
                        not_found += 1
                    else:
                        results.append(result)
                else:
                    failures += 1
            else:
                failures += 1
            if i < count - 1:
                await asyncio.sleep(3)

    _show_summary(results, not_found, failures, count)

def _show_summary(results: List[NextDNSResult], not_found: int, failures: int, total: int):
    console.print()
    successful = len(results)
    if results:
        table = Table(title=f"Tong ket ket qua ({successful}/{total})", show_header=True)
        table.add_column("#", style="dim", width=4)
        table.add_column("Email", style="cyan")
        table.add_column("API Key", style="yellow")
        table.add_column("Profile ID", style="magenta")
        table.add_column("Tao luc (UTC)", style="dim")
        for i, r in enumerate(results, 1):
            ts = (r.created_at or "").replace("T", " ").split("+")[0][:19]
            table.add_row(
                str(i),
                r.email or "N/A",
                (r.api_key[:8] + "...") if r.api_key else "N/A",
                r.profile_id or "N/A",
                ts,
            )
        console.print(table)
    else:
        console.print("[yellow]Khong co dang ky thanh cong nao co API key.[/yellow]")
    console.print(
        f"\n[green]Thanh cong (co API key):[/green] {successful}  "
        f"[yellow]Dang ky (chua co key):[/yellow] {not_found}  "
        f"[red]That bai:[/red] {failures}"
    )
    console.print(f"[dim]Ket qua luu tai {OUTPUT_FILE}[/dim]")

# ── Banner fbttc (CHI 1 LAN) ──────────────────────────────────────────────────
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
    [+] Tool      : NextDNS Auto Register
    [+] Chuc nang : Tao tai khoan + lay API Key tu dong
    [+] Version   : 2.0
    ═══════════════════════════════════════════════════════════════════
    """
    print(gradient_3(my_banner_text))
    print(gradient_2(my_info_text))

def main():
    parser = argparse.ArgumentParser(
        description="NextDNS Auto-Register — Tao tai khoan + lay API Key tu dong"
    )
    parser.add_argument("-c", "--count", type=int, default=0, help="So tai khoan can tao (0 = nhap tay)")
    parser.add_argument("-o", "--output", type=str, default=OUTPUT_FILE, help="File luu ket qua")
    parser.add_argument("-p", "--password", type=str, default=None, help="Mat khau chung cho tat ca")
    parser.add_argument("--visible", action="store_true", help="Hien cua so trinh duyet")
    parser.add_argument("-v", "--verbose", action="store_true", help="Bat log chi tiet")
    args = parser.parse_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)

    print_banner()  # CHI 1 LAN o day

    if args.count <= 0:
        console.print()
        try:
            user_input = console.input(
                "[cyan]Ban muon tao bao nhieu API key?[/cyan] (mac dinh: 1): "
            ).strip()
            args.count = int(user_input) if user_input else 1
        except (ValueError, EOFError):
            args.count = 1

    try:
        asyncio.run(run_batch(args.count, args.output, args.visible, args.password))
    except KeyboardInterrupt:
        console.print("\n[red]Da dung boi nguoi dung.[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
