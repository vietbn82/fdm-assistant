# Process preset — tầng process

Ba profile theo mục đích in. Tầng nào sở hữu gì: `docs/preset-model.md` mục 3.

Quy tắc đặt tên: `Novi {layer height} - {FIGURE|TOOL|TEST} @AC KX`

---

## Bộ hiện tại

| Preset | Kế thừa | Mục đích |
|---|---|---|
| `Novi 0.12 - FIGURE @AC KX` | `0.12mm High Quality @Kobra X` | sắc nét nhất, model nhỏ |
| `Novi 0.16 - FIGURE @AC KX` | `0.16mm High Quality @Kobra X` | model lớn hơn, vẫn cần sắc nét nhưng 0.12 quá lâu |
| `Novi 0.20 - TOOL @AC KX` | `0.20mm Standard @Kobra X` | chắc, đủ nhanh |
| `Novi 0.28 - TEST @AC KX` | `0.28mm Standard @Kobra X` | nhanh nhất, bỏ mọi thứ thừa |

Mỗi profile kế thừa preset hãng **đúng layer height của nó**, nên chỉ phải ghi
đè vài key. Không cái nào chép lại giá trị đã đúng sẵn ở cha.

🔵 Tốc độ **không** bị hạ xuống cho khớp trần flow của nhựa. Đó là việc của
filament preset, slicer tự làm lúc slice — xem `docs/preset-model.md` mục 3.

---

## Áp cho cả bốn profile

| Key | Cha | Đặt | Vì sao |
|---|---|---|---|
| `small_perimeter_threshold` | 0 | **20** | ngưỡng 0 mm khiến `small_perimeter_speed = 50%` **không bao giờ chạy** — không đoạn nào đủ điều kiện "chu vi nhỏ". 20 mm chu vi ≈ đường kính 6,4 mm |
| `wipe_before_external_loop` | 0 | **1** | lau trước khi vào tường ngoài, giấu điểm bắt đầu |
| `seam_gap` | 10% | **15%** | chừa hở nhiều hơn ở điểm khép vòng, bớt cục nhựa |
| `skirt_loops` | 0 | **2** | mồi nhựa trước khi vào vật — vị trí in đầu tiên hay thiếu nhựa |
| `wipe_on_loops` | 0 | **1** | |

🔵 `small_perimeter_threshold` đo theo **chu vi**, không phải bán kính. Lỗ và trụ
nhỏ hơn ngưỡng in ở 50% tốc độ tường ngoài — đầu đùn kịp bơm trong đoạn ngắn.

---

## FIGURE — ưu tiên sắc nét

Hai bản, cùng ý đồ, khác layer height. Chọn 0.12 cho model nhỏ nhiều chi tiết,
0.16 khi model lớn và 0.12 mất quá nhiều thời gian.

Đánh đổi: chậm, lấy cạnh sắc và mặt trên liền.

### FIGURE 0.12 — cha `0.12mm High Quality @Kobra X`

| Key | Cha | Đặt | Vì sao |
|---|---|---|---|
| `outer_wall_speed` | 60 | **50** | tốc độ tường ngoài quyết định độ sắc |
| `sparse_infill_density` | 15% | **12%** | figure không chịu lực |
| `sparse_infill_pattern` | 3dhoneycomb | **gyroid** | |
| `ironing_type` | no ironing | **top** | mặt trên phẳng |
| `seam_slope_type` | none | **all** | scarf joint, giấu đường seam |
| `detect_thin_wall` | 0 | **1** | giữ chi tiết mảnh |
| `slowdown_for_curled_perimeters` | 0 | **1** | |

Kế thừa sẵn: `wall_sequence = inner wall/outer wall` (outer in sau cùng — bề mặt
đẹp nhất), `outer_wall_acceleration = 2000`, `seam_position = aligned`,
`ironing_speed = 15`, `ironing_spacing = 0.1`, top/bottom shell 5/5.

