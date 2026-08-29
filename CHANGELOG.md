# Nhật ký

Mọi việc đã xong, mới nhất lên trên. `TODO.md` chỉ giữ việc còn treo,
`PENDING_APPLY.md` chỉ giữ thao tác chờ duyệt.

Diff từng dòng preset nằm ở `git log -- presets/`.

---

## 2026-08-29

### P19 P20 P21 🟢 áp

Backup `user_backup-tune-set-20260829-182807`. Áp cho **cả hai** preset FIGURE.

| Key | Cũ | Mới | Nhắm vào |
|---|---|---|---|
| `reduce_crossing_wall` | 0 *(kế thừa)* | **1** | tơ — travel không còn cắt ngang qua vật |
| `max_travel_detour_distance` | 0 *(kế thừa)* | **40** | trần cho đường vòng, tránh travel dài vô lý |
| `ironing_flow` | 8% | **10%** | mặt trên xước — trả về giá trị cha |
| `top_surface_speed` | 150 *(kế thừa)* | **80** | mặt trên xấu |

`--audit`: 0 lỗi. Đã đọc lại file xác nhận cả 8 lần ghi.

❌ **P6 và P22 không nằm trong lượt này** — Viet chỉ duyệt P19, P20, P21.

### P22 đóng — `skirt_loops = 0` và `prime_tower_width = 10` là cố ý

Viet xác nhận đã tự đặt hai giá trị đó trên `Novi 0.16 - FIGURE @AC KX`. Không
phải regression, không phải slicer xoá mất. Gỡ P22 khỏi `PENDING_APPLY.md`.

🔵 Ghi vào `profiles/process.md` để lần soát sau không báo lại: bảng "áp cho cả
bốn profile" giờ có ngoại lệ ở dòng `skirt_loops`.

🟡 Bài học cho tôi: thấy một khoá biến mất khỏi preset thì **hỏi trước khi gọi là
regression**. Lần 27/08 là revert thật, lần này là Viet cố ý — nhìn diff không
phân biệt được. Đúng tinh thần mục 6 `docs/working-rules.md`: slicer thắng.


### Bản in 29/08 17:00 — `Parametric_Model_Maker_1`, kết quả xấu

Nguồn: `Temp\ACGcode3mf\9527\0829-1700-Plate 1(01)_PLA_0.16_41m24s.gcode.3mf`,
đọc `Metadata/project_settings.config` và `slice_info.config`.

| | |
|---|---|
| Mẫu | `Parametric_Model_Maker_1`, Plate 1 |
| Thời gian / khối lượng | 41m24s, 6,42 g |
| process | `Novi 0.16 - FIGURE @AC KX` *(có sửa chưa lưu — xem dưới)* |
| machine | `Anycubic Kobra X 0.4 nozzle - high quality` |
| filament | `PLA Generic@KX 0.4` × 2 — matcha `#BAFB97` 3,69 g + white `#FFFFFF` 2,73 g |

🔴 **Đây là bản in 2 màu**, không phải 1 màu. Dùng slot 2 và slot 4, **không dùng
BBL**.

🟢 **P15, P16, P18 đều có hiệu lực trong bản in này** — đọc từ chính file gcode:

```
retraction_length 1.2   retraction_speed 45   retract_before_wipe 100%
z_hop_types Normal Lift  seam_slope_type none  filament_flow_ratio 1,1
nozzle_temperature 205,205   _initial_layer 210,210   ironing_flow 8%
```

Nên ba triệu chứng còn lại **không phải do preset bị revert**. Nguyên nhân nằm ở
những khoá chưa ai đụng tới.

### Sáu khoá chưa đụng, giải thích cả ba triệu chứng

| # | Khoá | Giá trị | Gây ra |
|---|---|---|---|
| 1 | `reduce_crossing_wall` | 0 *(kế thừa)* | tơ — travel cắt thẳng qua vật, mỗi layer 2 lần đi prime tower |
| 2 | `prime_tower_width` | 10 *(cha 30)* | tơ, lem màu — diện tích lau nhỏ 9 lần |
| 3 | `skirt_loops` | 🔴 0 — **bị xoá** | đường in đầu thiếu nhựa |
| 4 | `retraction_minimum_travel` | 1 | tơ **và** xước — không rút thì cũng không z-hop |
| 5 | `ironing_flow` | 8% *(cha 10%)* | mặt trên xước |
| 6 | `top_surface_speed` | 150 *(kế thừa)* | mặt trên xấu |

🔴 **Khoá 4 là mấu chốt cho triệu chứng 3.** Z-hop chỉ xảy ra **kèm theo
retraction**. Travel ngắn hơn 1 mm không rút, nên cũng không nhấc đầu in — nozzle
rê ngang qua mặt vừa in. Mặt trên đầy travel ngắn.

🔴 **Khoá 5 là mấu chốt còn lại.** Triệu chứng "mặt trên bị xước" là **mới**, và
`ironing_flow = 8%` cũng **mới** — bản 29/08 là lần đầu nó thật sự chạy. Là hoạt
động bằng cách rê nozzle trên một lớp nhựa mỏng; bớt 20% lớp đó thì nozzle cạ
thẳng vào mặt in.

Ghi thành P19–P22, và gỡ chặn P6.

### `Novi 0.16 - FIGURE` mất `skirt_loops` trong phiên slicer 16:59

Git commit `95f8911`:

```
+    "prime_tower_width": "10",
-    "seam_slope_type": "none",
-    "skirt_loops": "2",
```

- `seam_slope_type` mất là **vô hại** — trùng giá trị cha nên slicer bỏ override.
  Giá trị hiệu dụng vẫn `none`
- 🔴 `skirt_loops` mất là **mất thật** — cha để 0. `Novi 0.12 - FIGURE` vẫn còn 2,
  hai preset giờ lệch nhau
- 🔴 `prime_tower_width = 10` là khoá mới, chưa từng bàn

🟡 Ngoài ra project dùng `brim_type = auto_brim` trong khi preset ghi `brim_ears`
— tức plate mang **sửa đổi chưa lưu vào preset**. Bài học: `project_settings.config`
trong `.gcode.3mf` mới là thứ đã in, preset trên đĩa chỉ là điểm xuất phát.


### A7 🟢 — bốn slot đã đúng preset

Viet gán lại trong slicer rồi slice lại. Đọc `.conf` sau khi đóng slicer (16:41):

```
filament_colors = #F7E6DE,#FFFFFF,#000000,#BBFB98
filament    = PLA Bambulab Lite@KX 0.4    filament_01 = PLA Generic@KX 0.4
filament_02 = PLA Bambulab Lite@KX 0.4    filament_03 = PLA Generic@KX 0.4
```

| Slot | Nhựa | Màu | Preset |
|---|---|---|---|
| 1 | BBL PLA Lite | Beige | `PLA Bambulab Lite@KX 0.4` |
| 2 | Generic PLA | White | `PLA Generic@KX 0.4` |
| 3 | BBL PLA Lite | Black *(Viet xác nhận)* | `PLA Bambulab Lite@KX 0.4` |
| 4 | Generic PLA | Matcha | `PLA Generic@KX 0.4` |

🟢 Không còn slot nào dùng preset stock. `filament_retraction_length` giờ là `nil`
ở cả hai preset, nên `retraction_length = 1.2` ở tầng machine áp cho cả bốn slot.

### Đổi tên `PLA BBL Lite@KX 0.4` → `PLA Bambulab Lite@KX 0.4`

Viet đổi trong slicer. Slicer ghi file mới, xoá file cũ, cập nhật
`filament_settings_id` bên trong — đã kiểm cả ba.

Đã quét và sửa tên trong: `profiles/filament.md`, `TODO.md`, `PENDING_APPLY.md`,
`docs/preset-model.md`, `docs/tool.md`.

❌ **`CHANGELOG.md` giữ nguyên tên cũ.** Các mục trước ghi tên preset đúng như lúc
thao tác diễn ra; sửa lại là viết lại lịch sử. Ghi thành quy tắc: `docs/working-rules.md`
mục 10.

### P18 🟢 áp — lớp đầu preset Generic về 210 °C

Backup `user_backup-tune-set-20260829-164420`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `PLA Generic@KX 0.4` | `nozzle_temperature_initial_layer_HS` | 220 *(kế thừa)* | **210** |

