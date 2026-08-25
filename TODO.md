# TODO

> Mọi việc còn treo. Đây là các **quyết định** cần đưa ra.
> Thao tác preset cụ thể sẽ chạy sau khi quyết: `PENDING_APPLY.md`.
> Cập nhật: 2026-08-25.

Ký hiệu: ⏳ chờ / 📝 chưa bắt đầu / 🔴 chặn việc khác

---

## A. Chỉ Viet làm được

### A1 ⏳ Xác nhận trần flow 13 mm³/s có đủ không
`filament_max_volumetric_speed` đang để **13** — mặc định hãng, an toàn nhưng
chưa đo. Trước đó để 15 (trần Bambu công bố cho PLA Lite), đã hạ xuống 13.

- In một vật thành mỏng, xem tường có bị đùn thiếu không
- 🟢 Đã hạ về 13 sẵn (2026-08-24). Test giờ để xác nhận **13 có đủ không**,
  không phải 15 có quá không. Thấy thiếu nhựa thì báo, còn dư địa ở flow ratio

---

### A2 🔴 Chặn preset bị revert lần nữa
Commit `058b051` ghi đè loạt sửa ngày 23 bằng giá trị cũ. Nghi cloud sync kéo bản
trên mây đè bản local, hoặc slicer ở máy kia đẩy lên.

- 🔵 P1–P3 đã áp lại ngày 25/08. Mở slicer, **kiểm tra bằng mắt** nhiệt bàn = 60
- Nếu lại về 45: tắt sync profile trong Preferences rồi thử lại
- `python tools/acslicer_tune.py --check-drift` so được live với `presets/`

---

## B. Cần Viet chốt

### B1 📝 `initial_layer_print_height` cho `Novi 0.12 - FIGURE`
Bản 0.16 bạn đặt lớp đầu = 0.16, tức bằng chính layer height. Áp logic đó cho
0.12 thì lớp đầu còn 0.12 mm.

- Đang giữ **0.2** — dày hơn layer height, dung sai bám bàn tốt hơn
- Muốn thống nhất "lớp đầu = layer height" thì nói, tôi đặt 0.12
- 🟡 Vừa sửa xong lỗi bong bàn, hạ lớp đầu là đi ngược hướng đó

---

## C. Hàng đợi của tôi

*(trống)*

---

Việc đã xong: `CHANGELOG.md`. Quy ước làm việc: `docs/working-rules.md`.
