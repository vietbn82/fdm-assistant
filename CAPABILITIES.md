# Tôi làm được gì — và bạn làm gì để tôi tự động hơn

> Bản nháp để review. Phần 3 là việc bạn cần quyết, chưa cái nào được bật.

---

## 1. Đang làm được ngay, không cần thiết lập gì

### Đọc và phân tích

| Việc | Ghi chú |
|---|---|
| Đọc toàn bộ preset của slicer, giải chuỗi `inherits` ra giá trị thật | 643 preset hệ thống + 14 preset của bạn |
| Đối chiếu preset với giới hạn firmware và vật lý đùn nhựa | công cụ `acslicer_tune.py` |
| So sánh preset của bạn với preset gốc hãng, chỉ ra bạn đã đổi gì | |
| Đọc log slicer (`log\MainApp*`, `cloud_mqtt*`, `MachMQTT*`) để tìm lỗi | chưa dùng đến |
| Đọc file `.3mf`, `.gcode` nếu bạn chỉ đường dẫn | gcode là text, đọc/thống kê được |
| Giải thích một setting làm gì và đánh đổi ra sao | |

### Sửa và tạo

| Việc | Ghi chú |
|---|---|
| Sửa preset có backup + bump `.info`, revert được | đã dùng trong phiên đầu |
| Tạo preset mới (filament / process / machine) | chưa làm |
| Viết script Python xử lý preset hàng loạt | |
| Tính flush matrix cho tổ hợp màu bất kỳ | cần bạn chốt cách tính |
| Sinh test print (temp tower, flow test, retraction test) dưới dạng preset + hướng dẫn | vẫn cần bạn in và đo |

### Chạy lệnh

Chạy được PowerShell / Bash trên máy bạn: kiểm tra process, copy file, chạy
Python, gọi `git`. Có sandbox — thao tác nguy hiểm như xoá đệ quy thư mục sẽ bị
chặn và hỏi bạn (đã gặp ở phiên trước).

---

## 2. Không làm được

| Việc | Vì sao |
|---|---|
| ❌ Nói chuyện trực tiếp với máy in | Cần đăng nhập MQTT/cloud của bạn. Có token trong `.conf` nhưng tôi không dùng — vừa rủi ro vừa ngoài phạm vi. |
| ❌ Xem camera, theo dõi print đang chạy | |
| ❌ Đo lường thực tế: đùn thiếu/thừa, stringing, độ bám | Chỉ bạn nhìn được vật in. Mọi con số tôi đưa là suy ra từ config hoặc từ profile hãng, **không phải đo trên máy bạn**. |
| ❌ Biết filament thật trong máy | Tôi đọc `Filaments.md`. File sai → tôi sai theo. |
| ❌ Nhớ phiên trước | Mỗi phiên bắt đầu trắng. Xem mục 3.1. |

---

## 3. Tự động hoá — 3.1 đến 3.5 đã BẬT (2026-08-22)

