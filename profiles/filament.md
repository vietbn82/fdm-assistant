# Filament preset — tầng filament

**Viet cập nhật file này mỗi lần đổi cuộn.** Claude không có cách nào tự biết.
Sai ở đây thì mọi tư vấn nhiệt độ, flow, flush đều sai theo.

Tầng nào sở hữu gì: `docs/preset-model.md` mục 3.

---

## Cuộn đang nạp

| Slot | Sản phẩm | Màu | Hex | Nạp slot | Mở túi | Preset đang gán |
|---|---|---|---|---|---|---|
| 1 | Bambu Lab PLA Lite | Beige *(16700)* | `#F7E6DE` | 2026-08-29 | 2026-08-29 | `PLA Bambulab Lite@KX 0.4` |
| 2 | Generic PLA | White | `#FFFFFF` | 2026-08-23 | 2026-08-23 | `PLA Generic@KX 0.4` |
| 3 | Bambu Lab PLA Lite | Black | `#000000` | 2026-08-13 | 2026-08-13 | `PLA Bambulab Lite@KX 0.4` |
| 4 | Generic PLA | Matcha | `#BBFB98` | 2026-08-26 | 2026-08-26 | `PLA Generic@KX 0.4` |

🟢 **Bốn slot đều đúng, xác nhận 29/08 16:41.** Màu đọc từ `filament_colors` trong
`.conf` sau khi đóng slicer; preset đọc từ cùng bản ghi đó. Slot 3 Viet xác nhận
là cuộn BBL Black.

```
filament_colors = #F7E6DE,#FFFFFF,#000000,#BBFB98
filament    = PLA Bambulab Lite@KX 0.4    filament_01 = PLA Generic@KX 0.4
filament_02 = PLA Bambulab Lite@KX 0.4    filament_03 = PLA Generic@KX 0.4
```

🔵 **Màu đặt trên màn hình cảm ứng của máy in không tới được slicer.** Đã kiểm:
sau khi đặt trên máy, `.conf` vẫn nguyên màu cũ. Hai kho cấu hình riêng — màn
hình máy lo trạm nạp nhựa, slicer đọc kho của nó.

🟢 **Đã sửa xong lỗi preset stock ở slot 2 và 4 (29/08).** Trước đó hai slot đó
gán `Anycubic PLA @Anycubic Kobra X 0.4 nozzle`, hỏng ba thứ cùng lúc:

| | stock `Anycubic PLA @…` | preset đã chỉnh |
|---|---|---|
| `nozzle_temperature_HS` | 🔴 220 | 205 |
| `filament_flow_ratio` | 🔴 0.96 | 1.0 |
| `filament_retraction_length` | 🔴 0.8 — đè lên machine | `nil` → theo machine 1.2 |

🔴 Dòng thứ ba đáng nhớ nhất: `filament_retraction_length` ở tầng filament
**thắng** `retraction_length` ở tầng machine. Preset nhựa nào đặt số cứng ở đó
sẽ vô hiệu hoá mọi tinh chỉnh retraction ở tầng máy. Hai preset đang dùng đều để
`nil` — giữ nguyên như vậy.

🔴 **Flush đắt hơn trước.** Slot 1 beige gần trắng, slot 3 đen — cặp tối↔sáng cực
đại. Rời khỏi đen tốn 635–785 mm³ mỗi lần; xem ma trận trong `profiles/process.md`.

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

🟢 Đủ bốn hex, `flush_volumes_matrix` 4×4 đã tính xong — bảng trong
`profiles/process.md`.

## Độ ẩm

🟡 **Không có máy sấy nhựa.** Tính đến 2026-08-29: slot 1 mở hôm nay, slot 4 mở
26/08, slot 2 mở 23/08, slot 3 mở 13/08 — đều dưới một tháng nên hiện chưa phải
vấn đề. PLA đóng gói kín kèm gói hút ẩm thường khô sẵn.

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

### `PLA Bambulab Lite@KX 0.4` — slot 1, 3