Preset chỉ đè `nozzle_temperature_HS = 205`, quên bản `_initial_layer_HS`, nên lớp
đầu chạy 220 — chênh 15 °C so với các lớp sau, và chạm đúng trần
`nozzle_temperature_range_high = 220`. Giờ khớp với preset BBL.

### P17 🟢 — cloud sync tắt trên cả hai PC

Viet tắt *Auto sync user presets* trên PC còn lại. PC này vẫn `False`. Không PC
nào còn đường ghi đè preset của PC kia.

🟡 Đánh đổi: preset không tự lan sang PC kia nữa. Chuyển tay thì copy **cả cặp**
`.json` + `.info` từ `presets/` trong git. Ghi thành quy tắc thường trực:
`docs/working-rules.md` mục 9.


### A6 đóng — đọc slot map và ma trận flush từ gcode thật

Viet slice một mẫu 4 màu. Đọc thẳng gcode slicer vừa sinh
(`Temp\anycubicslicer_model\...\Metadata\.24448.0.gcode`, 16:31) thay vì `.conf` —
đây là thứ máy sẽ chạy, không phải ảnh chụp trạng thái.

```
; filament_colour      = #F7E6DE;#FFFFFF;#000000;#BBFB98
; filament_settings_id = "PLA BBL Lite@KX 0.4";"Anycubic PLA @…";"PLA Generic@KX 0.4";"Anycubic PLA @…"
; nozzle_temperature   = 205,220,205,220
; filament_flow_ratio  = 1,0.96,1,0.96
; filament_retraction_length = nil,0.8,nil,0.8
```

🟢 **Bốn màu đã đúng cả** — beige `#F7E6DE` và matcha `#BBFB98` đặt xong.

🔴 **Slot 2 và slot 4 dùng preset stock, hỏng ba thứ cùng lúc:** 220 °C thay vì
205, flow 0.96 thay vì 1.0, và `filament_retraction_length = 0.8` **đè lên**
`retraction_length = 1.2` ở tầng machine. Đúng cái hồi quy đã ghi hồi 24/08 — khoá
retraction ở tầng filament thắng tầng machine. Ba thứ đều đẩy về hướng tơ. Xem A7.

🟡 Slot 3 nạp BBL PLA Lite Black nhưng gán `PLA Generic@KX 0.4`.

### P15 và P16 xác nhận trong gcode thật

Không chỉ đọc lại file preset — đọc gcode để chắc slicer thật sự dùng:

```
; retraction_speed  = 45      ; retract_before_wipe = 100%
; z_hop_types = Normal Lift   ; seam_slope_type = none
; retraction_length = 1.2     ; filament_flow_ratio = 1,…,1,…
```

Và P16 nằm trong dòng lệnh thật, không chỉ trong khối config:

```
314788:G1 E-6 F1800 ; P16 ha ap suat vung nong chay, chong chay nhua cuoi ban in
```

### Ma trận flush thật, 4 màu mới

Đã thay bảng cũ trong `profiles/process.md`. Tổng **3854 mm³ ≈ 4,8 g** cho 12 lần
đổi màu.

🔴 Hàng Black chiếm 2205 mm³ — **57% toàn bộ**. Rời khỏi đen tốn 635–785 mm³ mỗi
lần; vào đen thì rẻ nhất bảng. Sắp thứ tự in để gom các đoạn đen lại.

🔴 Với FIGURE toàn bộ số đó là rác: `flush_into_objects = 0`, `flush_into_infill = 0`.

### A4 🟢 — đã tắt *Auto sync user presets* trên PC còn lại

Viet xác nhận. PC này vẫn `sync_user_preset = False`. Không PC nào còn đường ghi
đè preset của PC kia qua cloud.

🟡 Đổi lại: PC kia không nhận preset mới tự động nữa. Muốn đồng bộ thì copy cả cặp
`.json` + `.info` từ `presets/` trong git sang `%APPDATA%\AnycubicSlicerNext\user\855643\`.


### P15 🟢 áp — bộ sửa tơ + seam trở lại đĩa

Backup `user_backup-tune-set-20260829-161325`. Đã đọc lại file xác nhận cả 11 khoá.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| machine | `retraction_speed` | 35 | **45** |
| machine | `retract_before_wipe` | 70% | **100%** |
| machine | `z_hop_types` | *(kế thừa Slope Lift)* | **Normal Lift** |
| 2× FIGURE | `seam_slope_type` | external | **none** |
| 2× FIGURE | `ironing_flow` | *(kế thừa 10%)* | **8%** |
| 2× FIGURE | `ironing_inset` | *(kế thừa 0)* | **0.2** |
| 2× filament | `filament_flow_ratio` | 0.98 | **1.0** |

### P16 🟢 áp — retract ở cuối `machine_end_gcode`

Backup `user_backup-tune-p16-endgcode-20260829-161405`.

```
M400
G91
G1 E-6 F1800 ; P16 ha ap suat vung nong chay, chong chay nhua cuoi ban in
G1 Z5 F600 ; P16 nhac dau in khoi mat in
G90
M140 S0 ; turn off heatbed
M104 S0 ; turn off temperature
M107;turn off fan
M84; disable motors
; disable stepper motors
```

🔴 **Không dùng `--set` được, và đây là một cái bẫy thật.** `machine_end_gcode` là
**chuỗi** ở preset cha, nhưng `--set` bọc mọi giá trị machine/filament vào list khi
user preset chưa sở hữu khoá đó (`d[key] = [val] if kind in (filament, machine)
and not isinstance(old, str)`). `old` là `None` nên nó sẽ ghi
`["M400\nG91\n..."]` — sai kiểu, slicer đọc không ra.

Đã ghi bằng script riêng gọi thẳng `acslicer_tune.write_preset()` nên vẫn có
backup `user\` và vẫn bump `.info`. Đã đọc lại: kiểu `str` ✅.

📝 Chưa nghiệm thu — xem C2 trong `TODO.md`, có sẵn lệnh revert.

### 🔴 Sửa lại kết luận về nguyên nhân revert: chưa chứng minh được là do PC thứ hai

Giả thuyết hai PC ghi ở mục trên **nghe hợp lý nhưng không đứng vững** sau khi
soát thêm. Hai bằng chứng ngược:

**1. PC này đang tắt đồng bộ user preset.** `.conf`:

```
app.sync_user_preset  = False
app.sync_system_preset = True
```

Tắt thì PC này không đẩy lên — nhưng cũng không kéo về. Log phiên
28/08 21:58 → 29/08 15:33 không có một dòng nào về sync preset.

**2. Trạng thái bị revert trùng byte với một backup cục bộ.** So `user\` ngay
trước P15 với từng thư mục backup:

| Backup | Khác gì |
|---|---|
| `user_backup-tune-set-20260826-205206` | 🔴 **chỉ khác đúng 2 file Test1** *(tạo sau)*, còn lại giống hệt |
| `user_backup-tune-set-20260826-211029` | khác machine + 2 process + filament |
| `user_backup-tune-set-20260825-2*` | khác nhiều |

`-205206` chính là backup `acslicer_tune.py` chụp **ngay trước khi áp P8–P11**.
Tức trạng thái bị revert = đúng ảnh chụp trước P8, không sai một byte.

🟡 Hai cơ chế cùng khớp, không phân biệt được từ file:

- **Cloud kéo về.** PC này không đẩy lên, nên bản trên cloud vĩnh viễn là bản
  trước P8. Bất kỳ lần pull nào cũng trả về đúng ảnh đó
- **Khôi phục backup cục bộ.** Ai đó đổi tên `user_backup-tune-set-20260826-205206`
  thành `user`, đúng quy trình revert ghi trong `docs/tool.md`

Log chỉ lùi tới 28/08 nên sự kiện 27/08 không còn dấu vết. ❌ Không kết luận được.

🟢 **May là cách xử lý không đổi theo nguyên nhân:** đọc lại preset từ đĩa ngay
trước khi in. Đã thành bước bắt buộc trong C1.

### Không có chế độ "chỉ kéo về, không đẩy lên"

Viet hỏi làm sao để PC thứ hai chỉ nhận preset chứ không đẩy. 🔴 Slicer không có
tuỳ chọn đó. `sync_user_preset` là **một công tắc hai chiều** — Preferences →
*Auto sync user presets*. Bật thì cả đẩy lẫn kéo; tắt thì không cái nào.

Cách gần nhất: tắt trên PC kia, rồi chuyển preset sang bằng tay từ `presets/`
trong git. Ghi thành P17 mới.

### Nguyên nhân revert: hai PC cùng một tài khoản cloud

Viet in bằng **2 PC**, cả hai đăng nhập user id `855643`. PC còn lại không có ai
theo dõi preset nên vẫn giữ bộ 24–25/08.

| Bước | Xảy ra gì |
|---|---|
| 1 | PC này áp P8–P14 vào 26/08, `updated_time` nhảy lên 26/08 |
| 2 | PC kia mở slicer, mang theo bộ preset cũ **và `.info` cũ của nó** |
| 3 | Sync đẩy bộ cũ lên cloud |
| 4 | PC này mở slicer, kéo về, `.json` + `.info` bị thay cả cặp |

🟢 Giải thích được chi tiết khó nhất: `updated_time` **lùi về** 24/08 11:35 và
25/08 22:10. Trên một máy đơn không có cơ chế nào làm được — slicer flush RAM chỉ
ghi `.json`. File đến từ máy khác thì mới mang theo sidecar cũ.

🟢 Cũng giải thích vì sao cả năm đề xuất chết cùng lúc: sync không xét từng khoá,
nó thay **nguyên file**.

Cách chặn: [P17](PENDING_APPLY.md#p17), Viet chưa chốt.

### A5 — xoá `Novi 0.16 Test1- FIGURE @AC KX`

Backup `user_backup-delete-test1-20260829-155923`. Xoá cả `.json` và `.info`.
Kho user còn 8 preset: 2 filament, 1 machine, 5 process.

🟡 Nếu PC kia còn đăng nhập, cloud có thể dựng lại preset này ở lần mở slicer sau.
Kiểm tra lại sau khi chốt P17.

### Màu nhựa: màn hình máy in không nói chuyện với slicer

Viet đặt màu cuộn beige bằng màn hình cảm ứng trên máy. Đóng slicer lúc 15:33 rồi
đọc `.conf`:

```
filament_colors = #FF0000,#FF0000,#FFFFFF,#000000
```

Không có beige. 🔴 Hai kho cấu hình riêng — màn hình máy lo trạm nạp nhựa,
`filament_colors` trong `.conf` mới là số slicer đọc để tính
`flush_volumes_matrix`. Phải đặt trong slicer, tab Filament.

### `.conf` báo gán slot lệch `profiles/filament.md` ở 3/4 dòng

| Slot | `.conf` — preset | `.conf` — màu | `profiles/filament.md` |
|---|---|---|---|
| 1 | `PLA BBL Lite@KX 0.4` | `#FF0000` | BBL, Red ✅ |
| 2 | 🔴 `Anycubic PLA @…` *(stock)* | `#FF0000` | Generic PLA, White |
| 3 | 🔴 `PLA Generic@KX 0.4` | `#FFFFFF` | BBL, Black |
| 4 | 🔴 `Anycubic PLA @…` *(stock)* | `#000000` | Generic PLA, Matcha |

