# Preset hoạt động thế nào

Kiến thức nền, gần như không đổi. Giá trị đang đặt thực tế: `profiles/`.

---

## 1. Ba tầng preset

Mỗi lần in, slicer ghép **ba** preset lại với nhau:

| Tầng | Trả lời câu hỏi | Đổi khi nào |
|---|---|---|
| **machine** | Máy này là máy gì, chạy được đến đâu? | hiếm — chỉ khi đổi nozzle hoặc tinh chỉnh retraction |
| **filament** | Cuộn nhựa đang nạp là loại gì? | mỗi lần đổi cuộn |
| **process** | Bản in **này** muốn ra sao? | mỗi lần in, tuỳ mục đích |

Ba tầng độc lập nhau. Đổi cuộn nhựa không phải sửa lại profile in; đổi ý đồ in
không phải khai báo lại máy. Đó là lý do chia ba.

## 2. Kế thừa: preset con chỉ lưu phần khác cha

Preset của bạn **không** chứa đủ mọi setting. Nó chỉ lưu những key bạn đã đổi,
cộng một dòng trỏ về preset cha:

```json
{
  "name": "PLA Bambulab Lite@KX 0.4",
  "inherits": "Anycubic PLA @Anycubic Kobra X 0.4 nozzle",
  "filament_max_volumetric_speed": ["15"],
  "hot_plate_temp": ["50"]
}
```

File thật chỉ khoảng 10 dòng. Preset cha của hãng có hơn 200 setting. Giá trị
slicer thực sự dùng = **cha + con đè lên**:

```
Anycubic PLA @Kobra X  (hãng, ~200 setting)
        │  nozzle_temperature = 205
        │  filament_max_volumetric_speed = 13
        │  hot_plate_temp = 60
        ▼  đè lên bởi
BBL PLA Lite @Kobra X  (của bạn, 10 setting)
           filament_max_volumetric_speed = 15
           hot_plate_temp = 50

kết quả slicer dùng:
   nozzle_temperature = 205          ← kế thừa từ cha
   filament_max_volumetric_speed = 15 ← con đè
   hot_plate_temp = 50                ← con đè
```

Hai hệ quả cần nhớ:

- **Nhìn file preset của bạn không thấy được giá trị thật.** Phải gộp cả chuỗi.
  Lệnh `python tools/acslicer_tune.py --show "<tên>"` làm việc đó.
- **Preset càng mỏng càng tốt.** Mỗi key bạn ghi vào là một key ngừng theo kịp
  bản cập nhật của hãng. Đừng ghi lại một giá trị y hệt cha chỉ để "cho chắc".

## 3. Setting nào thuộc tầng nào

🔴 **Đặt nhầm tầng là lỗi hay gặp nhất.**

| Tầng | Chứa gì | Ví dụ |
|---|---|---|
| **machine** | thuộc tính cố định của máy và cách nó nhả/rút sợi | `retraction_length`, `z_hop`, `machine_max_*`, `nozzle_volume`, `single_extruder_multi_material`, `purge_in_prime_tower` |
| **filament** | thuộc tính của cuộn nhựa | `filament_max_volumetric_speed`, nhiệt độ nozzle/bàn, `filament_flow_ratio`, `pressure_advance` |
| **process** | ý đồ hình học của bản in này | `layer_height`, `wall_loops`, tốc độ, infill, ironing, `enable_prime_tower`, `flush_into_infill`, `flush_into_objects`, `flush_into_support` |

Trạng thái hiện tại của từng tầng: `profiles/printer.md`, `profiles/filament.md`,
`profiles/process.md`.

### Vì sao quan trọng — ví dụ có thật

BBL PLA Lite chỉ chảy được 15 mm³/s. Ở layer 0.20 mm, điều đó tương đương
~166 mm/s. Profile in đang ghi `sparse_infill_speed = 300`.

Có vẻ nên sửa 300 → 166 trong **process** preset cho khớp. **Sai.**

Vấn đề: 166 là con số của *cuộn nhựa này*. Ngày mai bạn lắp cuộn PLA chảy được
18 mm³/s — profile in vẫn ghi 166 và bạn in chậm hơn mức cần, mà không nhớ tại
sao. Giới hạn của một cuộn nhựa đã bám vào profile dùng chung cho mọi cuộn.

✅ Đúng: để `filament_max_volumetric_speed` ở **filament** preset. Slicer tự hạ
tốc độ xuống cho vừa, mỗi lần in, theo đúng cuộn đang dùng.

### Trường hợp dễ nhầm: prime tower và flush

`enable_prime_tower`, `flush_into_infill`, `flush_into_objects`,
`flush_into_support` nghe như thuộc về máy, nhưng nằm ở **process**.

Đúng vậy: chiến lược xả nhựa thừa khi đổi màu thay đổi theo từng bản in. Bản
figure không muốn nhựa thải nhét vào thân vật thể vì có thể lộ ra bề mặt; bản đồ
dùng thì nhét vào trong được, tiết kiệm nhựa. Cùng một máy, hai lựa chọn khác nhau.