| # | Hạng mục | Trạng thái | File |
|---|---|---|---|
| 3.1 | `CLAUDE.md` tự nạp mỗi phiên | 🟢 bật | `CLAUDE.md` |
| 3.2 | git + `.gitignore` chặn rò token | 🟢 bật | `.gitignore` |
| 3.3 | Allowlist quyền lệnh chỉ đọc | 🟢 bật | `.claude/settings.json` |
| 3.4 | Slash command | 🟢 bật | `.claude/commands/` |
| 3.5 | Hook chặn ghi `system\` + báo trạng thái | 🟢 bật, đã test | `.claude/hooks/` |
| 3.6 | Cập nhật `Filaments.md` khi đổi cuộn | ⏳ việc thủ công của bạn | — |

Lệnh dùng được ngay: `/audit`, `/apply`, `/preset <tên>`, `/newfilament`.

⏳ Hook chỉ nạp khi Claude Code khởi động lại phiên, hoặc bạn mở `/hooks` một
lần. Phiên hiện tại chưa có `.claude/` lúc bắt đầu nên chưa theo dõi thư mục đó.

Phần mô tả chi tiết từng hạng mục giữ lại bên dưới để tham chiếu.

### 3.1 `CLAUDE.md` — biến `WORKING_RULES.md` thành luật thật sự ⭐ cao nhất

Hiện `WORKING_RULES.md` chỉ là file thường; tôi chỉ đọc khi bạn nhắc. File tên
`CLAUDE.md` ở thư mục gốc dự án được **nạp tự động mỗi phiên**.

Cách làm: để tôi tạo `CLAUDE.md` trỏ sang các file kia, hoặc gộp thẳng vào.

Được gì: không phải nhắc lại bối cảnh máy in, quy tắc backup, ngôn ngữ trả lời.
Mất gì: nội dung đó tốn context mỗi phiên → giữ ngắn, chi tiết để ở file riêng.

📝 **Cần bạn quyết:** tạo `CLAUDE.md` gộp hay chỉ trỏ đường dẫn?

### 3.2 `git init` — lịch sử thay đổi preset ⭐ cao

Thư mục này chưa phải git repo. Preset thì đang nằm ở `%APPDATA%`, không có
lịch sử gì ngoài các thư mục backup timestamp tôi tạo.

Cách làm: `git init` ở `C:\WS\ACSlicerNext`, thêm script copy `user\` vào
`presets/` trong repo rồi commit. Mỗi lần sửa là một commit diff được.

Được gì:
- Xem chính xác dòng nào đổi, khi nào, vì sao (commit message).
- Revert từng thay đổi lẻ, không phải nuốt cả backup.
- Tôi tự đọc `git log` để biết phiên trước đã làm gì → bù cho việc không nhớ.

📝 **Cần bạn quyết:** có `git init` không? Có push lên remote riêng tư không?
⚠️ Nếu push: phải `.gitignore` `.conf` vì chứa token.

### 3.3 Allowlist quyền trong `.claude/settings.json` — bớt bị hỏi ⭐ trung bình

Hiện mỗi lệnh đọc file, chạy `python acslicer_tune.py --audit`, `Get-Process`
đều có thể phải hỏi bạn.

Cách làm: thêm allowlist cho các lệnh **chỉ đọc**, giữ nguyên việc hỏi với lệnh
ghi.

Gợi ý allowlist an toàn:

```
python acslicer_tune.py --list
python acslicer_tune.py --audit *
python acslicer_tune.py --show *
Get-Process
git status / git log / git diff
```

❌ Không allowlist: `--fix`, `--set`, `Remove-Item`, `Copy-Item`, `git push`.

📝 **Cần bạn quyết:** đồng ý danh sách trên? Có skill `/fewer-permission-prompts`
tự quét lịch sử và đề xuất, nếu bạn muốn dùng.

### 3.4 Slash command riêng — gõ ngắn ⭐ trung bình

Tạo `.claude/commands/audit.md` → bạn gõ `/audit`, tôi chạy đúng quy trình:
kiểm tra slicer, chạy audit, tóm tắt theo format quen thuộc.

Ý tưởng lệnh:

| Lệnh | Làm gì |
|---|---|
| `/audit` | kiểm tra toàn bộ preset, báo cáo, không ghi |
| `/apply` | audit rồi áp fix, kèm backup, theo đúng luật ở mục 3 `WORKING_RULES.md` |
| `/preset <tên>` | in giá trị đã giải đầy đủ của một preset |
| `/newfilament` | hỏi vài câu rồi sinh filament preset mới |

📝 **Cần bạn quyết:** muốn lệnh nào?

### 3.5 Hook — tự chạy, không cần bạn gõ ⭐ thấp, nhưng chặn được lỗi nặng

Hook là lệnh mà harness tự chạy, không phải tôi. Hai cái đáng giá:

| Hook | Tác dụng |
|---|---|
| `PreToolUse` chặn ghi vào `system\` | biến "❌ không bao giờ sửa preset hãng" thành ràng buộc kỹ thuật, không phải lời hứa |
| `SessionStart` | tự in trạng thái: slicer đang chạy không, backup gần nhất, việc còn treo |

📝 **Cần bạn quyết:** có bật không? Có skill `/update-config` để tôi viết hộ.

### 3.6 Cập nhật `Filaments.md` mỗi khi đổi cuộn ⭐ việc của bạn, rẻ

Đây là thứ tôi **không thể tự biết**. File sai thì mọi tư vấn về nhiệt độ,
flush, flow đều sai. Chỉ cần sửa 4 dòng mỗi lần thay cuộn.

Đề xuất bổ sung mỗi slot: thương hiệu chính xác, màu (mã hex nếu biết), ngày
mở túi, đã sấy chưa. Ẩm là nguyên nhân số một của lỗi in PLA mà nhìn giống lỗi
setting.

---

## 4. Việc còn treo

| Việc | Chờ ai |
|---|---|
| Flow test `BBL PLA Lite` ở 15 mm³/s | Viet in và xem thành wall |
| Chốt bật/tắt các mục 3.1 → 3.5 | Viet |
| Flush matrix 4×4 cho Red/White/Black/Cyan | Viet xác nhận có in 4 màu |
| `0.12 mm High Quality`: bottom shell 3 layer = 0.36 mm | Viet quyết |
| Slot 2 Generic PLA chưa có preset | Viet quyết |
