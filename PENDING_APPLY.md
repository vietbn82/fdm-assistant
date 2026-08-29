# PENDING APPLY — thay đổi preset chờ duyệt

Kho chứa mọi thay đổi preset đã đề xuất nhưng **chưa ghi vào máy**.

## Tổng quan

| ID | Nhắm vào | Preset | Trạng thái |
|---|---|---|---|
| [P6](#p6) | tơ ở travel ngắn + không z-hop | machine | 📝 **đã gỡ chặn** |

**Cách dùng:** đọc, rồi nói ID nào được duyệt — `"apply P1 P4"`. Claude lấy đúng
những dòng đó, chạy lệnh ghi kèm backup, rồi ghi kết quả sang `CHANGELOG.md`.

- Mỗi dòng có sẵn lệnh chính xác. Duyệt xong là chạy được, không phải suy diễn lại.
- ❌ Claude không tự áp bất cứ dòng nào ở đây, kể cả khi thấy hiển nhiên.
- 🟡 Đóng slicer trước khi áp. Mọi lần ghi đều backup `user\` trước.
- `TODO.md` là *quyết định* cần đưa ra. File này là *thao tác* sẽ chạy khi đã quyết.

Trạng thái: 📝 chờ duyệt / ⏳ chờ điều kiện khác / 🔴 chặn kỹ thuật

🟢 P15–P21 đã xong ngày 29/08 — chi tiết trong `CHANGELOG.md`.

---

## Đang chờ

<a id="p6"></a>
### P6 ⏳ Bắt được travel ngắn ở đỉnh — machine preset

| Key | Hiện tại | Đặt |
|---|---|---|
| `retraction_minimum_travel` | 1 | **0.5** |

```
python tools/acslicer_tune.py --set "Anycubic Kobra X 0.4 nozzle - high quality|retraction_minimum_travel=0.5"
```

Bước nhảy ngắn hơn 1 mm hiện **không** rút nhựa — ở đỉnh model tiết diện nhỏ thì
gần như mọi bước nhảy đều ngắn hơn thế.

🟢 **Đã gỡ chặn.** Điều kiện đặt ra là "in một bản với P15, còn tơ thì chạy P6".
Bản in 29/08 đã chạy đủ P15 và **vẫn rất nhiều tơ**. Điều kiện thoả.

🔴 **Và nó còn giải thích triệu chứng thứ ba.** Z-hop chỉ xảy ra **kèm theo
retraction**. Travel ngắn hơn `retraction_minimum_travel` thì không rút, nên cũng
**không nhấc đầu in** — nozzle rê thẳng ngang qua bề mặt vừa in. Trên mặt trên
đầy travel ngắn, đó chính là vết xước.

Hạ xuống 0.5 làm cả hai việc cùng lúc: rút nhựa ở quãng ngắn, và bật z-hop ở
những quãng đó.

🟡 Đánh đổi khi chạy: số lần rút tăng, mài nhựa nhiều hơn ở một điểm.

---

Thao tác đã áp dụng: `CHANGELOG.md`.