Gộp từ hai preset cũ (`BBL PLA Lite` và `BBL PLA Lite @Anycubic Kobra X 0.4
nozzle`) — mỗi cái giữ một nửa thông tin, không cái nào đủ. Đổi tên từ
`PLA BBL Lite@KX 0.4` sang tên hiện tại ngày 29/08.

| Key | Giá trị |
|---|---|
| `filament_max_volumetric_speed` | 13 *(kế thừa, chưa đo)* |
| `filament_flow_ratio` | **1.0** *(P14, áp lại bằng P15 ngày 29/08)* |
| `filament_density` / `filament_vendor` | 1.3 / BambuLab |
| `nozzle_temperature_HS` / `_initial_layer_HS` | **205 / 210** |
| `nozzle_temperature_range_high` | 215 |
| `pressure_advance` / `adaptive_pressure_advance` | 0.036 *(kế thừa)* / tắt |
| **`textured_plate_temp` / `_initial_layer`** | **60 / 60** *(kế thừa)* ← bàn đang dùng |
| `hot_plate_temp` / `_initial_layer` | 50 / 60 *(không dùng)* |
| `fan_min_speed_HS` / `fan_max_speed_HS` | 60 / 90 *(kế thừa)* |
| `overhang_fan_threshold` | 25% |
| `close_fan_the_first_x_layers` | 2 |
| `filament_retraction_length` / `_wipe_distance` | `nil` → theo machine |
| `slow_down_layer_time_HS` / `slow_down_min_speed` | 5 / 10 |

🔴 **Chỉ `textured_plate_temp*` có tác dụng.** `curr_bed_type = 4` cho máy đang
chọn, tức bàn Textured PEI. Cặp `hot_plate_temp*` chỉ áp dụng cho mặt bàn nhẵn —
sửa nhầm cặp đó thì không có gì xảy ra cả.

🔵 Cả hai khoá textured đã bị revert về 45/50 ngày 24/08, gây bong bàn. Khôi phục
60/60 ngày 25/08 — trùng đúng giá trị hãng.

🔵 Đổi tên từ `PLA BBL Lite@KX 0.4` sang tên hiện tại ngày 29/08. Các mục cũ
trong `CHANGELOG.md` vẫn giữ tên cũ — đó là tên preset lúc thao tác diễn ra.

### `PLA Generic@KX 0.4` — slot 2, 4

| Key | Giá trị |
|---|---|
| `filament_flow_ratio` | **1.0** *(P14, áp lại bằng P15)* |
| `filament_max_volumetric_speed` | 13 — mặc định hãng |
| `nozzle_temperature_HS` | 205 |
| `nozzle_temperature_initial_layer_HS` | **210** *(P18, 29/08)* |
| `nozzle_temperature_range_high` | 220 |
| **`textured_plate_temp` / `_initial_layer`** | **60 / 60** ← bàn đang dùng |
| `overhang_fan_threshold` | 25% |
| `filament_retraction_length` / `_wipe_distance` | `nil` → theo machine |

🔵 Trần flow để 13 chứ không phải 15. Con số 15 trước đó chép sang từ BBL, chưa
đo. Nhựa Generic không rõ nguồn thì không đoán cao.

🔵 Nhiệt bàn cũng bị revert về 45/55, khôi phục 60/60 ngày 25/08 cùng lúc với
BBL. Cùng một lỗi, cùng một cách sửa.

🔵 P18 (29/08): trước đó preset chỉ đè `nozzle_temperature_HS`, quên bản
`_initial_layer_HS`, nên lớp đầu in ở **220** trong khi các lớp sau 205. Giờ 210,
khớp với preset BBL.

Cả hai kế thừa `Anycubic PLA @Anycubic Kobra X 0.4 nozzle`.

🔵 Trần flow **13** đã đóng lại ngày 26/08: nó chỉ hạ *tốc độ* khi chạm trần,
không làm tường mỏng đi. Thủ phạm thiếu nhựa là `filament_flow_ratio`.