🟡 Bản in 29/08 Viet gọi là "BBL slot 3", nhưng `.conf` bảo slot 3 gán
`PLA Generic@KX 0.4`. Nếu `.conf` đúng thì bản in đó chạy sai cả preset nhựa —
thêm một nguyên nhân tơ chồng lên chuyện revert. Chưa phân xử được từ file:
A6 trong `TODO.md`.

### Cloud sync đã revert toàn bộ P8 P9 P10 P11 P14

Bản in `Novi 0.16 - FIGURE @AC KX` ngày 29/08 (BBL, slot 3) vẫn còn tơ nhiều.
Soát đĩa trước khi kết luận thì thấy **bộ sửa không còn ở đó**.

Đối chiếu `presets/` trong git — commit `6f48059` (26/08) áp, commit `2316edd`
(27/08) trả lại hết:

| Preset | Key | P8–P14 đặt | Trên đĩa 29/08 |
|---|---|---|---|
| machine | `retraction_speed` | 45 | 🔴 35 |
| machine | `retract_before_wipe` | 100% | 🔴 70% |
| machine | `z_hop_types` | Normal Lift | 🔴 khoá bị xoá |
| 2× FIGURE | `seam_slope_type` | none | 🔴 external |
| 2× FIGURE | `ironing_flow` / `ironing_inset` | 8% / 0.2 | 🔴 khoá bị xoá |
| 2× filament | `filament_flow_ratio` | 1.0 | 🔴 0.98 |

Không sót cái nào. Cả năm đề xuất bị xoá cùng một lúc.

**Cơ chế: cloud sync, không phải slicer flush.** Bằng chứng nằm ở `.info`.
`acslicer_tune.py` bump `updated_time` lên thời điểm ghi mỗi lần `--set`, nên sau
lần áp 26/08 ba sidecar phải mang mốc 26/08. Thực tế đọc được:

| Sidecar | `updated_time` | |
|---|---|---|
| machine | 1787546119 | 2026-08-24 11:35 |
| `Novi 0.16 - FIGURE` | 1787670644 | 2026-08-25 22:10 |
| `PLA BBL Lite@KX 0.4` | 1787629803 | 2026-08-25 10:50 |

Sidecar bị lùi về trước ngày áp, tức **cả cặp `.json` + `.info` bị thay bằng bản
cũ hơn** — slicer flush state trong RAM thì không làm được chuyện đó, nó chỉ ghi
`.json`. Cả ba đều mang `sync_info = update`.

🔴 Hệ quả cho quy trình: **bump `updated_time` không đủ để thắng cloud sync.**
Non-negotiable số 3 trong `CLAUDE.md` là điều kiện cần, không phải điều kiện đủ.
Ghi vào đĩa trong khi tài khoản còn đăng nhập là ghi vào chỗ có thể bị đè bất kỳ
lúc nào. Đề xuất P17 xử lý.

🟡 Hệ quả cho C1: bản in 29/08 **không nghiệm thu được gì**. Nó chạy bằng cấu
hình trước 26/08, nên "còn tơ" không phủ nhận P8–P11 — chỉ nói P8–P11 chưa từng
chạy. C1 phải in lại sau P15.

### Soát ba triệu chứng của bản in 29/08

| # | Triệu chứng | Nguyên nhân đọc được từ preset |
|---|---|---|
| 1 | còn tơ nhiều | bộ sửa tơ đã bị revert — xem trên |
| 2 | nhựa thừa kéo dài ở chỗ ngắt | `seam_slope_type = external` vẫn bật + `pressure_advance = 0.036` chưa hiệu chuẩn |
| 3 | sợi nhựa ~5 cm ở nozzle đầu và cuối bản in | `machine_end_gcode` không có lệnh retract nào |

Triệu chứng 3 tách làm hai vế khác hẳn nhau:

- **Cuối bản in** — `machine_end_gcode` đi thẳng `M400` → `M140 S0` → `M104 S0`.
  Nozzle đầy nhựa nóng đang chịu áp rồi nguội dần trong vài phút. Sửa được: P16.
- **Đầu bản in** — `machine_start_gcode` chỉ có `G9111`. Macro nằm trong firmware,
  tự gia nhiệt / home / cân bàn / mồi. Nozzle đứng ở nhiệt in suốt quá trình đó.
  ❌ Không sửa được từ preset.

### Phát hiện preset process thứ 6: `Novi 0.16 Test1- FIGURE @AC KX`

Kho có 6 process preset, `profiles/process.md` chỉ mô tả 5. Preset thừa là bản
copy của `Novi 0.16 - FIGURE` với `sparse_infill_pattern = lightning`,
`sparse_infill_density = 8%`, `top_shell_layers = 4`, và **thiếu** `brim_type`,
`outer_wall_speed`, `small_perimeter_threshold`, `wall_loops`, `seam_gap`.

📝 Chưa xử lý — chờ Viet nói giữ hay xoá. Xem A5 trong `TODO.md`.

### `profiles/` lệch đĩa ở bốn chỗ

Đọc lại toàn bộ chuỗi kế thừa và đối chiếu:

