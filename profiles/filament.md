# Filament preset — tầng filament

**Viet cập nhật file này mỗi lần đổi cuộn.** Claude không có cách nào tự biết.
Sai ở đây thì mọi tư vấn nhiệt độ, flow, flush đều sai theo.

Tầng nào sở hữu gì: `docs/preset-model.md` mục 3.

---

## Cuộn đang nạp

| Slot | Loại | Sản phẩm | Màu | Hex | Mở túi | Đã sấy |
|---|---|---|---|---|---|---|
| 1 | PLA | Bambu Lab PLA Lite | Red | — | — | — |
| 2 | PLA | Generic | White | — | — | — |
| 3 | PLA | Bambu Lab PLA Lite | Black | — | — | — |
| 4 | PLA | Bambu Lab PLA Lite | Cyan | — | — | — |

`—` = chưa ghi. Điền được thì tốt hơn:

- **Hex** — cần để tính `flush_volumes_matrix` 4×4. Cặp tối↔sáng tốn nhiều nhựa
  purge hơn hẳn cặp cùng tông.
- **Mở túi / Đã sấy** — 🟡 ẩm là nguyên nhân số một của lỗi in PLA mà triệu
  chứng nhìn hệt lỗi setting. Trước khi chỉnh preset vì stringing hay bề mặt
  xấu, kiểm tra cái này trước.

## Preset tương ứng

| Slot | Preset | Trần flow |
|---|---|---|
| 1, 3, 4 | `BBL PLA Lite @Anycubic Kobra X 0.4 nozzle` | 15 mm³/s ⏳ chưa test |
| 2 | `Anycubic PLA @Kobra X` *(stock)* | 13 mm³/s |

📝 Slot 2 chưa có preset riêng — ba lựa chọn ở B4 trong `TODO.md`.

## Toàn bộ filament preset của bạn

| Preset | Trần flow | Dùng ở slot | Ghi chú |
|---|---|---|---|
| `BBL PLA Lite @Anycubic Kobra X 0.4 nozzle` | 15 | 1, 3, 4 | 🟢 bàn lớp đầu đã sửa 45 → 50 |
| `BBL PLA Lite` | 15 | — | 🟢 `nozzle_temperature_range_high` 210 → 215, bàn lớp đầu 45 → 50 |
| `BBL PLA Lite - High Quantity @Anycubic Kobra X 0.4 nozzle` | 15 | — | `adaptive_pressure_advance` bật, `pressure_advance` 0.025 |
| `Anycubic PLA @Anycubic Kobra X 0.4 nozzle - Copy` | 18 | — | 📝 không dùng ở đâu — P4 trong `PENDING_APPLY.md`. Còn sót `pellet_flow_coefficient` (P13) |
| `Anycubic PLA @Anycubic Kobra S1 0.4 nozzle - Copy` | *(kế thừa)* | — | máy khác, không liên quan |

Cả bốn preset PLA Lite/PLA đều kế thừa `Anycubic PLA @Kobra X`.

## Trần flow — trạng thái

| | Giá trị | Nguồn |
|---|---|---|
| `Anycubic PLA @Kobra X` *(stock)* | 13 mm³/s | hãng |
| `Anycubic PLA High Speed @Kobra X` *(stock)* | 18 mm³/s | hãng — trần thực tế của hotend này |
| Ba preset BBL PLA Lite | 15 mm³/s | ⏳ **chưa đo**, là trần Bambu công bố cho PLA Lite |

⏳ A1 trong `TODO.md`: in flow test xác nhận 15 mm³/s. Thành wall đùn thiếu thì
hạ về 13 — lệnh sẵn ở P5–P7 trong `PENDING_APPLY.md`.
