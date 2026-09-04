# Nhật ký

Mọi việc đã xong, mới nhất lên trên. `TODO.md` chỉ giữ việc còn treo,
`PENDING_APPLY.md` chỉ giữ thao tác chờ duyệt.

Diff từng dòng preset nằm ở `git log -- presets/`.

---

## 2026-09-03

### Viet dựng lại toàn bộ preset trên slicer 2.0.0.2 — lấy máy làm chuẩn

Viet chỉnh tay trong UI, không qua `tools/acslicer_tune.py`. Theo
`docs/working-rules.md` mục 6: **slicer thắng**. Đã chạy `--export`, đồng bộ
`presets/` và viết lại `profiles/` theo đúng những gì đọc từ đĩa. ❌ Không khôi
phục gì từ git hay `user_backup-*`.

🟢 `--check-drift` báo 30 file lệch trước khi export. `--audit` sau export:
**0 lỗi, 1 warning** (top shell 2×0.28 = 0.56 mm trên `0.28 TEST`), 18 mục
flow-capped.

**Đổi tên toàn bộ** *(theo mục 10 — chỉ thêm dòng ghi nhận, không sửa mục cũ)*:

| Cũ | Mới |
|---|---|
| `Anycubic Kobra X 0.4 nozzle - high quality` | `Kobra X 0.4 - Single Color` |
| `Anycubic Kobra X 0.4 nozzle - high quality - TEST` | `Kobra X 0.4 - MultiColor` |
| `Novi 0.12 - FIGURE @AC KX` | `0.12 Figure @AC KX` |
| `Novi 0.16 - FIGURE @AC KX` | `0.16 FIGURE @AC KX` |
| `Novi 0.20 - FIGURE @AC KX` | `0.20 Figure @AC KX` |
| `Novi 0.20 - TOOL @AC KX` | `0.20 TOOL @AC KX` |
| `Novi 0.28 - TEST @AC KX` | `0.28 TEST @AC KX` |

🔵 Hai machine preset không còn tách theo `z_hop` (0.2 / 0.4) mà tách theo **số
màu**: Single Color không đè khoá nào, MultiColor đè năm khoá retraction.
`Novi 0.20 - FIGURE @AC KX -dinosaur` (preset project riêng, 02/09) đã bị xoá —
còn 9 preset user.

**Cấu trúc tốt lên**:

- 🟢 `0.20 Figure` kế thừa đúng `0.20mm High Quality`, hết vá `layer_height` tay
  — **B1 đóng lại**