| File | Ghi | Thực tế |
|---|---|---|
| `profiles/printer.md` | `retraction_length = 1` | 1.2 |
| `profiles/printer.md` | `retraction_minimum_travel = 2` | 1 |
| `profiles/printer.md` | *(không nhắc)* | `retract_before_wipe = 70%` |
| `profiles/filament.md` | `nozzle_temperature_HS = 212` | 205, initial layer 210 |

🔵 Ngược lại, mấy khoá `profiles/filament.md` ghi là "đang đặt" mà không thấy
trong file user preset — `filament_max_volumetric_speed = 13`,
`pressure_advance = 0.036`, `textured_plate_temp = 60/60`, `fan_min/max_speed_HS
= 60/90` — đều **đúng**, chỉ là kế thừa từ `Anycubic PLA @Anycubic Kobra X 0.4
nozzle` chứ không phải override. Giá trị hiệu dụng khớp.

---

## 2026-08-26

### P14 P12 — flow ratio và đồng bộ preset thứ 8

Backup `user_backup-tune-set-20260826-211029`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| 2× filament | `filament_flow_ratio` | 0.98 | **1.0** |
| `Novi 0.20 - FIGURE` | `ironing_flow` | 10% | **8%** |
| | `ironing_inset` | 0 | **0.2** |
| | `seam_slope_type` | external | **none** |
| | `brim_type` | auto_brim | **brim_ears** |
| | `initial_layer_speed` | 50 | **30** |
| | `initial_layer_infill_speed` | 200 | **50** |
| | `wall_loops` | 3 | **4** |

🟢 Năm preset process giờ đồng bộ với nhau về bộ sửa bám bàn và ironing.

🟡 `filament_flow_ratio = 1.0` là bước đoán +2% từ mức "hơi thiếu" Viet báo. Số
đo thật lấy bằng hộp một tường: `flow_ratio_mới = 0.98 × (0.42 / bề_dày_đo)`.

### Thêm bảng tổng quan vào `TODO.md` và `PENDING_APPLY.md`

Hai file đã dài tới mức phải đọc hết mới biết còn gì treo. Thêm bảng ở đầu, có
anchor link xuống từng mục.

`PENDING_APPLY.md` giờ chỉ còn P6, và đổi từ 📝 sang ⏳ — hoãn có chủ đích, không
phải chưa xét tới. `TODO.md` thêm mục C1: nghiệm thu bộ sửa tơ đang chờ một bản
in, và chính nó là thứ chặn P6.

### Chốt ba câu hỏi treo: A1, A2, B1

**B1 — giữ `Novi 0.20 - FIGURE @AC KX` nguyên cha `0.16mm High Quality`.** Lệch
quy ước nhưng chạy được. P13 (dựng lại preset) bỏ khỏi bucket.

**A1 — tường hơi thiếu nhựa.** 🔵 Nhưng thủ phạm **không phải** trần flow:
`filament_max_volumetric_speed` chỉ hạ *tốc độ* khi
`speed × layer_height × line_width` vượt trần, lượng nhựa trên mỗi mm đường đi
không đổi. Chạm trần thì in chậm hơn, không mỏng hơn. Nên 13 giữ nguyên và câu
hỏi "13 có đủ không" thực ra đặt sai — đã đủ, vì nó không phải thứ gây thiếu.

Thủ phạm là `filament_flow_ratio = 0.98`. Đề xuất P14 nâng lên 1.0, kèm cách đo
thật bằng hộp một tường thay vì đoán.

**A2 — khi preset trong slicer khác `presets/` trong git thì slicer thắng.** Ghi
thành quy tắc thường trực ở `docs/working-rules.md` mục 6. Lý do: không phân biệt
được "cloud sync ghi đè" với "Viet vừa đổi ý" chỉ bằng cách nhìn file. Đoán sai
theo hướng khôi phục thì xoá mất việc Viet vừa làm; đoán sai theo hướng giữ thì
chỉ mất một bản sửa đã có trong `CHANGELOG.md` và áp lại được.

A2 cũ (điều tra vụ revert) đóng lại. A2 mới là hiệu chuẩn Pressure Advance — số
`0.036` chưa bao giờ được đo, và nó chi phối trực tiếp cục nhựa ở seam.

### P8 P9 P10 P11 — bộ sửa tơ và seam

Backup `user_backup-tune-set-20260826-205206`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| machine | `retraction_speed` | 35 | **45** |
| machine | `retract_before_wipe` | 70% | **100%** |
| machine | `z_hop_types` | Slope Lift | **Normal Lift** |
| 2× FIGURE | `ironing_flow` | 10% | **8%** |
| 2× FIGURE | `ironing_inset` | 0 | **0.2** |
| 2× FIGURE | `seam_slope_type` | external | **none** |

**P11 đảo ngược P7.** P7 (25/08) làm scarf chạy mạnh hơn; P11 tắt scarf hẳn. Bằng
chứng là bản in đẹp ở slot 3 — nó không có scarf. Ba khoá P7 ghi hôm qua
(`seam_slope_conditional`, `seam_slope_min_length`, `scarf_joint_flow_ratio`) giờ
thành khoá chết, giữ lại phòng khi bật scarf lại.

🟡 P11 vốn đánh dấu ⏳ chờ in thử P7. Viet gọi tên nó tức là gỡ chặn — nên P7
chưa bao giờ được in thử, và sẽ không bao giờ. Chấp nhận: bằng chứng từ TOOL 0.20
đủ mạnh hơn một lần thử.

🟡 Bốn thay đổi cùng lúc, ba trong số đó (P8, P9, P10) đều nhắm vào tơ. Bản in
tới cho biết tơ hết hay không, **không** cho biết cái nào có công. P6 giữ lại
trong bucket vì lý do đó.

### Phát hiện preset thứ 8: `Novi 0.20 - FIGURE @AC KX`

Audit đếm 8 user preset thay vì 7. Viet tạo preset này trong slicer ngày 25/08
lúc 23:26; tôi không biết nên **mọi bản sửa từ đó tới nay không chạm vào nó**.

🔴 Nó thiếu cả bộ sửa bám bàn — `brim_type` vẫn auto_brim, `initial_layer_speed`
vẫn 50, `initial_layer_infill_speed` để 200. Đây đúng là cấu hình đã gây bong
bàn. In bằng preset này là quay lại rủi ro cũ. Đề xuất P12.

🟡 `inherits = 0.16mm High Quality` nhưng `layer_height = 0.2` — lệch quy ước
"kế thừa preset hãng đúng layer height". Ghi thành B1 trong `TODO.md`.

🔵 Bài học quy trình: `--audit` đếm số preset, và con số đó đổi là tín hiệu. Nếu
không để ý dòng "8 user presets" thì preset này còn trôi thêm nhiều ngày nữa.

### Slot 4 thay nhựa: Generic PLA màu matcha

Cuộn cũ là Bambu Lab PLA Lite Cyan, mở 13/08. Cập nhật `profiles/filament.md`.

⏳ Hex để trống, không bịa. `.conf` của máy này chỉ nhớ trạng thái một màu
(`#00FFFF` cũ); màu 4 slot nằm trong project `.3mf`. Viet đặt màu trong UI thì
slicer tự tính lại flush.

### Bản in đẹp ở slot 3 — dữ liệu đối chứng tốt nhất tới giờ

`Novi 0.20 - TOOL @AC KX`, slot 3, kết quả rất đẹp. Cùng cuộn
`PLA BBL Lite@KX 0.4`, cùng machine preset, cùng retraction như bản FIGURE bị tơ
và seam dư nhựa. **Khác mỗi process preset** — nên diff hai preset khoanh được
vùng nghi vấn.

Hai tính năng chỉ FIGURE mới có, rơi đúng vào hai lỗi còn lại:

| | TOOL 0.20 *(đẹp)* | FIGURE 0.16 *(lỗi)* |
|---|---|---|
| `ironing_type` | no ironing | **top** |
| `seam_slope_type` | none | **external** |
| `outer_wall_speed` | 120 | 50 |

🔴 **Lỗi của tôi tìm ra nhờ đó:** hạ `ironing_spacing` 0.15 → 0.1 mà không hạ
`ironing_flow`. Số đường miết tăng 1,5 lần, mỗi đường vẫn 10% flow — tổng nhựa
rải lên mặt trên tăng ~50%. Cộng `ironing_inset = 0` (miết sát mép, đẩy nhựa
tràn qua tường ngoài). Đề xuất P10.

