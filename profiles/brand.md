# Preset hãng — nguyên bản Anycubic cho Kobra X 0.4

Nguồn: `system\Anycubic\` — chỉ đọc, không sửa. Đây là danh sách + tóm tắt để
tra cứu khi cần biết hãng cho gì, khác preset đang dùng (`profiles/*.md`) ở đâu.
Chỉ liệt nozzle **0.4** — máy Viet đang dùng (`profiles/printer.md`).

🔵 File dài, đọc rồi trích chỗ cần — không phải nạp nguyên bộ nhớ mỗi lần.

---

## 1. Machine — `Anycubic Kobra X 0.4 nozzle`

Preset gốc, `profiles/printer.md` kế thừa từ đây.

| Key | Giá trị hãng |
|---|---|
| `nozzle_diameter` | 0.4 |
| `max_layer_height` / `min_layer_height` | 0.28 / 0.08 |
| `retraction_length` | 0.8 |
| `retraction_speed` | 30 |
| `z_hop` | 0.4 |
| `z_hop_types` | Slope Lift |
| `nozzle_volume` | 79 mm³ |
| `single_extruder_multi_material` | 1 |
| `printer_flush_multiplier` | 0.7 |

🟡 Hai preset đang dùng (`Kobra X 0.4 - Single Color` /
`Kobra X 0.4 - MultiColor`) kế thừa bản này. Single Color không đè gì;
MultiColor chỉ đè retraction — `z_hop` giờ để nguyên giá trị hãng. Xem
`profiles/printer.md`.

## 2. Filament — 17 preset cho nozzle 0.4

| Preset | Loại | Nozzle (in/lớp 1) | Bàn (in/lớp 1) | Flow cap (mm³/s) | Fan max |
|---|---|---|---|---|---|
| Anycubic PLA | PLA | 205/215 | 60/60 | 13 | 100% |
| Anycubic PLA+ | PLA | 205/215 | 60/60 | **18** | 100% |
| Anycubic PLA High Speed | PLA | 205/210 | 60/60 | **18** | 100% |
| Anycubic PLA Matte | PLA | 210/220 | 60/60 | 12 | 100% |
| Anycubic PLA Silk | PLA | 220/230 | 65/65 | 12 | 100% |
| Anycubic PLA Glow | PLA | 210/220 | 60/60 | 12 | 100% |
| Anycubic PLA Wood | PLA | 205/215 | 60/60 | 13 | 100% |
| Anycubic PLA Translucent | PLA | 205/215 | 60/60 | 13 | 100% |
| Anycubic PLA-CF | PLA-CF | 205/215 | 65/65 | 8 | 100% |
| Anycubic ABS | ABS | 205/215 | 100/100 | 10 | 100% |
| Anycubic ASA | ASA | 205/215 | 100/100 | 8 | 100% |
| Anycubic PETG | PETG | 230/230 | 75/75 | 8 | 80% |
| Generic PETG | PETG | 230/230 | 75/75 | 8 | 80% |
| Anycubic PETG-CF | PETG-CF | 230/230 | 75/75 | 8 | 80% |
| Anycubic TPU 95A | TPU | 205/215 | 60/60 | 3.2 | 100% |
| Anycubic TPU for ACE | TPU | 205/215 | 60/60 | 8 | 100% |
| Anycubic PVA | PVA (support tan nước) | 205/215 | 60/60 | 5 | 100% |

### Đặc điểm, mục tiêu

- **Anycubic PLA** — baseline, mọi PLA khác trong bảng kế thừa cách đặt nhiệt
  từ đây. Flow cap 13 mm³/s là mức "an toàn", không phải mức PLA tối đa máy
  chảy được.
- **PLA+ / PLA High Speed** — cùng flow cap 18 mm³/s, cao nhất nhóm PLA. Mục
  tiêu in nhanh, đánh đổi lấy độ mịn bề mặt so với PLA thường. `docs/preset-model.md`
  §6 dùng chính preset High Speed làm ví dụ "mức thực tế hơn".
- **PLA Matte / Silk / Glow / Wood / Translucent** — cùng flow cap thấp hơn
  (12–13), khác nhau ở hiệu ứng bề mặt (matte không bóng, silk bóng loang màu,
  glow dạ quang, wood pha bột gỗ, translucent bán trong suốt). Nhiệt nozzle cao
  hơn PLA thường ở Silk/Glow/Matte (210–230) vì phụ gia cần chảy nóng hơn để
  không tắc.
- **PLA-CF** — pha sợi carbon, flow cap tụt xuống 8 (sợi CF làm nhựa đặc hơn,
  khó đùn nhanh). Bàn nâng lên 65°C so với PLA thường.
- **ABS / ASA** — bàn 100°C, cần buồng kín giữ nhiệt để tránh cong vênh/tách
  lớp. Flow cap thấp hơn PLA (10 / 8) vì nhiệt độ chảy cao hơn nhưng tản nhiệt
  kém hơn khi in nhanh.
- **PETG / Generic PETG / PETG-CF** — nhiệt nozzle cao nhất nhóm không phải
  support (230°C), fan hạ còn 80% (PETG cần làm nguội chậm hơn PLA để bám lớp
  tốt). CF bản pha sợi carbon, cùng thông số nhiệt nhưng bền hơn, giòn hơn khi
  uốn.
- **TPU 95A / TPU for ACE** — dẻo, flow cap thấp nhất trong nhóm không phải PVA
  (3.2 / 8) vì tốc độ đùn nhanh làm sợi TPU mềm bị nén ngược trong ống dẫn
  (buckling) trước khi tới nozzle. "for ACE" cho hệ đổi màu tự động (ACE), cap
  cao hơn bản 95A thường.
- **PVA** — vật liệu support tan trong nước, không phải để in vật thể chính.
  Flow cap thấp nhất bảng (5) vì PVA hút ẩm mạnh, đùn nhanh dễ sủi bọt/đứt sợi.

🔴 Nhắc lại `docs/preset-model.md` §6: filament flow cap và process wall speed
là hai preset độc lập của hãng, có thể tự mâu thuẫn (process đòi hỏi mm³/s cao
hơn filament cho phép) — slicer âm thầm hạ tốc, không báo lỗi.

## 3. Process — 9 preset cho nozzle 0.4

| Preset | Layer | Số lớp thành | Infill | Inner wall spd | Outer wall spd | Infill spd | Top spd |
|---|---|---|---|---|---|---|---|
| 0.08mm Standard | 0.08 | 2 | 15% | 120 | 60 | 100 | 120 |
| 0.12mm Standard | 0.12 | 2 | 15% | 150 | 60 | 180 | 150 |
| 0.12mm High Quality | 0.12 | 2 | 15% | 150 | 60 | 180 | 150 |
| 0.16mm Standard | 0.16 | 2 | 15% | 300 | 200 | 350 | 200 |
| 0.16mm High Quality | 0.16 | 2 | 15% | 150 | 60 | 200 | 150 |
| 0.20mm Standard | 0.20 | 2 | 15% | 300 | 200 | 300 | 200 |
| 0.20mm High Quality | 0.20 | 2 | 15% | 150 | 60 | 200 | 150 |
| 0.24mm Standard | 0.24 | 2 | 15% | 230 | 200 | 230 | 200 |
| 0.28mm Standard | 0.28 | 2 | 15% | 200 | 200 | 200 | 200 |

### Đặc điểm, mục tiêu

- **Trục layer height 0.08 → 0.28** — càng mỏng càng mịn/lâu, càng dày càng thô/
  nhanh. 0.08 là mức mịn nhất máy cho phép ở nozzle 0.4 (`min_layer_height`);
  0.28 là mức dày nhất (`max_layer_height`, xem mục 1).
- **"High Quality" (0.12/0.16/0.20) vs "Standard" cùng layer** — HQ hạ hẳn tốc
  độ thành ngoài/thành trong (60/150 so với 200–300 của Standard) để đổi lấy bề
  mặt mịn hơn, ít rung bóng (ringing). 0.12mm chỉ có một mức tốc độ chung cho cả
  hai bản — ở layer mỏng nhất, "Standard" và "High Quality" trùng thông số.
- **0.16mm / 0.20mm Standard** — tốc độ cao nhất bảng (300 inner wall), preset
  hãng dùng cho in nhanh, chấp nhận bề mặt kém hơn HQ. Đây chính là preset gây
  mâu thuẫn với `Anycubic PLA` (13 mm³/s) nêu ở `docs/preset-model.md` §6.
- **0.24 / 0.28mm Standard** — layer dày, tốc độ hạ dần theo layer (230 → 200)
  vì đường ép dày hơn cần thời gian bám dính lớp dưới lâu hơn dù bản thân layer
  in nhanh hơn về thời gian tổng.
- **Không có preset "Draft"/"Fast" riêng** — hãng dùng chính 0.28mm Standard
  làm mức nhanh nhất, không tách thêm tier tốc độ như một số hãng khác.

🔵 Năm process preset Viet đang dùng thật (`profiles/process.md`) đều kế thừa từ
nhóm High Quality/Standard 0.4 nozzle này, ghi đè thêm theo mục đích in cụ thể
(FIGURE / TOOL / TEST) — không trùng số liệu gốc hãng ở bảng trên.

## 4. Đọc thêm

- Vì sao ba tầng machine/filament/process tách biệt, key nào thuộc tầng nào:
  `docs/preset-model.md` §1, §3.
- Giá trị đang dùng thật (khác bảng hãng ở trên): `profiles/printer.md`,
  `profiles/filament.md`, `profiles/process.md`.
- Trần động học, build volume: `docs/device.md`.
