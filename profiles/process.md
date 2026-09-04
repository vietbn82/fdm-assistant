# Process preset — tầng process

Năm profile theo mục đích in. Tầng nào sở hữu gì: `docs/preset-model.md` mục 3.

🟢 **Đọc từ đĩa 2026-09-03 22:0x, sau khi Viet dựng lại toàn bộ preset trên
slicer 2.0.0.2.** Bộ trên máy là chuẩn. Bộ cũ (`Novi … @AC KX`) không còn tồn
tại — mọi override cũ không nêu ở đây đều đã **bị bỏ**, giá trị hiệu dụng giờ
lấy từ preset hãng.

Tên: `{layer height} {Figure|FIGURE|TOOL|TEST} @AC KX`.
🟡 Chữ hoa/thường không nhất quán (`0.12 Figure` vs `0.16 FIGURE`) — chỉ là tên
hiển thị, không ảnh hưởng gì, nhưng grep phải để ý.

---

## Bộ hiện tại

| Preset | Kế thừa | Mục đích |
|---|---|---|
| `0.12 Figure @AC KX` | `0.12mm High Quality @Kobra X` | sắc nét nhất, model nhỏ |
| `0.16 FIGURE @AC KX` | `0.16mm High Quality @Kobra X` | model lớn hơn, vẫn cần sắc nét |
| `0.20 Figure @AC KX` | 🟢 `0.20mm High Quality @Kobra X` | figure nhanh hơn |
| `0.20 TOOL @AC KX` | `0.20mm Standard @Kobra X` | chắc, đủ nhanh |
| `0.28 TEST @AC KX` | `0.28mm Standard @Kobra X` | nhanh nhất |

🟢 **B1 (cha lệch) đã hết.** `0.20 Figure` giờ kế thừa đúng `0.20mm High Quality`
và **không còn** override `layer_height` tay — cấu trúc đúng, không phải chạy
được nhờ vá.

🔵 Preset user giờ rất mỏng: 11–15 khoá cho FIGURE, 7 cho TOOL, 6 cho TEST.
Càng mỏng càng dễ theo kịp khi hãng cập nhật profile gốc.

---

## FIGURE — ba bản dùng chung một bộ override

`0.12 Figure`, `0.16 FIGURE`, `0.20 Figure` **giống hệt nhau** về override, trừ
hai khoá lớp đầu chỉ có ở 0.20:

| Key | Cha | Đặt | Vì sao |
|---|---|---|---|
| `seam_gap` | 10% | **15%** | chừa hở nhiều hơn ở điểm khép vòng, bớt cục nhựa |
| `wipe_before_external_loop` | 0 | **1** | lau trước khi vào tường ngoài, giấu điểm bắt đầu |
| `wipe_on_loops` | 0 | **1** | |
| `slowdown_for_curled_perimeters` | 0 | **1** | chậm lại ở mép bị cong vênh |
| `reduce_crossing_wall` | 0 | **1** | travel không cắt ngang qua vật |
| `max_travel_detour_distance` | 0 | **40** | trần cho đường vòng của khoá trên |
| `prime_tower_width` | 30–35 | **10** | tháp mồi hẹp, bớt rác |
| `seam_slope_type` | none | **external** | scarf joint ở tường ngoài |
| `seam_slope_conditional` | 1 | **0** | 1 = phần lớn seam bị bỏ qua |
| `seam_slope_min_length` | 10 | **5** | figure chi tiết nhỏ, đa số viền dưới 10 mm |
| `scarf_joint_flow_ratio` | 1 | **0.95** | bớt nhựa ở đoạn chồng của scarf |
| `initial_layer_speed` | 50 | **30** *(chỉ 0.20)* | chậm hơn = bám bàn tốt hơn |
| `initial_layer_infill_speed` | 100 | **50** *(chỉ 0.20)* | |

