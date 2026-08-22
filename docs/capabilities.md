# Claude làm được gì, không làm được gì

Cơ chế tự động hoá và bố cục repo: `README.md`.
Quy tắc ai được sửa gì: `docs/working-rules.md`.

---

## 1. Không làm được — phần quan trọng nhất

| | Vì sao |
|---|---|
| ❌ Nói chuyện với máy in | Slicer đi qua `mqtts://mqtt-universe.anycubic.com:8883`, không phải LAN. Token có trong `.conf` nhưng không dùng. Máy in và máy tính hiện còn khác mạng WiFi |
| ❌ Xem camera, theo dõi print đang chạy | |
| ❌ Đo đùn thiếu/thừa, stringing, độ bám, ringing | chỉ bạn nhìn được vật in |
| ❌ Biết cuộn nhựa thật đang nạp | đọc `profiles/filament.md`; file sai thì sai theo |
| ❌ Nhớ phiên trước | mỗi phiên bắt đầu trắng — bù bằng `CLAUDE.md`, `TODO.md`, `git log` |

🟡 Hệ quả của ba dòng giữa: **mọi con số Claude đưa ra là suy từ config hoặc lấy
từ profile hãng, không phải đo trên máy bạn.** Rõ nhất ở
`filament_max_volumetric_speed` — luôn cần flow test xác nhận, không có ngoại lệ.

## 2. Làm được, nhưng cần bạn ra quyết định

| Việc | Chặn bởi |
|---|---|
| Tạo / xoá / đổi tên preset | cần bạn duyệt — `docs/working-rules.md` mục 3 |
| Đổi speed, flow, nhiệt độ, retraction | cần bạn duyệt |
| Tính flush matrix cho tổ hợp màu | cần slice thử 4 màu trước — A3 trong `TODO.md` |
| Soạn test print (temp tower, flow, retraction) | bạn in và đo |

## 3. Làm được ngay, không cần hỏi

Đọc và giải chuỗi kế thừa của toàn bộ kho preset (643 của hãng + 14 của bạn),
đối chiếu với giới hạn firmware và vật lý đùn nhựa, chỉ ra bạn đã đổi gì so với
bản gốc. Sửa các mâu thuẫn nội tại và dọn key rác. Đọc log slicer, đọc `.gcode`,
`.3mf`. Viết script xử lý hàng loạt. Giải thích một setting làm gì và đánh đổi ra sao.

## 4. Còn thủ công

**Việc của bạn, không tự động hoá được:** đóng slicer trước khi ghi, cập nhật
`profiles/filament.md` mỗi lần đổi cuộn, và in các bản test. Mục A trong `TODO.md`.

**Thiếu sót của công cụ:** chưa có `--unset`, chưa có rule multi-material, chưa
ghi được `.conf`. C5 trong `TODO.md`.
