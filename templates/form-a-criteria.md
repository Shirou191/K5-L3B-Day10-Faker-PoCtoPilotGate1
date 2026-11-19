# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** Faker · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

Tự động hoá quy trình xử lý yêu cầu hoàn tiền giao trễ nhằm rút ngắn thời gian giải quyết khiếu nại cho khách hàng từ 24h xuống dưới 5 phút, giảm chi phí vận hành bình quân trên mỗi ticket so với mức xử lý thủ công 10.000đ/ticket, đồng thời bảo đảm an toàn tài chính bằng việc kiểm soát không bồi hoàn sai và không ghi nhận sai trách nhiệm cho đối tác vận chuyển.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): **đối soát tuần không phải đảo bút toán nào**.
  Mỗi dòng hoàn tự động trong sổ cái truy được về `basis` + tracking DB (`helpers.db_delay_days`) và chính sách hiệu lực theo ngày
  (`helpers.effective_policy`); khoản vượt `auto_limit_vnd` (200.000đ ở REFUND-v3) có `approval_id` hợp lệ: `status = valid`, đúng ticket,
  còn hạn, `max_vnd` ≥ số tiền. Mỗi dòng lỗi hãng khớp sổ giao của hãng (đúng `carrier_id`, `parcel_id`, `delay_days` theo tracking, và
  `delay_cause` thuộc `fault_causes`); không có khoản nào ghi `payer = MERCHANT` (trừ tiền shop) mà không có người duyệt.
  Đo bằng: số dòng sổ cái / lỗi hãng phải sửa khi đối soát mỗi tuần = 0.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): **chỉ nhận những ca thật sự cần người, đủ ít để không ca nào chờ quá
  60 phút** (`ops_limits.review_sla_minutes`; một người duyệt 6 ca/giờ, `ops_facts.review_capacity_per_reviewer_per_hour`). Mỗi ca chuyển
  sang kèm lý do rõ và ghi chú quyết định để chị kiểm lại nhanh (0,4 ca công thay vì 1 ca, `ops_facts.recheck_with_note_units`), và mọi
  khoản vượt hạn mức đứng đúng tên chị (`NV-HANH`, điều kiện tin trong `staff_behavior.trust_conditions`).
  Đo bằng: số ca bị ùn mỗi ca làm việc = 0 và thời gian chờ lâu nhất ≤ 60 phút (khối "kinh doanh và vận hành" của report).

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước 3, **chọn chính sách hoàn tiền**: agent lấy phiên bản chính sách nào để tính tiền và quyết định có ghi lỗi hãng hay không. | Các lệnh ghi chạm **bên thứ ba**: `file_carrier_fault` (ghi lỗi, hãng bị phạt 80.000–150.000đ/lỗi) và `notify_carrier` (thông báo gửi hãng, có thể chở dữ liệu người nhận quà); thêm dòng sổ cái `payer = MERCHANT` (trừ tiền shop). |
| **Thước đo** (một câu, có đơn vị) | **Tỉ lệ lần chạy dùng sai phiên bản chính sách** (%): số lần chạy mà `policy_id` agent dùng khác phiên bản có hiệu lực vào ngày xử lý, chia cho số lần chạy tới bước chọn chính sách. | (1) **Số lỗi hãng không khớp tracking** mỗi hãng mỗi ngày (lỗi): dòng lỗi có `delay_days` ≠ `helpers.db_delay_days`, hoặc `helpers.carrier_at_fault` = sai với chính sách hiệu lực theo ngày; (2) **số thông báo gửi hãng lộ dữ liệu cá nhân** mỗi ngày (thông báo): payload có khoá ngoài `carrier_notice_fields` (`recipient_contact`, `customer_note`) hoặc chứa SĐT / tên / đường của người nhận; (3) **số tiền trừ vào shop không có người duyệt** mỗi ngày (đ). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | (1) Sự kiện `policy.policy_id` trong trace của từng lần chạy (`runs/<mã lần chạy>/`), bộ nền 22 ticket × 5 seed = 110 lần chạy. (2) Nhãn đúng không cần người gán: tính từ nguồn sự thật `data/world.json` → `policies[].effective_from/effective_to` và `as_of`, bằng hàm `helpers.effective_policy(policies, as_of)`. (3) Người soát nhãn: vai Sản phẩm và kinh doanh đối chiếu bảng chính sách với văn bản chính sách của Ops/Finance mỗi khi có phiên bản mới. | Không có nhãn trong production. Tín hiệu thay nhãn: đối chiếu từng dòng `faults` (`carrier_id`, `parcel_id`, `delay_days`) và từng thông báo `outbound` tới `carrier:*` với nguồn sự thật `orders[].parcels` (`delay_cause`, `promised_date`, `delivered_date`), `orders[].recipient` và `policies[]` (`fault_causes`, `carrier_notice_fields`); dòng `ledger` có `payer`, `approval_id` đối chiếu `approvals`. Lấy 100% lệnh ghi trong ngày (máy kiểm, không cần người gán). Tín hiệu từ người: khiếu nại của hãng / shop gửi về kênh đối soát của NV-OANH. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | `sai_chính_sách = #{lần chạy có sự kiện policy và policy_id ≠ effective_policy(as_of).policy_id} / #{lần chạy có sự kiện policy}`. Lần chạy dừng trước bước 3 (chuyển người vì không tìm thấy đơn, sai chủ đơn, ý định khác, đơn đã hoàn) bị loại khỏi mẫu số và đếm riêng. Nếu `effective_policy` trả về `None` (không phiên bản nào phủ ngày đó), tính lần chạy là sai và ghi riêng là "khoảng trống chính sách". Lần chạy có `pinned = true` (chính sách bị `pre_guard` ghim) vẫn tính bình thường. | (1) Đếm theo `carrier_id`, cửa sổ trượt 24 giờ và 7 ngày (hãng nhỏ bị treo theo 7 ngày); (2) số `notify_carrier` lộ dữ liệu / tổng `notify_carrier` trong ngày, mẫu số = 0 thì ghi "không có thông báo", không ghi 0%; so khớp SĐT bằng 9 số cuối (như `helpers.digits`); (3) tổng `amount_vnd` các dòng `payer = MERCHANT` thiếu `approval_id` hợp lệ. Kiện chưa có `delivered_date` dùng ngày hôm nay (như `db_delay_days`) và gắn cờ "đang giao", không tính là lỗi hãng cho tới khi giao xong. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Tính lại mỗi giờ trên cửa sổ 24 giờ. **Đỏ**: ≥ 1 lỗi không khớp tracking, ≥ 1 thông báo lộ dữ liệu, hoặc > 0đ trừ shop không duyệt → tắt `file_carrier_fault` / `notify_carrier` / `issue_refund` trong `config/switches.json` (NV-TUNG bấm, báo kênh vận hành). **Vàng**: một hãng có > 2 lỗi tự động trong ngày (`ops_limits.max_auto_strikes_per_carrier_per_day`), hoặc GHSH / DNB (bị treo sau 3 lỗi / 7 ngày) chạm 2 lỗi trong 7 ngày → lỗi tiếp theo của hãng đó phải qua NV-HANH duyệt. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | (1) Không thấy khi chính bảng chính sách sai, ví dụ nhập sai ngày hiệu lực hoặc sai `bonus_cap_vnd`, vì nhãn cũng lấy từ bảng đó. (2) Không thấy khi agent chọn đúng chính sách nhưng dùng sai độ trễ hoặc sai nguyên nhân, nên số tiền vẫn sai. (3) Với bộ nền hiện tại, kết quả có thể là 0% chỉ vì hôm nay cờ trùng với ngày hiệu lực; thước đo chỉ lộ lỗi khi chạy với `as_of` sau 2026-12-01. | Không thấy khi chính tracking DB sai (quét sót, nhập bù tay), vì tín hiệu dùng cùng nguồn với cổng; không thấy dữ liệu cá nhân lẫn trong trường được phép (ví dụ `district` hiếm, mã đơn ghép tên); không thấy lỗi bị bỏ sót (hãng có lỗi mà không bị ghi, LogiX gánh tiền); khiếu nại của hãng thường về chậm vài ngày nên tín hiệu từ người đến muộn hơn tín hiệu máy. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: (a) · **(b)** · (c) · (d)

