# TODO

> Mọi việc còn treo. Đây là các **quyết định** cần đưa ra.
> Thao tác preset cụ thể sẽ chạy sau khi quyết: `PENDING_APPLY.md`.
> Cập nhật: 2026-08-29.

## Tổng quan

| ID | Việc | Ai làm | Chặn cái gì |
|---|---|---|---|
| [A2](#a2) 🔴 | Hiệu chuẩn Pressure Advance | Viet, trong slicer | nhựa thừa ở seam — không setting nào thay được |
| [C3](#c3) 🔴 | In thử **1 màu** sau P19–P21 | Viet in | nghiệm thu, và P6 |
| [C2](#c2) ⏳ | Nghiệm thu P16 — retract cuối bản in | Viet chưa báo | giữ hay revert P16 |

Ký hiệu: ⏳ chờ / 📝 chưa bắt đầu / 🔴 chặn việc khác

---

## A. Chỉ Viet làm được

<a id="a2"></a>
### A2 🔴 Hiệu chuẩn Pressure Advance — giờ là việc quan trọng nhất
`pressure_advance = 0.036` kế thừa từ preset hãng, chưa bao giờ đo. Nó chi phối
lượng nhựa ở đầu và cuối mỗi đường in — tức chi phối trực tiếp **triệu chứng 2**
của bản in 29/08: nhựa thừa kéo dài ở chỗ ngắt.

- Slicer có sẵn: Calibration → Pressure Advance
- 🔵 P15 đã tắt scarf trở lại. Đo PA xong mới cân nhắc bật lại
- 🔴 **Bản in 29/08 đã loại hết các nghi phạm khác cho triệu chứng seam.** Scarf
  tắt, `seam_gap = 15%`, `wipe_before_external_loop = 1`, retraction 1.2 @ 45,
  `retract_before_wipe = 100%` — tất cả đều đã chạy, seam vẫn dư nhựa. Còn lại
  đúng một biến chưa bao giờ được đo
- ❌ Không có khoá preset nào thay thế được việc đo. Đoán thêm chỉ mất thêm bản in

---

## B. Cần Viet chốt

*(trống)*

---

## C. Hàng đợi của tôi

<a id="c3"></a>
### C3 🔴 In thử 1 màu sau P19–P21

🔴 **C1 đóng: P15 đã chạy đủ và vẫn rất nhiều tơ.** Bản in 29/08 17:00
(`Parametric_Model_Maker_1`) mang đủ `retraction_speed = 45`,
`retract_before_wipe = 100%`, `z_hop_types = Normal Lift`, `seam_slope_type = none`,
`filament_flow_ratio = 1` — đọc từ chính file gcode. Nên nguyên nhân nằm ở chỗ khác.

🟢 **P19, P20, P21 đã áp** — cả hai preset FIGURE:

| Key | Cũ | Mới | Nhắm vào |
|---|---|---|---|
| `reduce_crossing_wall` | 0 | **1** | tơ |
| `max_travel_detour_distance` | 0 | **40** | trần đường vòng |
| `ironing_flow` | 8% | **10%** | mặt trên xước |
| `top_surface_speed` | 150 | **80** | mặt trên xấu |

⏳ **P6 giữ lại có chủ đích.** Ba thay đổi trên đủ nhiều cho một bản in. Nếu bản
tới hết tơ thì P6 không cần; còn tơ thì P6 là nước đi tiếp theo, và lúc đó nó
đứng một mình nên quy được công.

🔵 P22 đóng — `skirt_loops = 0` và `prime_tower_width = 10` là Viet cố ý.

🔴 **In thử bản kế tiếp bằng 1 màu.** Bản 29/08 là in 2 màu: mỗi layer đầu in
chạy tới prime tower ở góc `x=20, y=214` rồi quay lại, hai lần. Đó là một nhóm
lỗi riêng — tơ giữa vật và tháp, lem màu, nozzle quét qua mặt trên — trộn lẫn với
lỗi retraction thì không tách được cái nào ra.

📝 Hết tơ ở bản 1 màu → quay lại in 2 màu để đo riêng phần prime tower.

<a id="c2"></a>
### C2 ⏳ Nghiệm thu P16 — retract ở cuối `machine_end_gcode`
Bản in 29/08 đã chạy P16 nhưng Viet chưa báo tình trạng nozzle lúc in xong.

| Dấu hiệu | Nghĩa |
|---|---|
| 🟢 nozzle sạch hoặc chỉ còn giọt nhỏ | P16 ăn — giữ |
| 🟡 đoạn đầu bản in **sau** bị hụt nhựa | hạ `E-6` xuống `E-4` |
| 🔴 máy báo lỗi ở cuối bản in, nhựa tuột khỏi đường nạp | revert ngay |

**Revert P16** — đóng slicer, rồi:

```powershell
$R = "$env:APPDATA\AnycubicSlicerNext"
Rename-Item "$R\user" "user_broken-p16"
Rename-Item "$R\user_backup-tune-p16-endgcode-20260829-161405" "user"
```

🟡 Backup đó chụp **sau** P15 nhưng **trước** P18 — khôi phục nó sẽ mất P18. Áp
lại P18 sau đó.

---

Việc đã xong: `CHANGELOG.md`. Quy ước làm việc: `docs/working-rules.md`.
