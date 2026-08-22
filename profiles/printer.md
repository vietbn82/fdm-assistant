# Printer preset — tầng machine

Trạng thái hiện tại, đổi khi tinh chỉnh máy.
Phần cứng bất biến: `docs/device.md`. Tầng nào sở hữu gì: `docs/preset-model.md` mục 3.

---

## Gốc: `Anycubic Kobra X 0.4 nozzle` (stock)

| Key | Giá trị |
|---|---|
| `retraction_length` | 0.8 mm |
| `retraction_minimum_travel` | 1 mm |
| `retraction_speed` / `deretraction_speed` | 30 / 30 mm/s |
| `z_hop` | 0.4 mm, kiểu `Slope Lift` |
| `retract_when_changing_layer` | 1 |
| `single_extruder_multi_material` | 1 — một hotend, bốn đường vào |
| `purge_in_prime_tower` | 0 — purge xả ra ngoài, không vào tower |
| `printer_flush_multiplier` | 0.7 |
| `nozzle_volume` | 79 mm³ |
| `max_layer_height` / `min_layer_height` | 0.28 / 0.08 mm |

Trần động học (`machine_max_*`) cũng nằm ở tầng này nhưng mô tả phần cứng —
xem `docs/device.md`.

## Preset của bạn

### `Anycubic Kobra X 0.4 nozzle - Copy`

Chỉ đổi `z_hop_types` → `Auto Lift`. Ngoài ra y hệt stock.
📝 Không rõ dùng để làm gì — cân nhắc xoá nếu không nhớ lý do tạo.

### `Anycubic Kobra X 0.4 nozzle - high quality`

| Key | Stock | Đang đặt | Ghi chú |
|---|---|---|---|
| `retraction_length` | 0.8 | **1** | dài hơn một chút |
| `retraction_speed` / `deretraction_speed` | 30 / 30 | **35 / 35** | |
| `retraction_minimum_travel` | 1 | **2** | ít retract vặt hơn |
| `retract_restart_extra` | 0 | 0 | 🟢 đã sửa từ −0.05 |
| `z_hop` | 0.4 | 0.4 | 🟢 đã sửa từ 0.1 |

Hai dòng cuối từng bị đặt sai và đã trả về mặc định: `retract_restart_extra` âm
gây đùn thiếu sau mỗi lần retract, `z_hop = 0.1` nhỏ hơn chính lớp nó cần vượt
qua nên nozzle vẫn va.

⏳ Chưa xác nhận các giá trị này còn nguyên sau khi mở lại slicer — A2 trong `TODO.md`.