🟡 **Lớp đầu của 0.12 và 0.16 giờ chạy tốc độ hãng (50 / 50 và 50 / 100).** Bộ cũ
hạ xuống 30 cho cả ba để bám bàn. Chỉ 0.20 còn giữ. Nếu lớp đầu bong góc trên
0.12/0.16 thì đây là chỗ nhìn trước tiên.

### Giá trị hiệu dụng, ba bản FIGURE

| Key | 0.12 | 0.16 | 0.20 |
|---|---|---|---|
| `layer_height` / `initial_layer_print_height` | 0.12 / 0.2 | 0.16 / 0.2 | 0.2 / 0.2 |
| `outer_wall_speed` / `inner_wall_speed` | 60 / 150 | 60 / 150 | 60 / 150 |
| `top_surface_speed` | 150 | 150 | 150 |
| `initial_layer_speed` / `_infill_speed` | 50 / 50 | 50 / 100 | **30 / 50** |
| `wall_loops` | 2 | 2 | 2 |
| `top` / `bottom_shell_layers` | 5 / 5 | **6** / 4 | 5 / 3 |
| `sparse_infill_density` / `pattern` | 15% / **3dhoneycomb** | 15% / gyroid | 15% / gyroid |
| `brim_type` / `ironing_type` | auto_brim / no ironing | auto_brim / no ironing | auto_brim / no ironing |
| `detect_thin_wall` | 0 | 0 | 0 |
| `small_perimeter_threshold` | 0 | 0 | 0 |
| `skirt_loops` | 0 | 0 | 0 |

Tất cả cột trên là **kế thừa từ hãng**, không phải override — ba bản khác nhau
chỉ vì cha khác nhau.

🟡 Ba khác biệt còn sót giữa ba bản, đều do cha, đều **không cố ý**:

| | Lệch | Hệ quả |
|---|---|---|
| `0.12` dùng `3dhoneycomb`, hai bản kia `gyroid` | cha 0.12 HQ đặt vậy | infill 0.12 không đẳng hướng như hai bản kia |
| `0.16` có `top_shell_layers = 6`, hai bản kia 5 | cha 0.16 HQ đặt vậy | 0.16 dày mặt trên hơn, in lâu hơn chút |
| `bottom_shell_layers` 5 / 4 / 3 | cha | mặt đáy 0.20 mỏng nhất (3 × 0.2 = 0.6 mm) |

📝 Muốn ba bản khớp nhau thì phải pin lại — nhưng đó là thêm override vào preset
vừa mới được dọn sạch. Chờ Viet chốt (B3 trong `TODO.md`).

### Những gì bộ cũ có mà bộ mới bỏ

| Key | Bộ cũ | Giờ | Rủi ro |
|---|---|---|---|
| `outer_wall_speed` | 50 | **60** *(cha)* | 🔵 nhanh hơn 20%, có thể lộ rung ở cạnh |
| `top_surface_speed` | 80 *(P21)* | **150** *(cha)* | 🟡 P21 sinh ra vì mặt trên xấu ở 150 — theo dõi lại |
| `initial_layer_speed` | 30 | **50** *(0.12, 0.16)* | 🟡 bám bàn, xem trên |
| `initial_layer_infill_speed` | 50 *(0.16)* | **100** *(cha)* | 🟡 infill lớp đầu nhanh gấp đôi |
| `detect_thin_wall` | 1 *(0.12, 0.16)* | **0** *(cha)* | 🔵 chi tiết mảnh có thể bị bỏ |
| `small_perimeter_threshold` | 20 | **0** *(cha)* | 🔵 `small_perimeter_speed` không bao giờ kích hoạt |
| `skirt_loops` | 0 *(cha, không đổi)* | **0** | ⚪ FIGURE chưa bao giờ đè khoá này — chỉ TOOL/TEST từng đặt 2 |
| `ironing_*` | 0.2 / 0.1 / 20 | *(cha)* | ⚪ vốn là khoá chết, `ironing_type = no ironing` |
| `layer_height` pin trên 0.20 | 0.2 | *(cha 0.20 HQ)* | 🟢 hết vá |

## TOOL 0.20 — override còn lại rất mỏng

