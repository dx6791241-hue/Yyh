import os
import sys
from time import sleep

# ================== BANNER ==================
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    ban = r'''
      ,--.'|                       ___                                         ,--.'|        
   ,--,  | :                     ,--.'|_                           ,---.   ,--,:  |        
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
        sleep(0.004)
    print("\n\033[1;97m                  ★ UPDATE LOG TUẦN NÀY ★\033[0m\n")

# ================== UPDATE LOG TUẦN NÀY ==================
def show_update_log():
    banner()
    print("\033[1;33m╔════════════════════════════════════════════════════════════════════╗")
    print("║               UPDATE LOG - 22/04/2026                 ║")
    print("╚════════════════════════════════════════════════════════════════════╝\033[0m\n")

    print("\033[1;32m[★] PHIÊN BẢN HIỆN TẠI: Multi Tool HectorVN v2.1\033[0m")
    print("\033[1;97mDev: Deltatrash09 (Dương Khôi) |  0949557645\033[0m\n")

    print("\033[1;36m══════════════════ CẬP NHẬT NỔI BẬT TUẦN NÀY ══════════════════\033[0m")

    updates = [
        "• UPDATE TOOL TƯƠNG TÁC CHÉO FACEBOOK",
        "• REWORK TOOL TRAO ĐỔI SUB FACEBOOK",

    ]

    for i, update in enumerate(updates, 1):
        print(f"\033[1;97m[{i:2d}]\033[0m {update}")

    print("\n\033[1;33m══════════════════ TUẦN SAU SẼ CẬP NHẬT ══════════════════\033[0m")
    print("\033[1;97m(UPDATE TOOL GOLIKE (ĐỊT MẸ HẾT THI RỒI HAHA)\033[0m\n")

    print("• [ ] REWORK TOOL DDOS(MAYBE)")

    print("\n\033[1;31m• Lưu ý: Key chỉ dùng được trong ngày, sang ngày mới phải lấy lại.\033[0m")
    print("\033[1;32m• Khuyến cáo không dùng VPN/Proxy vượt link để tránh bị khoá IP.\033[0m\n")

    print("\033[1;97mCảm ơn mọi người đã ủng hộ và sử dụng tool!\033[0m")

    input("\033[1;32mNhấn Enter để thoát Update Log...\033[0m")

# ================== CHẠY ==================
if __name__ == "__main__":
    try:
        show_update_log()
    except KeyboardInterrupt:
        print("\n\n\033[1;31mĐã thoát Update Log!\033[0m")
        sys.exit(0)
