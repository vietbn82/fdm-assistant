# Printer preset — tầng machine

Trạng thái hiện tại, đổi khi tinh chỉnh máy.
Phần cứng bất biến: `docs/device.md`. Tầng nào sở hữu gì: `docs/preset-model.md` mục 3.

---

## Preset duy nhất: `Anycubic Kobra X 0.4 nozzle - high quality`

Kế thừa `Anycubic Kobra X 0.4 nozzle` của hãng. Chỉ ghi đè phần retraction.

| Key | Hãng | Đang đặt | Vì sao |
|---|---|---|---|
| `retraction_length` | 0.8 | **1** | dài hơn chút, giảm oozing |
| `retraction_speed` | 30 | **35** | |
| `deretraction_speed` | 30 | **35** | |
| `retraction_minimum_travel` | 1 | **2** | bớt retract vặt ở quãng ngắn |
| `retract_restart_extra` | 0 | **0** | ✅ trả về 0 |
| `z_hop` | 0.4 | **0.4** | ✅ trả về 0.4 |

Hai dòng cuối từng bị đặt sai:

- `retract_restart_extra = -0.05` — giá trị âm đùn thiếu sau **mỗi** lần retract.
  Chỉ nên khác 0 khi đã đo được lượng ooze cụ thể, không đặt phỏng đoán.
- `z_hop = 0.16` — nhỏ hơn layer dày nhất máy in được (0.28), nên cú nhấc đầu in
  hạ xuống ngay trong chính lớp nó cần vượt qua. Nozzle vẫn va. 0.4 vượt được
  mọi layer height trong dải máy hỗ trợ.

## Kế thừa từ hãng, không đè

`z_hop_types = Slope Lift`, `retract_when_changing_layer = 1`,
`single_extruder_multi_material = 1`, `purge_in_prime_tower = 0`,
`printer_flush_multiplier = 0.7`, `nozzle_volume = 79`,
`max_layer_height / min_layer_height = 0.28 / 0.08`.

Trần động học (`machine_max_*`) cũng ở tầng này nhưng mô tả phần cứng — xem
`docs/device.md`.

📝 Preset `Anycubic Kobra X 0.4 nozzle - Copy` đã xoá. Nó chỉ khác hãng ở
`z_hop_types = Auto Lift` và không dùng ở đâu.
