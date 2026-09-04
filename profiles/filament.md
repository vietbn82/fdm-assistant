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

🔴 **Từ 2026-09-03 bảng này không kiểm chứng lại được nữa.** Slicer 2.0.0.2 bỏ
`filament_colors` và bảng gán slot→preset khỏi `.conf` — mục `presets` giờ chỉ
còn `filaments` (một mảng cờ khó đọc) và `machine`. Lần xác nhận cuối bằng máy
là **29/08 16:41**, trên bản 1.4.x. Từ nay đây là dữ liệu **do Viet khai**, không
có nguồn thứ hai.

🔵 **Màu đặt trên màn hình cảm ứng của máy in không tới được slicer.** Đã kiểm:
sau khi đặt trên máy, `.conf` vẫn nguyên màu cũ. Hai kho cấu hình riêng — màn
hình máy lo trạm nạp nhựa, slicer đọc kho của nó.

🔴 **Flush đắt.** Slot 1 beige gần trắng, slot 3 đen — cặp tối↔sáng cực đại. Rời
khỏi đen tốn 635–785 mm³ mỗi lần; ma trận trong `profiles/process.md` (đọc từ
gcode 29/08, chưa kiểm lại sau khi lên 2.0.0.2).

**Mỗi slot theo dõi riêng.** Thay cuộn ở slot 2 thì chỉ sửa dòng 2 — ba slot kia
giữ nguyên ngày của chúng.

Hai cột ngày khác nhau, đừng gộp:

| Cột | Là gì | Dùng để |
|---|---|---|
| **Nạp slot** | ngày cuộn này được lắp vào slot | biết cuộn nào đang ở đâu |
| **Mở túi** | ngày bóc túi hút chân không | 🟡 **tính tuổi ẩm** |

🟡 Với độ ẩm, chỉ cột **Mở túi** có ý nghĩa. Cuộn nằm yên trong slot ba tháng
vẫn hút ẩm y như cuộn để trên bàn — tháo ra lắp lại không reset gì cả.

## Độ ẩm

🟡 **Không có máy sấy nhựa.** Tính đến 2026-09-03: slot 3 mở 13/08 (3 tuần),
slot 2 mở 23/08, slot 4 mở 26/08, slot 1 mở 29/08 — tất cả vẫn dưới một tháng.

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

🟢 **Đọc từ đĩa 2026-09-03 21:5x, sau khi Viet dựng lại preset trên slicer
2.0.0.2.** Cả hai preset đều mỏng đi rõ rệt — nhiều khoá cũ đã bỏ, giờ kế thừa
`Anycubic PLA @Anycubic Kobra X 0.4 nozzle`.

### `PLA Bambulab Lite@KX 0.4` — slot 1, 3

Override thật trên đĩa (7 khoá):

| Key | Cha | Đặt | Vì sao |
|---|---|---|---|
| `nozzle_temperature_HS` | 220 | **203** | |
| `nozzle_temperature_initial_layer_HS` | 220 | **210** | lớp đầu nóng hơn để bám |
| `nozzle_temperature_range_high` | 230 | **220** | trần khai báo cho PLA Lite |
| `textured_plate_temp` / `_initial_layer` | 60 / 60 | **50 / 55** | ← bàn đang dùng |
| `hot_plate_temp` | 60 | **50** | ⚪ bàn nhẵn, không dùng |
| `close_fan_the_first_x_layers` | 1 | **2** | |
| `filament_vendor` | Generic | **BambuLab** | nhãn |
| `filament_retraction_length` / `_wipe_distance` | — | **`nil`** | 🟢 để machine quyết |

Kế thừa (không còn đè):

| Key | Giá trị hãng |
|---|---|
| `filament_flow_ratio` | **0.96** 🔴 xem dưới |
| `filament_max_volumetric_speed` | 13 *(chưa đo)* |
| `filament_density` | 1.24 *(trước pin 1.3)* |
| `nozzle_temperature` / `_initial_layer` | 205 / 215 |
| `pressure_advance` | 0.036 |
| `overhang_fan_threshold` | 50% *(trước pin 25%)* |
| `slow_down_min_speed` | 20 *(trước pin 10)* |

### `PLA Generic@KX 0.4` — slot 2, 4

Override thật trên đĩa (5 khoá):

| Key | Cha | Đặt |
|---|---|---|
| `nozzle_temperature_HS` | 220 | **200** |
| `nozzle_temperature_initial_layer_HS` | 220 | **210** |
| `nozzle_temperature_range_high` | 230 | **220** |
| `textured_plate_temp` / `_initial_layer` | 60 / 60 | **50 / 55** |
| `filament_vendor` | Generic | Generic *(nhãn)* |
| `filament_retraction_length` / `_wipe_distance` | — | **`nil`** |

Kế thừa: giống bảng của BBL — `filament_flow_ratio = 0.96`, flow cap 13,
`pressure_advance = 0.036`, `overhang_fan_threshold = 50%`,
`close_fan_the_first_x_layers = 1`.

🔵 Hai preset giờ **chỉ khác nhau bốn thứ**: nhiệt HS (203 vs 200),
`close_fan_the_first_x_layers` (2 vs 1), `hot_plate_temp` (khoá chết), và nhãn
vendor.

---

## Ba điểm đáng theo dõi sau đợt dựng lại

🔴 **`filament_flow_ratio` trở về 0.96 (kế thừa).** Bộ cũ pin **1.0** trên cả hai
preset — P14 rồi áp lại bằng P15 (29/08), chính là bản sửa đã chữa được **thiếu
nhựa / tường mỏng**. Bỏ pin nghĩa là đùn ít hơn 4%. Nếu thấy tường mỏng, mặt trên
hở khe, lớp không dính nhau thì đây là nghi phạm số một — pin lại 1.0.

🟡 **Nhiệt in hạ thêm.** 205 → 203 (BBL) và 205 → **200** (Generic). Bộ cũ từng
thử 200 (P28, 30/08) và trả lại 205 vì không giúp tơ mà bị nghi hại mặt trên.
Generic giờ quay lại đúng mức đó.

🔴 **Chỉ `textured_plate_temp*` có tác dụng.** `curr_bed_type = 4` — bàn Textured
PEI. Cặp `hot_plate_temp*` chỉ áp dụng cho mặt bàn nhẵn; sửa nhầm cặp đó thì
không có gì xảy ra. Mức 50/55 giữ nguyên như bộ cũ; từng bong bàn khi rơi 15° về
45/50 hồi 24/08, nên đừng hạ tiếp.

🟡 **PA vẫn để 0.036 (kế thừa), chưa kết luận.** Đo được 0.32 ngày 30/08 bằng PA
Pattern trên cả hai filament — cùng số cho hai loại nhựa củng cố giả thuyết nó
phản ánh buồng nóng chảy dùng chung 79 mm³. Nhưng ngay sau đó nozzle bị nghẹt
(đã cold-pull) nên phép đo không tin được. Cần đo lại khi chắc nozzle sạch.