🟡 **P7 có thể đi sai hướng.** Tôi giả định thêm scarf thì seam đẹp hơn; bản in
đẹp lại **không có scarf**. Scarf tăng giảm flow dọc đoạn nối, mà
`pressure_advance = 0.036` là số đoán, chưa hiệu chuẩn — nên scarf có thể đang
gây cục nhựa chứ không sửa. Ghi thành P11 nhưng **chặn lại**: P7 chưa in thử lần
nào, test P7 trước rồi mới quyết.

🔵 **Giả thuyết ẩm yếu đi nhiều.** Slot 3 cùng cuộn, cùng ngày mở túi 13/08 với
slot 1. Nhựa ẩm không chừa slot nào. Sấy lò không còn là việc nên làm trước.
Chưa loại hẳn — khác màu và khác layer height.

---

## 2026-08-25

### P7 — cho scarf joint chạy thật trên hai preset FIGURE

Backup `user_backup-tune-set-20260825-221044`.

`seam_slope_type = external` trông như đã bật từ lâu, nhưng hai khoá khác vô hiệu
hoá nó trên phần lớn đường viền. Cùng loại lỗi với `small_perimeter_threshold = 0`:
cài đặt có, tác dụng không.

| Key | Cũ | Mới | Vì sao |
|---|---|---|---|
| `seam_slope_conditional` | 1 | **0** | 1 = chỉ áp scarf khi điều kiện góc thoả, nhiều seam bị bỏ qua |
| `seam_slope_min_length` | 10 | **5** | đường viền ngắn hơn ngưỡng không có scarf. Figure chi tiết nhỏ thì đa số dưới 10 mm |
| `scarf_joint_flow_ratio` | 1 | **0.95** | bớt nhựa ở đoạn chồng của scarf |

🟡 Chỉ ghi vào `Novi 0.12 - FIGURE` và `Novi 0.16 - FIGURE`. TOOL và TEST có
`seam_slope_type = none` — scarf tắt hẳn, ba khoá trên là khoá chết ở đó. Bucket
ghi "cả 4 process" là sai, đã thu hẹp phạm vi.

🔵 Đánh đổi: scarf trên góc nhọn có thể làm cạnh hơi tròn. Thấy cạnh mất sắc thì
trả `seam_slope_conditional` về 1.

### B1 chốt: lớp đầu `Novi 0.12 - FIGURE` giữ 0.2

Không chép quy tắc "lớp đầu = layer height" từ bản 0.16 sang. Lớp đầu dày hơn
layer height cho dung sai bám bàn, và bám bàn là thứ vừa sửa xong.

### Chép bộ sửa bám bàn sang `Novi 0.12 - FIGURE @AC KX`

Backup `user_backup-tune-set-20260825-220223`.

| Key | Cũ | Mới |
|---|---|---|
| `brim_type` | auto_brim | **brim_ears** |
| `initial_layer_speed` | 50 | **30** |
| `initial_layer_infill_speed` | 100 | **50** |
| `wall_loops` | 3 | **4** |

🟡 `initial_layer_print_height` **không chép** — giữ 0.2. Bản 0.16 đặt lớp đầu
bằng chính layer height; áp logic đó cho 0.12 thì lớp đầu chỉ còn 0.12 mm, mất
dung sai bám bàn đúng lúc đang sửa bám bàn. Đang chờ Viet chốt.

🔵 `sparse_infill_density` cũng không chép — 0.12 giữ 18%, không phải giá trị
first-layer nên ngoài phạm vi lần này.

### Clone filament trong project tự hết — A3 đóng, không cần sửa file

Lần save 21:46 ghi lại project. `project_settings.config` giờ đúng cho cả bốn
slot: nhiệt bàn 60/60 ×4, `nozzle_temperature_HS` 212·212·205·212,
`fan_min_speed_HS` 60 ×4, `filament_max_volumetric_speed` 13 ×4,
`curr_bed_type = Textured PEI Plate`. `filament_settings_id` trỏ về bốn preset
thật, hết đuôi `(...3mf)`.

Ba khối `Metadata/filament_settings_*.config` còn sót nhưng không còn ai tham
chiếu — rác chết, không vào g-code. ❌ Không xoá: phải mở nén rồi ghi lại file
model 24 MB để đổi lấy 0 thay đổi trong bản in.

🔵 Bài học đọc chỉ số: `filament_settings_id` cho biết **trỏ vào đâu**,
`project_settings.config` cho biết **giá trị thật lúc slice**. Lần trước tôi đọc
cái đầu rồi kết luận ba slot lạnh — phải đọc cái sau mới chắc.

### Viet tự chỉnh `Novi 0.16 - FIGURE @AC KX` trong slicer — hết bong bàn

Lưu bằng nút save preset trong slicer, không qua `acslicer_tune.py`. Không cần
backup vì slicer tự ghi.

| Key | Cũ | Mới |
|---|---|---|
| `brim_type` | auto_brim | **brim_ears** |
| `initial_layer_speed` | 50 | **30** |
| `initial_layer_infill_speed` | 100 | **50** |
| `initial_layer_print_height` | 0.2 | **0.16** |
| `wall_loops` | 3 | **4** |
| `sparse_infill_density` | 18% | **15%** *(= cha, override bị bỏ)* |

🟢 `small_perimeter_threshold`, `wipe_before_external_loop`, `seam_gap` áp sáng
cùng ngày vẫn còn — slicer không xoá gì của tôi.

### Phân biệt "slicer bỏ key" với "preset bị revert"

Lần lưu này xoá hai key khỏi user preset: `sparse_infill_density` ở process, và
`textured_plate_temp*` ở `PLA Generic@KX 0.4`. Cả hai **vô hại** — giá trị trùng
với cha nên slicer không lưu override, giá trị hiệu lực không đổi.

🔵 Cách phân biệt, dùng lại được về sau:

| Dấu hiệu | Nghĩa |
|---|---|
| key mất, **giá trị hiệu lực không đổi** | slicer dọn override trùng cha — bình thường |
| key mất hoặc đổi, **giá trị hiệu lực đổi** | bị ghi đè — điều tra như `058b051` |

Chỉ so nội dung file thì hai ca này giống nhau. Phải flatten cả chuỗi `inherits`
mới thấy khác. Kiểm chứng: cả hai filament vẫn ra `textured_plate_temp` 60/60.

### Tìm ra chỉnh sửa nằm trong project, không phải preset

Tưởng là preset đã đổi, nhưng mọi file preset còn nguyên mtime của lần ghi trước
— chỉ `.conf` đổi. Sửa của Viet nằm trong
`ArticulatedCuteCrab_MultipartBambuStudioA1.3mf`, đọc ra bằng cách unzip và diff
`Metadata/project_settings.config` với preset đã flatten.

🔴 Phát hiện kèm theo: project đó gán ba trong bốn slot vào **filament clone
project-local** — tên có đuôi `(...3mf)`, còn giữ nhiệt bàn 50/45,
`nozzle_temperature_HS = 202`, `filament_max_volumetric_speed = 15`. Ảnh chụp từ
khoảng 22/08. Bản in vừa rồi hết bong vì nó dùng **slot 1**, slot duy nhất trỏ
vào preset thật ở 60 °C. In 4 màu trong project này thì ba slot kia vẫn lạnh.

⏳ Gán lại slot 2/3/4 về preset thật: chỉ làm được trong UI, đang treo ở
`TODO.md`.

## 2026-08-25 *(sáng)*

### Preset bị revert — khôi phục, và tìm ra bàn nhiệt sai loại

Bản in đẹp hơn nhiều nhưng bong khỏi bàn ở vài vị trí, kèm nhựa cháy đen bám
ngược lên nozzle. Backup `user_backup-tune-set-20260825-105003` và
`...-105013`.

**Không phải chỉnh sai — preset đã bị ghi đè.** Commit `058b051` (24/08, sau
`9a80457`) xoá loạt sửa của ngày 23 và ghi lại giá trị cũ. Nghi cloud sync kéo
bản trên mây đè bản local. Chi tiết theo dõi ở A4 trong `TODO.md`.

