# Cách slicer lưu preset

Kiến thức nền, gần như không đổi. Giá trị đang đặt thực tế: `profiles/`.

---

## 1. Bố cục

```
%APPDATA%\AnycubicSlicerNext\
  AnycubicSlicerNext.conf      trạng thái app + cặp machine/filament/process đang chọn
  system\Anycubic\             preset hãng — CHỈ ĐỌC
  user\855643\                 preset của bạn
    {machine,process,filament}\*.json
    filament\base\*.json       snapshot cache, TRÙNG TÊN với preset thật
    *.info                     sidecar sync, chứa updated_time
  log\  crash\                 log MQTT / cloud SDK / app
```

Preset user chỉ lưu **key đã đổi** cộng `"inherits": "<tên cha>"`. Giá trị thực
tế = cả chuỗi kế thừa gộp lại.

## 2. Bốn cái bẫy — đọc trước khi đụng vào file

Chỗ duy nhất mô tả chúng. Tài liệu khác chỉ trỏ về đây.

| # | Bẫy | Hậu quả nếu bỏ qua |
|---|---|---|
| 1 | **Slicer đang chạy** giữ preset trong RAM, flush xuống đĩa lúc thoát | xoá sạch mọi thay đổi ghi từ bên ngoài |
| 2 | `filament\base\X.json` **trùng `"name"`** với `filament\X.json` | đọc nhầm snapshot cache thay vì preset sống; file top-level mới là bản thật |
| 3 | Sửa `.json` mà không bump `updated_time` trong `.info` | cloud sync coi file là cũ và ghi đè lại |
| 4 | `.conf` **không phải JSON thuần** — có dòng `# MD5 checksum` ở cuối | parse hỏng; phải dùng `raw_decode`, ghi lại thì phải tính lại MD5 |

`tools/acslicer_tune.py` xử lý cả bốn. Ghi tay thì tự lo.

## 3. Setting nào thuộc tầng nào

🔴 **Nhầm tầng là lỗi hay gặp nhất.** Đặt đúng chỗ thì giá trị sống đúng vòng
đời của nó; đặt sai thì nó bám dai hơn thứ nó mô tả.

| Tầng | Mô tả cái gì | Ví dụ | Trạng thái hiện tại |
|---|---|---|---|
| **machine** | thuộc tính cố định của máy và cách nó nhả sợi | `retraction_length`, `z_hop`, `machine_max_*`, `nozzle_volume`, `single_extruder_multi_material`, `purge_in_prime_tower` | `profiles/printer.md` |
| **filament** | thuộc tính của cuộn nhựa | `filament_max_volumetric_speed`, nhiệt độ nozzle/bàn, `filament_flow_ratio`, `pressure_advance` | `profiles/filament.md` |
| **process** | ý đồ hình học của bản in này | `layer_height`, `wall_loops`, tốc độ, infill, ironing, **`enable_prime_tower`, `flush_into_infill`, `flush_into_objects`, `flush_into_support`** | `profiles/process.md` |

🟡 Nhóm prime tower / flush **nằm ở process**, dù nghe như thuộc về máy. Đúng
vậy: chiến lược purge thay đổi theo từng bản in — bản figure không muốn nhựa
thải nhét vào thân vật thể, bản đồ dùng thì có.

## 4. Preset hãng tự mâu thuẫn ngay khi cài

🔴 `Anycubic PLA @Kobra X` khai `filament_max_volumetric_speed = 13`, nhưng
process `0.20mm Standard @Kobra X` của **chính hãng** yêu cầu
`inner_wall_speed = 300` — tức 27 mm³/s, gấp đôi trần.

Slicer âm thầm kẹp tốc độ xuống. Hệ quả: số trong UI và thời gian ước tính đều
sai, và mọi preset kế thừa từ đó đều thừa hưởng mâu thuẫn này.

Preset `Anycubic PLA High Speed @Kobra X` của hãng dùng 18 mm³/s trên cùng
hotend — đó là trần thực tế cho PLA chạy tốt.

❌ **Đừng sửa bằng cách kẹp speed trong process preset.** Trần flow thuộc
filament, slicer đã tự enforce lúc slice. Kẹp vào process là nhét giới hạn của
một loại nhựa vào profile dùng chung — đã thử và đã rollback, xem mục D
`TODO.md`.