| Key | Cha | Đặt | Vì sao |
|---|---|---|---|
| `sparse_infill_pattern` | grid | **gyroid** | đẳng hướng, chịu lực mọi chiều |
| `small_perimeter_threshold` | 0 | **20** | ngưỡng 0 mm khiến `small_perimeter_speed` không bao giờ chạy |
| `seam_gap` | 10% | **15%** | |
| `wipe_before_external_loop` / `wipe_on_loops` | 0 / 0 | **1 / 1** | |
| `slowdown_for_curled_perimeters` | 0 | **1** | |
| `overhang_2_4_speed` | 30 | **30** | ⚪ trùng giá trị cha — pin thừa, vô hại |

Hiệu dụng: `wall_loops = 2`, `wall_sequence = inner wall/outer wall`,
`sparse_infill_density = 15%`, `bottom_shell_layers = 3`, `top_shell_layers = 5`,
`outer_wall_speed = 200`, `inner_wall_speed = 300`.

🔴 **Bộ cũ đặt độ bền, bộ mới thì không.** `wall_loops` 4 → 2,
`wall_sequence = inner-outer-inner` → mặc định, `sparse_infill_density` 25% → 15%,
`bottom_shell_layers` 4 → 3. Preset TOOL giờ gần như bằng `0.20mm Standard` của
hãng, chỉ khác infill pattern và mấy khoá seam. Đồ dùng chịu lực in bằng preset
này sẽ **yếu hơn hẳn** so với trước 03/09.

🟡 `outer_wall_speed` 120 → **200**. Bộ cũ hạ xuống 120 vì 200 mm/s quá nhanh cho
dung sai máy i3. Thực tế trần flow hạ nó xuống ~154 mm/s (xem dưới) nhưng vẫn
nhanh hơn 120 rõ rệt.

## TEST 0.28 — chỉ nhanh

| Key | Cha | Đặt |
|---|---|---|
| `sparse_infill_density` | 15% | **10%** |
| `sparse_infill_pattern` | grid | **3dhoneycomb** |
| `top_shell_layers` | 3 | **2** |
| `bottom_shell_layers` | 3 | **2** |
| `flush_into_objects` / `flush_into_infill` | 0 / 0 | **1 / 1** |

🟡 `--audit`: top shell 2 × 0.28 = 0.56 mm < 0.6 mm — mặt trên có thể hơi rỗ.
Chấp nhận được với bản thử, đó là chỗ đổi lấy tốc độ.

🟢 **Không cần đổi Printer preset nữa khi in 0.28.** Bộ cũ bắt chuyển sang bản
`- TEST` vì `z_hop = 0.2` không vượt nổi lớp 0.28; giờ `z_hop` để nguyên 0.4 của
hãng ở cả hai machine preset.

🔵 Bỏ so với bộ cũ: `brim_type = no_brim` (giờ `auto_brim`), `skirt_loops = 2`,
`seam_gap`, `small_perimeter_threshold`, `wipe_*`, `slowdown_for_curled_perimeters`.

📝 Khi test một thứ cụ thể — dung sai lỗ, khớp nối, overhang — chỉ nâng chất
lượng đúng vùng đó bằng **height range modifier** hoặc **object setting
override**, đừng đổi cả profile.

---

## Trần flow quyết định tốc độ, không phải layer height

`filament_max_volumetric_speed = 13` mm³/s trên cả hai filament preset. Số dưới
đọc từ `--audit --flow`, tức tốc độ **thật** sau khi slicer hạ xuống:

| Preset | Khoá bị hạ | Đặt | Thật |
|---|---|---|---|
| `0.12 Figure` | — | | 🟢 không khoá nào chạm trần |
| `0.16 FIGURE` | `sparse_infill_speed` | 200 | 180 |
| | `internal_solid_infill_speed` | 200 | 193 |
| | `gap_infill_speed` | 250 | 180 |
| `0.20 Figure` | `inner_wall_speed` | 150 | 144 |
| | `sparse_infill_speed` | 200 | 144 |
| | `internal_solid_infill_speed` | 200 | 154 |
| `0.20 TOOL` | `outer_wall_speed` | 200 | 154 |
| | `inner_wall_speed` / `sparse_infill_speed` | 300 | 144 |
| | `internal_solid_infill_speed` | 250 | 154 |
| | `top_surface_speed` | 200 | 154 |
| `0.28 TEST` | mọi tốc độ chính | 200 | 103–110 |

