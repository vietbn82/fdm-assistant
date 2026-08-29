# Quy tắc làm việc — Viet ↔ Claude

Sửa thẳng vào file này. Claude đọc lại mỗi phiên qua `CLAUDE.md`.

---

## 1. Ai sửa cái gì

| Nơi | Vai trò | Tần suất đổi | Ai sửa |
|---|---|---|---|
| `TODO.md` | quyết định còn treo — đọc đầu mỗi phiên | thường xuyên | cả hai |
| `PENDING_APPLY.md` | thao tác preset chờ duyệt | thường xuyên | Claude ghi, Viet duyệt |
| `CHANGELOG.md` | việc đã xong, mới nhất lên trên | mỗi lần xong việc | Claude |
| `presets/` | bản sao preset thật, để có lịch sử git | tự động | ❌ không sửa tay — sinh ra từ `--export` |
| `profiles/` | trạng thái máy hiện tại | theo mỗi lần chỉnh máy | cả hai |
| `profiles/filament.md` | cuộn nhựa đang nạp | mỗi lần đổi cuộn | **Viet** — Claude không tự biết được |
| `docs/` | kiến thức nền, quy tắc | hiếm | cả hai |
| `tools/` | công cụ đọc/sửa preset | hiếm | Claude |
| `.claude/` | quyền, hook, slash command | hiếm | Claude, khi được yêu cầu |
| `%APPDATA%\...\user\` | preset thật | — | chỉ qua `tools/acslicer_tune.py` |
| `%APPDATA%\...\system\` | preset hãng | — | ❌ không bao giờ |

🔵 Ranh giới `docs/` ↔ `profiles/` là **tần suất đổi**, không phải chủ đề. Số
liệu mô tả trạng thái máy hiện tại thuộc `profiles/`; kiến thức đúng bất kể máy
đang cấu hình thế nào thuộc `docs/`. Sửa preset xong thì cập nhật `profiles/`.

## 2. Quy trình ghi preset

Bắt buộc, không ngoại lệ. Bốn cái bẫy đằng sau quy trình này ở
`docs/preset-model.md` mục 5.

1. **Kiểm tra slicer đã đóng.** Đang chạy thì dừng, báo Viet đóng. Không tự kill
   process trừ khi được cho phép trong chính lượt đó.
2. **Backup toàn bộ `user\`** trước mọi lần ghi, tên có timestamp.
3. **Bump `updated_time`** trong `.info` của mọi file đã sửa.
4. **Báo đường dẫn backup** trong câu trả lời, để revert được ngay.

## 3. Tự làm vs phải hỏi

| Loại thay đổi | |
|---|---|
| Mâu thuẫn nội tại — nhiệt vượt range đã khai, accel vượt firmware, support gap không chia hết layer height | ✅ tự làm |
| Xoá key rác từ preset copy (`pellet_flow_coefficient`, giá trị `nil`) | ✅ tự làm |
| Speed, flow, nhiệt độ, retraction — bất cứ thứ gì đổi chất lượng in | ⚠️ hỏi trước |
| `filament_max_volumetric_speed` | ⚠️ hỏi trước, và luôn cần flow test |
| Tạo hoặc xoá preset | ⚠️ hỏi trước |
| Ghi `.conf` | ⚠️ hỏi, và phải tính lại MD5 |
| Sửa `system\` | ❌ không bao giờ — hook chặn |
| `git add` / `commit` / `push` cho `docs/`, `tools/`, `.claude/`, file gốc | ❌ không tự làm, kể cả khi vừa xong việc |
| Commit + push `presets/` | ✅ tự làm, **chỉ qua `tools/preset_autocommit.py`** |

## 4. Đặt giá trị đúng tầng

| Thuộc về | Tầng |
|---|---|
| Trần flow, nhiệt độ | filament preset |
| Giới hạn động học, retraction | machine preset |
| Hình học, tốc độ, chiến lược purge | process preset |

Bảng đầy đủ và các trường hợp dễ nhầm: `docs/preset-model.md` mục 3.

❌ Không hạ speed của process cho khớp trần flow của một loại nhựa — slicer đã tự
enforce lúc slice, mà cái pin đó sống lâu hơn cuộn nhựa.

❌ Không pin một key vốn đang kế thừa chỉ để "cho chắc". Preset user càng mỏng
càng dễ theo kịp khi hãng cập nhật profile gốc.

## 5. Cách trả lời

- Tiếng Việt, trừ khi Viet hỏi bằng tiếng Anh.
- Thuật ngữ, tên key, tên preset, lệnh CLI, thông báo lỗi: **giữ nguyên gốc**.
- Bullet và bảng trước, văn xuôi sau. Ngắn.
- Icon: 🟢 xong 🔴 lỗi 🟡 rủi ro 🔵 thông tin 📝 todo ⏳ chờ ❌ đừng.
- Kết thúc bằng **⚠️ ACTION REQUIRED**, hoặc ghi "None".

Ngôn ngữ theo thư mục: `docs/` tiếng Việt (Viet đọc). `CLAUDE.md`, `.claude/`,
`README.md` tiếng Anh (chỉ thị cho model, và repo là public).

## 6. Xử lý tình huống

**Viet chọn nhiều đáp án mâu thuẫn** — đừng hỏi lại vòng vo. Tự chọn cách hiểu
hợp lý nhất, nói rõ đã hiểu thế nào và vì sao, rồi làm. Có phương án loại trừ
nhau thì ưu tiên cái ít rủi ro hơn và nêu cái bị bỏ.

**Phát hiện việc đã làm là sai** — sửa ngay trong cùng lượt, nói thẳng sai chỗ
nào, không dài dòng xin lỗi. Có backup thì rollback trước, giải thích sau.

**Đưa số liệu** — ghi rõ nguồn: đọc từ config / lấy từ profile hãng / là ước
lượng. ❌ Không trình bày kinh nghiệm chung như thể đã đo trên máy này.

**Preset trong slicer khác với `presets/` trong git** — 🟢 **slicer thắng**.
Kho preset đang chạy là nguồn sự thật; `presets/` chỉ là bản sao để theo dõi
lịch sử. ❌ Không tự khôi phục từ git hay từ `user_backup-*/` để "sửa" lệch.
Chạy `--export` cho git bám theo slicer, rồi báo cái gì đã đổi.

🔵 Chốt ngày 26/08 sau vụ `058b051` ghi đè loạt sửa ngày 23. Lý do: Viet chỉnh
trong UI thường xuyên, và không có cách nào phân biệt "cloud sync ghi đè" với
"Viet vừa đổi ý" chỉ bằng cách nhìn file. Đoán sai theo hướng khôi phục sẽ xoá
mất việc Viet vừa làm; đoán sai theo hướng giữ thì chỉ mất một bản sửa đã ghi
trong `CHANGELOG.md` và áp lại được.

🟡 Vẫn phải **báo** khi thấy lệch — giữ không có nghĩa là im lặng. Cách phân biệt
lệch thật với lệch giả: xem `CHANGELOG.md` mục "Phân biệt slicer bỏ key với
preset bị revert".

## 7. Bảo mật

`AnycubicSlicerNext.conf` chứa token cloud đã mã hoá và `current_device_id`.
Không in ra, không đưa vào `.md`, không commit. Trích `.conf` thì lọc bỏ
`anycubic_cloud` và `anycubic_remote_printing`.

🟡 Remote GitHub là **public**. `.gitignore` đã chặn `*.conf`, `user_backup-*/`,
`log/`, `crash/`.

❌ Không gửi gì ra ngoài — cloud, web, share link — khi chưa hỏi.

## 8. Việc còn treo

`TODO.md` là nguồn duy nhất. Đừng chép danh sách sang chỗ khác, hai bản sẽ lệch.
Xong việc nào thì chuyển sang `CHANGELOG.md` trong cùng lượt, đừng để tích lại.

## 9. Hai PC, và cloud sync đã tắt trên cả hai

Viet in bằng **2 PC**, cùng tài khoản `855643`. Từ 29/08 cả hai đều đặt
Preferences → *Auto sync user presets* = **off** (`app.sync_user_preset = False`
trong `.conf`).

Lý do: ngày 27/08 toàn bộ P8–P11 và P14 bị trả về giá trị cũ, cả `.json` lẫn
`.info`. Không chứng minh được thủ phạm là cloud hay một lần khôi phục backup cục
bộ, nên tắt sync là cách cắt bớt bề mặt rủi ro.

Hệ quả phải nhớ:

- ❌ Preset **không** tự lan sang PC kia nữa. Đừng giả định nó đã có bản mới
- Chuyển tay: copy **cả cặp** `.json` + `.info` từ `presets/` trong git sang
  `%APPDATA%\AnycubicSlicerNext\user\855643\`. Thiếu `.info` thì preset bị coi là
  cũ hơn thực tế
- ❌ Đừng đổi tên `user_backup-*` thành `user` trừ khi cố ý revert — đó là một
  trong hai giả thuyết cho vụ 27/08
- 🔴 Chạy `python tools/acslicer_tune.py --check-drift` **ngay trước khi in**.
  Lần trước mất trọn một bản in mới phát hiện preset đã bị trả về giá trị cũ

## 10. Đổi tên preset

Slicer đổi tên bằng cách ghi file mới và xoá file cũ, đồng thời cập nhật
`filament_settings_id` / `print_settings_id` bên trong. Sau mỗi lần Viet đổi tên:

- Quét lại `profiles/`, `TODO.md`, `PENDING_APPLY.md`, `docs/` và sửa mọi chỗ nhắc
  tên cũ
- ❌ **Không sửa `CHANGELOG.md`.** Mục cũ ghi tên preset lúc thao tác diễn ra;
  sửa lại là viết lại lịch sử. Thêm một dòng ghi nhận việc đổi tên là đủ
