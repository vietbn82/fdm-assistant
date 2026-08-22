# TODO

> Mọi việc còn treo. Đây là các **quyết định** cần đưa ra.
> Thao tác preset cụ thể sẽ chạy sau khi quyết: `PENDING_APPLY.md`.
> Cập nhật: 2026-08-22.

Ký hiệu: ⏳ chờ / 📝 chưa bắt đầu / 🟢 xong / 🔴 chặn việc khác

---

## A. Chỉ Viet làm được (vật lý, không tự động hoá được)

### A1 ⏳ Flow test `BBL PLA Lite` ở 15 mm³/s
Đã nâng `filament_max_volumetric_speed` từ 13 lên 15 nhưng **chưa xác minh**.
15 là trần Bambu công bố cho PLA Lite, không phải số đo trên hotend của bạn.

- In một vật thành mỏng hoặc flow test, xem tường có bị đùn thiếu không.
- Thiếu → hạ về 13: `python tools/acslicer_tune.py --set "BBL PLA Lite @Anycubic Kobra X 0.4 nozzle|filament_max_volumetric_speed=13"`
- Áp cho cả 3 preset: `BBL PLA Lite`, `BBL PLA Lite @Kobra X`, `BBL PLA Lite - High Quantity @Kobra X`

### A2 ⏳ Xác nhận preset còn nguyên sau khi mở lại slicer
Phiên trước đã ghi 8 giá trị rồi đóng slicer. Cloud sync **có thể** ghi đè bằng
bản trên server. Chưa ai kiểm tra.

- Mở slicer, xem `BBL PLA Lite` còn `nozzle_temperature_range_high = 215` không.
- Bị revert → `.info` `updated_time` chưa đủ, phải tìm cách khác.

### A3 📝 Slice thử một model 4 màu (mở khoá C3, C4)
🔴 **Chặn toàn bộ việc 4 màu.** `.conf` hiện vẫn cấu hình single-filament cho
Kobra X: `flush_volumes_matrix` là `"0.000000"` (1×1, cần 4×4),
`filament_colors` là `"#FFFFFF"` chứ không phải Red/White/Black/Cyan.

Slicer chỉ sinh ma trận khi thực sự slice nhiều màu. Cần một lần chạy để có
baseline, sau đó mới chỉnh số được.

### A4 📝 Mở `/hooks` một lần (hoặc restart Claude Code)
Hook ở `.claude/hooks/` đã viết và test xong nhưng **chưa hiệu lực**. Phiên hiện
tại khởi động khi chưa có thư mục `.claude/` nên nó không theo dõi.

### A5 🔁 Cập nhật `profiles/filament.md` mỗi lần đổi cuộn — việc lặp lại
Thứ tôi không thể tự biết. File sai thì mọi tư vấn nhiệt độ / flush / flow đều
sai theo. Nên ghi thêm: thương hiệu chính xác, mã màu hex, ngày mở túi, đã sấy
chưa. Ẩm là nguyên nhân số một của lỗi in PLA mà nhìn giống lỗi setting.

---

## B. Cần Viet chốt (tôi làm được ngay khi có quyết định)

### B1 📝 Có làm FIG / TOOL / TEST không?
Đề xuất đầy đủ ở `profiles/process.md`. Rút 7 preset còn 3–4.
Chốt rồi tôi tạo preset và chỉnh các giá trị đã liệt kê.

### B2 📝 Xoá preset trùng lặp?
| Preset | Lý do |
|---|---|
| `0.20mm PLA Lite @AC KX - Copy` | bị `- fix first layer` thay thế hoàn toàn |
| `0.20mm Standard @AC KX - Copy` | gần như y hệt vendor default |
| `0.20mm - High Quality Novi @AC KX` | trùng `0.12 mm - High Quality Novi` trừ `layer_height` |

Cái thứ ba: xoá, hay giữ thành `FIG 0.20 @KX` nếu bạn thật sự hay dùng 0.20 cho figure?

### B3 📝 `0.12 mm High Quality`: bottom shell 3 lớp = 0.36 mm
Dưới 0.4 mm. Lên 4 lớp nếu thấy đáy bị lộ / xuyên sáng. Không đổi nếu chưa gặp.