- 🟢 `filament\base\` giờ rỗng, không còn file trùng tên (bẫy 2)
- 🟢 Preset user mỏng hẳn: filament 5–7 khoá, process 6–15, machine 0–5

**Override đã bỏ, cần theo dõi** — chi tiết trong `profiles/`:

| Tầng | Bỏ | Hệ quả |
|---|---|---|
| filament | `filament_flow_ratio = 1` (P14/P15) | 🔴 về 0.96, đùn ít hơn 4% — B2 |
| filament | `filament_density`, `overhang_fan_threshold`, `slow_down_*` | 🔵 về giá trị hãng |
| filament | nhiệt HS 205 → 203 (BBL) / **200** (Generic) | 🟡 Generic quay lại mức P28 đã bỏ |
| machine | `z_hop = 0.2`, `z_hop_types = Normal Lift` (P10) | 🟢 hết cảnh báo z_hop < layer 0.28 |
| machine | `purge_in_prime_tower = 1` (P30) | 🟡 purge có thể bị bỏ qua khi in nhiều màu không support |
| process | `top_surface_speed = 80` (P21) | 🟡 về 150, mức từng bị chê mặt trên xấu |
| process | `outer_wall_speed`, `initial_layer_speed` (0.12/0.16), `detect_thin_wall`, `small_perimeter_threshold`, `skirt_loops` | 🔵 về giá trị hãng |
| process | TOOL: `wall_loops` 4→2, infill 25%→15%, `wall_sequence`, `flush_into_*` | 🔴 độ bền giảm rõ — B4 |
| process | TEST: `brim_type = no_brim` | 🔵 về `auto_brim` |

🟢 Giữ nguyên: `filament_retraction_length = nil` (để machine quyết),
`textured_plate_temp` 50/55, `pressure_advance = 0.036`, flow cap 13,
`seam_gap 15%` + `wipe_*` + scarf joint trên FIGURE, `flush_into_*` trên TEST.

🔴 **`.conf` bản 2.0.0.2 không còn lưu `filament_colors` và bảng gán
slot→preset.** Mục `presets` chỉ còn `filaments` (mảng cờ) và `machine`. Từ nay
bảng slot trong `profiles/filament.md` không kiểm chứng lại được bằng config —
xác nhận cuối là 29/08 trên bản 1.4.x. Ma trận flush cũng chỉ đọc lại được bằng
cách slice một mẫu 4 màu rồi đọc gcode.

📝 Sinh ra B2, B3, B4 trong `TODO.md` — hỏi cho rõ ý định, không phải đề xuất
khôi phục.

📘 Báo cáo so sánh ảnh hưởng trước/sau đầy đủ (định lượng từng khoá, xếp hạng
rủi ro, bảng hoàn tác): `IMPACT-2026-09-03.md`.

## 2026-09-02 (2)

### Slicer đã update lên v2.0.0.1 — soát thư viện hãng, không phát sinh lỗi

Đọc từ `.conf`: `"version": "2.0.0.1"`. Không có bộ nhớ giữa phiên nên không tự
biết được — Viet báo mới hay.

🔵 **Tính năng chính bản 2.0** (theo trang chủ Anycubic, không tìm được changelog
chi tiết cấp preset công khai): giao diện Workspace mới, quản lý file cloud +
local, Print History (tìm/lọc/in lại), thêm điều khiển máy in (AI Detection,
Calibration, Print Assistance, điều khiển đùn/nozzle/bàn nhiệt). Khuyến nghị
cập nhật **firmware máy in dòng KX lên V2.0.0** trước khi dùng bản slicer này —
đáng chú ý vì macro `G9111` (mồi nhựa/home/cân bàn) nằm trong firmware, không
phải trong preset.

🟢 **Preset thứ 10 xuất hiện: `Novi 0.20 - FIGURE @AC KX -dinosaur`.** Viet xác
nhận: preset riêng cho một project cụ thể, không cần theo dõi trong
`profiles/process.md`.

🟢 **Soát thư viện hãng (630 file / 629 index được, trước là 643) — chuỗi kế
thừa của cả 10 preset user vẫn resolve đúng, `--audit` 0 lỗi.** Đối chiếu giá
trị các preset cha đang dùng với số đã ghi trong `profiles/`:

| Preset cha | Key | Đã ghi trước | Hiện tại | |
|---|---|---|---|---|
| `Anycubic Kobra X 0.4 nozzle` (machine) | retraction/z_hop/wipe/nozzle_volume/... | — | **không đổi** | 🟢 khớp toàn bộ bảng "Hãng" trong `profiles/printer.md` |
| `Anycubic PLA @Anycubic Kobra X 0.4 nozzle` (filament) | `nozzle_temperature_HS`, `filament_flow_ratio`, `filament_retraction_length`, `filament_max_volumetric_speed` | 220 / 0.96 / 0.8 / 13 | **không đổi** | 🟢 |
| `0.16mm High Quality @Anycubic Kobra X 0.4 nozzle` (process) | `sparse_infill_density` | **12%** *(B2, 30/08)* | **15%** | 🔴 hãng đã đổi mặc định |

🔴 **Một drift thật:** `0.16mm High Quality` — cha thật của `Novi 0.20 -
FIGURE @AC KX` (do lỗi kế thừa sai đã biết, B1) — đổi `sparse_infill_density`
gốc từ 12% lên 15%. Override tay 15% đặt ngày 30/08 (B2, để khớp 0.16 lúc đó
cha còn 12%) giờ **trùng giá trị cha mới** — không sai, nhưng có thể bị slicer
tự bỏ khỏi file khi mở lại (không phải bug, xem hành vi tương tự ở
`profiles/process.md` mục FIGURE). Không cần sửa gì — hiệu lực vẫn là 15% dù
đọc từ override hay từ cha.

📝 B1 (kế thừa sai cha của `Novi 0.20 - FIGURE`) vẫn treo, không nằm trong
`TODO.md` hiện tại — nêu lại ở đây vì bản update này chạm đúng preset cha bị
ảnh hưởng.

## 2026-09-02

### P31 🟢 áp — `machine_end_gcode` trả về gốc hãng, bỏ P16 + P25-v2

Viet báo kẹt nhựa thường xuyên khi in slot 4, nghi `machine_end_gcode` là thủ
phạm, yêu cầu bỏ hết. **Đã cảnh báo trước khi ghi:** đoạn này chỉ chạy sau khi
in xong, không chạy giữa lúc đang in — khó giải thích được kẹt nhựa xảy ra
trong lúc in. Viet vẫn chọn bỏ, ghi lại theo yêu cầu.

Backup `user_backup-tune-set-20260902-085908`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `Anycubic Kobra X 0.4 nozzle - high quality` | `machine_end_gcode` | P16 + P25-v2 (retract 6mm + wipe + z-hop trước khi tắt nhiệt) | **gốc hãng** — thẳng `M400` → tắt bàn/nhiệt/fan/motor, không retract |
| `Anycubic Kobra X 0.4 nozzle - high quality - TEST` | `machine_end_gcode` | như trên | như trên |

Đọc lại xác nhận cả hai. `--audit`: 0 lỗi, 2 warning cũ không đổi (`z_hop` FIGURE/TOOL,
top shell TEST 0.28) — không phát sinh finding mới từ thay đổi này.

🔴 **Rủi ro chưa kiểm chứng, cần theo dõi:** bỏ retract cuối bản in nghĩa là
nozzle đầy nhựa chịu áp nguội dần giữa hai lần in trở lại — đúng vấn đề P16
từng sửa (oozing/đọng cục ở đầu phun, xem C2 trong lịch sử 29/08). Có thể sinh
ra một kiểu nghẹt khác cho lần in kế tiếp, chứ không chắc hết kẹt nhựa đang gặp.

🔵 Nghi phạm hợp lý hơn cho triệu chứng gốc (load tay ra nhựa, in thì không) vẫn
chưa kiểm: nghiến nhựa ở bánh răng đùn (grinding) hoặc nghẹt một phần — xem
mục dưới đây.

### Kẹt nhựa thường xuyên slot 4 — chẩn đoán, chưa xử lý

Viet báo "thường xuyên bị tắt nhựa khi in slot 4". Đã loại được nghẹt cứng đầu
nozzle kiểu 30/08: load filament từ màn hình máy vẫn ra nhựa bình thường, chỉ
lúc in mới không ra — khác triệu chứng 30/08 (lúc đó load tay cũng fail).

🔵 slot 2 và slot 4 dùng chung preset `PLA Generic@KX 0.4`, slot 2 không báo lỗi
→ preset không phải nghi phạm chính.

Nghi phạm còn treo, cần Viet kiểm tay (Claude không xem/đo phần cứng được):

1. **Nghiến nhựa (grinding) tại bánh răng đùn** — gear cắn lặp lại đúng 1 điểm
   lúc rút/đẩy đổi màu (buồng chung 79mm³) → mòn rãnh → trượt. Kiểm: vết mòn/bột
   nhựa quanh bánh răng, tiếng click lặp lúc lỗi.
2. **Nghẹt một phần** — đủ thông cho lưu lượng thấp (load tay), không đủ cho
   lưu lượng cao (in).
3. **Kẹt/rối cuộn slot 4 trên trục hoặc ống dẫn** — load tay đẩy đoạn ngắn chưa
   chạm điểm kẹt, in kéo dài quãng đường mới chạm.

📝 Chuyển thành A10 trong `TODO.md`, chờ Viet kiểm tay và báo lại.

## 2026-08-30

### B2 áp — đồng bộ `prime_tower_width` và `sparse_infill` theo 0.16

Viet chốt: cả ba bản FIGURE theo 0.16. Backup
`user_backup-tune-set-20260830-202701`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `Novi 0.12 - FIGURE` | `prime_tower_width` | 35 *(kế thừa)* | **10** |
| `Novi 0.12 - FIGURE` | `sparse_infill_density` | 18% | **15%** |
| `Novi 0.20 - FIGURE` | `prime_tower_width` | 30 *(kế thừa)* | **10** |
| `Novi 0.20 - FIGURE` | `sparse_infill_density` | 12% | **15%** |
| `Novi 0.20 - FIGURE` | `sparse_infill_pattern` | grid | **gyroid** |

Đọc lại xác nhận cả năm. Cập nhật `profiles/process.md`.

### B3 áp — tạo machine preset thứ hai riêng cho TEST 0.28

Backup `user_backup-tune-b3-create-test-machine-20260830-202720`. Tạo mới
(không qua `--set` vì đó là preset chưa tồn tại):

```
Anycubic Kobra X 0.4 nozzle - high quality - TEST
```

Nhân bản y hệt preset chính (`retraction_length=1.6`, `purge_in_prime_tower=1`,
`machine_end_gcode` P16+P25-v2...), chỉ đổi `z_hop = 0.4` thay vì 0.2.

Lý do: `z_hop` không tồn tại ở tầng process trong schema slicer này (đã kiểm
`fdm_process_common.json` và toàn bộ preset process của hãng — không có ở
đâu). Không override riêng cho `Novi 0.28 - TEST @AC KX` được, nên chỉ còn cách
tách hẳn một machine preset khác.

`tools/acslicer_tune.py --list` xác nhận preset mới được index đúng.
`--audit`: preset mới không bị cảnh báo z_hop (0.4 ≥ 0.28), preset chính vẫn
cảnh báo như cũ (0.2 < 0.28, chỉ dùng cho FIGURE/TOOL). Mirror push `1cf4e19`.

🔴 **Hai preset không tự đồng bộ với nhau.** Sửa retraction/purge/end-gcode ở
preset chính sau này phải nhớ áp lại cho bản TEST — ghi thành quy tắc trong
`profiles/printer.md`.

🟡 Viet phải tự chọn đúng Printer preset trong slicer khi in bằng
`Novi 0.28 - TEST @AC KX` — không có liên kết tự động giữa machine và process
preset.


### FIGURE 0.16 làm chuẩn — soát và đồng bộ 0.12, 0.20

Viet yêu cầu. Đọc giá trị **hiệu dụng** (qua chuỗi kế thừa, không chỉ override
thô) của cả ba preset để so sánh công bằng.

**0.12 đã khớp 0.16** ở mọi giá trị hiệu dụng — không cần sửa.

**0.20 lệch thật**, chưa từng đồng bộ từ lúc Viet tạo 25/08. Backup
`user_backup-tune-set-20260830-194406`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `Novi 0.20 - FIGURE` | `initial_layer_speed` | 50 *(kế thừa)* | **30** |
| `Novi 0.20 - FIGURE` | `initial_layer_infill_speed` | 200 | **50** |
| `Novi 0.20 - FIGURE` | `reduce_crossing_wall` | 0 *(kế thừa)* | **1** *(P19)* |
| `Novi 0.20 - FIGURE` | `max_travel_detour_distance` | 0 *(kế thừa)* | **40** *(P19)* |
| `Novi 0.20 - FIGURE` | `top_surface_speed` | 150 *(kế thừa)* | **80** *(P21)* |

Đọc lại xác nhận cả năm. `--audit` không thêm lỗi. Mirror push `4c37666`.

🔴 `initial_layer_infill_speed = 200` đáng chú ý nhất — ngược hẳn logic "chậm
hơn để bám bàn" áp cho 0.12/0.16 từ 25/08. 0.20 đã chạy sai giá trị này hơn
5 ngày mà không ai để ý vì preset ít dùng.

🟡 **Còn hai khoá khác nhau, chưa tự sửa — chờ Viet quyết:**

| Key | 0.12 | 0.16 | 0.20 |
|---|---|---|---|
| `prime_tower_width` | 35 | **10** *(P22, Viet cố ý riêng 0.16)* | 30 |
| `sparse_infill_density`/`pattern` | 18%/gyroid | 15%/gyroid | 12%/grid |

Không tự đổi vì `prime_tower_width=10` được ghi rõ là lựa chọn riêng cho 0.16;
`sparse_infill` khác nhau ba bản có thể là chủ ý (mỗi lần tạo cho một model cụ
thể), không phải bug.

Đã cập nhật `profiles/process.md` mục FIGURE 0.20.

### Câu hỏi: override `z_hop` riêng cho `Novi 0.28 - TEST @AC KX`?

🔴 **Không được — sai tầng, không phải chưa muốn làm.** Kiểm toàn bộ
`fdm_process_common.json` (template gốc mọi process preset kế thừa) và cả cây
preset process của hãng: `z_hop` **không tồn tại** ở tầng process trong schema
của slicer này, chỉ có ở machine. Ghi `z_hop` vào JSON của một process preset
thì slicer không đọc được key đó ở ngữ cảnh in — vô nghĩa.

Máy chỉ có một machine preset active tại một thời điểm, không tự đổi theo
process preset đang chọn. Muốn TEST dùng z_hop=0.4 trong khi FIGURE dùng 0.2,
cách duy nhất là tạo **machine preset thứ hai** riêng cho TEST và tự tay chuyển
Printer preset khi in TEST — phá vỡ quy ước "chỉ một machine preset" đang giữ.
Chưa làm, chờ Viet xác nhận có muốn đánh đổi đó không.


### `z_hop` hạ xuống 0.2 — cùng loại rủi ro đã gặp trước

Backup `user_backup-tune-set-20260830-193915`.

| Key | Cũ | Mới |
|---|---|---|
| machine `z_hop` | 0.4 | **0.2** |

Đọc lại xác nhận. Mirror push `fa2a235`.

🟡 **`--audit` tự báo đúng cảnh báo cũ:** `z_hop 0.2 < max layer height 0.28 -
hop lands inside the layer it should clear, nozzle still collides`. An toàn với
mọi process FIGURE đang dùng (0.12/0.16/0.20), nhưng `Novi 0.28 - TEST @AC KX`
thì cú nhấc không đủ vượt lớp. Đã báo trước khi ghi, Viet chọn vẫn áp.

Đã cập nhật `profiles/printer.md` — nhân tiện đồng bộ lại cả bảng key/value
(nhiều dòng đã lệch thực tế nhiều ngày: `retraction_length` còn ghi 1.2 trong
khi đĩa đã là 1.6, `purge_in_prime_tower` còn ghi 0/pending trong khi đã bật).


### B1 áp — bật lại scarf cho FIGURE

Backup `user_backup-tune-set-20260830-193738`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `Novi 0.12 - FIGURE @AC KX` | `seam_slope_type` | none | **external** |
| `Novi 0.16 - FIGURE @AC KX` | `seam_slope_type` | none | **external** |

Ba khoá chết (`seam_slope_conditional=0`, `seam_slope_min_length=5`,
`scarf_joint_flow_ratio=0.95`) đã sẵn trên đĩa từ 25/08, không cần ghi lại —
chỉ cần bật `seam_slope_type` là sống lại nguyên vẹn. Đọc lại xác nhận cả hai.
`--audit` 0 lỗi. Mirror push `00dd308`.

### A2, A8 xoá khỏi TODO

Viet chốt: không cần theo dõi tiếp cả hai.

- **A2** (đo PA thật) — cấu hình hiện tại đã cho bản in đẹp bằng PA kế thừa
  (0.036), không cần đo thêm
- **A8** (nhựa thừa đầu bản in, macro `G9111`) — giới hạn phần cứng đã ghi
  thường trực ở `docs/capabilities.md` mục 1, không cần giữ trong TODO nữa

Kiến thức nền tảng vẫn còn nguyên trong `docs/capabilities.md` và
`CHANGELOG.md` — chỉ bỏ khỏi danh sách việc treo.


### Nozzle sạch, bản in đẹp — đóng chuỗi tơ/mặt trên/nghẹt kéo dài hai ngày

Viet xác nhận bản in 1 màu sau cold pull: **đẹp**. Đóng A10 (nozzle đã sạch) và
C9 (tơ + mặt trên nghiệm thu xong) cùng lúc.

**Cấu hình đang chạy tốt, chốt lại làm mốc:**

| Preset | Key | Giá trị |
|---|---|---|
| machine | `retraction_length` | 1.6 |
| machine | `retraction_minimum_travel` | 0.5 |
| machine | `retraction_speed` / `retract_before_wipe` | 45 / 100% |
| machine | `z_hop_types` | Normal Lift |
| machine | `purge_in_prime_tower` | 1 |
| machine | `machine_end_gcode` | P16 + P25-v2 (retract đủ rồi mới wipe) |
| 2× filament | `pressure_advance` | 0.036 *(kế thừa — chưa đo lại, nhưng đang chạy tốt)* |
| 2× filament | `textured_plate_temp` / `_initial_layer` | 50 / 55 |
| 3× FIGURE | `top_surface_line_width` | 0.42 *(mặc định hãng)* |
| 2× FIGURE | `brim_type` / `wall_loops` / `ironing_type` | mặc định hãng (auto_brim / 2 / no ironing) |

🔵 **Không rõ nghẹt đã hết nhờ cold pull, hay tơ/mặt trên hết nhờ trả PA và line
width về mặc định hãng, hay cả hai.** Không cố tách — kết quả tốt là đủ, không
cần quy công cho từng thay đổi ở đây.

📝 **A2 (đo PA thật) và B1 (bật lại scarf) chuyển sang không khẩn** — cấu hình
hiện tại đã cho kết quả tốt bằng `pressure_advance` kế thừa (0.036). Vẫn có thể
làm nếu Viet muốn tối ưu thêm, nhưng không còn là việc phải làm để hết lỗi.


### Nghẹt nozzle xác nhận qua triệu chứng vật lý — rồi Viet đảo cả PA lẫn line width

Chuỗi troubleshooting phần cứng: in slot 4 không ra nhựa → load slot 4 từ màn
hình cũng không ra → load slot 1 cũng không ra (loại bỏ nguyên nhân riêng slot
4, chỉ về điểm chung) → unload được, load không được. **Rút được, đùn không
được = dấu hiệu kinh điển của nghẹt đầu nozzle**, không phải hỏng motor hay
hỏng heater. Đã hướng dẫn cold pull.

### PA trả về 0.036; `top_surface_line_width` trả về 0.42

Sau cold pull, Viet báo "thiếu nhựa rất nhiều", top surface rất mỏng — yêu
cầu hạ PA về 0.036 (từ 0.32 đo hôm nay) và tăng lại line width.

🟡 **Đã cảnh báo trước khi ghi:** thiếu nhựa lúc này nhiều khả năng vẫn là dư
âm của nghẹt chưa sạch hẳn, không hẳn do PA hay line width. Đổi preset ngay
lúc này che mất khả năng phân biệt hai nguyên nhân — Viet chọn đổi vẫn, ghi lại
theo yêu cầu.

Backup `user_backup-tune-set-20260830-171817`.

| Preset | Key | Cũ (đo hôm nay) | Mới |
|---|---|---|---|
| `PLA Generic@KX 0.4` | `pressure_advance` | 0.32 | **0.036** |
| `PLA Bambulab Lite@KX 0.4` | `pressure_advance` | 0.32 | **0.036** |
| 3× FIGURE | `top_surface_line_width` | 0.32 | **0.42** *(về đúng giá trị hãng)* |

Đọc lại xác nhận cả năm. `--audit`: cảnh báo "PA very high" biến mất — đúng vì
0.036 nằm trong dải bình thường. Mirror push `db6f0bf`.

🔴 **Hai giá trị đo được hôm nay (PA 0.32, line width 0.32→0.42 do quá mỏng)
coi như bị gác lại**, không phải kết luận sai — chỉ là chưa kiểm chứng được vì
lẫn với sự cố nghẹt nozzle. Cần in lại sau khi chắc chắn nozzle đã sạch mới
đánh giá lại được cả hai.


### A2 đóng — Pressure Advance đo được: 0.32 cho cả hai filament

Viet chạy PA Pattern trên máy thật (đã gỡ được rào cản `T`/bước mồi tự dựng
trước đó). Kết quả: **cả `PLA Generic@KX 0.4` và `PLA Bambulab Lite@KX 0.4`
cùng cho 0.32** — gấp ~9 lần giá trị kế thừa cũ (0.036).

🟢 **Hai cuộn ra cùng số là bằng chứng ủng hộ giả thuyết đã theo đuổi suốt hai
ngày:** buồng nóng chảy dùng chung cho cả 4 màu (`nozzle_volume = 79` mm³, gấp
4–5 lần hotend đơn màu thường thấy) là yếu tố quyết định PA ở đây, không phải
đặc tính riêng của từng loại nhựa.

Backup `user_backup-tune-set-20260830-145621`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `PLA Generic@KX 0.4` | `pressure_advance` | 0.036 *(kế thừa)* | **0.32** |
| `PLA Bambulab Lite@KX 0.4` | `pressure_advance` | 0.036 *(kế thừa)* | **0.32** |

Đọc lại xác nhận cả hai. Mirror push `a329194`.

🟡 `--audit` bật thêm 1 warning: `pressure_advance 0.32 very high for direct
drive PLA`. **Đúng như kỳ vọng, không phải lỗi** — ngưỡng cảnh báo giả định
hotend đơn màu thông thường, không tính tới buồng nóng chảy dùng chung của đầu
4-in-1. Ghi chú lại để lần audit sau không báo nhầm.

📝 Giờ có cơ sở để cân nhắc bật lại scarf (`seam_slope_type = external`) cho
FIGURE — tắt trước đây một phần vì "PA chưa hiệu chuẩn". Chưa áp, chờ Viet
quyết.


### Sau P31 (retraction 1.6) + nhiệt bàn 50/55 — top layer vẫn vừa thiếu vừa thừa nhựa

Viet báo: mặt trên vẫn có chỗ thiếu nhựa, có vài nốt dư nhựa — cả hai cùng tồn
tại trên cùng một bản in.

🔴 **Cả thiếu lẫn thừa cùng lúc là dấu hiệu PA sai kinh điển, không phải một
phía.** PA thấp gây phình ở điểm dừng/đổi hướng (thừa); PA cao (hoặc bù chưa
đủ ngay sau đó) gây hụt nhựa ngay sau (thiếu). Cùng một bản in thấy cả hai
nghĩa là đang dao động quanh sai số PA, không phải lệch một chiều do
`retraction_length` hay nhiệt bàn — cả hai đều đã chỉnh và không giải quyết
được gốc.

📝 Củng cố thêm cho A2 (đo Pressure Advance) là bước còn lại duy nhất, không
phải dò thêm số retraction hay nhiệt bàn.


### Chốt lại nhiệt bàn — lớp đầu 55, các lớp sau 50

Viet chỉnh lại con số vừa đặt: thay vì 55/55 đều, chốt **lớp đầu 55 / các lớp
sau 50**. Backup `user_backup-tune-set-20260830-133329`.

| Preset | Key | Cũ (55/55) | Mới |
|---|---|---|---|
| `PLA Generic@KX 0.4` | `textured_plate_temp` | 55 | **50** |
| `PLA Generic@KX 0.4` | `textured_plate_temp_initial_layer` | 55 | 55 *(không đổi)* |
| `PLA Bambulab Lite@KX 0.4` | `textured_plate_temp` | 55 | **50** |
| `PLA Bambulab Lite@KX 0.4` | `textured_plate_temp_initial_layer` | 55 | 55 *(không đổi)* |

Đọc lại xác nhận cả bốn. `--audit` 0 lỗi, 1 warning cũ. Mirror push `e3637b6`.

🔵 Lớp đầu giữ 55 (cao hơn các lớp sau) để ưu tiên bám bàn; các lớp sau hạ thêm
xuống 50 — tổng cộng thấp hơn giá trị hãng (60) 10°.


### Giảm nhiệt bàn 5° cho cả hai preset filament

Viet yêu cầu, đã hỏi rõ phạm vi trước khi ghi: áp cho **cả `PLA Generic@KX 0.4`
và `PLA Bambulab Lite@KX 0.4`**, giảm **cả lớp đầu lẫn các lớp sau**.

Backup `user_backup-tune-set-20260830-132917`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `PLA Generic@KX 0.4` | `textured_plate_temp` | 60 *(kế thừa)* | **55** |
| `PLA Generic@KX 0.4` | `textured_plate_temp_initial_layer` | 60 *(kế thừa)* | **55** |
| `PLA Bambulab Lite@KX 0.4` | `textured_plate_temp` | 60 *(kế thừa)* | **55** |
| `PLA Bambulab Lite@KX 0.4` | `textured_plate_temp_initial_layer` | 60 *(kế thừa)* | **55** |

Đọc lại xác nhận cả bốn. `--audit` 0 lỗi, 1 warning cũ. Mirror push `bf705fc`.

🔴 **Lịch sử đáng nhớ:** cặp khoá này từng bị revert xuống 45/50 ngày 24/08 và
gây bong bàn, phải khôi phục 60/60 ngày 25/08. Lần này khác — Viet chủ ý hạ 5°
(60→55), không phải revert ngoài ý muốn, và mức hạ nhỏ hơn nhiều so với cú rơi
15° từng gây lỗi. Vẫn đáng để ý dấu hiệu bong góc bàn ở bản in tới.


### Bản in sau P26/P30 — mặt trên dư nhựa dạng chấm rải rác; P31 dò lại `retraction_length`

Viet xác nhận: dư nhựa là **chấm nhỏ rải rác**, không phải dư đều cả mặt —
khớp giả thuyết mỗi lần rút/bù lại (deretract) sau retract 1.8 mm hơi thừa,
đúng chỗ dễ lộ khi `pressure_advance = 0.036` chưa hiệu chuẩn. Loại được giả
thuyết tháp mồi — gcode xác nhận `purge_in_prime_tower = 1` (P30) hoạt động
thật, purge chạy đúng tại toạ độ tháp (X~20-41), tách biệt vật lý khỏi model.

**P31 🟢 áp** — dò xuống mức giữa 1.2 (cũ) và 1.8 (P26), theo Viet chọn 1.6
thay vì 1.5 tôi đề xuất.

Backup `user_backup-tune-set-20260830-132622`.

| Key | Cũ | Mới |
|---|---|---|
| `retraction_length` | 1.8 | **1.6** |

Đọc lại xác nhận. `--audit` 0 lỗi. Mirror push `8917e6f`.


### P30 P26 🟢 áp

Backup `user_backup-tune-set-20260830-122730`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| machine | `purge_in_prime_tower` | 0 *(kế thừa)* | **1** |
| machine | `retraction_length` | 1.2 | **1.8** |

Đọc lại xác nhận cả hai. `--audit` 0 lỗi, 1 warning cũ (top shell TEST 0.28,
không liên quan). Mirror push `12ce145`.


### Bản in 30/08 11:42 — tơ giảm rất nhiều; mặt trên tìm ra bằng chứng trực tiếp

🟢 **Tơ giảm rất nhiều**, chỉ còn ở trụ nhỏ. Chưa áp P26 — cải thiện này đến từ
tổ hợp P6/P15/P19/P27/P29 cộng với việc Viet luôn chọn lại filament trước khi
in (A9), đảm bảo cả hai màu nhận đủ mọi fix thay vì một màu bị kẹt ở preset cũ.

🔴 **Mặt trên vẫn có mảng thiếu nhựa lộ bên trong, ~1 cm².** Hỏi hai câu để loại
giả thuyết: (1) mảng đó có nằm trên khoảng rỗng bên trong model không — Viet trả
lời **không**; (2) vị trí có lặp lại cùng chỗ mỗi lần in không — **không**. Loại
hẳn nguyên nhân model-geometry/bridging.

**Đọc gcode bản in tại điểm đổi màu (`T1`, dòng 29818) tìm ra bằng chứng trực
tiếp:**

```
;;; G1 E8 F300
;;; M400 P3643
;;; G1 E13 F1200
;;; G1 E9.16733 F300     (x8 — các đường zig-zag của tháp mồi)
...
;;; G1 E-2 F1200
```

**Toàn bộ chuỗi purge sau khi đổi màu bị comment (`;;;`) — không đùn một giọt
nhựa nào.** Không phải lỗi ghi file, slicer chủ động không phát các lệnh này.

🔴 **Cơ chế:** `purge_in_prime_tower = 0` (machine, kế thừa hãng, chưa từng
đụng — đã ghi nhận từ đầu là "an toàn, không đổi" nhưng chưa hiểu hết hệ quả).
FIGURE đặt `flush_into_objects = 0`, `flush_into_infill = 0`, chỉ còn
`flush_into_support = 1` — model này không dùng support
(`enable_support = 0`). Ba đích xả đều vô hiệu, và `purge_in_prime_tower = 0`
khoá luôn đường xả vào tháp mồi. Không còn chỗ nào nhận nhựa xả → slicer bỏ hẳn
bước purge.

Đầu in quay lại in model ngay sau đó với buồng nóng chảy **chưa được mồi lại**
— vài mm đầu tiên có thể thiếu nhựa. Vị trí lỗi phụ thuộc layer nào trùng lúc
đổi màu, nên ngẫu nhiên giữa các lần in — khớp đúng mô tả của Viet.

Ghi thành **P30** — bật `purge_in_prime_tower = 1`, cho tháp mồi một đích xả
đảm bảo bất kể model có support hay không. Theo mô tả Orca/BambuStudio, đây là
lưới an toàn dự phòng ("chỉ dùng khi các đường xả khác không đủ"), không đổi
hành vi TOOL/TEST vì chúng đã có đích xả hợp lệ (`flush_into_infill/objects = 1`).


### P29 áp — trả nhiệt PLA Generic về 205; P27 chỉnh sâu hơn — 0.32 thay vì 0.36

Backup `user_backup-tune-set-20260830-113318`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| `PLA Generic@KX 0.4` | `nozzle_temperature_HS` | 200 | **205** |
| 3× FIGURE | `top_surface_line_width` | 0.36 | **0.32** |

Đọc lại xác nhận cả bốn file. `--audit` 0 lỗi, 1 warning cũ (không liên quan).
Mirror push `5660841`.

🔵 0.32 mm = 80% đường kính nozzle — dưới mức 90% (0.36) áp hôm qua, Viet chủ
động giảm sâu hơn sau khi 0.36 "đỡ hơn nhưng vẫn xấu". Ở 0.16 mm × 80 mm/s ×
0.32 mm ≈ 4,1 mm³/s, còn xa trần flow 13.

### A9 đóng — Viet xác nhận luôn chọn lại filament trước khi in

Không còn nguy cơ project dùng preset đóng băng — Viet tự làm bước đồng bộ mỗi
lần, không cần tôi nhắc nữa.


### Phát hiện: project cũ dùng bản chụp preset đóng băng, không ăn theo thư viện

Bản in 30/08 10:45 (project "keychain_Daniel", 2 màu: white + matcha, cả hai
gán tên preset `PLA Generic@KX 0.4`). Đọc gcode phát hiện hai giá trị nhiệt
khác nhau cho cùng một tên preset:

```
filament_settings_id = ["PLA Generic@KX 0.4", "PLA Generic@KX 0.4(keychain_Daniel.3mf)"]
nozzle_temperature   = [200, 205]
```

Slot 1 (white) đọc đúng thư viện mới nhất (200, sau P28). Slot 2 (matcha) bị
đóng băng ở bản chụp cũ hơn (205, trước P28 nhưng sau P15 vì flow_ratio đã là 1.0) — tên có hậu tố `(keychain_Daniel.3mf)`.

🔴 **Cơ chế:** khi một object trong project được gán filament, slicer nhúng một
bản sao cấu hình tại thời điểm đó vào file project. Sửa preset trong thư viện
sau đó không tự lan sang những slot đã bị đóng băng kiểu này — im lặng, không
cảnh báo.

Ghi thành mục 7 mới trong `docs/preset-model.md` và A9 trong `TODO.md`. Cách
sửa: chọn lại filament cho object đó trong UI để ép đồng bộ lại.

🔴 Hệ quả: **P28 (hạ nhiệt PLA Generic xuống 200) chưa được kiểm đầy đủ** — chỉ
một trong hai slot của bản in 30/08 thực sự chạy ở 200 °C.

### Bản in 30/08 10:45 — tơ vẫn còn, mặt trên vẫn xấu

Viet đổi cuộn mới (in slot 4) và báo: tơ không đổi, mặt trên "xước, thiếu nhựa"
— đỡ hơn sau P27 (line width 0.36) nhưng vẫn xấu.

🔴 **Tơ không đổi dù đã hạ nhiệt (P28).** Nhiệt độ không phải nghi phạm chính
cho tơ trên máy này — củng cố thêm cho P26 (buồng nóng chảy 79 mm³ dùng chung,
retraction_length có thể chưa đủ) thay vì tiếp tục hạ nhiệt.

🔴 **Mặt trên xấu hơn có thể chính là do P28.** Nhiệt thấp hơn → nhựa chảy kém
hơn → các đường mặt trên hoà vào nhau kém hơn → đúng chiều với "thiếu nhựa".
Cùng lúc đó slot matcha lại KHÔNG chạy ở 200 (xem phát hiện trên) nên không thể
kết luận chắc — nhưng đủ nghi để đề xuất trả về, tách biến.

Ghi thành **P29**: trả `nozzle_temperature_HS` của `PLA Generic@KX 0.4` về 205,
đóng thử nghiệm P28.


### P27 P28 🟢 áp

Backup `user_backup-tune-set-20260830-100417`.

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| 3× FIGURE | `top_surface_line_width` | 0.42 *(kế thừa)* | **0.36** |
| `PLA Generic@KX 0.4` | `nozzle_temperature_HS` | 205 | **200** |

Đọc lại xác nhận cả bốn file. `--audit` 0 lỗi, 1 warning cũ (top shell TEST
0.28, không liên quan). Mirror push `f5de447`.

🔵 `nozzle_temperature_initial_layer_HS` giữ nguyên 210 — chỉ hạ nhiệt in, chưa
đụng lớp đầu.


### P25-v2 🟢 áp

Backup `user_backup-tune-p25v2-endgcode-order-20260830-095617`.

```
M400
G91
G1 E-6 F1800 ; P25v2 rut du truoc khi wipe, khop retract_before_wipe=100%
G1 X3 Y3 F3000 ; P25v2 wipe - keo giot nhua khoi mui in
G1 Z5 F600 ; P16 nhac dau in khoi mat in
G90
M140 S0 ; turn off heatbed
M104 S0 ; turn off temperature
M107;turn off fan
M84; disable motors
; disable stepper motors
```

Đọc lại xác nhận kiểu `str`, thứ tự đã đảo đúng: rút đủ 6 mm trước, wipe sau.
`--audit` 0 lỗi.


### Bản in 30/08 00:18 — P6 và P25 không đổi gì, kết quả âm thật

Kiểm gcode trước khi kết luận: file `0830-0018-Plate 1(01)_PLA_0.16_26m8s`
mang đúng cả hai — `retraction_minimum_travel = 0.5`, `machine_end_gcode` có
khối wipe của P25 nguyên vẹn. `print_settings_id = Novi 0.16 - FIGURE @AC KX`,
2 màu (matcha + white, `PLA Generic@KX 0.4`). Không phải trường hợp preset chưa
kịp áp — đây là kết quả âm thật.

🟢 Seam vẫn hết dư nhựa, không tái phát.

🔴 **P25 sai thứ tự — tự nhận lỗi.** Viết lại làm rút nửa chừng (`E-2`) rồi mới
wipe, rồi mới rút nốt (`E-4`) — ngược với `retract_before_wipe = 100%` mà mọi
retract khác trong bản in đang dùng (rút đủ trước, wipe sau). Trong lúc wipe,
đầu in mới rút 2/6 mm nên còn áp lực — nhiều khả năng chính là lý do giọt nhựa
vẫn ứ ra. Ghi lại **P25-v2**: rút đủ 6 mm trước, rồi mới wipe.

🔴 **Tơ không đổi sau P6** — ngưỡng travel hạ 1 → 0.5 mm không có tác dụng quan
sát được. Cùng với P15 (retract 45, wipe 100%, z-hop Normal Lift) và P19
(`reduce_crossing_wall`), gần như mọi khoá "chuẩn" cho stringing đã tinh chỉnh.
Còn một khoá chưa từng động tới: `retraction_length = 1.2` mm, tăng đúng một
lần từ 0.8 mm của hãng hôm 24/08.

Ghi lại **P26** — tăng lên 1.8 mm. Lý lẽ: `nozzle_volume = 79` mm³ là buồng
nóng chảy **dùng chung cho cả 4 màu** trên đầu 4-in-1, lớn hơn nhiều hotend
đơn màu điển hình (15–20 mm³). Cảnh báo "retract > 2.0 mm là kiểu bowden" trong
`docs/tool.md` được đặt ra cho hotend đơn màu — chưa chắc áp dụng đúng cho
buồng chung to gấp 4–5 lần. 1.8 mm vẫn dưới ngưỡng cảnh báo đó.

🟡 Bản in này lại dùng 2 màu — chưa cô lập được biến prime tower khỏi phép đo
tơ. Nếu P25-v2 + P26 vẫn không hết, nên in 1 màu trước khi tìm nghi phạm khác.


### P6 P25 🟢 áp

Backup `user_backup-tune-set-20260830-001342` (P6),
`user_backup-tune-p25-endgcode-wipe-20260830-001359` (P25).

| Preset | Key | Cũ | Mới |
|---|---|---|---|
| machine | `retraction_minimum_travel` | 1 | **0.5** |
| machine | `machine_end_gcode` | *(P16, không wipe)* | **+bước wipe 3 mm** |

```
M400
G91
G1 E-2 F1800 ; P25 rut mot phan truoc, giu it ap luc de wipe khong ray nhua
G1 X3 Y3 F3000 ; P25 wipe - keo giot nhua khoi mui in
G1 E-4 F1800 ; P25 rut not phan con lai
G1 Z5 F600 ; P16 nhac dau in khoi mat in
G90
M140 S0 ; turn off heatbed
M104 S0 ; turn off temperature
M107;turn off fan
M84; disable motors
; disable stepper motors
```

Đã đọc lại xác nhận cả hai. `--audit` 0 lỗi. `--check-drift` báo lệch trước khi
autocommit — đúng như kỳ vọng, vì vừa ghi xong chưa export; autocommit đã đồng
bộ ngay sau.


### Viet chỉnh tay trong slicer: brim auto, wall_loops 2, ironing tắt — cho cả 3 biến thể FIGURE

Không phải thao tác của tôi, ghi lại theo yêu cầu "lưu lại nó". Đọc từ đĩa sau
khi đóng slicer, áp dụng trên `Novi 0.12/0.16/0.20 - FIGURE @AC KX`:

| Key | Trước | Giờ |
|---|---|---|
| `brim_type` | `brim_ears` | `auto_brim` *(= cha, khoá biến mất)* |
| `wall_loops` | 4 | 2 *(= cha, khoá biến mất)* |
| `ironing_type` | `top` | `no ironing` *(= cha, khoá biến mất)* |

Cả ba khoá không còn override — trùng giá trị cha nên slicer tự bỏ, đúng cơ chế
đã thấy nhiều lần (`sparse_infill_density` từng bỏ y hệt vậy hồi 25/08).

🟡 Kéo theo hệ quả: `ironing_speed`, `ironing_spacing`, `ironing_inset` vẫn còn
là override trên đĩa (0.12, 0.16) nhưng giờ là **khoá chết** — vô nghĩa khi
`ironing_type = no ironing`. Giữ lại phòng khi bật ironing trở lại cho từng mẫu.

🟡 Phát hiện thêm, không nằm trong ba thay đổi trên: `Novi 0.16 - FIGURE` có
`top_shell_layers = 5`, chưa từng ghi trong tài liệu (từng ghi kế thừa 6/4).
Không rõ đổi khi nào — hỏi Viet, chưa tự sửa.

Đã cập nhật `profiles/process.md`.

### Bản in test 30/08 — seam hết, tơ còn nhiều, nốt nhựa mới cuối bản in

🟢 **Seam hết dư nhựa.** Không tách được công của cái nào trong: scarf tắt
(P15, đã có từ trước), hay ba khoá vừa trả về mặc định ở trên (đổi ngay trước
bản in này). Không cần hành động thêm trừ khi seam tái phát.

🔴 **Tơ vẫn còn nhiều.** Đã có đủ `reduce_crossing_wall = 1` (P19),
`retraction_speed = 45`, `retract_before_wipe = 100%`, `z_hop_types = Normal
Lift` (P15) — ironing tắt nên loại được khả năng nhầm ironing artifact với tơ.
Nghi phạm còn lại: [P6](PENDING_APPLY.md#p6) —
`retraction_minimum_travel = 1` khiến bước nhảy ngắn hơn 1 mm không rút nhựa.
Model FIGURE nhiều chi tiết nhỏ thì phần lớn travel giữa các đảo ngắn hơn
ngưỡng đó. Ghi lại đề xuất `apply P6`, chờ Viet duyệt.

🔴 **Lỗi mới: nốt nhựa dư ở điểm kết thúc bản in.** Khác triệu chứng cũ ở đầu
bản in (A8, do macro `G9111` firmware, không sửa được). Cái này nằm trong
`machine_end_gcode`, sửa được từ slicer.

Cơ chế: mọi retract giữa bản in đều có một bước wipe đi kèm — nozzle di chuyển
dọc travel kế tiếp để kéo giọt nhựa cuối ra khỏi mũi. Retract **cuối cùng** của
cả bản in không có travel nào theo sau, nên không wipe được — giọt nhựa còn
treo đúng tại điểm dừng. Không phải lỗi của P16 (retract + z-hop vẫn cần, C2 đã
xác nhận); đây là khoảng trống P16 chưa che.

Ghi thành P25 — chèn một bước wipe 3 mm vào giữa `machine_end_gcode`, tổng
lượng rút giữ nguyên 6 mm. Chờ Viet duyệt.

## 2026-08-29

### Slot 2 đã fix — in bình thường

Viet xác nhận. Trả lời luôn câu hỏi treo từ vụ PA: cơ cấu nạp không hỏng, chỉ
bài hiệu chuẩn thiếu `T` + bước mồi mới không ra nhựa. Không cần nghi phần cứng
slot 2 nữa.

### C2 🟢 đóng — P16 hoạt động tốt

Retract 6 mm + nhấc Z ở `machine_end_gcode` xác nhận ổn, nozzle sạch cuối bản in.
Giữ nguyên, không revert.

### Nhựa thừa đầu bản in — nằm trong macro `G9111`, ngoài tầm sửa từ slicer

Viet mô tả chi tiết trình tự lúc bắt đầu in:

1. Đùn nhựa thải (purge mồi)
2. Di chuyển đầu in tới vị trí wiper silicone, chấm xuống bàn — **trong lúc di
   chuyển này, nhựa vẫn chảy ra khoảng 5 cm**, vướng vào bàn in
3. Lau đầu in vào wiper
4. Di chuyển tới điểm bắt đầu in — sau bước lau, **vẫn còn dư khoảng 1 cm** nhựa,
   tiếp tục vướng bàn

🔴 **Toàn bộ chuỗi trên chạy bên trong lệnh `G9111`** — dòng duy nhất còn lại
trong `machine_start_gcode` sau khi gỡ P23/P24. Slicer không phát thêm lệnh nào
khác trước đó. `G9111` là một macro Klipper định nghĩa trong `printer.cfg` **trên
bo mạch máy in**, không phải file nào trong `%APPDATA%\AnycubicSlicerNext\`.

❌ **Không sửa được từ đây.** Đúng như đã ghi ở kết luận cũ về "đầu bản in không
sửa được từ slicer" — giờ có thêm chi tiết: không chỉ nhiệt độ nozzle đứng yên,
mà cả trình tự purge → di chuyển → wipe → di chuyển đều do macro quyết định,
gồm cả *quãng đường* và *có retract giữa các bước hay không*.

Hai điểm rò rỉ khác nhau, đáng phân biệt khi báo cho Anycubic hoặc tìm cách sửa
firmware:

| Điểm | Mô tả | Khả năng |
|---|---|---|
| Purge → wiper (5 cm) | Không retract trước khi di chuyển, hoặc quãng đường quá dài so với tốc độ chảy tự nhiên | macro thiếu `G1 E-` trước lệnh travel |
| Wiper → điểm in (1 cm) | Wipe xong không lau hết, hoặc thiếu retract sau lau | macro chưa bù đủ, hoặc do chính cơ chế lau (ép nhựa ra thêm) |

📝 Đường duy nhất để sửa: `printer.cfg` trên máy — nằm ngoài phạm vi repo này
(`docs/capabilities.md` mục 1: "Nói chuyện với máy in" đã chặn, giờ thêm rõ
macro khởi động cũng cùng nhóm không truy cập được).


### C4 🟢 — gỡ P23 và P24 khỏi `machine_start_gcode`

Backup `user_backup-tune-c4-drop-startgcode-20260829-213824`.

Cách gỡ: **xoá hẳn khoá `machine_start_gcode` khỏi user preset**, không khôi phục
backup. Trước P23 preset không hề sở hữu khoá này — nó kế thừa từ hãng. Xoá khoá
là trả về đúng trạng thái đó và **không đụng gì khác**; khôi phục backup thì sẽ
kéo lùi cả P18, P19, P20, P21.

Đã đọc lại giá trị hiệu dụng: 8 dòng gốc của hãng, không còn `T1`, không còn purge.

Trạng thái machine preset sau khi gỡ:

```
retraction_length 1.2   retraction_speed 45   retract_before_wipe 100%
z_hop 0.4   z_hop_types Normal Lift   retract_restart_extra 0
retraction_minimum_travel 1   deretraction_speed 35
machine_end_gcode  <- P16 con nguyen
```

### Hiệu chuẩn PA bỏ dở — tổng kết để không lặp lại

Ba lần chạy, ba rào chắn khác nhau, không lần nào ra được số:

| Lần | Rào | Sửa | Kết quả |
|---|---|---|---|
| 18:39 | gcode không có lệnh `T` nào — đầu 4-in-1 không gạt slot | P23 thêm `T1` | máy ra vài vệt mỏng |
| 19:36 | không có bước mồi, đường dẫn 79 mm³ rỗng | P24 cách A: đổi process lấy `skirt_loops = 2` | 🔴 bộ sinh ép `skirt_loops = 0`, vô hiệu |
| 21:08 | — | P24 cách B: purge 53 mm sợi trong start gcode | vẫn không ra nhựa |

🔴 **Gcode ở lần cuối đã đúng** — kiểm bằng cách đọc file: có `T1`, có
`G1 X120 Y12 E25 F300`, `E40`, `E53`. Lệnh đùn thật, không phải travel. Phía
slicer hết chỗ sửa.

Còn lại hai khả năng, **chỉ phân biệt được bằng cách nhìn máy**:

- đầu in **có** chạy tới `Y = 12` kéo một đường mà không ra nhựa → cơ cấu nạp
  slot 2 không ăn, lỗi máy
- đầu in **không** chạy tới đó → máy in file cũ, không phải file vừa slice
  *(file cuối 18m57s, các file trước 18m19s — phân biệt bằng thời gian trên máy)*

📝 Tạm dừng A2. Quay lại nghiệm thu P19/P20/P21 bằng một bản in thật 1 màu — nó
cũng trả lời gián tiếp việc slot 2 có nạp bình thường hay không, mà không tốn
thêm một bài test hỏng.

🔵 Ghi lại cho lần sau: **mọi bài hiệu chuẩn một-filament trên máy này đều thiếu
cả `T` lẫn bước mồi.** Flow rate, temperature tower, retraction tower cũng vậy.
Muốn dùng chúng thì phải dựng lại P23 + P24, và trước hết phải giải quyết được
việc máy không đẩy nhựa.


### P24 🟢 áp cách B — purge line trong `machine_start_gcode`

Backup `user_backup-tune-p24-purge-20260829-204740`. Nối sau dòng `T1` của P23:

```
M82 ; P24 purge - absolute E, slicer set lai M83 ngay sau start gcode
G90
G92 E0
G1 Z5 F600
G1 X20 Y12 F6000
G1 Z0.3 F600
G1 X120 Y12 E25 F300 ; purge cham, lap day duong dan 79mm3
G1 X235 Y12 E40 F900 ; keo dai, gat cuc nhua ra
G1 X235 Y12.7 F6000
G1 X20 Y12.7 E53 F1500 ; luot ve, lau sach
G92 E0
G1 Z5 F600 ; P24 purge het
```

53 mm sợi tổng cộng — thừa sức lấp 79 mm³ ≈ 33 mm của đường dẫn chung.

🔵 `M82` an toàn vì slicer phát `G90/G21/M83` của nó **ngay sau** start gcode, ghi
đè lại chế độ tương đối.

🔵 Chạy ở `Y = 12`, ngoài vùng bài PA (`X 44–215, Y 100–143`), trong bàn 260 × 260.

🟢 Lợi phụ: đường purge là **phép thử phần cứng**. Nó không ra nhựa nghĩa là vấn
đề nằm ở máy hoặc firmware, không phải ở gcode slicer sinh ra.

🔴 Thay đổi **tạm**, gỡ cùng lúc với `T1` — C4 trong `TODO.md`.


### Cách A của P24 chết — bộ sinh bài PA ép `skirt_loops = 0`

Đổi process sang `Novi 0.12 - FIGURE @AC KX` (preset đó giữ `skirt_loops = 2`)
rồi chạy lại wizard lúc 20:17. Đọc gcode:

```
print_settings_id = Novi 0.12 - FIGURE @AC KX
skirt_loops       = 0
```

🔴 Bộ sinh bài hiệu chuẩn **ghi đè** `skirt_loops` về 0 bất kể process nào đang
chọn. Đổi process không có tác dụng.

Còn lại đúng một đường: cách B của P24 — purge line trong `machine_start_gcode`.

🔵 Ghi lại để không thử lại: **bài hiệu chuẩn của Orca không kế thừa
`skirt_loops` từ process preset.** Mọi cách mồi nhựa phải nằm ngoài nó, tức trong
`machine_start_gcode`.


### P23 có tác dụng, nhưng bài PA vẫn thiếu nhựa — không có bước mồi

Lần chạy 19:36 sau P23. Gcode có `T1` ✅ và máy **đã ra nhựa** — nhưng chỉ vài vệt
rất mỏng ở viền, không đọc được dải nào.

```
; bài PA 19:36                     ; bản in thường
T1                                 T0
...                                ...
G1 E1.2 F2100  <-- chỉ deretract   (prime tower / skirt in truoc)
G1 X44.744 Y143.213 E2.23286       (da day nhua khi vao vat)
```

| | |
|---|---|
| Đường dẫn chung đầu 4-in-1 | `nozzle_volume = 79` mm³ ≈ **33 mm sợi** |
| Khung viền bài PA đùn | ~22 mm sợi |

Khung viền chưa đủ để **lấp đầy** đường dẫn, nói gì tới đắp lên bàn. Đúng triệu
chứng "vài vệt mỏng như tơ ở viền".

🔴 **Vì sao không có skirt:** bài hiệu chuẩn mượn process đang chọn ở cửa sổ chính
— `Novi 0.16 - FIGURE @AC KX`, mà preset đó Viet cố ý để `skirt_loops = 0`
(xem P22 đã đóng). `Novi 0.12 - FIGURE` vẫn giữ 2.

Ghi thành P24, hai cách. Cách A không sửa preset nào: đổi process sang
`Novi 0.12 - FIGURE @AC KX` rồi chạy wizard.

🔵 Bài học: `skirt_loops = 0` là lựa chọn hợp lý cho bản in thật trên máy một
màu, nhưng trên đầu 4-in-1 nó cũng bỏ luôn bước mồi sau mỗi lần đổi slot. Với bài
hiệu chuẩn — chạy một filament, không prime tower — đó là bước mồi duy nhất còn lại.


### P23 🟢 áp — `T1` vào cuối `machine_start_gcode`

Backup `user_backup-tune-p23-startgcode-T1-20260829-193347`. Slot 2 (white,
`PLA Generic@KX 0.4`) → `T1`.

```
...
; first_layer_print_size = {first_layer_print_size[0]},{first_layer_print_size[1]}
T1 ; P23 tam thoi - chon slot 2 (white, Generic) cho bai hieu chuan
```

Kiểu trên đĩa: `str` ✅. `--audit` 0 lỗi. Script có chốt chặn — thấy dòng `T` sẵn
thì dừng, không nhân đôi.

🔴 **Là thay đổi tạm.** Gỡ ngay sau khi đo xong PA. Để lâu thì mọi bản in nhiều
màu bắt đầu bằng `T0`/`T2`/`T3` sẽ bị ép thêm một lần đổi màu vô ích ở đầu bản in.

**Gỡ:** đóng slicer rồi khôi phục backup ở trên, hoặc xoá đúng dòng cuối.


### Bài hiệu chuẩn PA chạy nhưng không ra nhựa — thiếu lệnh chọn slot

Viet chạy Calibration → Pressure Advance. Máy chạy hết bài, không đùn tí nhựa nào.

Đọc gcode `0829-1839-pa_pattern_100_2000_plate(01)_PLA_0.2_18m19s.gcode.3mf`:

| File gcode | Số filament trong project | Lệnh `T` |
|---|---|---|
| PA pattern 18:39 | 1 | 🔴 **0** |
| Bản in 2 màu 17:00 | 4 | `T0`, `T1` |
| Bản 1 màu 14:35 | 4 | `T3` |
| Bản 1 màu 09:32 | 2 | `T1` |

🔴 **Mọi bản in bình thường đều có lệnh `T`, kể cả bản chỉ dùng một màu** — vì
project của chúng khai nhiều filament. Bài hiệu chuẩn khai **đúng một** filament,
slicer bỏ hẳn nhánh multi-material và không phát `T`. Đầu in 4-in-1 cần `T` để gạt
cơ cấu chọn slot; không có nó thì motor đùn quay nhưng không slot nào nối vào
đường nạp.

So sánh cùng vị trí trong file:

```
; bản in thường            ; bài PA
M83                        M83
M900 K0.036                M900 K0.036
T0            <-- có       (không có gì)
M75                        M75
```

🟢 Phần còn lại của bài test hoàn toàn bình thường: 2105 đường đùn, 1444 mm nhựa,
165 lệnh `M900` quét PA. Chỉ thiếu đúng một dòng.

Ghi thành P23 — nối `T#` vào cuối `machine_start_gcode`, **tạm thời**, gỡ sau khi
đo xong.