**Máy chạy bàn Textured PEI**, không phải bàn nhẵn. `curr_bed_type = 4` cho
`Anycubic Kobra X 0.4 nozzle - high quality`, nên cặp key có tác dụng là
`textured_plate_temp*`. Sau revert, bàn chạy 50 lớp đầu rồi tụt về **45** duy
trì — quá lạnh cho PLA. Vật bám lớp đầu rồi bong giữa chừng, nozzle đập vào,
nhựa quấn lên đầu in và cháy thành carbon.

🔵 Nhựa cháy là **hậu quả**, không phải nguyên nhân. Carbon bong ra từng mảnh
rơi vào dòng nhựa — nhiều khả năng chính là các điểm thiếu nhựa rải rác trước
đó. Ba triệu chứng cùng một chuỗi nhân quả.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `PLA BBL Lite@KX 0.4` | `textured_plate_temp_initial_layer` | 50 | **60** |
| `PLA BBL Lite@KX 0.4` | `textured_plate_temp` | 45 | **60** |
| `PLA BBL Lite@KX 0.4` | `nozzle_temperature_HS` | 210 | **212** |
| `PLA BBL Lite@KX 0.4` | `fan_min_speed_HS` | *(vắng)* | **60** |
| `PLA Generic@KX 0.4` | `textured_plate_temp_initial_layer` | 55 | **60** |
| `PLA Generic@KX 0.4` | `textured_plate_temp` | 45 | **60** |

🔵 Giá trị hãng của cả hai khoá `textured_plate_temp*` vốn đã là 60/60. Con số
45/50 nằm trong user preset là override **lạnh hơn hãng** — dấu vết rõ ràng của
lần revert, không phải mặc định.

🟡 `fan_min_speed_HS` thực ra đã là 60 nhờ kế thừa từ hãng — bucket ghi "hiện
tại 80" là sai, 80 là `fan_min_speed` (khoá máy này bỏ qua). Vẫn ghi 60 tường
minh để lần ghi đè sau nhìn thấy được trong `git diff`.

### `small_perimeter_speed` chưa từng chạy

`small_perimeter_threshold = 0` nghĩa là không đoạn nào đủ điều kiện "chu vi
nhỏ", nên `small_perimeter_speed = 50%` là cài đặt chết. Lỗ và trụ nhỏ vẫn in ở
tốc độ tường ngoài đầy đủ, đầu đùn không kịp bơm trong đoạn ngắn — ra thiếu
nhựa.

Đặt ngưỡng **20 mm** chu vi (≈ đường kính 6,4 mm) cho cả bốn process.

### Giảm seam

Cả bốn process: `wipe_before_external_loop` 0 → **1**, `seam_gap` 10% → **15%**.

### Phần cứng — Viet đã làm

Nozzle đã được làm sạch, bàn PEI đã rửa. Hai việc này preset không thay được và
là điều kiện để đánh giá bản in tới.

---

## 2026-08-24

### Sửa hồi quy nhiệt bàn — bản in bong thành "mỳ tôm"

Bản in bong khỏi bàn ngay từ mấy lớp đầu. Hai lỗi, cả hai do tôi.
Backup `user_backup-tune-set-20260824-121615`.

**Nhiệt bàn 50 thay vì 60.** Lúc gộp hai preset BBL, chúng ghi nhiệt bàn mâu
thuẫn nhau (50/45 và 45/50). Tôi chốt phẳng 50 — lấy con số từ preset cũ chưa rõ
nguồn gốc thay vì quay về giá trị hãng là 60. Thiếu 10 °C thì PLA bám yếu. Lớp
đầu đã có dấu hiệu bong ở lần in trước, lần này bong hẳn.

🔵 Bài học: khi hai giá trị mâu thuẫn nhau và không biết cái nào đúng, mốc để
quay về là **giá trị của hãng**, không phải trung bình hay một trong hai.

**Lệnh giảm quạt chưa từng có tác dụng.** Máy này chỉ đọc biến thể `_HS`. Slicer
đã lặng lẽ xoá `fan_min_speed = 60` và giữ `fan_min_speed_HS = 80`. Cùng lý do
`nozzle_temperature = 212` bị xoá còn `nozzle_temperature_HS = 212` sống sót —
phần nhiệt may mà đúng vì đã đặt cả hai khoá.

| Key | Cũ | Mới |
|---|---|---|
| `hot_plate_temp` / `_initial_layer` | 50 / 50 | 60 / 60 |
| `textured_plate_temp` / `_initial_layer` | 50 / 50 | 60 / 60 |
| `fan_min_speed_HS` | 80 | 60 |

🟢 Pressure advance không bị ảnh hưởng. Slicer xoá `pressure_advance` và
`adaptive_pressure_advance` khỏi preset vì chúng đã trùng giá trị cha — đúng
hành vi, giá trị hiệu lực vẫn là 0.036 và tắt.

**Nới ngưỡng cảnh báo nhiệt bàn** trong `tools/acslicer_tune.py` từ `+5` lên
`+15` so với `temperature_vitrification`. Ở mức cũ nó kêu ngay với bàn 60 °C cho
PLA — vốn là chuẩn ngành, là mặc định của hãng, và đã có
`elefant_foot_compensation` bù. Cảnh báo đúng mà vô dụng thì chỉ làm nhiễu.

### Tăng infill FIGURE 12% → 18%

Backup `user_backup-tune-set-20260824-114109`. Audit: 0 lỗi.

`sparse_infill_density` 12% → 18% cho cả `Novi 0.12` và `Novi 0.16 - FIGURE`,
giữ nguyên `gyroid`. Cùng với wall 3, đây là đòn bẩy vật liệu cuối cùng cho độ
bền của profile FIGURE.

🟡 Áp dù chưa xác định được kiểu gãy. Nếu vật **tách theo lớp ngang** chứ không
gãy ngang thân thì thay đổi này không giúp gì — liên kết giữa các lớp là bài
toán nhiệt hoặc ẩm, không phải lượng vật liệu. Bản in trước đã chạy 3 wall mà
vẫn gãy, nên khả năng đó là đáng kể.

### Mồi nozzle bằng skirt, tơ đợt 2, đồng bộ wall

Backup `user_backup-tune-set-20260824-113519`. Audit: 0 lỗi.

**Vị trí in đầu tiên của lớp đầu bị bong và thiếu nhựa.** `skirt_loops = 0` ở
cả bốn profile — không có gì mồi nozzle trước khi vào vật in. Nozzle rỉ nhựa
lúc gia nhiệt nên mất áp, và những đường đùn đầu tiên bị đói, rơi đúng vào chỗ
vật bắt đầu. Đặt `skirt_loops = 2` cho cả bốn.

🔵 Chẩn đoán trước đó sai. Khi triệu chứng được mô tả là "một vài vị trí" thì
suy ra bàn cong; khi biết rõ là "**vị trí đầu tiên**" thì đó là chuyện mồi
nozzle. Hai lỗi khác nhau, cần hỏi cho rõ trước khi kết luận.

**Tơ vẫn còn sau khi sửa PA và nâng nhiệt.** Ba đòn bẩy cùng trục kiểm soát rỉ
nhựa:

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `Kobra X 0.4 - high quality` | `retraction_length` | 1 | 1.2 |
| `Kobra X 0.4 - high quality` | `retract_before_wipe` | 0% | 70% |
| cả 4 process | `wipe_on_loops` | 0 | 1 |

**Wall.** `Novi 0.16 - FIGURE` hoá ra đã được đổi sang 3 wall trong UI từ trước
— bản in bị gãy đã chạy ở 3 wall, nên wall không phải nút thắt. Đồng bộ
`Novi 0.12 - FIGURE` lên 3 cho cùng mục đích thì cùng độ dày vỏ.

⏳ Còn treo: nếu vật **tách theo lớp ngang** chứ không gãy ngang thân thì thêm
wall hay infill đều không cứu được — đó là bài toán nhiệt hoặc ẩm. Cuộn slot 1
mở 2026-08-13, không máy sấy.

### Sửa pressure advance hỏng và tách lớp

Từ một bản in `Novi 0.16 - FIGURE @AC KX` trên slot 1 (BBL PLA Lite).
Backup `user_backup-tune-set-20260824-083913`. Audit: 0 lỗi.

**Nhựa dư ở đường seam.** `adaptive_pressure_advance = 1` nhưng
`adaptive_pressure_advance_model` toàn số `0` — chưa hiệu chuẩn bao giờ. PA tính
ra gần bằng 0, nozzle đùn tiếp khi lẽ ra phải dừng, nhựa dư đọng đúng chỗ kết
thúc vòng. Slot 2 không bị vì nó tắt adaptive và dùng PA tĩnh 0.036.

