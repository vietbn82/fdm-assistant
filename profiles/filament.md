# Filament preset — tầng filament

**Viet cập nhật file này mỗi lần đổi cuộn.** Claude không có cách nào tự biết.
Sai ở đây thì mọi tư vấn nhiệt độ, flow, flush đều sai theo.

Tầng nào sở hữu gì: `docs/preset-model.md` mục 3.

---

## Cuộn đang nạp

| Slot | Sản phẩm | Màu | Hex | Nạp slot | Mở túi | Preset đang gán |
|---|---|---|---|---|---|---|
| 1 | Bambu Lab PLA Lite | Red | `#FF0000` | 2026-08-13 | 2026-08-13 | `PLA BBL Lite@KX 0.4` |
| 2 | Generic PLA | White | `#FFFFFF` | 2026-08-23 | 2026-08-23 | 🟡 `Anycubic PLA @Kobra X` *(stock)* |
| 3 | Bambu Lab PLA Lite | Black | `#000000` | 2026-08-13 | 2026-08-13 | `PLA BBL Lite@KX 0.4` |
| 4 | Bambu Lab PLA Lite | Cyan | `#0080C0` | 2026-08-13 | 2026-08-13 | `PLA BBL Lite@KX 0.4` |

Hex lấy từ `filament_colors` trong `.conf` — tức màu bạn đã chọn trong UI, không
phải bảng của hãng. Đó mới là giá trị slicer thật sự dùng để tính flush.

🟡 **Kiểm tra slot 2 đang gán preset nào.** Lần soát trước nó dùng preset stock
chứ không phải `PLA Generic@KX 0.4`. Gán slot nằm trong state của project, không
đọc được từ `.conf` — phải nhìn trong UI: tab Filament, slot 2.

**Mỗi slot theo dõi riêng.** Thay cuộn ở slot 2 thì chỉ sửa dòng 2 — ba slot kia
giữ nguyên ngày của chúng.

Hai cột ngày khác nhau, đừng gộp:

| Cột | Là gì | Dùng để |
|---|---|---|
| **Nạp slot** | ngày cuộn này được lắp vào slot | biết cuộn nào đang ở đâu |
| **Mở túi** | ngày bóc túi hút chân không | 🟡 **tính tuổi ẩm** |

🟡 Với độ ẩm, chỉ cột **Mở túi** có ý nghĩa. Cuộn nằm yên trong slot ba tháng
vẫn hút ẩm y như cuộn để trên bàn — tháo ra lắp lại không reset gì cả. Cuộn đã
mở lâu rồi mới lắp vào máy thì hai ngày này lệch xa nhau, và cột bên phải mới
là cột đáng tin.

📝 Mã hex còn thiếu — cần để tính `flush_volumes_matrix` 4×4. Cặp tối↔sáng
(Black ↔ White) tốn nhiều nhựa purge hơn hẳn cặp cùng tông.

## Độ ẩm

🟡 **Không có máy sấy nhựa.** Slot 2 mở hôm nay, ba slot còn lại mở 2026-08-13
— đều dưới một tháng nên hiện chưa phải vấn đề. PLA đóng gói kín kèm gói hút ẩm
thường khô sẵn.

Cần biết vì ẩm gây ra triệu chứng **nhìn hệt lỗi setting**: stringing, bề mặt
rỗ, tiếng lách tách khi đùn, lớp bám kém. Chỉnh preset để chữa mấy thứ đó là
chữa sai bệnh.

Mốc tham khảo tính từ cột **Mở túi**, môi trường phòng bình thường:

| Tuổi | |
|---|---|
| < 1 tháng | 🟢 yên tâm |
| 1–3 tháng | 🔵 để ý, thấy stringing thì nghi ẩm trước khi nghi setting |
| > 3 tháng | 🟡 nghi ẩm đầu tiên. Nếu cất trong túi kín kèm hút ẩm thì kéo dài hơn nhiều |

Không có máy sấy thì:

- Giữ cuộn trong túi kín kèm gói hút ẩm khi không in — rẻ nhất và hiệu quả nhất
- PLA hút ẩm chậm hơn PETG/Nylon nhiều, dùng vài tuần trong phòng khô thường ổn
- Nghi ẩm mà không có máy sấy: lò nướng 45–50 °C trong 4–6 giờ ⚠️ nhiệt độ phải
  dưới điểm mềm (~54 °C), lò có sai số lớn thì đừng liều
- 📝 Nếu chuyển sang PETG hoặc TPU thì máy sấy gần như bắt buộc

## Preset

### `PLA BBL Lite@KX 0.4` — slot 1, 3, 4

Gộp từ hai preset cũ (`BBL PLA Lite` và `BBL PLA Lite @Anycubic Kobra X 0.4
nozzle`) — mỗi cái giữ một nửa thông tin, không cái nào đủ.

| Key | Giá trị |
|---|---|
| `filament_max_volumetric_speed` | 13 *(hãng)* ⏳ chưa đo |
| `filament_flow_ratio` | 0.98 |
| `filament_density` / `filament_vendor` | 1.3 / BambuLab |
| `nozzle_temperature_HS` / `_initial_layer_HS` | 212 / 212 |
| `nozzle_temperature_range_high` | 215 |
| `pressure_advance` / `adaptive_pressure_advance` | 0.036 / tắt |
| **`textured_plate_temp` / `_initial_layer`** | **60 / 60** ← bàn đang dùng |
| `hot_plate_temp` / `_initial_layer` | 50 / 60 *(không dùng)* |
| `fan_min_speed_HS` / `fan_max_speed_HS` | 60 / 90 |
| `overhang_fan_threshold` | 25% |
| `close_fan_the_first_x_layers` | 2 |
| `filament_retraction_length` / `_wipe_distance` | `nil` → theo machine |
| `slow_down_layer_time_HS` / `slow_down_min_speed` | 5 / 10 |

🔴 **Chỉ `textured_plate_temp*` có tác dụng.** `curr_bed_type = 4` cho máy đang
chọn, tức bàn Textured PEI. Cặp `hot_plate_temp*` chỉ áp dụng cho mặt bàn nhẵn —
sửa nhầm cặp đó thì không có gì xảy ra cả.

🔵 Cả hai khoá textured đã bị revert về 45/50 ngày 24/08, gây bong bàn. Khôi phục
60/60 ngày 25/08 — trùng đúng giá trị hãng.

### `PLA Generic@KX 0.4` — slot 2

| Key | Giá trị |
|---|---|
| `filament_max_volumetric_speed` | 13 — mặc định hãng |
| `nozzle_temperature_HS` | 205 |
| `nozzle_temperature_range_high` | 220 |
| **`textured_plate_temp` / `_initial_layer`** | **60 / 60** ← bàn đang dùng |
| `overhang_fan_threshold` | 25% |
| `filament_retraction_length` / `_wipe_distance` | `nil` → theo machine |

🔵 Trần flow để 13 chứ không phải 15. Con số 15 trước đó chép sang từ BBL, chưa
đo. Nhựa Generic không rõ nguồn thì không đoán cao.

🔵 Nhiệt bàn cũng bị revert về 45/55, khôi phục 60/60 ngày 25/08 cùng lúc với
BBL. Cùng một lỗi, cùng một cách sửa.

Cả hai kế thừa `Anycubic PLA @Anycubic Kobra X 0.4 nozzle`.

⏳ A1 trong `TODO.md`: in thử để xác nhận trần flow **13** có đủ không. 13 là
mặc định hãng; 15 là trần Bambu công bố, cả hai đều chưa đo trên hotend này.
