# Process preset — tầng process

Bảy preset hiện có, và đề xuất gom lại theo mục đích in.
Tầng nào sở hữu gì: `docs/preset-model.md` mục 3.

---

## 1. Hiện trạng: chia theo layer height, không theo mục đích

| preset | lớp | wall | infill | top | ironing | outer/inner | support |
|---|---|---|---|---|---|---|---|
| `0.12 mm - High Quality Novi` | 0.12 | 2 | 12% gyroid | 5 | top | 60/150 | 0 |
| `0.20mm - High Quality Novi` | 0.20 | 2 | 12% gyroid | 5 | top | 60/150 | 0 |
| `0.20mm - Standard Novi` | 0.20 | 3 | 20% 3dhoneycomb | 6 | không | 60/100 | **1** |
| `0.20mm PLA Lite - Copy` | 0.20 | 2 | 15% honeycomb | 5 | top | 50/65 | 0 |
| `0.20mm PLA Lite - fix first layer` | 0.20 | 2 | 15% honeycomb | 5 | top | 50/65 | 0 |
| `0.20mm Standard - Copy` | 0.20 | 2 | 15% honeycomb | 5 | top | 200/300 | 0 |
| `0.24mm Fast speed` | 0.24 | 2 | 10% grid | 4 | không | 200/230 | 0 |

Cả bảy kế thừa `0.20mm Standard @Kobra X` của hãng, riêng `0.24mm Fast speed`
kế thừa `0.24mm Standard @Kobra X`.

- 🔴 Hai cái `High Quality Novi` **giống hệt nhau** trừ `layer_height`. Một
  profile bị nhân đôi, không phải hai ý đồ.
- 🔴 Ba cái `PLA Lite - Copy` / `fix first layer` / `Standard - Copy` chỉ khác
  `seam_slope_type` và tốc độ wall. Ba lần thử cùng một thứ, chưa dọn lần nào.
- 🟡 `enable_support = 1` đóng cứng trong `0.20 Standard Novi`. Support là
  thuộc tính **từng model** — để trong profile nghĩa là mọi print đều sinh support.
- 🟡 Không có profile "test" thật. `0.24 Fast speed` gần nhất nhưng vẫn giữ 4
  top shell và 10% infill, tốn thời gian cho bề mặt mà bản test không cần.
- 🟢 `0.20mm - Standard Novi`: `support_top_z_distance` đã sửa 0.16 → 0.2 cho
  chia hết layer height.

## 2. Trần flow quyết định tốc độ, không phải layer height

Với `filament_max_volumetric_speed` = 15 mm³/s:

| layer | line width | tốc độ tối đa thực tế |
|---|---|---|
| 0.12 | 0.42 | ~297 mm/s — flow không phải giới hạn, chất lượng mới là |
| 0.16 | 0.45 | ~208 mm/s |
| 0.20 | 0.45 | ~166 mm/s |
| 0.24 | 0.45 | ~138 mm/s |
| 0.28 | 0.45 | ~119 mm/s |

🔵 **Trên trần flow, layer dày hơn không cho tốc độ cao hơn** — throughput đứng
yên ở 15 mm³/s. Cái lợi duy nhất của layer dày là **ít lớp hơn**: bớt thời gian
Z, bớt accel/decel, bớt đổi hướng. Vẫn đáng, nhưng không tuyến tính như thường
nghĩ. Đặt `sparse_infill_speed = 300` ở layer 0.28 là con số hư cấu.

---

# Đề xuất: ba profile theo mục đích

> ⏳ **Chưa áp dụng.** Chốt ở B1, B2 trong `TODO.md`; lệnh sẵn ở P8–P12 trong
> `PENDING_APPLY.md`.

## 3. FIG — figure, ưu tiên sắc nét

Đánh đổi: chậm, lấy cạnh sắc và bề mặt liền.

| Setting | Giá trị | Vì sao |
|---|---|---|
| `layer_height` | 0.12 *(0.16 cho model lớn)* | chi tiết dọc |
| `wall_loops` | 2 | tường dày không giúp gì cho figure |
| `wall_sequence` | `inner wall/outer wall` | outer in **sau cùng**, đắp lên nền đặc — bề mặt đẹp nhất |
| `outer_wall_speed` | 50 | thứ quyết định độ sắc |
| `outer_wall_acceleration` | 2000–3000 | accel cao làm tròn góc |
| `seam_slope_type` | `all` *(scarf joint)* | giấu đường seam |
| `seam_position` | `aligned` hoặc `rear` | dồn seam về một phía |
| `sparse_infill_density` | 10–12% gyroid | figure không chịu lực |
| `top_shell_layers` | 5 | |
| `ironing_type` | `top`, speed 20, spacing 0.10–0.12 | mặt trên phẳng |
| `detect_thin_wall` | 1 | giữ chi tiết mảnh |
| `slowdown_for_curled_perimeters` | 1 | |

🟡 Cả hai preset `High Quality Novi` hiện dùng `outer wall/inner wall` — in
tường ngoài **trước**. Tốt cho dung sai kích thước, xấu cho bề mặt. Figure nên đảo.

## 4. TOOL — đồ dùng, ưu tiên chắc + nhanh

