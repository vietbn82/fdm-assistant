# Máy in và phần mềm

## Nguồn số liệu — đọc trước

Mọi con số ở trang này đọc từ preset của slicer, **không phải đo trực tiếp**.
Phân biệt hai loại, vì nó quyết định có nên sửa hay không:

| | Ví dụ | Sửa preset thì sao |
|---|---|---|
| **Sự thật phần cứng** | vùng in, đường kính nozzle, trần động học | không đổi được thực tế; sửa sai chỉ làm slicer tính sai hoặc đâm nozzle |
| **Lựa chọn tinh chỉnh** | retraction, z-hop, tốc độ, flush | giá trị **chính là** setting; đây mới là thứ đáng chỉnh |

Trang này chỉ chứa loại thứ nhất. Loại thứ hai ở `profiles/`:

- Giá trị cấu hình đang đặt — `profiles/printer.md`
- Cách slicer lưu preset — `docs/preset-model.md`

🔵 Trần động học là **khai báo phía slicer**, giới hạn thật nằm trong
`printer.cfg` của Klipper trên máy. Preset đặt `emit_machine_limits_to_gcode = 1`
nên slicer còn ghi `SET_VELOCITY_LIMIT` vào đầu gcode để ép máy theo. Klipper kẹp
`VELOCITY` và `ACCEL` về mức trong config của nó, nên khai cao hơn thực tế chỉ
làm **ước tính thời gian sai**, không hỏng gì.

Trong bốn con số, chỉ **gia tốc** và **jerk** đáng đối chiếu. Tốc độ 450 mm/s gần
như không chạm tới: trần flow đã giới hạn ở ~166 mm/s khi đùn nhựa, nên 450 chỉ
áp dụng cho travel.

🟢 Jerk 20 map sang `square_corner_velocity` — cao gấp 4 lần mặc định Klipper (5),
và đây là tham số Klipper **không** kẹp. Triệu chứng nếu quá cao là ringing quanh
góc và lỗ. Viet xác nhận **không thấy ringing**, nên để nguyên. Xem A6 trong
`TODO.md` nếu sau này muốn đối chiếu cho đủ.

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