🟢 Ở layer 0.12, trần flow không phải giới hạn (~297 mm/s). Chất lượng mới là
thứ quyết định tốc độ, nên giá trị của hãng dùng được nguyên.

### FIGURE 0.16 — cha `0.16mm High Quality @Kobra X`

| Key | Cha | Đặt | Vì sao |
|---|---|---|---|
| `outer_wall_speed` | 60 | **50** | như trên |
| `sparse_infill_density` | 15% | **12%** | |
| `ironing_type` | no ironing | **top** | |
| `ironing_speed` | 30 | **20** | 30 là bào chứ không phải miết |
| `ironing_spacing` | 0.15 | **0.1** | |
| `seam_slope_type` | none | **all** | |
| `detect_thin_wall` | 0 | **1** | |
| `slowdown_for_curled_perimeters` | 0 | **1** | |

Kế thừa sẵn: `wall_sequence`, `outer_wall_acceleration = 2000`, `seam_position =
aligned`, `wall_loops = 2`, top/bottom shell **6/4**.

🟢 Bớt được một override so với bản 0.12: cha của 0.16 đã dùng `gyroid` sẵn.
Ngược lại phải đè `ironing_speed` và `ironing_spacing` vì cha đặt 30 / 0.15,
trong khi cha của 0.12 đã đặt sẵn 15 / 0.1.

🔵 Flow vẫn chưa chạm trần: nhanh nhất 200 mm/s → 14,4 mm³/s ở layer 0.16, dưới
15. Với slot 2 (Generic, trần 13) thì phần internal solid bị hạ nhẹ.

## TOOL 0.20 — ưu tiên chắc + nhanh

Đánh đổi: bỏ hoàn thiện bề mặt, lấy độ bền.

| Key | Cha | Đặt | Vì sao |
|---|---|---|---|
| `wall_loops` | 2 | **4** | 🔵 độ bền đến từ tường, rẻ hơn nhiều so với tăng infill |
| `wall_sequence` | inner wall/outer wall | **inner-outer-inner wall** | liên kết tường tốt nhất |
| `sparse_infill_density` | 15% | **25%** | trên 30% gần như không thêm độ bền |
| `sparse_infill_pattern` | grid | **gyroid** | đẳng hướng, chịu lực mọi chiều |
| `bottom_shell_layers` | 3 | **4** | |
| `outer_wall_speed` | 200 | **120** | 200 mm/s quá nhanh cho dung sai trên máy i3 |

Kế thừa sẵn: `ironing_type = no ironing`, `enable_support = 0`,
`ensure_vertical_shell_thickness = ensure_all`, `top_shell_layers = 5`.

🟢 `enable_support` để ở 0 và **không đè**. Support là thuộc tính từng model,
bật trong profile nghĩa là mọi bản in đều sinh support.

## TEST 0.28 — chỉ nhanh

Đánh đổi: bỏ mọi thứ không phải cái đang cần kiểm tra.

| Key | Cha | Đặt | Vì sao |
|---|---|---|---|
| `sparse_infill_density` | 15% | **5%** | |
| `sparse_infill_pattern` | grid | **lightning** | chỉ đỡ mặt trên, nhanh hơn hẳn grid |
| `top_shell_layers` | 3 | **2** | |
| `bottom_shell_layers` | 3 | **2** | |
| `brim_type` | auto_brim | **no_brim** | bật lại thủ công khi model chân nhỏ |

🟡 Top shell 2 × 0.28 = 0.56 mm, dưới ngưỡng 0.6 mm nên mặt trên có thể hơi
rỗ. Chấp nhận được với bản thử — đó chính là chỗ đổi lấy tốc độ.

📝 Khi test một thứ cụ thể — dung sai lỗ, khớp nối, overhang — chỉ nâng chất
lượng đúng vùng đó bằng **height range modifier** hoặc **object setting
override**, đừng đổi cả profile.

---

## Trần flow quyết định tốc độ, không phải layer height

