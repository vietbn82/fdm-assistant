# PENDING APPLY — thay đổi preset chờ duyệt

Kho chứa mọi thay đổi preset đã đề xuất nhưng **chưa ghi vào máy**.

**Cách dùng:** đọc, rồi nói ID nào được duyệt — `"apply P1 P4"`. Claude lấy đúng
những dòng đó, chạy lệnh ghi kèm backup, rồi ghi kết quả sang `CHANGELOG.md`.

- Mỗi dòng có sẵn lệnh chính xác. Duyệt xong là chạy được, không phải suy diễn lại.
- ❌ Claude không tự áp bất cứ dòng nào ở đây, kể cả khi thấy hiển nhiên.
- 🟡 Đóng slicer trước khi áp. Mọi lần ghi đều backup `user\` trước.
- `TODO.md` là *quyết định* cần đưa ra. File này là *thao tác* sẽ chạy khi đã quyết.

Trạng thái: 📝 chờ duyệt / ⏳ chờ điều kiện khác / 🔴 chặn kỹ thuật

---

## Đang chờ

### P6 📝 Bắt được travel ngắn ở đỉnh — machine preset

| Key | Hiện tại | Đặt |
|---|---|---|
| `retraction_minimum_travel` | 1 | **0.5** |

```
python tools/acslicer_tune.py --set "Anycubic Kobra X 0.4 nozzle - high quality|retraction_minimum_travel=0.5"
```

Ở đỉnh model tiết diện nhỏ, các bước nhảy ngắn hơn 1 mm hiện **không** rút nhựa
— đó là chỗ sinh tơ. Hạ ngưỡng để chúng cũng được rút.

🟡 Đánh đổi: số lần rút tăng, mài nhựa nhiều hơn ở một điểm. Cố ý để riêng: in
thử với P1–P5 trước đã, vì nozzle vừa làm sạch nên phần tơ có thể đã tự hết.

---

Thao tác đã áp dụng: `CHANGELOG.md`.
