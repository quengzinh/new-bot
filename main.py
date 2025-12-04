import os
from keep_alive import keep_alive
# Các import cần thiết cho python-telegram-bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update


# Danh sách mã -> danh sách câu trả lời
answers = {
    "1a4": ["mẫu mực / màn đêm / dau bao / ca kiem / ca biet / day dua / dan bau / bao cao / lao hoa / dap hop / cao gia"],
    "2b1": ["xo bo / tu bi"],
    "b3c2": ["bach cau"],
    "2u2": ["u buồn / xấu hổ / thư kí / yeu ot / dau co"],
    "1a5": ["cầu phao / bạc tình / sâu thẳm / vàng son / sâu bệnh / bao quát / hanh tau / xà ngang / bánh gai / báo mộng"],
    "g5o": ["ga hoa mo"],
    "4m2": ["khuc mac"],
    "3n5": ["khong kich / dien thoai"],
    "3n3": ["thong ke / hat nhan / quan tam / nhan duc / tien dao"],
    "4a1": ["hau bao / gia han / hoa hau / ly gian / cau may"],
    "3b3": ["cao buoc / cua bien / tam benh"],
    "c4": ["cai co / co bap / co cua / cay cu / cam ta / cua so / ca dao"],
    "2c2o5": ["an chao da bat"],
    "t5": ["tai hoa / tam that / to tien / tam tai / tui ngu / tang ca"],
    "h6": ["hoi cung / hai long"],
    "1ap9": ["da phuong tien"],
    "4c3": ["cham cong / dinh cong"],
    "1o4": ["vo mong / moc tui / hoa mat / coi coc / bom tan"],
    "2s1": ["vo su / ha si"],
    "a1d2": ["ap dao"],
    "3k1": ["sao ke"],
    "n7": ["nong tính"],
    "1h2a2u": ["nha dau tu"],
    "2a3": ["qua loa / pha gia / giai ma"],
    "2i2": ["nhi ca / cai to"],
    "1a3": ["tan ca / lau la / cam ky / ma tuy / ca map / hoa le / cau cu / ca lon"],
    "6g": ["tho cong"],
    "5n1": ["hao hung / thi cong / quy hang / cam tinh"],
    "1u2a2u3": ["tum nam tum ba"],
    "5a1": ["tham bai"],
    "2o3o6o": ["thoc cao gao kem"],
    "1i4": ["tinh so / dinh ba / thien vi"],
    "h5": ["hoa tay / hut hon"],
    "1h4a1": ["thanh bai"],
    "1u3": ["vu tru"],
    "m4o1": ["mui nhon"],
    "y6": ["yeu kieu"],
    "n2c2c4": ["nha choc troi"],
    "4c2": ["ruou can / kich cau"],
    "1i4o1": ["kinh luoc"],
    "3h2": ["xich lo / ban hoc / bai hoc / hanh ly"],
    "c7a3": ["chat doc da cam"],
    "3c2": ["ngu coc / meo cam"],
    "h3t2": ["hong tam"],
    "1u2t2": ["quan tam"],
    "1a4": ["cau tha / lan can / tao tau / da giac / dao tau / hanh ha / bao ham / sao mai / san soc / cao gia / dap hop / mau muc / man dem / dau bao / ca kiem / ca biet / day dua / dan bau / bao cao"],
    "1h4": ["thu rac / tho the / chia se"],
    "a3": ["am no"],
    "3h1": ["do thi"],
    "t4tu3": ["tuong tuong"],
    "3c1": ["mac co"],
    "4u": ["cam tu / quy cu / co lau"],
    "g5n1": ["giay bong"],
    "b1t5": ["bi truyen"],
    "2c3": ["hoc bua / luc duc"],
    "1i6": ["kim cuong"],
    "3u2": ["ep cung / tu tung"],
    "m1h2": ["ma hoa"],
    "t2t4": ["tro trong"],
    "4g4": ["thang quan"],
    "c3m6o1": ["ca nam tren thot"],
    "2a4": ["than mat / hoa vang / hoa binh / trai cam / tham hoa / rua tien"],
    "5a": ["nhan ma / binh ma / dai gia"],
    "1a3c4": ["ca nuoc ngot"],
    "c6": ["cung cau / cau truc / cao kien / cuu canh"],
    "1e4": ["ten lua / neo don / keo keo / den dau"],
    "t6u2": ["thang thung"],
    "2e3": ["tien le"],
    "3a5": ["khoan hong"],
    "x5": ["xa bong / xe tang"],
    "t4d2": ["tranh dau"],
    "t2o3": ["treo gio / thuoc la"],
    "1u5": ["cua mieng / vui tinh / quy tien / tuong tu / tu (4) tuong"],
    "3n2h1": ["thanh chi"],
    "1g3": ["ngua o"],
    "1a3o2": ["nang long"],
    "2e2h2": ["tien nhan"],
    "1o4a4": ["do dau vao lua"],
    "2o4": ["cuoi tru / suon nui / nuoc hoa"],
    "3r3i2": ["the rut tien"],
    "2a4c": ["phat giac"],
    "1o2g3": ["cong giao"],
    "n4h4": ["nhiet huyet"],
    "3m6": ["kiem chuyen"],
    "1a1b5": ["nam ban cau"],
    "2n3": ["can cau / han han / dan ong / bong da / dang ki / cong bo"],
    "c3d3": ["chan dung"],
    "n4i2": ["nhan tien"],
    "1u5c1": ["duong lich"],
    "t3h2": ["thoi han"],
    "1h8": ["thuoc thang / thuong vien"],
    "1i5": ["tinh bao / tieu hoc / gia lanh / sieu sao / vien tro"],
    "1u3t6": ["cua so tinh yeu"],
    "2o2c2": ["guong cau"],
    "1o5": ["hoa sung / long nao"],
    "5r3": ["giao tranh"],
    "x5": ["xa bong / xe tang"],
    "1i3": ["dia oc / bi kip / bi hai"],
    "3i": ["o mai"],
    "3v1": ["thu vi"],
    "2n5o5": ["len voi xuong cho"],
    "1y4": ["ky quai / ly biet"],
    "3a1": ["bo rao"],
    "2o3": ["dao ngu / cao tay / bao ngu"],
    "3h3": ["canh cam / gach hoa / canh bac / binh yen / ngu hanh"],
    "2n4": ["lanh lan / tan cong / ton giao / bong den"],
    "t3t3": ["tong tich / tung tang"],
    "1g4": ["ngoai o"],
    "b5": ["ban bac / be bong / banh bo"],
    "l3t4": ["lich thiep / lang thang"],
    "3h4": ["cach mang"],
    "t2o1g4": ["thuong dinh"],
    "1a4n1": ["tan duong"],
    "c2o4": ["chuot rut"],
    "1o3": ["mo man / co loa / co con / ao anh / uot at"],
    "b3": ["bi oi / be lu"],
    "3u1": ["y thuc / đá lửa"],
    "2e3a": ["điện hoa"],
    "3n6": ["trung tướng"],
    "d4u": ["đầu gấu"],
    "2a3g3": ["mưa bóng mây"],
    "q4r2": ["quat tran"],
    "k2t2": ["kho tam"],
    "2a6": ["gia truyền / thần thông"],
    "7n1": ["quan trong"],
    "d5": ["đồng bộ / dau thu / đào sâu"],
    "1a2u4": ["cay but tre"],
    "5d4": ["thiên đường"],
    "4d1": ["khẩu độ / thái độ"],
    "1h4b3": ["thương binh"],
    "2g3": ["ông bầu"],
    "5c3": ["chiến công"],
    "a4o": ["anh hào"],
    "2h1": ["mơ hồ"],
    "4n1": ["bê tông / đá bóng / nhà ống"],
    "c3s2": ["chăm sóc"],
    "1u4h2a1": ["duong chi tay"],
    "3y2t3": ["chạy mất dép"],
    "4b2": ["long bao / lang ben / nhat bao"],
    "3t5": ["hậu trường"],
    "2u5": ["chuẩn xác / thuoc lao"],
    "2o7": ["phòng không"],
    "3m2": ["mai moi"],
    "2a3m2": ["sua rua mat"],
    "1h5": ["khoa moi / pháo đài"],
    "3k3": ["mat khau"],
    "4c1": ["quan ca / kế sách"],
    "g3r6": ["giá trên trời"],
    "5e1": ["hoa tiet"],
    "2e6": ["diem vuong"],
    "b4": ["bị cáo / ba hoa / bọ gậy"],
    "h3i2t4": ["hoc lien thong"],
}

