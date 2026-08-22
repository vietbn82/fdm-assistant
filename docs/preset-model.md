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
  "name": "BBL PLA Lite @Anycubic Kobra X 0.4 nozzle",
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
  AnycubicSlicerNext.conf      trạng thái app + bộ ba preset đang chọn
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
`filament\base\BBL PLA Lite @Kobra X.json` và `filament\BBL PLA Lite @Kobra X.json`
có cùng `"name"` bên trong. Bản trong `base\` là ảnh chụp cache đầy đủ; bản
top-level mới là preset sống. Đọc nhầm sẽ ra giá trị cũ.

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
- Mọi preset kế thừa từ đó — tức là **cả bảy** process preset của bạn — thừa
  hưởng nguyên mâu thuẫn này

🔵 Cùng hotend, preset `Anycubic PLA High Speed @Kobra X` của hãng dùng 18 mm³/s.
Đó là mức thực tế hơn cho PLA chạy tốt.

❌ Đừng sửa bằng cách hạ tốc độ trong process preset — đó chính là lỗi nhầm tầng
ở mục 3. Slicer đã tự lo phần đó rồi.
