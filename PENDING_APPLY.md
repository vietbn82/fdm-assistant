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

### 🔴 Scarf joint đang gần như không chạy

`seam_slope_type = external` trông như đã bật, nhưng hai khoá khác vô hiệu hoá nó
trên phần lớn đường viền — cùng loại lỗi với `small_perimeter_threshold = 0`:

| Key | Hiện tại | Hệ quả |
|---|---|---|
| `seam_slope_conditional` | 1 | chỉ áp scarf khi điều kiện góc thoả — nhiều seam bị bỏ qua |
| `seam_slope_min_length` | 10 | đường viền ngắn hơn 10 mm **không** có scarf |

Với figure nhiều chi tiết nhỏ, đa số đường viền dưới 10 mm. Nghĩa là chúng vẫn
khép vòng theo kiểu cũ — đúng chỗ sinh cục nhựa.

### P6 📝 Bắt được travel ngắn ở đỉnh — machine preset

| Key | Hiện tại | Đặt |
|---|---|---|
| `retraction_minimum_travel` | 1 | **0.5** |

```
python tools/acslicer_tune.py --set "Anycubic Kobra X 0.4 nozzle - high quality|retraction_minimum_travel=0.5"
```

Bước nhảy ngắn hơn 1 mm hiện **không** rút nhựa — ở đỉnh model tiết diện nhỏ thì
gần như mọi bước nhảy đều ngắn hơn thế.

### P7 📝 Cho scarf joint chạy thật — cả 4 process

| Key | Hiện tại | Đặt | Vì sao |
|---|---|---|---|
| `seam_slope_conditional` | 1 | **0** | áp scarf mọi seam, không chờ điều kiện góc |
| `seam_slope_min_length` | 10 | **5** | phủ được các đường viền nhỏ |
| `scarf_joint_flow_ratio` | 1 | **0.95** | bớt nhựa ở đoạn chồng của scarf |

```
python tools/acslicer_tune.py --set "Novi 0.12 - FIGURE @AC KX|seam_slope_conditional=0" --set "Novi 0.16 - FIGURE @AC KX|seam_slope_conditional=0" --set "Novi 0.20 - TOOL @AC KX|seam_slope_conditional=0" --set "Novi 0.28 - TEST @AC KX|seam_slope_conditional=0" --set "Novi 0.12 - FIGURE @AC KX|seam_slope_min_length=5" --set "Novi 0.16 - FIGURE @AC KX|seam_slope_min_length=5" --set "Novi 0.20 - TOOL @AC KX|seam_slope_min_length=5" --set "Novi 0.28 - TEST @AC KX|seam_slope_min_length=5" --set "Novi 0.12 - FIGURE @AC KX|scarf_joint_flow_ratio=0.95" --set "Novi 0.16 - FIGURE @AC KX|scarf_joint_flow_ratio=0.95" --set "Novi 0.20 - TOOL @AC KX|scarf_joint_flow_ratio=0.95" --set "Novi 0.28 - TEST @AC KX|scarf_joint_flow_ratio=0.95"
```

🟡 Scarf trên góc nhọn có thể làm cạnh hơi tròn. Với FIGURE là đánh đổi đáng;
thấy cạnh mất sắc thì trả `seam_slope_conditional` về 1.

### P8 📝 Rút nhựa dứt khoát hơn — machine preset

| Key | Hiện tại | Đặt | Vì sao |
|---|---|---|---|
| `retraction_speed` | 35 | **45** | rút nhanh thì sợi đứt gọn, không kéo dài |
| `retract_before_wipe` | 70% | **100%** | rút hết trước khi lau, không còn áp suất để rỉ ra trong lúc lau |

```
python tools/acslicer_tune.py --set "Anycubic Kobra X 0.4 nozzle - high quality|retraction_speed=45" --set "Anycubic Kobra X 0.4 nozzle - high quality|retract_before_wipe=100%"
```

❌ Không tăng `retraction_length` quá 1.2. Direct drive, đường ống ngắn — rút dài
hơn chỉ hút không khí vào nozzle, gây thiếu nhựa ở đầu đường kế tiếp.

### P9 📝 Đổi kiểu z-hop — machine preset

| Key | Hiện tại | Đặt |
|---|---|---|
| `z_hop_types` | Slope Lift | **Normal Lift** |

```
python tools/acslicer_tune.py --set "Anycubic Kobra X 0.4 nozzle - high quality|z_hop_types=Normal Lift"
```

Slope Lift nâng chéo, nozzle còn quét ngang sát mặt in trong lúc lên — kéo theo
phần nhựa rỉ. Normal Lift lên thẳng rồi mới đi.

🟡 Chậm hơn một chút vì mất chuyển động chéo. Áp riêng nếu muốn đo tác dụng.

---

Thao tác đã áp dụng: `CHANGELOG.md`.
