# PENDING APPLY — thay đổi preset chờ duyệt

Kho chứa mọi thay đổi preset đã đề xuất nhưng **chưa ghi vào máy**. Không có
thay đổi nào ở đây đã được áp dụng.

**Cách dùng:** đọc, rồi nói ID nào được duyệt — `"apply P1 P4 P7"` hoặc
`"apply nhóm 2"`. Claude lấy đúng những dòng đó, chạy lệnh ghi kèm backup, rồi
chuyển chúng xuống mục **Đã áp dụng** ở cuối file.

- Mỗi dòng có sẵn lệnh chính xác. Duyệt xong là chạy được, không phải suy diễn lại.
- ❌ Claude không tự áp bất cứ dòng nào ở đây, kể cả khi thấy hiển nhiên.
- 🟡 Đóng slicer trước khi áp. Mọi lần ghi đều backup `user\` trước.
- `TODO.md` là *quyết định* cần đưa ra. File này là *thao tác* sẽ chạy khi đã quyết.

Trạng thái: 📝 chờ duyệt / ⏳ chờ điều kiện khác / 🔴 chặn kỹ thuật

---

## Nhóm 1 — Sửa độc lập, không phụ thuộc quyết định nào

| ID | Preset | Key | Hiện tại | Đề xuất | Vì sao |
|---|---|---|---|---|---|
| P1 📝 | `0.20mm - Standard Novi @AC KX` | `enable_support` | `1` | `0` | support là thuộc tính từng model, không phải từng profile — bật sẵn nghĩa là mọi print đều sinh support |
| P2 📝 | `0.20mm - Standard Novi @AC KX` | `bridge_speed` | `15` | `30` | mặc định hãng là 30; 15 chậm tới mức bridge võng vì ngấm nhiệt. **Chỉ áp nếu bạn không cố ý đặt thấp** — B6 trong `TODO.md` |
| P3 📝 | `0.12 mm - High Quality Novi @AC KX` | `bottom_shell_layers` | *(kế thừa 3)* | `4` | 3 × 0.12 = 0.36 mm, dưới ngưỡng 0.4 mm. Chỉ áp nếu bạn từng thấy đáy lộ/xuyên sáng — B3 |

```bash
python tools/acslicer_tune.py --set "0.20mm - Standard Novi @AC KX|enable_support=0"      # P1
python tools/acslicer_tune.py --set "0.20mm - Standard Novi @AC KX|bridge_speed=30"       # P2
python tools/acslicer_tune.py --set "0.12 mm - High Quality Novi @AC KX|bottom_shell_layers=4"  # P3
```

## Nhóm 2 — Trần flow

| ID | Preset | Key | Hiện tại | Đề xuất | Điều kiện |
|---|---|---|---|---|---|
| P4 📝 | `Anycubic PLA @Anycubic Kobra X 0.4 nozzle - Copy` | `filament_max_volumetric_speed` | `18` | `13` | 18 là số Anycubic dùng cho `PLA High Speed`, chưa đo trên máy này, và preset này **không nằm ở slot nào**. Trả về mặc định trừ khi bạn định gán cho slot 2 — B4, B5 |
| P5 ⏳ | `BBL PLA Lite` | `filament_max_volumetric_speed` | `15` | `13` | **chỉ khi flow test A1 thất bại** |
| P6 ⏳ | `BBL PLA Lite @Anycubic Kobra X 0.4 nozzle` | `filament_max_volumetric_speed` | `15` | `13` | như trên |
| P7 ⏳ | `BBL PLA Lite - High Quantity @Anycubic Kobra X 0.4 nozzle` | `filament_max_volumetric_speed` | `15` | `13` | như trên |

```bash
# P4
python tools/acslicer_tune.py --set "Anycubic PLA @Anycubic Kobra X 0.4 nozzle - Copy|filament_max_volumetric_speed=13"
# P5 P6 P7 — chỉ chạy nếu flow test 15 mm3/s cho ra thành wall đùn thiếu
python tools/acslicer_tune.py \
  --set "BBL PLA Lite|filament_max_volumetric_speed=13" \
  --set "BBL PLA Lite @Anycubic Kobra X 0.4 nozzle|filament_max_volumetric_speed=13" \
  --set "BBL PLA Lite - High Quantity @Anycubic Kobra X 0.4 nozzle|filament_max_volumetric_speed=13"
```

## Nhóm 3 — FIG / TOOL / TEST ⏳ chờ B1

Chỉ chạy sau khi bạn chốt có làm ba profile theo mục đích. Lý do từng giá trị:
`profiles/process.md` mục 3–5.

### P8 ⏳ `0.12 mm - High Quality Novi @AC KX` → FIG

| Key | Hiện tại | Đề xuất |
|---|---|---|
| `wall_sequence` | `outer wall/inner wall` | `inner wall/outer wall` — outer in sau cùng, bề mặt đẹp hơn |
| `outer_wall_speed` | `60` | `50` |
| `outer_wall_acceleration` | *(kế thừa)* | `2500` |
| `detect_thin_wall` | *(kế thừa 0)* | `1` |
| `seam_position` | *(kế thừa)* | `aligned` |

```bash
python tools/acslicer_tune.py \
  --set "0.12 mm - High Quality Novi @AC KX|wall_sequence=inner wall/outer wall" \
  --set "0.12 mm - High Quality Novi @AC KX|outer_wall_speed=50" \
  --set "0.12 mm - High Quality Novi @AC KX|outer_wall_acceleration=2500" \
  --set "0.12 mm - High Quality Novi @AC KX|detect_thin_wall=1" \
  --set "0.12 mm - High Quality Novi @AC KX|seam_position=aligned"
