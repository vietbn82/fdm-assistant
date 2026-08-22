# Devices And Software

> Các mục đánh dấu 🔎 là do Claude đọc trực tiếp từ config của slicer
> (`%APPDATA%\AnycubicSlicerNext\`), không phải người dùng nhập.
> Cập nhật lần cuối: 2026-08-22.

## Máy in

| Mục | Giá trị | Nguồn |
|---|---|---|
| Model | Anycubic Kobra X | user |
| Nozzle đang dùng | 0.4 mm, hardened steel | user |
| Nozzle hỗ trợ | 0.25 / 0.4 / 0.6 / 0.8 | 🔎 `machine_model.nozzle_diameter` |
| Multi-color | Bộ đầu in 4 màu tiêu chuẩn (tích hợp, không phải ACE rời) | user |
| Kiểu khung | i3 | 🔎 `printer_structure` |
| Firmware flavor | Klipper | 🔎 `gcode_flavor` |
| Vùng in | 260 × 260 × 260 mm | 🔎 `printable_area`, `printable_height` |
| `setting_id` | GM040 | 🔎 |

### Giới hạn động học (firmware)

| Tham số | Giá trị |
|---|---|
| `machine_max_speed_x` / `_y` | 450 mm/s |
| `machine_max_speed_z` | 12 mm/s |
| `machine_max_speed_e` | 250 mm/s |
| `machine_max_acceleration_x` / `_y` | 10000 mm/s² |
| `machine_max_acceleration_travel` | 10000 mm/s² |
| `machine_max_acceleration_extruding` | 6500 mm/s² |
| `machine_max_acceleration_retracting` | 6500 mm/s² |
| `machine_max_acceleration_z` | 1000 mm/s² |
| `machine_max_jerk_x` / `_y` / `_z` | 20 mm/s |
| `machine_max_jerk_e` | 1 mm/s |

🔵 Đây là trần cứng. Mọi giá trị speed/accel trong process preset vượt mức này
đều bị firmware kẹp xuống — số hiển thị trong slicer thành vô nghĩa.

### Hotend & extruder

| Tham số | Giá trị |
|---|---|
| `nozzle_type` | hardened_steel |
| `nozzle_volume` | 79 mm³ |
| `nozzle_height` | 4 mm |
| `min_layer_height` / `max_layer_height` | 0.08 / 0.28 mm |
| Kiểu truyền động | direct drive (suy ra từ `retraction_length` 0.8 mm) |

### Retraction mặc định (hệ thống)

| Tham số | Giá trị |
|---|---|
| `retraction_length` | 0.8 mm |
| `retraction_speed` / `deretraction_speed` | 30 / 30 mm/s |
| `retraction_minimum_travel` | 1 mm |
| `z_hop` | 0.4 mm, kiểu `Slope Lift` |
| `retract_when_changing_layer` | 1 |

### Multi-material

| Tham số | Giá trị | Ghi chú |
|---|---|---|
| `single_extruder_multi_material` | 1 | 1 hotend, 4 đường vào |
| `enable_prime_tower` | 1 | |
| `purge_in_prime_tower` | 0 | purge xả ra ngoài, không vào tower |
| `printer_flush_multiplier` | 0.7 | |
| `flush_into_infill` | 0 | 🟡 chưa thu hồi purge |
| `flush_into_objects` | 0 | 🟡 chưa thu hồi purge |
| `flush_into_support` | 1 | |
| `prime_tower_width` | 30 mm | |

🟡 **Chưa từng slice 4 màu trên máy này.** Mọi pairing Kobra X đã lưu trong
`.conf` vẫn là single-filament: `flush_volumes_matrix = "0.000000"` (1×1, cần
4×4), `flush_volumes_vector` chỉ 2 phần tử, `filament_colors = "#FFFFFF"`.
Bốn slot hiện tại (xem `Filaments.md`) là Red / White / Black / Cyan — các cặp
tối↔sáng cần flush khoảng 450–650 mm³, không phải 140 mm³ mặc định.

## Phần mềm

| Mục | Giá trị | Nguồn |
|---|---|---|
| Slicer | Anycubic Slicer Next | user |
| Version | 1.4.1.2 (build `20260604104233`) | 🔎 `crash/version.txt` |
| Nhân | dẫn xuất từ OrcaSlicer / BambuStudio (schema preset giống hệt) | 🔎 |
| Region / Language | Global / en_GB | 🔎 `app.region`, `app.language` |
| Đơn vị | mm | 🔎 `app.units = 0` |
| Tài khoản cloud | user id `855643` (đã đăng nhập) | 🔎 tên thư mục `user\855643` |

### Vị trí dữ liệu

```
%APPDATA%\AnycubicSlicerNext\
  AnycubicSlicerNext.conf      trạng thái app + cặp machine/filament/process đang chọn
                               (JSON hợp lệ + 1 dòng "# MD5 checksum" ở cuối)
  system\Anycubic\             preset gốc của hãng, CHỈ ĐỌC
  user\855643\                 preset của bạn (chỉ lưu key đã đổi + "inherits")
  user\855643\filament\base\   bản snapshot cache, TRÙNG TÊN với preset thật
  user\855643\*.info           sidecar sync, chứa updated_time
  log\, crash\                 log MQTT / cloud SDK / app
%LOCALAPPDATA%\AnycubicSlicerNext\1.4.1.2\EBWebView\   WebView2, không liên quan preset
```

### Bẫy đã gặp khi thao tác file preset

1. `filament\base\X.json` và `filament\X.json` cùng `"name"`. File top-level là
   preset sống; bản trong `base` không được phép thắng khi build index.
2. Sửa `.json` mà không bump `updated_time` trong `.info` → cloud sync coi file
   là cũ và ghi đè lại.
3. `.conf` không phải JSON thuần — có dòng `# MD5 checksum` phía sau. Phải dùng
   `raw_decode`. Nếu ghi lại `.conf` thì phải tính lại MD5.
4. **Phải đóng slicer trước khi ghi.** Nó giữ preset trong RAM và flush xuống
   đĩa lúc thoát, xoá sạch mọi thay đổi từ bên ngoài.

## Preset của người dùng (14 cái)

| Loại | Tên | Kế thừa |
|---|---|---|
| machine | `Anycubic Kobra X 0.4 nozzle - Copy` | stock |
| machine | `Anycubic Kobra X 0.4 nozzle - high quality` | stock |
| filament | `Anycubic PLA @Kobra X - Copy` | `Anycubic PLA @Kobra X` |
| filament | `BBL PLA Lite` | `Anycubic PLA @Kobra X` |
| filament | `BBL PLA Lite @Kobra X` | `Anycubic PLA @Kobra X` |
| filament | `BBL PLA Lite - High Quantity @Kobra X` | `Anycubic PLA @Kobra X` |
| filament | `Anycubic PLA @Kobra S1 - Copy` | máy khác, không dùng |
| process | `0.12 mm - High Quality Novi @AC KX` | `0.20mm Standard @Kobra X` |
| process | `0.20mm - High Quality Novi @AC KX` | `0.20mm Standard @Kobra X` |
| process | `0.20mm - Standard Novi @AC KX` | `0.20mm Standard @Kobra X` |
| process | `0.20mm PLA Lite @AC KX - Copy` | `0.20mm Standard @Kobra X` |
| process | `0.20mm PLA Lite @AC KX - fix first layer` | `0.20mm Standard @Kobra X` |
| process | `0.20mm Standard @AC KX - Copy` | `0.20mm Standard @Kobra X` |
| process | `0.24mm Fast speed @AC KX` | `0.24mm Standard @Kobra X` |

## Vấn đề đã biết của preset gốc Anycubic

🔴 Preset hãng **tự mâu thuẫn ngay khi cài**: `Anycubic PLA @Kobra X` khai
`filament_max_volumetric_speed = 13`, nhưng process `0.20mm Standard @Kobra X`
của chính hãng yêu cầu `inner_wall_speed = 300` → 27 mm³/s, gấp đôi trần.
Slicer âm thầm kẹp tốc độ xuống; số trong UI và thời gian ước tính đều sai.

Preset `Anycubic PLA High Speed @Kobra X` của hãng dùng 18 mm³/s trên cùng
hotend — đó là mức trần thực tế cho PLA chạy tốt.

❌ Không sửa bằng cách kẹp speed trong process preset — giới hạn flow thuộc về
filament, slicer đã tự enforce lúc slice. Kẹp vào process là nhét giới hạn của
một loại nhựa vào profile dùng chung.
