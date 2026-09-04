# TODO

> Mọi việc còn treo. Đây là các **quyết định** cần đưa ra.
> Thao tác preset cụ thể sẽ chạy sau khi quyết: `PENDING_APPLY.md`.
> Cập nhật: 2026-09-03.

## Tổng quan

| ID | Việc | Chặn bởi |
|---|---|---|
| A10 | Kẹt nhựa thường xuyên slot 4 khi in — chưa rõ nguyên nhân | Viet kiểm tay phần cứng |
| B2 | `filament_flow_ratio` trở về 0.96 sau khi dựng lại preset — cố ý hay bỏ sót? | Viet chốt |
| B3 | Ba bản FIGURE lệch nhau ở infill pattern / shell layers (do cha) — pin cho khớp hay để nguyên? | Viet chốt |
| B4 | TOOL 0.20 mất bộ override độ bền (`wall_loops` 4→2, infill 25%→15%) — cố ý hay bỏ sót? | Viet chốt |

Ký hiệu: ⏳ chờ / 📝 chưa bắt đầu / 🔴 chặn việc khác

---

## A. Chỉ Viet làm được

### A10 — Kẹt nhựa thường xuyên slot 4, chưa rõ nguyên nhân

Loại được nghẹt cứng đầu nozzle (load tay vẫn ra nhựa bình thường, chỉ lúc in
mới không ra). slot 2 dùng chung preset `PLA Generic@KX 0.4`, không lỗi → không
nghi preset.

Cần Viet kiểm tay, Claude không xem/đo phần cứng được:

1. Vết mòn/bột nhựa quanh bánh răng đùn (nghi nghiến nhựa khi rút/đẩy đổi màu)
2. Tiếng click lặp ở motor đùn lúc lỗi xảy ra
3. Cuộn slot 4 có bị rối trên trục, ống dẫn có gập không
4. Lỗi rơi vào lúc nào: đầu bản in hay sau N lần đổi màu vào slot 4

P31 (02/09, `CHANGELOG.md`) đã bỏ `machine_end_gcode` theo yêu cầu Viet nhưng
không chắc liên quan — đoạn đó chỉ chạy sau khi in xong.

---

## B. Cần Viet chốt

Cả ba mục dưới sinh ra từ đợt dựng lại preset ngày 03/09 trên slicer 2.0.0.2.
🟢 Bộ preset trên máy đang là chuẩn — đây là **hỏi cho rõ ý định**, không phải
đề xuất khôi phục. Chốt xong mục nào thì mới chuyển thành dòng trong
`PENDING_APPLY.md`.

### B2 — `filament_flow_ratio` 1.0 → 0.96 (kế thừa)

Bộ cũ pin 1.0 trên cả hai filament preset (P14, áp lại bằng P15 ngày 29/08).
Đó chính là bản sửa đã chữa **thiếu nhựa / tường mỏng**. Giờ không còn pin, giá
trị hãng 0.96 có hiệu lực — đùn ít hơn 4%.

- Nếu là chủ ý (muốn preset mỏng, chấp nhận số hãng): 🟢 không làm gì
- Nếu bỏ sót: pin lại `filament_flow_ratio = 1` cho cả hai preset

🟡 Triệu chứng nếu sai: tường mỏng, mặt trên hở khe, lớp bám kém.

### B3 — Ba bản FIGURE lệch nhau ba khoá, đều do cha

| | 0.12 | 0.16 | 0.20 |
|---|---|---|---|
| `sparse_infill_pattern` | 3dhoneycomb | gyroid | gyroid |
| `top_shell_layers` | 5 | 6 | 5 |
| `bottom_shell_layers` | 5 | 4 | 3 |

Pin cho khớp thì thêm override vào preset vừa dọn sạch; để nguyên thì ba bản
FIGURE cho kết quả hơi khác nhau. Bộ cũ chọn pin cho khớp.

### B4 — TOOL 0.20 không còn khác Standard bao nhiêu

Bỏ so với bộ cũ: `wall_loops` 4→2, `wall_sequence` inner-outer-inner→mặc định,
`sparse_infill_density` 25%→15%, `bottom_shell_layers` 4→3, `outer_wall_speed`
120→200, `flush_into_objects/_infill` 1→0.

Preset TOOL giờ gần bằng `0.20mm Standard` của hãng. Đồ dùng chịu lực in bằng nó
sẽ yếu hơn hẳn so với trước 03/09.

---

## C. Hàng đợi của tôi

*(trống)*

---

Việc đã xong: `CHANGELOG.md`. Quy ước làm việc: `docs/working-rules.md`.
