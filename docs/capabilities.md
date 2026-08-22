# Claude làm được gì trong dự án này

---

## 1. Làm được

**Đọc và phân tích**

- Đọc toàn bộ kho preset, giải chuỗi `inherits` ra giá trị thực tế
  *(643 preset hãng + 14 của bạn)*
- Đối chiếu preset với giới hạn firmware và vật lý đùn nhựa
- So preset của bạn với bản gốc hãng, chỉ ra đã đổi gì
- Đọc log slicer (`log\MainApp*`, `cloud_mqtt*`, `MachMQTT*`) khi cần tìm lỗi
- Đọc `.3mf`, `.gcode` nếu được chỉ đường dẫn
- Giải thích một setting làm gì và đánh đổi ra sao

**Sửa và tạo**

- Sửa preset kèm backup và bump `.info` — revert được
- Tạo preset filament / process / machine mới
- Viết script xử lý preset hàng loạt
- Tính flush matrix cho tổ hợp màu bất kỳ
- Soạn test print (temp tower, flow test, retraction) — bạn in và đo

**Chạy lệnh** — PowerShell và Bash trên máy bạn: kiểm tra process, copy file,
chạy Python, gọi `git`. Có sandbox: thao tác nguy hiểm như xoá đệ quy thư mục
bị chặn và hỏi lại.

## 2. Không làm được

| | Vì sao |
|---|---|
| ❌ Nói chuyện với máy in | cần đăng nhập MQTT/cloud. Token có trong `.conf` nhưng không dùng — vừa rủi ro vừa ngoài phạm vi |
| ❌ Xem camera, theo dõi print đang chạy | |
| ❌ Đo đùn thiếu/thừa, stringing, độ bám | chỉ bạn nhìn được vật in |
| ❌ Biết cuộn nhựa thật đang nạp | đọc `profiles/filament.md`; file sai thì sai theo |
| ❌ Nhớ phiên trước | mỗi phiên bắt đầu trắng — bù lại bằng `CLAUDE.md`, `TODO.md`, `git log` |

🟡 Hệ quả của hai dòng cuối bảng: **mọi con số Claude đưa ra là suy từ config
hoặc lấy từ profile hãng, không phải đo trên máy bạn.** Đặc biệt đúng với
`filament_max_volumetric_speed` — luôn cần flow test xác nhận.

## 3. Đã tự động hoá

| Cơ chế | Tác dụng | File |
|---|---|---|
| Context tự nạp | không phải nhắc lại bối cảnh máy, quy tắc backup, ngôn ngữ | `CLAUDE.md` |
| Git + `.gitignore` | lịch sử diff/revert, chặn rò token lên remote public | `.gitignore` |
| Allowlist quyền | lệnh chỉ đọc chạy thẳng; `--fix`, `--set`, `git` thì hỏi | `.claude/settings.json` |
| Slash command | `/audit` `/apply` `/preset` `/newfilament` | `.claude/commands/` |
| Hook chặn ghi `system\` | biến "không bao giờ sửa preset hãng" từ lời hứa thành ràng buộc kỹ thuật | `.claude/hooks/guard_system_presets.py` |
| Hook báo trạng thái | mỗi phiên tự biết: slicer đang mở không, backup gần nhất, git state | `.claude/hooks/session_status.py` |

⏳ Hook chỉ nạp khi Claude Code khởi động lại, hoặc mở `/hooks` một lần.

## 4. Còn thủ công

**Việc của bạn, không tự động hoá được:** cập nhật `profiles/filament.md` mỗi lần
đổi cuộn, và in các bản test. Xem mục A trong `TODO.md`.

**Thiếu sót của công cụ:** `tools/acslicer_tune.py` chưa có `--unset`, chưa có
rule multi-material, chưa ghi được `.conf`. Xem C5 trong `TODO.md`.
