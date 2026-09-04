# Printer preset — tầng machine

Trạng thái hiện tại, đổi khi tinh chỉnh máy.
Phần cứng bất biến: `docs/device.md`. Tầng nào sở hữu gì: `docs/preset-model.md` mục 3.

🟢 **Đọc từ đĩa 2026-09-03 22:0x, sau khi Viet dựng lại toàn bộ preset trên
slicer 2.0.0.2.** Bộ preset trên máy là chuẩn; mọi mục cũ mâu thuẫn với bảng
dưới đã bị thay.

---

## Hai machine preset — tách theo in một màu / bốn màu

| Machine preset | Dùng khi in | Ghi đè gì |
|---|---|---|
| `Kobra X 0.4 - Single Color` | in một màu | 🔵 **không ghi đè gì** — bằng đúng preset hãng |
| `Kobra X 0.4 - MultiColor` | in nhiều màu, có đổi màu | năm khoá retraction |

Cả hai kế thừa `Anycubic Kobra X 0.4 nozzle`.

🟢 Slicer đang chọn `Kobra X 0.4 - Single Color` (`presets.machine` trong `.conf`).

🔵 Cách tách đã **đổi bản chất** so với bộ cũ (`- high quality` /
`- high quality - TEST`, tách theo `z_hop` 0.2 / 0.4). Giờ tách theo **số màu**,
và `z_hop` để nguyên của hãng ở cả hai.

## `Kobra X 0.4 - MultiColor`

| Key | Hãng | Đang đặt | Vì sao |
|---|---|---|---|
| `retraction_length` | 0.8 | **1.6** | buồng nóng chảy dùng chung 79 mm³ cần rút dài hơn hotend đơn màu |
| `retraction_speed` | 30 | **45** | rút dứt khoát, bớt tơ |
| `deretraction_speed` | 30 | **35** | |
| `retraction_minimum_travel` | 1 | **0.5** | bắt cả travel ngắn |
| `retract_before_wipe` | 0% | **100%** | rút xong hẳn rồi mới lau |

## `Kobra X 0.4 - Single Color`

Không có khoá override nào. Giá trị hiệu dụng = preset hãng:

| Key | Giá trị |
|---|---|
| `retraction_length` / `_speed` / `deretraction_speed` | 0.8 / 30 / 30 |
| `retraction_minimum_travel` | 1 |
| `retract_before_wipe` | 0% |

🟡 Preset rỗng nên **chỉ có giá trị như một chỗ đứng để chuyển nhanh** — mọi
cập nhật của hãng tự chảy qua. Đổi retraction ở đây thì nhớ nó không tự lan
sang bản MultiColor, hai preset không đồng bộ với nhau.

## Kế thừa của hãng ở cả hai preset

| Key | Giá trị hãng | Trước đây từng đè |
|---|---|---|
| `z_hop` | **0.4** | 🔵 0.2 (bộ cũ) — nay bỏ, hết cảnh báo z_hop < `max_layer_height` |
| `z_hop_types` | **Slope Lift** | 🔵 Normal Lift (P10, bộ cũ) — nay bỏ |
| `purge_in_prime_tower` | **0** | 🟡 1 (P30, bộ cũ) — nay bỏ, xem cảnh báo dưới |
| `retract_restart_extra` | 0 | 0 |
| `machine_end_gcode` | gốc hãng | P16/P25-v2 thêm retract + wipe, P31 đã trả về gốc |
| `retract_when_changing_layer` / `wipe` / `wipe_distance` | 1 / 1 / 2 | |
| `single_extruder_multi_material` | 1 | |
| `printer_flush_multiplier` | 0.7 | |
| `nozzle_volume` | 79 mm³ | |
| `max_layer_height` / `min_layer_height` | 0.28 / 0.08 | |

🟡 **`purge_in_prime_tower = 0` trở lại.** Đây đúng là điều kiện P30 (30/08) đã
sửa: khi in FIGURE **không có support**, không còn đường xả hợp lệ nào nên purge
sau đổi màu bị bỏ qua hoàn toàn — bằng chứng đọc trực tiếp từ gcode lúc đó.
Chỉ ảnh hưởng bản in nhiều màu. Thấy lem màu ở lớp đầu sau mỗi lần đổi màu thì
bật lại `purge_in_prime_tower = 1` trên `Kobra X 0.4 - MultiColor` — đề xuất P32
trong `PENDING_APPLY.md`.

🔴 **Không sửa được bằng UI trên máy này** (kiểm 04/09, bản 2.0.0.2). Ô nhập
chỉ được dựng ở Printer Settings → *Multimaterial* → nhóm *Wipe tower*, mà trang
đó chỉ tồn tại khi máy khai `extruders_count > 1`. Kobra X khai một extruder
(đổi màu do firmware ACE lo), và bản Anycubic **không có Expert mode** — Advanced
là mức cao nhất. Trang Print Settings → *Multimaterial* → *Prime tower* có tồn
tại nhưng không chứa khoá này. Chi tiết: `docs/preset-model.md` mục 8.

🔵 `machine_end_gcode` gốc hãng:

```
M400
M140 S0 ; turn off heatbed
M104 S0 ; turn off temperature
M107;turn off fan
M84; disable motors
; disable stepper motors
```

Không có `G1 E-` (retract) hay wipe/z-hop lúc kết thúc — nozzle đầy nhựa chịu
áp rồi nguội dần. Giống trạng thái sau P31 (02/09), khi Viet bỏ đoạn tự thêm vì
nghi liên quan kẹt nhựa slot 4 (A10 trong `TODO.md`).

🔵 **Đầu bản in không sửa được.** `machine_start_gcode` chỉ có một dòng `G9111`,
macro nằm trong firmware — nó tự gia nhiệt, home, cân bàn, mồi. Nozzle đứng ở
nhiệt in suốt quá trình đó.

Trần động học (`machine_max_*`) cũng ở tầng này nhưng mô tả phần cứng — xem
`docs/device.md`.
