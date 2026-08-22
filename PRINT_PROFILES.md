# Ba mục đích in — đề xuất, chưa áp dụng

> Trạng thái hiện tại: **preset chưa chia theo mục đích**, đang chia theo layer
> height cộng vài lần thử nghiệm chưa dọn. File này là đề xuất cấu trúc lại.
> Chưa tạo/xoá preset nào — theo `WORKING_RULES.md` mục 3, việc đó phải hỏi.

## Hiện trạng

| preset | lớp | wall | infill | top | ironing | outer/inner | support |
|---|---|---|---|---|---|---|---|
| `0.12 mm - High Quality Novi @AC KX` | 0.12 | 2 | 12% gyroid | 5 | top | 60/150 | 0 |
| `0.20mm - High Quality Novi @AC KX` | 0.20 | 2 | 12% gyroid | 5 | top | 60/150 | 0 |
| `0.20mm - Standard Novi @AC KX` | 0.20 | 3 | 20% 3dhoneycomb | 6 | không | 60/100 | **1** |
| `0.20mm PLA Lite @AC KX - Copy` | 0.20 | 2 | 15% honeycomb | 5 | top | 50/65 | 0 |
| `0.20mm PLA Lite @AC KX - fix first layer` | 0.20 | 2 | 15% honeycomb | 5 | top | 50/65 | 0 |
| `0.20mm Standard @AC KX - Copy` | 0.20 | 2 | 15% honeycomb | 5 | top | 200/300 | 0 |
| `0.24mm Fast speed @AC KX` | 0.24 | 2 | 10% grid | 4 | không | 200/230 | 0 |

Vấn đề:

- 🔴 Hai cái `High Quality Novi` **giống hệt nhau** trừ `layer_height`. Là một
  profile bị nhân đôi, không phải hai ý đồ khác nhau.
- 🔴 Ba cái `PLA Lite - Copy` / `fix first layer` / `Standard - Copy` chỉ khác
  `seam_slope_type` và tốc độ wall. Ba lần thử cùng một thứ, không lần nào bị dọn.
- 🟡 `enable_support = 1` bị đóng cứng trong `0.20 Standard Novi`. Support là
  thuộc tính **từng model**, bật trong profile nghĩa là mọi print đều sinh support.
- 🟡 Không có profile "test" thật. `0.24 Fast speed` vẫn giữ 4 top shell và
  10% infill — vẫn tốn thời gian cho bề mặt mà bản test không cần.

## Trần flow quyết định tốc độ, không phải layer height

Với `filament_max_volumetric_speed` = 15 mm³/s (BBL PLA Lite hiện tại):

| layer | line width | tốc độ tối đa thực tế |
|---|---|---|
| 0.12 | 0.42 | ~297 mm/s (flow không phải giới hạn, chất lượng mới là) |
| 0.16 | 0.45 | ~208 mm/s |
| 0.20 | 0.45 | ~166 mm/s |
| 0.24 | 0.45 | ~138 mm/s |
| 0.28 | 0.45 | ~119 mm/s |

🔵 **Trên trần flow, layer dày hơn không cho tốc độ cao hơn** — throughput đứng
yên ở 15 mm³/s. Cái lợi duy nhất của layer dày là **ít lớp hơn**: giảm thời gian
Z, giảm accel/decel, giảm số lần đổi hướng. Vẫn đáng, nhưng không tuyến tính như
người ta hay tưởng. Đặt `sparse_infill_speed = 300` ở layer 0.28 là con số hư cấu.

---

## Đề xuất: 3 profile theo mục đích

### FIG — figure, ưu tiên độ sắc nét

Đánh đổi: chậm, đổi lấy cạnh sắc và bề mặt liền.

| Setting | Giá trị | Vì sao |
|---|---|---|
| `layer_height` | 0.12 (0.16 cho model lớn) | chi tiết dọc |
| `wall_loops` | 2 | tường dày không giúp gì cho figure |
| `wall_sequence` | `inner wall/outer wall` | outer in **sau cùng**, đắp lên nền đặc — bề mặt đẹp nhất |
| `outer_wall_speed` | 50 | chậm ở tường ngoài là thứ quyết định độ sắc |
| `outer_wall_acceleration` | 2000–3000 | accel cao làm tròn góc |
| `seam_slope_type` | `all` (scarf joint) | giấu đường seam |
| `seam_position` | `aligned` hoặc `rear` | dồn seam về một phía |
| `sparse_infill_density` | 10–12% gyroid | figure không chịu lực |
| `top_shell_layers` | 5 | |
| `ironing_type` | `top`, speed 20, spacing 0.10–0.12 | mặt trên phẳng |
| `slowdown_for_curled_perimeters` | 1 | |
| `detect_thin_wall` | 1 | giữ chi tiết mảnh |

🟡 Cả hai preset `High Quality Novi` hiện dùng `outer wall/inner wall` — in
tường ngoài **trước**. Cái đó tốt cho độ chính xác kích thước, xấu cho bề mặt.
Với figure nên đảo lại.

