# PENDING APPLY — thay đổi preset chờ duyệt

Kho chứa mọi thay đổi preset đã đề xuất nhưng **chưa ghi vào máy**.

## Tổng quan

| ID | Nhắm vào | Preset | Trạng thái |
|---|---|---|---|
| P32 | `purge_in_prime_tower = 1` | `Kobra X 0.4 - MultiColor` | 📝 chờ duyệt |

🔵 03/09: Viet dựng lại toàn bộ preset trên slicer 2.0.0.2, bộ trên máy là chuẩn.
Ba điểm cần Viet chốt ý định (B2 flow_ratio, B3 FIGURE lệch nhau, B4 TOOL mất
override độ bền) nằm ở `TODO.md` — chỉ khi chốt xong mới thành dòng ở đây.

**Cách dùng:** đọc, rồi nói ID nào được duyệt — `"apply P1 P4"`. Claude lấy đúng
những dòng đó, chạy lệnh ghi kèm backup, rồi ghi kết quả sang `CHANGELOG.md`.

- Mỗi dòng có sẵn lệnh chính xác. Duyệt xong là chạy được, không phải suy diễn lại.
- ❌ Claude không tự áp bất cứ dòng nào ở đây, kể cả khi thấy hiển nhiên.
- 🟡 Đóng slicer trước khi áp. Mọi lần ghi đều backup `user\` trước.
- `TODO.md` là *quyết định* cần đưa ra. File này là *thao tác* sẽ chạy khi đã quyết.

Trạng thái: 📝 chờ duyệt / ⏳ chờ điều kiện khác / 🔴 chặn kỹ thuật

🟢 P15–P21 (29/08); P6, P25, P25-v2, P27 (0.36→0.32), P28, P29, P30, P26
(30/08) đã xong — chi tiết trong `CHANGELOG.md`. P25 hoá ra sai thứ tự, P25-v2
sửa lại và đã áp. P28 (hạ nhiệt 200) không giúp tơ và bị nghi hại mặt trên, P29
trả lại 205. P30 bật `purge_in_prime_tower` — bằng chứng trực tiếp là purge bị
bỏ qua sau đổi màu khi FIGURE in không support. P26 tăng `retraction_length`
lên 1.8 cho tơ còn sót ở chi tiết nhỏ.

---

## P32 — bật lại `purge_in_prime_tower` (chỉ sửa được bằng file)

🔴 **Khoá này không có trong UI của slicer 2.0.0.2** — không phải Viet tìm sót.
Xem mục "Vì sao không thấy trên UI" trong `docs/preset-model.md` mục 8.

Đây là khoá P30 (30/08) từng bật vì bằng chứng đọc từ gcode: khi in nhiều màu
mà bản in **không có support**, không còn đường xả hợp lệ nên purge sau đổi màu
bị bỏ qua hoàn toàn. Đợt dựng lại 03/09 làm mất override này.

Chỉ áp cho bản MultiColor — in một màu không có đổi màu nên khoá vô nghĩa.

```bash
python tools/acslicer_tune.py --set "Kobra X 0.4 - MultiColor|purge_in_prime_tower=1"
```

🟡 Điều kiện: đóng slicer trước. Công cụ tự backup `user\` và bump `updated_time`.

🔵 Cách kiểm sau khi áp: slice một mẫu 4 màu không support, tìm khối purge trong
gcode ngay sau mỗi lệnh đổi màu.

---

Thao tác đã áp dụng: `CHANGELOG.md`.