🔵 **Trên trần flow, layer dày hơn không cho tốc độ cao hơn** — throughput đứng
yên. Cái lợi duy nhất của layer dày là **ít lớp hơn**: bớt thời gian Z, bớt
accel/decel, bớt đổi hướng.

🔵 Tốc độ **không** bị hạ tay xuống cho khớp trần flow. Slicer tự làm lúc slice —
xem `docs/preset-model.md` mục 3. Muốn nhanh hơn thật thì phải nâng trần flow ở
tầng filament, và phải đo trước.

---

## In 4 màu

| | FIGURE (cả ba) | TOOL | TEST |
|---|---|---|---|
| `flush_into_objects` | ❌ 0 | ❌ 0 | ✅ 1 |
| `flush_into_infill` | ❌ 0 | ❌ 0 | ✅ 1 |
| `flush_into_support` | 1 | 1 | 1 |
| `enable_prime_tower` | 1 | 1 | 1 |
| `prime_tower_width` | 10 | 30 | 30 |

🟡 **TOOL đã tắt thu hồi purge (đổi 03/09).** Bộ cũ bật `flush_into_objects` +
`_infill` cho TOOL và TEST; giờ chỉ TEST. Với TOOL, toàn bộ nhựa purge thành rác
trừ khi bản in có support. Bật lại nếu thấy tốn nhựa — nhựa thải nằm khuất bên
trong đồ dùng, hiếm khi lộ.

🟡 `purge_in_prime_tower` ở tầng machine giờ là **0** (kế thừa hãng) — xem cảnh
báo trong `profiles/printer.md`. Hai khoá này khác nhau: `flush_into_*` quyết
định *xả vào đâu*, `purge_in_prime_tower` quyết định *có xả vào tháp mồi không*.

### Ma trận flush (đọc từ gcode 2026-08-29)

🔵 Nguồn: gcode slicer sinh ra lúc 16:31 ngày 29/08 cho một mẫu 4 màu. Đơn vị
mm³, đọc theo hàng: **từ** màu hàng **sang** màu cột.

| từ ↓ / sang → | Beige | White | Black | Matcha |
|---|---|---|---|---|
| **Beige** `#F7E6DE` | — | 188 | 142 | 169 |
| **White** `#FFFFFF` | 139 | — | 142 | 174 |
| **Black** `#000000` | **785** | **785** | — | **635** |
| **Matcha** `#BBFB98` | 216 | 276 | 203 | — |

Tổng **3854 mm³** nếu chạy đủ 12 lần đổi màu ≈ 4,8 g PLA.

🔴 **Hàng Black một mình chiếm 2205 mm³ — 57% toàn bộ.** Đổi *từ* đen sang bất kỳ
màu nào cũng đắt; đổi *sang* đen thì rẻ nhất bảng (142–203).

📝 Sắp thứ tự in để **gom các đoạn màu đen lại**. Mỗi lần rời đen tốn 635–785 mm³.

🟡 **Bảng này chưa kiểm lại sau khi lên 2.0.0.2.** `.conf` của bản 2.0.0.2 không
còn lưu `filament_colors` và bảng gán slot→preset (mục `presets` chỉ còn
`filaments` và `machine`), nên không đọc lại được từ config — muốn số mới phải
slice một mẫu 4 màu rồi đọc gcode. Xem `profiles/filament.md`.

`printer_flush_multiplier = 0.7` ở machine preset là hệ số nhân chung — hạ xuống
sẽ giảm cả 12 ô cùng lúc, nhưng chỉ nên làm sau khi thấy bản in thật không lem.