🟡 Đây là hạn chế của máy 4-in-1 với bộ calibration kế thừa từ Orca: mọi bài
hiệu chuẩn một-filament đều dính, không riêng PA. Flow rate, temperature tower,
retraction tower cũng sẽ không ra nhựa nếu chạy như hiện tại.


### 🔴 Máy khai `gcode_flavor = klipper` nhưng slicer phát `M900`, không phải `SET_PRESSURE_ADVANCE`

Đọc gcode bản in 29/08:

```
M900 K0.036; Override pressure advance value
```

`SET_PRESSURE_ADVANCE` **không xuất hiện lần nào**. `M900 K` là lệnh Linear
Advance của Marlin; Klipper **không** hiểu nó theo mặc định — phải có
`[gcode_macro M900]` trong `printer.cfg` ánh xạ sang `SET_PRESSURE_ADVANCE`.

🔴 Hệ quả: **chưa chắc máy có nghe `pressure_advance` của slicer hay không.** Nếu
firmware Anycubic không định nghĩa macro M900 thì con số trong filament preset
không có tác dụng gì, và PA thật là giá trị nằm trong `printer.cfg`.

Điều đó khớp với việc seam vẫn dư nhựa qua nhiều lần chỉnh preset.

📝 Phải kiểm trước khi hiệu chuẩn — xem A2 trong `TODO.md`. Cách kiểm: chạy bài
PA Pattern; nếu **mọi dải trong bài test trông giống hệt nhau** thì máy đang bỏ
qua lệnh, và hiệu chuẩn từ slicer là vô nghĩa.

🔵 Bộ bài hiệu chuẩn có sẵn trong
`C:\Program Files\AnycubicSlicerNext\resources\calib\` — `pressure_advance/`
có ba mẫu: `pa_pattern.3mf`, `pressure_advance_test.stl`, `tower_with_seam.stl`.


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