Đánh đổi: bỏ hoàn thiện bề mặt, lấy độ bền và thời gian.

| Setting | Giá trị | Vì sao |
|---|---|---|
| `layer_height` | 0.20 | |
| `wall_loops` | 4 | 🔵 độ bền đến từ **tường**, không phải infill — thêm 1 wall rẻ hơn nhiều so với tăng 10% infill |
| `wall_sequence` | `inner-outer-inner wall` | liên kết tường tốt nhất |
| `sparse_infill_density` | 25% | trên 30% gần như không thêm độ bền cho vật thành dày |
| `sparse_infill_pattern` | `gyroid` hoặc `cubic` | đẳng hướng, chịu lực mọi chiều |
| `top_shell_layers` / `bottom` | 5 / 4 | |
| `outer_wall_speed` / `inner_wall_speed` | 120 / 160 | 160 sát trần flow ở 0.20 |
| `ironing_type` | `no ironing` | tốn thời gian, không tăng độ bền |
| `ensure_vertical_shell_thickness` | `ensure_all` | |
| `enable_support` | **0** | bật theo từng model, không đóng cứng |

## 5. TEST — bản thử, chỉ nhanh

Đánh đổi: bỏ mọi thứ không phải cái đang cần kiểm tra.

| Setting | Giá trị | Vì sao |
|---|---|---|
| `layer_height` | 0.28 *(max của máy)* | ít lớp nhất |
| `wall_loops` | 2 | 1 wall thì thành quá yếu, hay bung khi cầm |
| `sparse_infill_density` | 5% | |
| `sparse_infill_pattern` | `lightning` | 🔵 chỉ đỡ phần mặt trên — nhanh hơn hẳn grid |
| `top_shell_layers` / `bottom` | 2 / 2 | |
| `ironing_type` | `no ironing` | |
| `brim_type` | `no_brim` *(trừ model chân nhỏ)* | |
| tốc độ | ~119 mm/s, sát trần flow ở 0.28 | |
| `reduce_crossing_wall` | 0 | tính toán tránh tường tốn thời gian slice |

📝 Khi test một thứ cụ thể — dung sai lỗ, khớp nối, overhang — chỉ nâng chất
lượng đúng vùng đó bằng **height range modifier** hoặc **object setting
override**, đừng đổi cả profile.

## 6. Ánh xạ chuyển đổi

| Preset hiện có | Đề xuất |
|---|---|
| `0.12 mm - High Quality Novi` | → `FIG 0.12 @KX`, sửa `wall_sequence` |
| `0.20mm - High Quality Novi` | 🔴 trùng cái trên — xoá, hoặc giữ thành `FIG 0.20 @KX` nếu thật sự hay dùng |
| `0.20mm - Standard Novi` | → `TOOL 0.20 @KX`, bỏ `enable_support`, wall 3 → 4 |
| `0.20mm PLA Lite - Copy` | 🔴 xoá — bị `fix first layer` thay thế |
| `0.20mm PLA Lite - fix first layer` | giữ nếu bản sửa first layer thật sự hiệu quả, đổi tên cho rõ |
| `0.20mm Standard - Copy` | 🔴 xoá — gần như y hệt vendor default |
| `0.24mm Fast speed` | → `TEST 0.28 @KX`, hạ top/bottom shell, đổi sang `lightning` |

Từ 7 preset còn **3–4**.

---

## 7. In 4 màu

Nhóm prime tower / flush nằm ở tầng process, nên chiến lược purge đổi theo mục đích:

| | FIG | TOOL | TEST |
|---|---|---|---|
| `flush_into_objects` | ❌ 0 | ✅ 1 | ✅ 1 |
| `flush_into_infill` | ❌ 0 | ✅ 1 | ✅ 1 |
| `flush_into_support` | 1 | 1 | 1 |
| `enable_prime_tower` | 1 | 1 | chỉ khi cần |
| flush tối↔sáng | cao, 450–650 mm³ | vừa, 300–400 | thấp, chấp nhận lem |

Với FIG, nhựa xả vào thân vật thể có thể lộ ra bề mặt hoặc lẫn màu ở lớp kế
tiếp. Với TOOL và TEST thì nằm khuất bên trong — thu hồi được phần lớn nhựa
purge, giảm rác đáng kể.

**Mặc định hiện tại** *(kế thừa từ `0.20mm Standard @Kobra X` của hãng)*:
`enable_prime_tower` 1, `prime_tower_width` 30 mm, `flush_into_infill` 0,
`flush_into_objects` 0, `flush_into_support` 1.

🟡 Hai cái bằng 0 nghĩa là **không thu hồi nhựa purge**. Chỉ support được tận
dụng, mà support không phải lúc nào cũng có.

🔴 **Chưa từng slice 4 màu.** Mọi pairing Kobra X trong `.conf` vẫn là
single-filament: `flush_volumes_matrix` là `"0.000000"` (1×1, cần 4×4),
`flush_volumes_vector` chỉ 2 phần tử, `filament_colors` là `"#FFFFFF"`.

So sánh: entry Bambu A1 trong cùng file có matrix 4×4 thật, giá trị 108–608.
Slicer chỉ tạo ma trận khi thực sự slice nhiều màu — A3 trong `TODO.md`.
