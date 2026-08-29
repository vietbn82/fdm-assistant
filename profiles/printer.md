# Printer preset — tầng machine

Trạng thái hiện tại, đổi khi tinh chỉnh máy.
Phần cứng bất biến: `docs/device.md`. Tầng nào sở hữu gì: `docs/preset-model.md` mục 3.

---

## Preset duy nhất: `Anycubic Kobra X 0.4 nozzle - high quality`

Kế thừa `Anycubic Kobra X 0.4 nozzle` của hãng. Chỉ ghi đè phần retraction.

| Key | Hãng | Đang đặt | Vì sao |
|---|---|---|---|
| `retraction_length` | 0.8 | **1.2** | dài hơn, giảm oozing |
| `retraction_speed` | 30 | **45** | P9 — rút dứt khoát hơn, bớt tơ |
| `deretraction_speed` | 30 | **35** | |
| `retraction_minimum_travel` | 1 | **1** | ✅ trùng hãng — P6 đề xuất hạ xuống 0.5 |
| `retract_before_wipe` | 0% | **100%** | P8 — rút xong hẳn rồi mới lau |
| `z_hop_types` | Slope Lift | **Normal Lift** | P10 — nhấc thẳng, không kéo lê qua mặt in |
| `retract_restart_extra` | 0 | **0** | ✅ trả về 0 |
| `z_hop` | 0.4 | **0.4** | ✅ trả về 0.4 |
| `machine_end_gcode` | *(không retract)* | **+3 dòng** | P16 — xem dưới |

🔵 Bảng đọc từ đĩa ngày 29/08 sau khi áp P15 và P16. Ba giá trị P8/P9/P10 từng bị
revert ngày 27/08, đã đưa trở lại.

### `machine_end_gcode` — P16

```
M400
G91
G1 E-6 F1800 ; P16 ha ap suat vung nong chay, chong chay nhua cuoi ban in
G1 Z5 F600 ; P16 nhac dau in khoi mat in
G90
M140 S0 ; turn off heatbed
M104 S0 ; turn off temperature
M107;turn off fan
M84; disable motors
; disable stepper motors
```

Bản gốc của hãng đi thẳng `M400` → `M140 S0` → `M104 S0`, không có một lệnh
`G1 E-` nào — nozzle đầy nhựa chịu áp rồi nguội dần trong vài phút.

📝 Chưa nghiệm thu, có sẵn lệnh revert: C2 trong `TODO.md`.

🔵 **Đầu bản in không sửa được.** `machine_start_gcode` chỉ có một dòng `G9111`,
macro nằm trong firmware — nó tự gia nhiệt, home, cân bàn, mồi. Nozzle đứng ở
nhiệt in suốt quá trình đó.

Hai dòng cuối từng bị đặt sai:

- `retract_restart_extra = -0.05` — giá trị âm đùn thiếu sau **mỗi** lần retract.
  Chỉ nên khác 0 khi đã đo được lượng ooze cụ thể, không đặt phỏng đoán.
- `z_hop = 0.16` — nhỏ hơn layer dày nhất máy in được (0.28), nên cú nhấc đầu in
  hạ xuống ngay trong chính lớp nó cần vượt qua. Nozzle vẫn va. 0.4 vượt được
  mọi layer height trong dải máy hỗ trợ.

## Kế thừa từ hãng, không đè

`retract_when_changing_layer = 1`, `wipe = 1`, `wipe_distance = 2`,
`single_extruder_multi_material = 1`, `purge_in_prime_tower = 0`,
`printer_flush_multiplier = 0.7`, `nozzle_volume = 79`,
`max_layer_height / min_layer_height = 0.28 / 0.08`.

Trần động học (`machine_max_*`) cũng ở tầng này nhưng mô tả phần cứng — xem
`docs/device.md`.

📝 Preset `Anycubic Kobra X 0.4 nozzle - Copy` đã xoá. Nó chỉ khác hãng ở
`z_hop_types = Auto Lift` và không dùng ở đâu.
