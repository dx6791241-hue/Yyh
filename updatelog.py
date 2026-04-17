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
    print("║               UPDATE LOG - TUẦN 06/04 - 12/04/2026                 ║")
    print("╚════════════════════════════════════════════════════════════════════╝\033[0m\n")

    print("\033[1;32m[★] PHIÊN BẢN HIỆN TẠI: Multi Tool HectorVN v2.1\033[0m")
    print("\033[1;97mDev: Deltatrash09 (Dương Khôi) |  0949557645\033[0m\n")

    print("\033[1;36m══════════════════ CẬP NHẬT NỔI BẬT TUẦN NÀY ══════════════════\033[0m")

    updates = [
        "• Rework hoàn toàn SPAMSMS BETA (V1) - Tăng tốc độ, ổn định hơn, giảm lỗi",
        "• Thêm tính năng Lọc Proxy Live (option 1.8) - Kiểm tra proxy chất lượng cao",
        "• Xây dựng hệ thống Key theo IP mới (hết hạn 23:59 hàng ngày)",
        "• Thêm cơ chế lưu key tự động vào file ip_key.json (mã hóa Base64)",
        "• Thêm option Tạo Mail Ảo (1.7) vào menu chính",
        "• Cải tiến banner + animation mượt mà, thêm thông báo debug lựa chọn",
        "• Fix lỗi thời gian kiểm tra key và một số lỗi nhỏ khác",
    ]

    for i, update in enumerate(updates, 1):
        print(f"\033[1;97m[{i:2d}]\033[0m {update}")

    print("\n\033[1;33m══════════════════ TUẦN SAU SẼ CẬP NHẬT ══════════════════\033[0m")
    print("\033[1;97m(Update TOOL VUA THOÁT HIỂM X WORLD)\033[0m\n")

    print("• [ ] Cập nhật TDS TikTok  - Tăng tốc follow/like/comment")
    print("• [ ] Thêm anti-detect & random delay cho các tool spam")
    print("• [ ] Tối ưu TOOL DOSS WEB V2 (mạnh hơn)")
    print("• [ ] Hỗ trợ proxy SOCKS5/HTTP tốt hơn")

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
