# Quy tắc làm việc — Viet ↔ Claude

> Bản nháp để review. Sửa thẳng vào file, tôi đọc lại mỗi phiên.
> Muốn tôi tự nạp file này mỗi lần khởi động: xem `CAPABILITIES.md` mục
> "Biến file này thành luật thật sự".

---

## 1. Phạm vi dự án

Repo này quản lý **cấu hình Anycubic Slicer Next cho Kobra X**, không phải code
sản phẩm. Nguồn sự thật nằm ở hai chỗ tách biệt:

| Nơi | Vai trò | Ai sửa |
|---|---|---|
| `C:\WS\ACSlicerNext\*.md` | tài liệu, ý định, quy tắc | cả hai |
| `C:\WS\ACSlicerNext\*.py` | công cụ đọc/sửa preset | Claude |
| `%APPDATA%\AnycubicSlicerNext\user\` | preset thật | chỉ qua công cụ |
| `%APPDATA%\AnycubicSlicerNext\system\` | preset hãng | ❌ không bao giờ sửa |

---

## 2. Trước khi ghi vào preset

Bắt buộc, không có ngoại lệ:

1. **Kiểm tra slicer đã đóng chưa.** Đang chạy → dừng lại, báo tôi đóng. Không
   tự kill process trừ khi tôi cho phép rõ ràng trong lượt đó.
2. **Backup toàn bộ `user\`** trước mọi lần ghi. Tên có timestamp.
3. **Bump `updated_time`** trong `.info` của mọi file đã sửa.
4. **Báo lại đường dẫn backup** trong câu trả lời, để tôi revert được ngay.

## 3. Thay đổi nào được tự làm, thay đổi nào phải hỏi

| Loại | Tự làm | Hỏi trước |
|---|---|---|
| Sửa mâu thuẫn nội tại (temp vượt range đã khai, accel vượt firmware, support gap không chia hết layer height) | ✅ | |
| Xoá key rác từ preset copy (`pellet_flow_coefficient`, `nil`) | ✅ | |
| Đổi giá trị ảnh hưởng chất lượng in (speed, flow, nhiệt độ, retraction) | | ✅ |
| Đổi `filament_max_volumetric_speed` | | ✅ — luôn cần flow test |
| Tạo preset mới | | ✅ |
| Sửa file trong `system\` | ❌ không bao giờ | |
| Ghi lại `.conf` | ❌ trừ khi tính lại MD5 và tôi đồng ý | |

## 4. Nguyên tắc đặt giá trị đúng tầng

❌ Không nhét giới hạn của một loại nhựa vào process preset.
✅ Giới hạn flow thuộc filament preset. Giới hạn động học thuộc machine preset.
Process preset chỉ chứa ý đồ hình học và tốc độ mong muốn.

❌ Không pin một key vốn đang kế thừa, chỉ để "cho chắc". Preset user càng mỏng
càng dễ theo kịp khi hãng cập nhật profile gốc.

## 5. Cách trả lời

- Tiếng Việt, trừ khi tôi hỏi bằng tiếng Anh.
- Thuật ngữ kỹ thuật, tên key, tên preset, lệnh CLI, thông báo lỗi: **giữ
  nguyên gốc**, không dịch.
- Ngắn gọn. Bullet và bảng trước, văn xuôi sau.
- Icon trạng thái: 🟢 xong 🔴 lỗi 🟡 rủi ro 🔵 thông tin 📝 việc cần làm
  ⏳ đang chờ ❌ đừng làm.
- Kết thúc mọi câu trả lời bằng mục **⚠️ ACTION REQUIRED** — việc cần tôi làm,
  hoặc ghi rõ "None".

## 6. Khi tôi chọn nhiều đáp án mâu thuẫn

Đừng hỏi lại vòng vo. Tự chọn cách hiểu hợp lý nhất, **nói rõ đã hiểu thế nào
và vì sao**, rồi làm. Nếu có phương án loại trừ nhau, ưu tiên cái ít rủi ro hơn
và nêu cái bị bỏ.

## 7. Khi phát hiện việc đã làm là sai

Sửa ngay trong cùng lượt, nói thẳng cái gì sai và tại sao, không dài dòng xin
lỗi. Đã có backup thì rollback trước, giải thích sau.

## 8. Đừng làm

- ❌ Đoán thông số máy. Đọc từ config hoặc hỏi tôi.
- ❌ Đưa số liệu "kinh nghiệm chung" như thể đã đo trên máy tôi. Ghi rõ nguồn:
  đọc từ config / lấy từ profile hãng / là ước lượng.
- ❌ Đề xuất mà không nói rủi ro đi kèm.
- ❌ Xoá đệ quy thư mục. Copy đè hoặc rename, để tôi tự dọn.
- ❌ Gửi bất cứ thứ gì ra ngoài (cloud, web, share link) khi chưa hỏi. Config có
  token đăng nhập và user id.

## 9. Dữ liệu nhạy cảm

`AnycubicSlicerNext.conf` chứa token cloud đã mã hoá và `current_device_id`.
Không in ra, không đưa vào file `.md`, không upload. Khi cần trích `.conf` thì
lọc bỏ mọi key thuộc `anycubic_cloud` và `anycubic_remote_printing`.

## 10. Trạng thái đang chờ

| Việc | Trạng thái | Ai |
|---|---|---|
| Flow test xác nhận `BBL PLA Lite` ở 15 mm³/s | ⏳ chờ in | Viet |
| Cấu hình flush matrix 4×4 cho 4 màu | 📝 chưa bắt đầu | cần Viet chốt |
| `0.12 mm High Quality` bottom shell 0.36 mm (3 layer) | 📝 chờ quyết định | Viet |
| Slot 2 (Generic PLA trắng) chưa có filament preset riêng | 📝 chưa bắt đầu | cần Viet chốt |
