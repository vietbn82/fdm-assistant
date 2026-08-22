# Máy in và phần mềm

Thông tin về **phần cứng** — thứ tồn tại ngoài đời, sửa preset không đổi được.

Giá trị cấu hình đang đặt: `profiles/printer.md`.
Cách slicer lưu preset: `docs/preset-model.md`.

---

## Máy in

| | |
|---|---|
| Model | Anycubic Kobra X *(user)* |
| Nozzle đang lắp | 0.4 mm hardened steel *(user)* |
| Nozzle máy hỗ trợ | 0.25 / 0.4 / 0.6 / 0.8 |
| Multi-color | bộ đầu in 4 màu **tích hợp**, không phải ACE rời *(user)* |
| Vùng in | 260 × 260 × 260 mm |
| Kiểu khung | i3 |
| Firmware | Klipper |
| Truyền động sợi | direct drive |
| Hotend | 79 mm³ melt zone, cao 4 mm |
| Layer height khả dụng | 0.08 – 0.28 mm |

## Trần động học

| | X / Y | Z | E |
|---|---|---|---|
| Tốc độ | 450 mm/s | 12 mm/s | 250 mm/s |
| Gia tốc | 10000 mm/s² | 1000 mm/s² | 6500 mm/s² |
| Jerk | 20 mm/s | 20 mm/s | 1 mm/s |

Gia tốc theo vai trò: travel 10000, extruding 6500, retracting 6500 mm/s².

🔵 Speed hay accel trong process preset vượt các mức này bị kẹp xuống — số hiển
thị trong slicer thành vô nghĩa.

## Slicer

| | |
|---|---|
| Anycubic Slicer Next | 1.4.1.2, build `20260604104233` |
| Nhân | dẫn xuất OrcaSlicer / BambuStudio — schema preset giống hệt |
| Region / Language / Đơn vị | Global / en_GB / mm |
| Tài khoản cloud | user id `855643`, đã đăng nhập |

---

## Nguồn số liệu

Mọi con số trên đọc từ preset của slicer, không phải đo trực tiếp. Phân biệt hai
loại — quan trọng khi quyết định có nên sửa:

| | Ví dụ | Sửa preset thì sao |
|---|---|---|
| **Sự thật phần cứng** | vùng in, đường kính nozzle, trần động học | không đổi được thực tế; sửa sai chỉ làm slicer tính sai hoặc đâm nozzle |
| **Lựa chọn tinh chỉnh** | retraction, z-hop, tốc độ, flush | giá trị **chính là** setting; đây mới là thứ đáng chỉnh |

Trang này chỉ chứa loại thứ nhất. Loại thứ hai ở `profiles/`.

🟡 Trần động học nằm ở nhóm một nhưng có một lưu ý: nó là **khai báo phía
slicer**, giới hạn thật nằm trong config Klipper trên máy. Hai bên có thể lệch —
chưa ai đối chiếu.