## 4. File nằm ở đâu

```
%APPDATA%\AnycubicSlicerNext\
  AnycubicSlicerNext.conf      trạng thái app + machine preset đang chọn
                               🔵 bản 2.0.0.2 bỏ filament_colors và bảng gán slot
  system\Anycubic\             preset hãng — CHỈ ĐỌC
  user\855643\                 preset của bạn
    machine\ process\ filament\    *.json
    filament\base\*.json           bản sao cache, xem bẫy #2
    *.info                         file đi kèm, chứa updated_time
  log\  crash\                 log MQTT / cloud SDK / app
```

Mỗi preset `.json` có một file `.info` cùng tên đi kèm. `.info` không chứa
setting — nó giữ thông tin đồng bộ cloud, trong đó có `updated_time`.

## 5. Bốn cái bẫy khi sửa file trực tiếp

Chỗ duy nhất mô tả chúng. Tài liệu khác chỉ trỏ về đây.

**Bẫy 1 — slicer đang chạy sẽ xoá thành quả của bạn.**
Nó nạp toàn bộ preset vào RAM lúc khởi động và ghi đè xuống đĩa lúc thoát. Sửa
file khi slicer đang mở = mất trắng khi nó đóng. Luôn đóng slicer trước.

**Bẫy 2 — `filament\base\` chứa file trùng tên với preset thật.**
`filament\base\PLA Bambulab Lite@KX 0.4.json` và
`filament\PLA Bambulab Lite@KX 0.4.json` có cùng `"name"` bên trong. Bản trong `base\` là ảnh chụp cache đầy đủ; bản
top-level mới là preset sống. Đọc nhầm sẽ ra giá trị cũ.

🔵 **Tính đến 03/09 (slicer 2.0.0.2) `filament\base\` đang rỗng** — đợt dựng lại
preset đã dọn sạch. Bẫy vẫn còn hiệu lực: slicer sinh lại `base\` bất cứ lúc
nào, đừng bỏ bước kiểm.

**Bẫy 3 — sửa `.json` mà quên `.info` thì cloud sync khôi phục lại bản cũ.**
Sync so `updated_time` trong `.info`. Không tăng số đó, nó coi file trên máy bạn
là cũ hơn bản trên server và ghi đè ngược lại. Sửa xong phải cập nhật `.info`.

**Bẫy 4 — `.conf` không phải JSON hợp lệ.**
Nó là JSON, rồi thêm một dòng `# MD5 checksum <hash>` ở cuối. Parser thường sẽ
báo lỗi; phải dùng `raw_decode` để đọc phần JSON và bỏ qua phần đuôi. Ghi lại
file thì phải tính lại MD5, nếu không slicer coi file hỏng.

🟢 `tools/acslicer_tune.py` xử lý sẵn bẫy 2, 3, 4. Bẫy 1 thì không ai xử lý hộ
được — bạn phải tự đóng slicer.

## 6. Preset hãng tự mâu thuẫn ngay khi cài

Ví dụ tổng hợp mọi thứ ở trên.

Preset filament `Anycubic PLA @Kobra X` khai cuộn nhựa chảy tối đa 13 mm³/s.
Preset process `0.20mm Standard @Kobra X` — cũng của hãng, cũng cho máy này —
yêu cầu `inner_wall_speed = 300`, tức 27 mm³/s. **Gấp đôi mức nhựa chảy được.**

Slicer không báo lỗi. Nó lặng lẽ hạ tốc độ xuống còn ~144 mm/s cho vừa trần
flow, rồi in. Hậu quả:

- Số hiển thị trong UI không phải tốc độ thật
- Thời gian ước tính sai theo
- Mọi preset kế thừa từ đó — tức là **cả năm** process preset của bạn — thừa
  hưởng nguyên mâu thuẫn này

🔵 Cùng hotend, preset `Anycubic PLA High Speed @Kobra X` của hãng dùng 18 mm³/s.
Đó là mức thực tế hơn cho PLA chạy tốt.

❌ Đừng sửa bằng cách hạ tốc độ trong process preset — đó chính là lỗi nhầm tầng
ở mục 3. Slicer đã tự lo phần đó rồi.

## 7. Project (`.3mf`) có thể mang bản chụp preset riêng, không ăn theo thư viện