Cờ `adaptive_pressure_advance` này được mang sang khi gộp hai preset BBL mà
không kiểm model có dữ liệu không.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `PLA BBL Lite@KX 0.4` | `adaptive_pressure_advance` | 1 | 0 |
| `PLA BBL Lite@KX 0.4` | `pressure_advance` | 0.025 | 0.036 |
| `Novi 0.12 / 0.16 - FIGURE` | `seam_slope_type` | all | external |

`seam_slope_type = all` áp scarf joint cho cả tường trong — không ai nhìn thấy,
mà mỗi chỗ vát là một lần chuyển lượng nhựa đẩy thêm vật liệu ra ngoài.

**Lớp giòn, tách được bằng tay.** Nhiệt 202 °C ở đáy dải PLA, quạt tối thiểu
80%, và FIGURE in chậm ở layer mỏng nên mỗi đường nhựa nguội hẳn trước khi lớp
sau đắp lên.

| Key | Cũ | Mới |
|---|---|---|
| `nozzle_temperature_HS` | 202 | 212 |
| `nozzle_temperature` | 205 *(kế thừa)* | 212 |
| `fan_min_speed` | 80 | 60 |

Đặt cả hai khoá nhiệt để không phụ thuộc slicer đọc khoá nào. `overhang_fan_speed`
giữ 100 nên overhang vẫn được làm mát tối đa dù quạt nền hạ xuống.

🟡 Hai nhóm này đối nghịch nhau — nâng nhiệt làm tăng tơ. Áp cùng lúc là có chủ
ý: sửa PA giảm tơ, bù lại phần nhiệt tăng thêm.

---

## 2026-08-23

### Chống xệ overhang và giảm tơ, từ một bản in thật

Bản in một màu trên slot 2 với `Novi 0.20 - TOOL @AC KX` cho ba triệu chứng.
Backup `user_backup-tune-set-20260823-223042`. Audit sau khi ghi: 0 lỗi.

**Xệ ở đỉnh lỗ tròn.** Đỉnh lỗ là vòng cung thoải dần thành dốc. Vùng 25–50%
đầu cung chạy 50 mm/s và **chưa được tăng quạt**, vì `overhang_fan_threshold`
đặt ở 50%. Xệ bắt đầu từ đó rồi phần dốc hơn đắp lên chỗ đã xệ. Quạt vốn đã
100% ở overhang — vấn đề là vào quá muộn, không phải thiếu mát.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `Novi 0.20 - TOOL @AC KX` | `overhang_2_4_speed` | 50 | 30 |
| `Novi 0.20 - TOOL @AC KX` | `slowdown_for_curled_perimeters` | 0 | 1 |
| `Novi 0.28 - TEST @AC KX` | `slowdown_for_curled_perimeters` | 0 | 1 |
| `PLA Generic@KX 0.4` | `overhang_fan_threshold` | 50% | 25% |
| `PLA BBL Lite@KX 0.4` | `overhang_fan_threshold` | 50% | 25% |

Hai preset FIGURE không cần đụng: preset gốc High Quality của hãng vốn đã đặt
overhang 2/4 và 3/4 là 30/10 thay vì 50/30. `overhang_2_4_speed` của TEST giữ
50 — chậm mọi overhang đi ngược mục đích của profile đó.

**Tơ còn sót sau khi sửa retraction.** `retraction_minimum_travel = 2` nghĩa là
mọi quãng di chuyển dưới 2 mm không retract chút nào; vật nhiều chi tiết nhỏ thì
đó là rất nhiều đoạn kéo tơ. Hạ về 1 ở machine preset.

**Thiếu nhựa first layer theo đốm** — không sửa bằng preset. Thiếu theo đốm là
khoảng cách nozzle–bàn không đều, thiếu đều khắp mới là flow. Cần level bàn.
Đề xuất hạ `initial_layer_speed` 50 → 30 để lại trong `PENDING_APPLY.md` như
biện pháp giảm nhẹ, chỉ dùng nếu level xong vẫn còn.

### Sửa hồi quy retraction, thêm `Novi 0.16 - FIGURE @AC KX`

**Hồi quy do lần gộp filament trước đó.** `filament_retraction_length = "nil"`
không phải rác — nó nghĩa là "đừng đè lên machine preset". Lúc gộp hai preset
BBL thành một, key đó bị xoá vì tưởng là nhiễu, nên filament rơi về giá trị
`0.8` của vendor và **đè lên** `retraction_length = 1` đã tinh chỉnh ở machine.
Retraction thực tế tụt 1 → 0.8 mm, và phần tinh chỉnh machine thành vô hiệu.
Cùng lỗi ở `PLA Generic@KX 0.4`, mất thêm `filament_wipe_distance`.

Khôi phục cả ba key. Backup `user_backup-tune-set-20260823-171013`.

Sửa cả gốc rễ trong `tools/acslicer_tune.py`: rule cũ báo `nil` là "harmless but
noisy" — chính nó dẫn tới quyết định xoá. Thay bằng rule ngược lại, cảnh báo khi
một key `filament_*` **đang đè** lên machine preset, kèm đề xuất đặt `nil`.

**Preset mới `Novi 0.16 - FIGURE @AC KX`** — kế thừa `0.16mm High Quality
@Kobra X`, cho model lớn mà 0.12 mất quá nhiều thời gian. Bớt được một override
so với bản 0.12 vì cha đã dùng `gyroid` sẵn, nhưng phải đè `ironing_speed`
30 → 20 và `ironing_spacing` 0.15 → 0.1. Backup
`user_backup-tune-new-016-figure-20260823-222044`. Audit: 0 lỗi, 7 preset.

### Bật thu hồi nhựa purge cho TOOL và TEST

Backup `user_backup-tune-set-20260823-033101`. Audit sau khi ghi: 0 lỗi.

| Preset | `flush_into_infill` | `flush_into_objects` |
|---|---|---|
| `Novi 0.20 - TOOL @AC KX` | 0 → **1** | 0 → **1** |
| `Novi 0.28 - TEST @AC KX` | 0 → **1** | 0 → **1** |
| `Novi 0.12 - FIGURE @AC KX` | giữ 0 | giữ 0 |

Ma trận flush là 3634 mm³ cho 12 lần đổi màu và trước đó **toàn bộ thành rác** —
chỉ `flush_into_support` bật, mà support không phải bản in nào cũng có. Giờ TOOL
và TEST nhét nhựa thải vào infill và phần đặc của vật thể, thu hồi được phần lớn.

FIGURE cố ý giữ 0: nhựa thải trong thân vật thể có thể lộ ra bề mặt hoặc lẫn màu
sang lớp kế tiếp, mà đó đúng là thứ profile này tồn tại để tránh.

### Cấu hình 4 màu và preset đang chạy

Slice thử một model 4 màu để slicer sinh `flush_volumes_matrix`. Ma trận 4×4 nó
tự tính hợp lý, không phải chỉnh: đổi **sang White** đắt nhất (785 mm³), đổi
**từ White** rẻ nhất (142, đúng sàn) — màu đậm phủ lên trắng nhanh, ngược lại
thì không. Tổng 3634 mm³ cho 12 lần đổi màu.

🔵 Ước tính ban đầu 450–650 mm³ cho cặp tối↔sáng là thấp hơn thực tế. Slicer
tính theo khoảng cách màu và rộng tay hơn.

Đọc `.conf` phát hiện hai preset đã tạo nhưng chưa được chọn — đã sửa trong UI:

| | Trước | Sau |
|---|---|---|
| Machine | stock `Anycubic Kobra X 0.4 nozzle` | `- high quality` *(retraction đã tinh chỉnh mới có hiệu lực)* |
| Slot 2 | stock `Anycubic PLA @Kobra X` | `PLA Generic@KX 0.4` |

Khoá quyết định machine nào đang chạy là `presets.machine` trong `.conf`, không
phải danh sách `anycubic_presets` — danh sách đó giữ một entry cho **mỗi** machine
preset, chỉ là bộ nhớ "lần cuối dùng máy này thì chọn gì".

### Đóng ba mục TODO — không làm, có lý do