```

### P9 ⏳ `0.20mm - Standard Novi @AC KX` → TOOL

| Key | Hiện tại | Đề xuất |
|---|---|---|
| `wall_loops` | `3` | `4` — độ bền đến từ tường, rẻ hơn tăng infill |
| `sparse_infill_density` | `20%` | `25%` |
| `sparse_infill_pattern` | `3dhoneycomb` | `gyroid` — đẳng hướng |
| `top_shell_layers` | `6` | `5` |
| `bottom_shell_layers` | *(kế thừa 3)* | `4` |
| `inner_wall_speed` | `100` | `160` — sát trần flow ở layer 0.20 |
| `outer_wall_speed` | `60` | `120` |

Bao gồm cả P1 (`enable_support=0`) — nếu duyệt P9 thì P1 nằm trong đó.

```bash
python tools/acslicer_tune.py \
  --set "0.20mm - Standard Novi @AC KX|wall_loops=4" \
  --set "0.20mm - Standard Novi @AC KX|sparse_infill_density=25%" \
  --set "0.20mm - Standard Novi @AC KX|sparse_infill_pattern=gyroid" \
  --set "0.20mm - Standard Novi @AC KX|top_shell_layers=5" \
  --set "0.20mm - Standard Novi @AC KX|bottom_shell_layers=4" \
  --set "0.20mm - Standard Novi @AC KX|inner_wall_speed=160" \
  --set "0.20mm - Standard Novi @AC KX|outer_wall_speed=120" \
  --set "0.20mm - Standard Novi @AC KX|enable_support=0"
```

### P10 ⏳ `0.24mm Fast speed @AC KX` → TEST

| Key | Hiện tại | Đề xuất |
|---|---|---|
| `layer_height` | *(kế thừa 0.24)* | `0.28` — max của máy |
| `sparse_infill_density` | `10%` | `5%` |
| `sparse_infill_pattern` | *(kế thừa grid)* | `lightning` — chỉ đỡ mặt trên |
| `top_shell_layers` | *(kế thừa 4)* | `2` |
| `bottom_shell_layers` | *(kế thừa 3)* | `2` |
| `brim_type` | *(kế thừa auto_brim)* | `no_brim` |
| `reduce_crossing_wall` | *(kế thừa)* | `0` |

```bash
python tools/acslicer_tune.py \
  --set "0.24mm Fast speed @AC KX|layer_height=0.28" \
  --set "0.24mm Fast speed @AC KX|sparse_infill_density=5%" \
  --set "0.24mm Fast speed @AC KX|sparse_infill_pattern=lightning" \
  --set "0.24mm Fast speed @AC KX|top_shell_layers=2" \
  --set "0.24mm Fast speed @AC KX|bottom_shell_layers=2" \
  --set "0.24mm Fast speed @AC KX|brim_type=no_brim" \
  --set "0.24mm Fast speed @AC KX|reduce_crossing_wall=0"
```

### P11 ⏳ Đổi tên ba preset — chờ B1

`0.12 mm - High Quality Novi @AC KX` → `FIG 0.12 @KX`
`0.20mm - Standard Novi @AC KX` → `TOOL 0.20 @KX`
`0.24mm Fast speed @AC KX` → `TEST 0.28 @KX`

🔴 Đổi tên phải sửa cả `name`, `print_settings_id`, tên file `.json` và `.info`,
đồng thời cập nhật `anycubic_presets` trong `.conf` — mà ghi `.conf` cần tính lại
MD5, chưa làm được. Xem C5 trong `TODO.md`. Cách vòng: đổi tên trong UI slicer.

### P12 ⏳ Xoá ba preset trùng lặp — chờ B2

| Preset | Lý do |
|---|---|
| `0.20mm PLA Lite @AC KX - Copy` | bị `- fix first layer` thay thế hoàn toàn |
| `0.20mm Standard @AC KX - Copy` | gần như y hệt vendor default |
| `0.20mm - High Quality Novi @AC KX` | trùng `0.12 mm - High Quality Novi` trừ `layer_height` |

Xoá = gỡ cặp `.json` + `.info`. An toàn vì có backup, nhưng nên làm trong UI
slicer để `.conf` tự cập nhật theo.

## Nhóm 4 — Chặn kỹ thuật

| ID | Việc | Chặn bởi |
|---|---|---|
| P13 🔴 | Xoá `pellet_flow_coefficient` khỏi `Anycubic PLA @Anycubic Kobra X 0.4 nozzle - Copy` | công cụ chưa có `--unset` — C5 |
| P14 🔴 | `flush_volumes_matrix` 4×4 cho Red/White/Black/Cyan | chưa slice thử 4 màu — A3 |
| P15 🔴 | `flush_into_objects` / `flush_into_infill` theo mục đích | A3, và cần ghi `.conf` — C5 |

🔵 P13 chỉ là rác thẩm mỹ, không ảnh hưởng bản in. Không vội.

---

## Đã áp dụng

*(trống — mọi thứ đã áp dụng ở các phiên trước nằm ở mục D trong `TODO.md`)*
