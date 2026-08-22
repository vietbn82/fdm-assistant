# tools/acslicer_tune.py

Đọc kho preset của Anycubic Slicer Next, giải chuỗi kế thừa, đối chiếu giá trị
thực tế với giới hạn của máy và của nhựa, và ghi sửa nếu được yêu cầu.

Chỉ đụng vào file. Không nói chuyện với máy in, không gọi cloud.

Bố cục kho preset và bốn cái bẫy khi ghi file: `docs/preset-model.md` mục 1–2.
Công cụ xử lý sẵn cả bốn — trừ bẫy số 1, **bạn phải đóng slicer trước khi ghi**.

---

## Lệnh

```bash
python tools/acslicer_tune.py --list                   # preset của bạn + preset cha
python tools/acslicer_tune.py --show "<tên preset>"    # giá trị đã giải đầy đủ
python tools/acslicer_tune.py --audit                  # báo cáo, không ghi
python tools/acslicer_tune.py --audit --flow           # + tốc độ bị trần flow kẹp
python tools/acslicer_tune.py --audit --fix            # áp sửa, backup trước
python tools/acslicer_tune.py --set "BBL PLA Lite|filament_max_volumetric_speed=15"
```

Thêm `--yes` để bỏ qua bước xác nhận. `--set` lặp lại được nhiều lần.

Mọi lần ghi đều copy `user\` sang
`%APPDATA%\AnycubicSlicerNext\user_backup-tune-<tag>-<timestamp>` trước.
Revert = xoá `user\`, đổi tên backup lại thành `user`.

## Mức độ nghiêm trọng

| | Nghĩa |
|---|---|
| `ERR` | mâu thuẫn nội tại — slicer hoặc firmware sẽ không làm theo con số bạn gõ |
| `WARN` | hợp lệ nhưng nhiều khả năng hại chất lượng in |
| `FLOW` | tốc độ vượt trần flow của nhựa, nên tốc độ thật thấp hơn số hiển thị *(cần `--flow`)* |
| `INFO` | rác thẩm mỹ còn sót từ thao tác copy preset |

`--fix` chỉ áp `ERR`, `WARN`, `FLOW` — và chỉ những mục có giá trị thay thế rõ ràng.

🟡 `FLOW` mặc định bị ẩn vì **preset hãng cũng vi phạm** (xem `docs/preset-model.md`
mục 4). Nó là thông tin chẩn đoán, không phải lỗi của bạn.

## Kiểm tra những gì

**process**
- Layer height so với nozzle và `max_layer_height`
- Lưu lượng thể tích: `speed × layer_height × line_width` so với
  `filament_max_volumetric_speed`
- Speed so với `machine_max_speed_x/y`; accel so với
  `machine_max_acceleration_extruding` / `_travel`
- Thang tốc độ overhang phải giảm dần *(giá trị 0 nghĩa là tắt, không phải dừng)*
- Tường ngoài không được nhanh hơn tường trong
- Tốc độ và khoảng cách ironing; `bridge_flow`
- Độ dày top/bottom shell tính ra mm
- `support_top_z_distance` phải là bội số nguyên của layer height

**filament**
- Nhiệt độ nằm trong range đã khai
- `filament_flow_ratio`, `pressure_advance`, trần thể tích vô lý
- Nhiệt bàn vượt điểm mềm của nhựa
- Bàn lớp đầu nguội hơn các lớp sau
- Key rác của máy in dạng hạt và giá trị `nil` sót từ preset copy

**machine**
- `retraction_length` kiểu bowden trên máy direct drive
- `retract_restart_extra` âm
- Tốc độ retraction quá cao
- `z_hop` nhỏ hơn chính lớp nó cần vượt qua

## Chưa có

`--unset` để xoá key, rule multi-material, `--diff` so với preset cha, và ghi
`.conf` an toàn. Chi tiết ở C5 trong `TODO.md`.
