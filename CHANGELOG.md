# Nhật ký

Mọi việc đã xong, mới nhất lên trên. `TODO.md` chỉ giữ việc còn treo,
`PENDING_APPLY.md` chỉ giữ thao tác chờ duyệt.

Diff từng dòng preset nằm ở `git log -- presets/`.

---

## 2026-08-25

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