**Đối chiếu trần động học slicer ↔ Klipper** — bỏ. Slicer khai 450 mm/s,
10000 mm/s² accel, jerk 20 và ghi `SET_VELOCITY_LIMIT` vào gcode
(`emit_machine_limits_to_gcode = 1`). Klipper tự hạ `VELOCITY`/`ACCEL` về mức
trong `printer.cfg` nên khai cao chỉ làm ước tính thời gian sai. Tham số duy
nhất Klipper không hạ là `square_corner_velocity = 20`, gấp 4 lần mặc định của
nó — triệu chứng nếu quá cao là ringing quanh góc, và Viet xác nhận không thấy.
Moonraker cũng không tới được vì máy in khác mạng WiFi. Phân tích giữ ở
`docs/device.md`; nêu lại chỉ khi thấy ringing.

**Cập nhật `profiles/filament.md` khi đổi cuộn** — chuyển thành quy ước, không
phải task. Không có trạng thái "xong" nên không thuộc `TODO.md`. Đã nằm trong
bảng phân vai ở `docs/working-rules.md` mục 1.

**Bổ sung công cụ** — bỏ cả ba mục từng liệt kê:

| Từng đề xuất | Vì sao bỏ |
|---|---|
| `--unset` xoá key | key rác đã biến mất khi preset được viết lại |
| `--diff` so với cha | preset giờ mỏng và do script sinh, không còn override thừa |
| ghi `.conf` an toàn kèm MD5 | flush matrix sửa được trong UI slicer, không cần chạm `.conf` |
| rule multi-material | chờ A2 mới biết có cần không; slicer tự tính flush từ màu |

### Tái cấu trúc toàn bộ preset

Chạy qua `tools/restructure_2026_08.py`, backup
`user_backup-tune-restructure-20260823-024205`. Audit sau khi chạy: **0 lỗi**.

Từ **12 preset xuống 6**.

**Xoá 10**

| | Vì sao |
|---|---|
| `Anycubic PLA @Anycubic Kobra S1 0.4 nozzle - Copy` | không có máy Kobra S1 |
| `BBL PLA Lite`, `BBL PLA Lite @Anycubic Kobra X 0.4 nozzle` | gộp làm một |
| 7 process preset cũ | thay bằng bộ theo mục đích |

**Machine** — `Anycubic Kobra X 0.4 nozzle - high quality`

| Key | Cũ | Mới | Vì sao |
|---|---|---|---|
| `retract_restart_extra` | `-0.05` | `0` | giá trị âm đùn thiếu sau mỗi lần retract |
| `z_hop` | `0.16` | `0.4` | 0.16 nhỏ hơn layer dày nhất (0.28) nên nozzle vẫn va |

**Filament** — còn 2

- `PLA BBL Lite@KX 0.4` — gộp từ hai preset cũ, mỗi bản chỉ giữ một nửa thông
  tin. Nhiệt bàn hai bản mâu thuẫn nhau (50/45 và 45/50), chốt phẳng 50/50.
- `PLA Generic@KX 0.4` — `filament_max_volumetric_speed` 15 → 13. Số 15 chép
  sang từ BBL chứ chưa đo.

**Process** — 3 preset mới, `Novi {layer} - {category} @AC KX`

| Preset | Kế thừa | Đè lên |
|---|---|---|
| `Novi 0.12 - FIGURE @AC KX` | `0.12mm High Quality @Kobra X` | outer 50, gyroid 12%, ironing top, scarf seam, thin wall, curled perimeter |
| `Novi 0.20 - TOOL @AC KX` | `0.20mm Standard @Kobra X` | wall 4, inner-outer-inner, gyroid 25%, bottom 4, outer 120 |
| `Novi 0.28 - TEST @AC KX` | `0.28mm Standard @Kobra X` | lightning 5%, top/bottom 2, no brim |

Mỗi cái kế thừa preset hãng **đúng layer height của nó** nên chỉ cần 5–7 key
override. Tốc độ **không** bị hạ cho khớp trần flow — đó là việc của filament
preset, slicer tự làm lúc slice.

### Lịch sử preset tự động

Preset trước đây không có lịch sử ngoài đống thư mục `user_backup-*` — ghi lại
trạng thái nhưng không ghi ý định, và không diff được.

- `acslicer_tune.py --export` mirror kho preset sống vào `presets/`, ghi lại JSON
  với key đã sắp xếp để diff có nghĩa. Bỏ tầng thư mục userid, bỏ `filament/base/`.
- `--check-drift` báo khi mirror lệch kho sống.
- `tools/preset_autocommit.py` chạy từ Scheduled Task mỗi 10 phút, commit **chỉ khi
  slicer đã đóng** — nó ghi đè preset từ RAM lúc thoát, nên snapshot chụp lúc nó
  còn mở có thể dính giá trị sắp bị ghi đè.
- Script từ chối nếu có gì staged ngoài `presets/`, kiểm tra lại sau `git add`,
  và quét nội dung giống credential trước khi push — remote là public và không
  ai ngồi xem.
- `CLAUDE.md` luật 7 thêm ngoại lệ hẹp cho riêng `presets/`.
- Hook `SessionStart` báo commit chưa push và log autocommit gần nhất.
- Sửa cửa sổ cmd nhấp nháy bằng `CREATE_NO_WINDOW` — `pythonw.exe` không có
  console nên mỗi subprocess tự bật cửa sổ mới.

### Viết lại tài liệu

- `docs/preset-model.md` viết lại. Bản cũ mở đầu bằng cây thư mục và danh sách
  bẫy khi người đọc chưa biết preset là gì. Bản mới đi từ ba tầng → kế thừa (có
  ví dụ gộp cha/con bằng số thật) → tầng nào sở hữu gì → bố cục → bẫy.
- Bỏ từ "kẹp" ở mọi nơi — bản dịch tự chế của "clamp", không mang nghĩa gì.
- `README.md` thêm mục "How it works", giải thích cơ chế thay vì liệt kê tính năng.
- `docs/capabilities.md` 62 → 44 dòng, đưa phần giới hạn lên đầu.
- `docs/device.md` mở đầu bằng cảnh báo nguồn số liệu, thu hẹp cảnh báo động học
  còn hai con số thật sự đáng quan tâm.
- Tách `docs/` (ổn định) khỏi `profiles/` (trạng thái) theo **tần suất đổi**.

---

## 2026-08-22

### Sửa 8 giá trị mâu thuẫn

Audit từ **3 lỗi xuống 0**.

| Preset | Thay đổi |
|---|---|
| `BBL PLA Lite` | `nozzle_temperature_range_high` 210 → 215 |
| `BBL PLA Lite`, `BBL PLA Lite @Kobra X` | nhiệt bàn lớp đầu 45 → 50 |
| `Kobra X - high quality` | `retract_restart_extra` −0.05 → 0, `z_hop` 0.1 → 0.4 |
| `0.20mm - Standard Novi` | `support_top_z_distance` 0.16 → 0.2 |

Nâng trần flow: `Anycubic PLA - Copy` → 18, ba preset BBL PLA Lite → 15.

### Rollback 25 lần hạ tốc độ sai tầng

Đã hạ tốc độ trong process preset cho khớp trần flow của BBL PLA Lite, rồi nhận
ra đó là lỗi nhầm tầng: trần flow thuộc filament preset, slicer đã tự enforce
lúc slice, và cái pin đó sống lâu hơn cuộn nhựa. Khôi phục từ backup.

Ngoài ra hai lỗi trong chính công cụ: clamp dùng trần 13 chứ không phải trần
mới, và phần lớn thao tác ghi thêm key vốn đang kế thừa.

### Công cụ và hạ tầng

- `tools/acslicer_tune.py` — giải chuỗi kế thừa, đối chiếu giới hạn firmware và
  vật lý đùn nhựa, ghi sửa kèm backup. Xử lý 3 trong 4 cái bẫy của kho preset.
- `.gitignore` chặn `*.conf` (token cloud), backup, log.
- Allowlist quyền cho lệnh chỉ đọc; `--fix`, `--set`, `git` thì hỏi.
- 4 slash command: `/audit` `/apply` `/preset` `/newfilament`.
- Hook `PreToolUse` chặn ghi vào `system\`, hook `SessionStart` báo trạng thái.
- `CLAUDE.md` tự nạp mỗi phiên.
