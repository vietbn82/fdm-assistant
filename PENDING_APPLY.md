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

| ID | Preset | Key | Hiện tại | Đề xuất | Điều kiện |
|---|---|---|---|---|---|
| P1 ⏳ | `PLA BBL Lite@KX 0.4` | `filament_max_volumetric_speed` | `15` | `13` | **chỉ khi flow test A1 thất bại** |

```bash
# P1
python tools/acslicer_tune.py --set "PLA BBL Lite@KX 0.4|filament_max_volumetric_speed=13"
```

### P2 📝 Giảm nhẹ lỗi first layer — process TOOL

⚠️ **Đây chỉ là giảm nhẹ, không phải chữa gốc.** Thiếu nhựa theo đốm là do
khoảng cách nozzle–bàn không đều. Level bàn / chỉnh z-offset trước; chỉ áp P2
nếu sau khi level vẫn còn.

| Key | Hiện tại | Đề xuất | Vì sao |
|---|---|---|---|
| `initial_layer_speed` | `50` | `30` | chậm hơn thì nhựa có thời gian ép xuống, che được sai lệch nhỏ của bàn |

```bash
python tools/acslicer_tune.py --set "Novi 0.20 - TOOL @AC KX|initial_layer_speed=30"
```

---

Thao tác đã áp dụng: `CHANGELOG.md`.