Với `filament_max_volumetric_speed` = 15 mm³/s *(hiện đang để 13 — bảng dưới
giữ 15 để so sánh, tốc độ thực tế thấp hơn ~13%)*:

| layer | line width | tốc độ tối đa thực tế |
|---|---|---|
| 0.12 | 0.42 | ~297 mm/s — flow không phải giới hạn |
| 0.16 | 0.45 | ~208 mm/s — vẫn chưa chạm |
| 0.20 | 0.45 | ~166 mm/s |
| 0.28 | 0.45 | ~119 mm/s |

🔵 **Trên trần flow, layer dày hơn không cho tốc độ cao hơn** — throughput đứng
yên. Cái lợi duy nhất của layer dày là **ít lớp hơn**: bớt thời gian Z, bớt
accel/decel, bớt đổi hướng. Vẫn đáng, nhưng không tuyến tính như thường nghĩ.

Đó là lý do TEST ở 0.28 nhanh hơn TOOL ở 0.20, nhưng không nhanh gấp rưỡi.

---

## In 4 màu

Nhóm prime tower và flush nằm ở tầng process, nên chiến lược purge đổi theo mục đích:

| | FIGURE | TOOL | TEST |
|---|---|---|---|
| `flush_into_objects` | ❌ 0 | ✅ 1 | ✅ 1 |
| `flush_into_infill` | ❌ 0 | ✅ 1 | ✅ 1 |
| `flush_into_support` | 1 | 1 | 1 |
| `enable_prime_tower` | 1 | 1 | chỉ khi cần |
| flush tối↔sáng | cao, 450–650 mm³ | vừa, 300–400 | thấp, chấp nhận lem |

Với FIGURE, nhựa xả vào thân vật thể có thể lộ ra bề mặt hoặc lẫn màu ở lớp kế
tiếp. Với TOOL và TEST thì nằm khuất bên trong — thu hồi được phần lớn nhựa
purge, giảm rác đáng kể.

🟢 **Đã bật** cho TOOL và TEST ngày 2026-08-23. FIGURE giữ 0 như mặc định hãng.

### Ma trận flush thật (slicer tự tính, 2026-08-23)

Đơn vị mm³, đọc theo hàng: **từ** màu hàng **sang** màu cột.

| từ ↓ / sang → | Red | White | Black | Cyan |
|---|---|---|---|---|
| **Red** | — | **785** | 174 | 142 |
| **White** | 142 | — | 142 | 142 |
| **Black** | 388 | **785** | — | 285 |
| **Cyan** | 214 | 285 | 150 | — |

Tổng **3634 mm³** nếu chạy đủ 12 lần đổi màu ≈ 4,5 g PLA.

🟢 Con số hợp lý, không cần chỉnh. Quy luật rõ ràng: đổi **sang White** đắt nhất
(785) vì màu sáng bị màu cũ làm bẩn dễ nhất; đổi **từ White** rẻ nhất (142, đúng
sàn) vì màu đậm phủ lên trắng rất nhanh.

🔵 Ước tính trước đó của tôi là 450–650 mm³ cho cặp tối↔sáng — thấp hơn thực tế.
Slicer tính từ khoảng cách màu và rộng tay hơn. Dùng số của slicer.

`printer_flush_multiplier = 0.7` ở machine preset là hệ số nhân chung — hạ xuống
sẽ giảm cả 12 ô cùng lúc, nhưng chỉ nên làm sau khi thấy bản in thật không lem.

🟢 Trước đây toàn bộ 3634 mm³ thành rác vì chỉ `flush_into_support` bật, mà
support không phải bản in nào cũng có. TOOL và TEST giờ thu hồi được phần lớn.

🟡 `flush_into_objects` nhét nhựa thải vào **phần đặc** của vật thể, không chỉ
infill. Với đồ dùng thì không thấy — nhưng nếu in đồ dùng cần mặt ngoài đẹp thì
tắt lại cho riêng bản đó.
