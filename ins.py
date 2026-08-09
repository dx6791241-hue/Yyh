#!/usr/bin/env python3
"""
Golike Instagram Full Auto — Cookie Edition + Check Ban
"""
import sys
import io
import os
os.system("")
import time
import random

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
    )

from golike_gauth import GolikeAuth, auto_solve_captcha
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired, ChallengeRequired, FeedbackRequired,
    UserNotFound, ClientError
)

SESSION_FILE = "ig_session.json"

# ── Gradient ──────────────────────────────────────────────────────────────────
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
    [+] Tool      : Golike Instagram Full Auto
    [+] Chuc nang : Auto follow/like/comment + Check Ban + Complete
    [+] Version   : 2.1  |  Cookie Edition
    ═══════════════════════════════════════════════════════════════════
    """
    print(gradient_3(my_banner_text))
    print(gradient_2(my_info_text))


# ── Instagram Login ───────────────────────────────────────────────────────────
def login_by_cookie():
    cl = Client()
    cl.delay_range = [1, 3]

    print(gradient_2("\n  ╔══════════════════════════════════════════════╗"))
    print(gradient_2("  ║     NHẬP COOKIE INSTAGRAM (sessionid)        ║"))
    print(gradient_2("  ╚══════════════════════════════════════════════╝\n"))

    cookie_str = input("  » Dán cookie vào đây: ").strip()
    if not cookie_str:
        print("  [-] Cookie trống!")
        return None

    sessionid = None
    for item in cookie_str.split(";"):
        item = item.strip()
        if item.startswith("sessionid="):
            sessionid = item.split("=", 1)[1].strip()
            break

    if not sessionid:
        print("  [-] Không tìm thấy sessionid trong cookie!")
        return None

    try:
        cl.login_by_sessionid(sessionid)
        user = cl.account_info()
        print(f"  [+] Đăng nhập thành công: @{user.username} (ID: {user.pk})")
        cl.dump_settings(SESSION_FILE)
        return cl
    except Exception as e:
        print(f"  [-] Cookie lỗi hoặc hết hạn: {e}")
        print("      Thử lấy lại cookie mới từ trình duyệt.")
        return None


# ── Check acc còn sống ────────────────────────────────────────────────────────
def is_user_alive(cl, object_id):
    """
    Kiểm tra acc Instagram còn tồn tại / chưa bị ban.
    Trả về (alive: bool, username: str | None)
    """
    try:
        user_id = int(object_id)
    except Exception:
        # object_id là username
        try:
            user_id = cl.user_id_from_username(object_id.replace("@", "").strip("/"))
        except Exception:
            return False, None

    try:
        info = cl.user_info(user_id)
        username = info.username
        # Một số dấu hiệu acc die / restricted
        if getattr(info, "is_private", False) is None and not username:
            return False, None
        return True, username
    except UserNotFound:
        return False, None
    except ClientError as e:
        msg = str(e).lower()
        if any(x in msg for x in ["not found", "unavailable", "banned", "suspended", "deleted"]):
            return False, None
        # Lỗi khác (rate limit...) → coi như tạm bỏ qua, vẫn cho thử
        return True, None
    except Exception:
        return True, None  # lỗi lạ thì vẫn cho thử


# ── Instagram Action ──────────────────────────────────────────────────────────
def do_instagram_action(cl, job_type, object_id, comment_text=None):
    try:
        if job_type == "follow":
            alive, username = is_user_alive(cl, object_id)
            if not alive:
                print(f"      → Acc đích BỊ BAN / KHÔNG TỒN TẠI → Skip")
                return False

            try:
                user_id = int(object_id)
            except Exception:
                user_id = cl.user_id_from_username(object_id.replace("@", "").strip("/"))

            cl.user_follow(user_id)
            link = f"https://www.instagram.com/{username}/" if username else f"https://www.instagram.com/user/{object_id}/"
            print(f"      → Đã FOLLOW {object_id} (@{username or '?'})")
            print(f"      → Check: {link}")
            return True

        elif job_type == "like":
            media_id = object_id
            if "instagram.com" in str(object_id):
                media_id = cl.media_pk_from_url(object_id)
            cl.media_like(media_id)
            print(f"      → Đã LIKE {object_id}")
            return True

        elif job_type == "comment":
            if not comment_text:
                print("      → Job comment không có nội dung → bỏ qua")
                return False
            media_id = object_id
            if "instagram.com" in str(object_id):
                media_id = cl.media_pk_from_url(object_id)
            cl.media_comment(media_id, comment_text)
            print(f"      → Đã COMMENT: {comment_text}")
            return True

        else:
            print(f"      → Loại job chưa hỗ trợ: {job_type}")
            return False

    except FeedbackRequired as e:
        print(f"      → Instagram tạm chặn: {e}")
        return False
    except Exception as e:
        print(f"      → Lỗi Instagram: {e}")
        return False


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print_banner()

    ig = login_by_cookie()
    if not ig:
        return

    print(gradient_2("\n  ╔══════════════════════════════════════════════╗"))
    print(gradient_2("  ║            CẤU HÌNH GOLIKE                   ║"))
    print(gradient_2("  ╚══════════════════════════════════════════════╝\n"))

    TOKEN = input("  » Nhập Authorization Golike: ").strip()
    IG_ACCOUNT_ID = input("  » Nhập Instagram Account ID(6 số): ").strip()
    try:
        MAX_JOB = int(input("  » Số job muốn làm (0 = chạy mãi): ").strip() or "0")
    except Exception:
        MAX_JOB = 0

    print("\n  [*] Khởi tạo GolikeAuth...")
    try:
        auth = GolikeAuth.from_token(
            TOKEN,
            enable_sig=True,
            fetch_session=True,
            captcha_solver=auto_solve_captcha,
            captcha_max_attempts=3,
        )
        print(f"  [+] Golike : {auth.username}")
        print(f"  [+] Device : {auth.device_id}\n")
    except Exception as e:
        print(f"  [-] Lỗi khởi tạo Golike: {e}")
        return

    done = 0
    skipped = 0
    failed = 0
    banned = 0
    last_ads_id = None

    print(gradient_3("  ══════════════════════════════════════════════"))
    print(gradient_3("           BẮT ĐẦU CHẠY AUTO JOB"))
    print(gradient_3("  ══════════════════════════════════════════════\n"))

    while True:
        if MAX_JOB > 0 and done >= MAX_JOB:
            print(f"\n  [*] Đã làm đủ {MAX_JOB} job. Dừng.")
            break

        try:
            r = auth.get(
                "/advertising/publishers/instagram/jobs",
                params={"instagram_account_id": IG_ACCOUNT_ID, "data": "null"},
            )
            data = r.json()
            print(f"  [GET] status={r.status_code}")

            if r.status_code != 200 or not data.get("data"):
                print(f"  [-] Không có job: {data.get('message') or data}")
                time.sleep(8)
                continue

            job = data["data"]
            ads_id = job.get("id") or job.get("ads_id")
            job_type = (job.get("type") or "follow").lower()
            object_id = str(job.get("object_id") or job.get("link") or "")
            comment_text = job.get("comment") or job.get("message") or job.get("content")

            if ads_id == last_ads_id:
                print(f"  [!] Job {ads_id} bị kẹt → Skip")
                auth.post("/advertising/publishers/instagram/skip-jobs", json={
                    "ads_id": ads_id,
                    "object_id": object_id,
                    "account_id": int(IG_ACCOUNT_ID),
                    "type": job_type,
                })
                last_ads_id = None
                skipped += 1
                time.sleep(4)
                continue

            last_ads_id = ads_id
            print(f"  [+] Job: ads_id={ads_id} | type={job_type} | object={object_id}")

            success = do_instagram_action(ig, job_type, object_id, comment_text)
            if not success:
                # Phân biệt skip vì ban hay lỗi khác
                if job_type == "follow":
                    banned += 1
                else:
                    skipped += 1

                auth.post("/advertising/publishers/instagram/skip-jobs", json={
                    "ads_id": ads_id,
                    "object_id": object_id,
                    "account_id": int(IG_ACCOUNT_ID),
                    "type": job_type,
                })
                last_ads_id = None
                time.sleep(4)
                continue

            # Đợi lâu hơn để Golike kịp check
            wait = random.uniform(10, 16)
            print(f"      → Đợi {wait:.1f}s cho Golike check...")
            time.sleep(wait)

            body = {
                "instagram_users_advertising_id": ads_id,
                "instagram_account_id": int(IG_ACCOUNT_ID),
                "async": True,
                "data": comment_text if job_type == "comment" else None,
            }

            r2 = auth.post("/advertising/publishers/instagram/complete-jobs", json=body)
            print(f"  [COMPLETE] {r2.status_code} | {r2.text[:140]}")

            if r2.status_code == 200:
                done += 1
                last_ads_id = None
                print(f"  [✓] OK #{done}  |  Ban-skip: {banned}  |  Skip: {skipped}  |  Fail: {failed}\n")
            else:
                msg = r2.json().get("message") or r2.json().get("error") or ""
                print(f"  [-] Complete thất bại: {msg}")
                failed += 1
                # Retry 1 lần sau 12s
                time.sleep(12)
                r3 = auth.post("/advertising/publishers/instagram/complete-jobs", json=body)
                if r3.status_code == 200:
                    done += 1
                    last_ads_id = None
                    failed -= 1
                    print(f"  [✓] Retry thành công #{done}\n")
                else:
                    print(f"  [-] Retry vẫn fail → Skip job")
                    auth.post("/advertising/publishers/instagram/skip-jobs", json={
                        "ads_id": ads_id,
                        "object_id": object_id,
                        "account_id": int(IG_ACCOUNT_ID),
                        "type": job_type,
                    })
                    last_ads_id = None
                    time.sleep(4)

        except KeyboardInterrupt:
            print("\n  [!] Người dùng dừng tool.")
            break
        except Exception as e:
            print(f"  [!] Lỗi: {e}")
            time.sleep(6)

        time.sleep(random.uniform(6, 10))

    print(gradient_2("\n  ══════════════════════════════════════════════"))
    print(f"  Tổng kết → Thành công: {done} | Ban-skip: {banned} | Skip: {skipped} | Fail: {failed}")
    print(gradient_2("  ══════════════════════════════════════════════\n"))


if __name__ == "__main__":
    main()