Phát hiện 30/08. Sửa `PLA Generic@KX 0.4` trong thư viện (`user\855643\filament\`)
**không đảm bảo** một project đã lưu sẽ dùng bản mới.

Bản in 30/08 10:45, hai màu cùng gán preset tên `PLA Generic@KX 0.4`, nhưng gcode
cho ra hai giá trị nhiệt khác nhau:

```
filament_settings_id = ["PLA Generic@KX 0.4", "PLA Generic@KX 0.4(keychain_Daniel.3mf)"]
nozzle_temperature   = [200, 205]
```

Slot 1 (`filament`) đọc đúng bản thư viện mới nhất (200, sau P28). Slot 2
(`filament_01`) bị **đóng băng** ở một bản chụp cũ hơn — tên có hậu tố
`(keychain_Daniel.3mf)`, thời điểm chụp nằm giữa P15 (flow=1.0, đã có) và P28
(nhiệt=200, chưa có) — tức chụp lúc project được lưu, ở đâu đó giữa 29/08 và
sáng 30/08.

🔴 **Cơ chế:** khi một object/slot trong project được gán filament preset, slicer
nhúng một bản sao cấu hình *tại thời điểm đó* vào file project. Sửa preset trong
thư viện sau đó chỉ cập nhật những slot **chưa từng bị đóng băng** — slot đã có
bản chụp riêng thì im lặng giữ nguyên, không có cảnh báo nào.

❌ **Hệ quả cho quy trình:** không thể tin gcode của một project **đã lưu từ
trước** phản ánh đúng preset thư viện hiện tại, dù `filament_settings_id` ghi
đúng tên. Phải đọc `nozzle_temperature` / `filament_flow_ratio` thật trong
gcode, không suy từ tên preset.

🟡 **Cách buộc một slot đồng bộ lại:** trong slicer, mở lại dropdown chọn
filament cho đúng slot đó và chọn lại `PLA Generic@KX 0.4` từ thư viện — thao
tác này thay bản chụp cũ bằng tham chiếu mới. Xoá object rồi thêm lại cũng được.

📝 Không có cách nào phát hiện từ `.conf` hay từ preset trên đĩa — chỉ thấy được
khi đọc gcode/project đã xuất ra.


## 8. Có khoá slicer đọc nhưng UI không cho sửa

Phát hiện 04/09 với `purge_in_prime_tower`: không tìm thấy ở đâu trong UI 2.0.0.2,
kể cả Advanced mode và ô tìm kiếm setting.

🔵 **Khoá có thật và slicer vẫn dùng khi slice.** Label + tooltip dựng sẵn trong
`AnycubicSlicer.dll`, và có 10 chỗ trong code tham chiếu tới tên khoá:

```
"Purge in prime tower"  /  "Purge remaining filament into prime tower."
```

🔴 Nhưng **chỉ đúng một chỗ trong code dựng ô nhập cho nó**, và chỗ đó không bao
giờ chạy trên Kobra X:

| Nơi | Nội dung | Có hiện không |
|---|---|---|
| Printer Settings → *Multimaterial* → nhóm **Wipe tower** | `enable_filament_ramming`, **`purge_in_prime_tower`**, `printer_flush_multiplier` | ❌ trang chỉ được dựng khi `extruders_count > 1` |
| Print Settings → *Multimaterial* → nhóm **Prime tower** | `enable_prime_tower`, `prime_tower_width`, `prime_volume`, `prime_tower_brim_width`, `wipe_tower_*`, `single_extruder_multi_material_priming` | ✅ có trang, nhưng **không chứa** `purge_in_prime_tower` |

Kobra X khai **một** extruder (`nozzle_diameter` là mảng 1 phần tử, không có
`extruders_count`) — đổi màu do firmware ACE lo, không phải nhiều extruder. Nên
trang Printer → Multimaterial không tồn tại, và ô đó không bao giờ được vẽ.

🟡 **Bản Anycubic không có Expert mode.** Chuỗi `"Expert"` không tồn tại trong
DLL; chỉ có một công tắc Advanced (`ParamsPanel::OnToggled`, log
`Advanced mode toogle to %1%`). Không có mức nào cao hơn để lộ thêm khoá.

🔵 Ô tìm kiếm setting chỉ quét khoá **đã nằm trên một trang** — khoá không thuộc
trang nào thì tìm cũng không ra.

✅ **Cách sửa duy nhất: ghi thẳng file preset.**

```bash
python tools/acslicer_tune.py --set "Kobra X 0.4 - MultiColor|purge_in_prime_tower=1"
```

❌ Đừng đặt `extruders_count = 2` để ép trang hiện ra. Nó kéo theo mảng
`nozzle_diameter` / `extruder_offset` / lệnh `T`, sai hẳn mô hình máy.

🟡 Slicer **không** xoá khoá lạ khi lưu lại preset — P30 (30/08) đặt bằng file và
sống qua nhiều phiên. Nhưng vì UI không hiện, khoá kiểu này biến mất lặng lẽ khi
dựng lại preset từ đầu, đúng như đã xảy ra 03/09.

### Cách kiểm một khoá có sửa được bằng UI không

❌ Đừng đếm số lần chuỗi xuất hiện trong DLL — compiler gộp chuỗi trùng, một khoá
dùng ở mười chỗ vẫn chỉ có một chuỗi. Đếm kiểu đó cho kết luận sai.

✅ Đếm **lệnh code trỏ tới chuỗi** (`lea reg,[rip+disp32]`), rồi xem hàm nào chứa
chúng: hàm dựng trang có kèm tiêu đề nhóm (`"Prime tower"`, `param_tower`) và một
dãy tên khoá liền nhau. Không có hàm nào như vậy → khoá không có ô nhập.
