# Nhật ký

Mọi việc đã xong, mới nhất lên trên. `TODO.md` chỉ giữ việc còn treo,
`PENDING_APPLY.md` chỉ giữ thao tác chờ duyệt.

Diff từng dòng preset nằm ở `git log -- presets/`.

---

## 2026-08-24

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