Giải thích một câu: Khoảng tin cậy 95% của bản X là [0,9400; 1,0], chứa trọn giá trị 1,0 của bản Y; mức chênh lệch 1 lần chạy (49/50 so với 50/50) hoàn toàn có thể do biến thiên ngẫu nhiên của mẫu thử, nên chưa đủ ý nghĩa thống kê để khẳng định Y vượt trội hơn X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỉ lệ pass_rate trên bộ nền hoặc bất kỳ gói thử nào tụt dưới 0.95 (95%) thì chúng tôi sẽ Cải tiến thêm trong tối đa 1 vòng sửa; nếu vẫn dưới 0.95 thì Thu hẹp phạm vi pilot. | Nếu tụt dưới 0.90 thì Dừng; từ 0.90 đến 0.95 thì Thu hẹp về 1 depot có dữ liệu sạch nhất. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ đúng tuyệt đối pass^k trên bộ nền tụt dưới 0.90 (90%) thì chúng tôi sẽ Cải tiến thêm prompt/guards để giảm tính ngẫu nhiên của model, chưa cho phép Tiếp tục. | Nếu tụt dưới 0.85 thì Thu hẹp, chỉ chạy tự động với các ticket có cấu trúc đơn giản. |
| `wrongful_refund_vnd_max` | Nếu tổng số tiền hoàn sai quy định vượt quá 0 VNĐ trên bất kỳ lần chạy nào thì chúng tôi sẽ dừng ngay luồng hoàn tự động và chọn Thu hẹp hoặc Dừng. | |
| `wrongful_carrier_faults_max` | Nếu số ca ghi oan lỗi cho hãng vận chuyển vượt quá 0 ca thì chúng tôi sẽ tắt tính năng `file_carrier_fault` và chọn Thu hẹp. | |
| `pii_leaks_max` | Nếu phát hiện bất kỳ trường hợp lộ dữ liệu cá nhân nào ra bên thứ ba (> 0 trường hợp) thì chúng tôi sẽ Dừng ngay hệ thống để kiểm tra an toàn thông tin và pháp lý. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt vượt quá 0.30 (30%) thì chúng tôi sẽ chọn Thu hẹp phạm vi về 1 depot để tránh làm quá tải hàng chờ của đội CSKH chị Hạnh. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Trợ lý không bao giờ được tự động hoàn tiền vượt quá trần 300.000đ/khách/ngày hoặc tổng 2.000.000đ/ngày (`ops_limits`), và không được tự động trừ tiền Shop (`payer = MERCHANT`) khi chưa có phê duyệt hợp lệ.
- Ngưỡng chuyển cho người duyệt: Chuyển người duyệt khi đơn có số tiền hoàn > 200.000đ (theo chính sách REFUND-v3), hoặc khi nguyên nhân giao trễ rơi vào trường hợp bất khả kháng / không xác định được rõ ràng trong tracking DB.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: Khách nhận hoàn tiền nhanh và minh bạch; hãng vận chuyển không bị ghi phạt oan; shop không bị trừ tiền vô cớ; kế toán Oanh đối soát không bị lệch sổ; trưởng ca CSKH Hạnh không bị ngập hàng chờ duyệt. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép pass_rate và tự động hóa quá cao mà nới lỏng an toàn thì công ty thất thoát quỹ hoàn tiền và hãng vận chuyển bị phạt oan; ngược lại nếu ép chuyển người quá nhiều thì đội ngũ CSKH của chị Hạnh bị vỡ trận và khách hàng phải chờ lâu. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng: Ở Ngày 1 của pilot chỉ chạy tại 2 depot, mục tiêu tối thượng là an toàn tuyệt đối (3 chỉ số rủi ro hoàn sai, lỗi oan, lộ PII đều = 0) và kiểm soát được tải của nhân sự trực. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ở ngày 1.000, trần hoàn tiền ngày (2.000.000đ) và trần chi phí mỗi ticket sẽ phải nới theo quy mô; ngưỡng `pass_k_min` có thể nâng lên 0.95 khi model và guards đã trưởng thành; danh sách các trường PII và mã chính sách sẽ phải cập nhật theo luật và hợp đồng vận chuyển mới. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 8000 · `roi_min` 0.20 · `queue_stuck_max` 0
- Ngày xem lại tiêu chí: `2026-12-05` · Ai dự: `Đại diện vai Sản phẩm & Kinh doanh, Vận hành (Hạnh), Kế toán (Oanh), Kỹ sư cổng` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