### TOOL — đồ dùng, ưu tiên chắc + nhanh

Đánh đổi: bỏ hoàn thiện bề mặt, đổi lấy độ bền và thời gian.

| Setting | Giá trị | Vì sao |
|---|---|---|
| `layer_height` | 0.20 | |
| `wall_loops` | 4 | 🔵 độ bền đến từ **tường**, không phải infill — thêm 1 wall rẻ hơn nhiều so với tăng 10% infill |
| `wall_sequence` | `inner-outer-inner wall` | liên kết tường tốt nhất |
| `sparse_infill_density` | 25% | đủ; trên 30% gần như không thêm độ bền cho vật thành dày |
| `sparse_infill_pattern` | `gyroid` hoặc `cubic` | đẳng hướng, chịu lực mọi chiều |
| `top_shell_layers` / `bottom` | 5 / 4 | |
| `ironing_type` | `no ironing` | tốn thời gian, không tăng độ bền |
| `outer_wall_speed` | 120 | |
| `inner_wall_speed` | 160 (sát trần flow ở 0.20) | |
| `ensure_vertical_shell_thickness` | `ensure_all` | |
| `enable_support` | **0** | bật theo từng model, không đóng cứng ở đây |

### TEST — bản thử, chỉ nhanh

Đánh đổi: bỏ mọi thứ không phải cái đang cần kiểm tra.

| Setting | Giá trị | Vì sao |
|---|---|---|
| `layer_height` | 0.28 (max của máy) | ít lớp nhất |
| `wall_loops` | 2 | 1 wall thì thành quá yếu, hay bung khi cầm |
| `sparse_infill_density` | 5% | |
| `sparse_infill_pattern` | `lightning` | 🔵 chỉ đỡ phần mặt trên, nhanh hơn hẳn grid |
| `top_shell_layers` / `bottom` | 2 / 2 | |
| `ironing_type` | `no ironing` | |
| `brim_type` | `no_brim` (trừ khi model chân nhỏ) | |
| tốc độ | sát trần flow: ~119 mm/s ở 0.28 | |
| `reduce_crossing_wall` | 0 | tính toán tránh tường tốn thời gian slice |

📝 Nguyên tắc: khi test một thứ cụ thể (dung sai lỗ, khớp nối, overhang), chỉ
nâng chất lượng đúng vùng đó — dùng **height range modifier** hoặc
**object setting override** trong slicer, không đổi cả profile.

---

## Ánh xạ chuyển đổi

| Preset hiện có | Đề xuất |
|---|---|
| `0.12 mm - High Quality Novi @AC KX` | giữ, đổi tên `FIG 0.12 @KX`, sửa `wall_sequence` |
| `0.20mm - High Quality Novi @AC KX` | 🔴 trùng cái trên — xoá, hoặc giữ thành `FIG 0.20 @KX` nếu thật sự hay dùng |
| `0.20mm - Standard Novi @AC KX` | giữ làm gốc `TOOL 0.20 @KX`, bỏ `enable_support`, wall 3 → 4 |
| `0.20mm PLA Lite @AC KX - Copy` | 🔴 xoá — bị `fix first layer` thay thế |
| `0.20mm PLA Lite @AC KX - fix first layer` | giữ nếu bản sửa first layer thật sự hiệu quả, đổi tên cho rõ |
| `0.20mm Standard @AC KX - Copy` | 🔴 xoá — gần như y hệt vendor default |
| `0.24mm Fast speed @AC KX` | gốc cho `TEST 0.28 @KX`, hạ top/bottom shell, đổi sang `lightning` |

Từ 7 preset còn **3–4**.

## In 4 màu theo mục đích

Máy có bộ 4 màu tích hợp. Chiến lược flush khác nhau hẳn giữa ba mục đích:

| | FIG | TOOL | TEST |
|---|---|---|---|
| `flush_into_objects` | ❌ 0 | ✅ 1 | ✅ 1 |
| `flush_into_infill` | ❌ 0 | ✅ 1 | ✅ 1 |
| `flush_into_support` | 1 | 1 | 1 |
| `enable_prime_tower` | 1 | 1 | chỉ khi cần |
| flush tối↔sáng | cao (450–650 mm³) | trung bình (300–400) | thấp, chấp nhận lem |

Lý do: với FIG, nhựa xả vào thân vật thể có thể lộ ra bề mặt hoặc lẫn màu ở lớp
kế tiếp. Với TOOL và TEST thì nằm khuất bên trong — thu hồi được phần lớn nhựa
purge, giảm rác đáng kể.

🟡 Hiện `.conf` vẫn cấu hình single-filament cho Kobra X: `flush_volumes_matrix`
là `"0.000000"` (1×1, cần 4×4), `filament_colors` là `"#FFFFFF"` chứ không phải
Red/White/Black/Cyan. Phải slice thử một model 4 màu một lần để slicer sinh ra
matrix, rồi mới chỉnh số được.