# ------------------ HÀM XỬ LÝ TIN NHẮN (MESSAGE HANDLER) ---------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy nội dung tin nhắn, chuyển về chữ thường và loại bỏ khoảng trắng thừa
    text = update.message.text.lower().strip()

    # Kiểm tra mã trong danh sách answers
    if text in answers:
        reply_list = answers[text]
        # Nối các câu trả lời bằng dấu xuống dòng
        reply_text = "\n".join(reply_list)
    else:
        reply_text = "Không tìm thấy mã bạn nhập. Vui lòng kiểm tra lại."

    # Gửi tin nhắn trả lời
    await update.message.reply_text(reply_text)


# ------------------ HÀM KHỞI TẠO VÀ CHẠY BOT (MAIN FUNCTION) ---------------------
def main():
    # Lấy token từ biến môi trường BOT_TOKEN (đã thiết lập trên Render)
    TOKEN = os.getenv("BOT_TOKEN")

    if TOKEN is None:
        print("❌ LỖI: BOT_TOKEN không tồn tại trong biến môi trường!")
        return

    # 1. Xây dựng ứng dụng bot
    app = ApplicationBuilder().token(TOKEN).build()

    # 2. Thêm trình xử lý: Xử lý TẤT CẢ tin nhắn văn bản KHÔNG phải là lệnh (/start)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 3. Khởi động keep_alive server (để Render hoặc các dịch vụ khác ping)
    keep_alive()

    print("Bot đang chạy Polling 24/7...")
    # 4. Bắt đầu Polling
    app.run_polling()

# ------------------ ĐIỂM KHỞI CHẠY ---------------------
if __name__ == "__main__":
    main()