### B4 📝 Slot 2 (Generic PLA, trắng) chưa có filament preset
Đang dùng stock `Anycubic PLA @Kobra X` (13 mm³/s) — chấp nhận được.
Ba lựa chọn:
- giữ nguyên stock
- tạo preset riêng qua `/newfilament`
- gán `Anycubic PLA @Kobra X - Copy` (đã nâng lên 18) cho slot này — xem B5

### B5 📝 `Anycubic PLA @Kobra X - Copy` đang để 18 mm³/s nhưng không dùng ở slot nào
Phiên đầu tôi nâng nhầm preset này (lúc đó chưa đọc `profiles/filament.md`). 18 là con
số Anycubic dùng cho `PLA High Speed` của họ, chưa đo trên máy bạn.
Giữ để dành cho slot 2, hay trả về 13?

### B6 📝 `0.20mm - Standard Novi`: `bridge_speed = 15`
Chậm tới mức bridge có thể võng vì ngấm nhiệt. Mặc định hãng là 30.
Bạn cố tình đặt thấp, hay là tàn dư của một lần thử?

### B7 📝 Bỏ cloud user id `855643` khỏi `docs/device.md`?
Repo GitHub là **public**. Không phải credential, chỉ là định danh tài khoản.
Rủi ro thấp, nhưng bỏ đi cũng không mất gì.

---

## C. Hàng đợi của tôi (chờ B, hoặc chờ A3)

### C1 📝 Tạo FIG / TOOL / TEST — chờ B1
Gồm cả: sửa `wall_sequence` của FIG thành `inner wall/outer wall` (hiện là
`outer wall/inner wall`, in tường ngoài trước — tốt cho dung sai, xấu cho bề mặt),
và bỏ `enable_support = 1` khỏi profile TOOL (support là thuộc tính từng model).

### C2 📝 Xoá key rác `pellet_flow_coefficient`
Chỉ nằm ở `Anycubic PLA @Kobra X - Copy` *(đã kiểm lại — không có ở `BBL PLA
Lite` như ghi nhầm trước đó)*. Là key của máy in dạng hạt, vô nghĩa với FDM,
sót lại từ thao tác copy preset.
🔵 Chặn kỹ thuật: `tools/acslicer_tune.py` chưa có `--unset` để xoá key — xem C5.
Thao tác đã xếp sẵn ở P13 trong `PENDING_APPLY.md`.

### C3 📝 Tính `flush_volumes_matrix` 4×4 — chờ A3
Cho Red / White / Black / Cyan. Các cặp tối↔sáng cần khoảng 450–650 mm³,
không phải 140 mm³ mặc định.

### C4 📝 Cấu hình thu hồi purge theo mục đích — chờ A3 + B1
FIG tắt `flush_into_objects` / `flush_into_infill` (nhựa xả lộ ra bề mặt);
TOOL và TEST bật cả hai (nằm khuất bên trong, thu hồi được phần lớn nhựa purge).
Bảng đầy đủ ở cuối `profiles/process.md`.

### C5 📝 Bổ sung `tools/acslicer_tune.py`
| Thiếu | Để làm gì |
|---|---|
| `--unset "PRESET\|key"` | xoá key rác — chặn C2 |
| rule multi-material | kiểm tra kích thước flush matrix, số màu, thiết lập prime tower |
| `--diff "PRESET"` | so preset với cha, chỉ ra override vô nghĩa (trùng giá trị cha) |
| ghi `.conf` an toàn | tính lại MD5 ở dòng cuối — cần cho C3 |

---

## D. Đã xong trong các phiên trước

🟢 Sửa 8 giá trị mâu thuẫn: `nozzle_temperature_range_high` 210→215,
nhiệt độ bàn lớp đầu, `retract_restart_extra` −0.05→0, `z_hop` 0.1→0.4,
`support_top_z_distance` 0.16→0.2. Audit từ 3 lỗi xuống 0.
🟢 Nâng flow cap: `Anycubic PLA - Copy` 18, ba preset BBL PLA Lite 15.
🟢 Rollback 25 clamp tốc độ sai tầng — giới hạn flow thuộc filament preset,
slicer đã tự enforce lúc slice.
🟢 `tools/acslicer_tune.py` + `docs/tool.md`.
🟢 Tự động hoá 3.1–3.5: `CLAUDE.md`, `.gitignore`, allowlist quyền,
4 slash command, 2 hook (đã pipe-test 6/6).
🟢 `docs/device.md` viết lại từ config thật.
🟢 `docs/working-rules.md`, `docs/capabilities.md`, `profiles/process.md`.
