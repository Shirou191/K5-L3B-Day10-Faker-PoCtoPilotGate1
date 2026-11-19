# Team

## Thông tin nhóm

- Tên nhóm : Faker
- Lớp: `L3B`
- Repo của bàn: K5-L3B-Day10-Faker-PoCtoPilotGate1
- Thẻ sự cố đã bốc (S1–S8): S8

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Phan Đào Minh Quân | 2A202603971 | Kỹ sư cổng | ✔ |
|   2 | Trần Quang Hà | 2A202603962 | Sản phẩm và kinh doanh |   |
|   3 | Bùi Quý Anh |  | Vận hành và pháp lý |   |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## PhanDaoMinhQuan-2A202603971

### Phần việc phụ trách

Trưởng nhóm, vai **Kỹ sư cổng**. Câu 1.3 (Phiếu A mục A2, cột Offline); câu 2.1, 2.2, 2.6, 2.7, 2.8 (Phiếu B mục B0, B1, B2, B7.1–B7.3);
chạy lệnh chốt vòng 1 và đo mốc prepared (B8); câu 3.0, 3.1 phần trace, 3.4, 3.5 phần code, 3.6 (Phiếu C mục C0, C1, C2, C6, C7, C8).
File: `lab10/guards.py`, `lab10/monitors.py`.

### Đóng góp cụ thể

- Thước đo offline câu 1.3: tỉ lệ lần chạy dùng sai phiên bản chính sách (agent chọn chính sách theo cờ `index_active` thay vì ngày hiệu lực; drift REFUND-v4 từ 01/12).
- Đo mốc base, dò `T-002@55` (agent tin số ngày khách khai), viết cổng vòng 1: ghim chính sách theo ngày hiệu lực (`pre_guard`),
  tiền hoàn theo mức được hưởng từ tracking, lỗi hãng chỉ khi tracking ghi nguyên nhân thuộc lỗi hãng, lọc dữ liệu gửi hãng (`write_gate`);
  thêm từng cổng một, mỗi lần một `--note`; hai ticket hiểm `--adhoc`.
- Vòng 2 (thẻ S8): dò 9 ticket, tìm 3 lỗi (mã phê duyệt không còn giá trị; chia nhỏ khoản hoàn vượt trần 300.000đ/khách/ngày; CSKH kiểm tay 100%);
  thêm hai nhánh cổng trong `write_gate` cho `issue_refund` và hai chỉ số theo dõi `customer_auto_refund_cap_breaches`, `invalid_approval_block_rate`.
- Xử lý lỗi xuống dòng CRLF trên Windows làm lệch hash file tiêu chí và file bị khoá (khôi phục đúng byte, ghi lại trong B0, C0).

### Bằng chứng

- Commit: `a43f1f2` (Phiếu B phần A), `e08eb26` (chốt cổng vòng 1, quyết định v1, checkpoint `f838c08a`), `d801f6b` (cổng C7), `c0030e7` (chỉ số C8), `98c9e0f` (fault tree C6).
- Lần chạy: base `runs/R-base-before-20261119-154243-bde05c`, prepared `runs/R-base-prepared-20261119-164242-adb4d3`,
  S8 after `runs/R-S8-after-20261119-170659-5df4a6`, grade S8 **PASS-VISIBLE** `runs/R-S8-grade-20261119-171014-69c5f7.json`.
- Phiếu: A mục A2 (câu 1.3); B mục B0, B1, B2, B7.1–B7.3, B0 dòng 6–7; C mục C0, C1, C2, C6, C7, C8.

### Exit ticket

Học được: Đánh giá một hệ thống AI phải đặt luật trước, đo sau, nhìn cả kỹ thuật lẫn tiền, người và pháp lý. Cổng bảo vệ nên nằm ngoài model, kết hợp code, con số và con người.


Chưa chắc: Kết quả trên dữ liệu giả có còn đúng khi chạy thật không, và làm sao đo được những thứ như lòng tin của người dùng.

## TranQuangHa-2A202603962

### Phần việc phụ trách

Vai **Sản phẩm và kinh doanh**.
- Khối 1: Câu 1.1, 1.2 (mục tiêu hệ thống Phiếu A mục A1), Câu 1.3, 1.4 (thước đo offline/online A2), Câu 1.5 (khoảng tin cậy A3), Câu 1.6 (câu tiêu chí A4); chốt và ký bản tiêu chí `config/acceptance_criteria.json`.
- Khối 2: Câu 2.3 (Phiếu B mục B3: bản đồ dữ liệu và phân tích drift chuyển đổi chính sách REFUND-v3 sang v4), Câu 2.9 (Phiếu B mục B7.4: thiết lập cổng tài chính trong `config/operating_gates.json`), tham gia Pre-mortem B6; đồng thuận Quyết định Gate 1 v1 (B8).
- Khối 3: Câu 3.2 (Phiếu C mục C5: xây dựng 4 điều kiện đặc tả hợp lệ của `approval_id` xử lý triệt để sự cố S8), chủ trì Quyết định Gate 1 v2 và 3 dòng bắt buộc (C12).
File: `config/acceptance_criteria.json`, `config/operating_gates.json` (mục `business`), `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md`, `templates/form-c-incident.md`.

### Đóng góp cụ thể

- Xây dựng bản tiêu chí chấp nhận Gate 1 với 5 chỉ số an toàn bắt buộc và 1 chỉ số nên có; đặt điều kiện dừng nghiêm ngặt bảo vệ quyền lợi khách hàng và uy tín pháp lý.
- Phân tích rủi ro trôi dạt phân phối (distribution drift) khi hệ sinh thái thay đổi chính sách từ 01/12, chỉ ra lỗi agent dựa vào cờ `index_active` và đề xuất cơ chế ghim chính sách theo ngày hiệu lực.
- Thiết lập các cổng kinh doanh trong `config/operating_gates.json`: trần chi hoàn tự động ngày 2.000.000đ, ngân sách xử lý tối đa 8.000đ/ticket, phạm vi thử nghiệm 100%, bảo đảm ROI tối thiểu 0.20 (kết quả thực tế sau sửa đạt 2.39).
- Viết đặc tả kỹ thuật 4 điều kiện kiểm tra mã duyệt (`approval_id` còn hạn, đúng ticket, đúng trạng thái `valid`, đủ hạn mức `max_vnd`) giúp loại bỏ hoàn toàn 5 ca dùng mã sai, khôi phục niềm tin của trưởng ca CSKH (kiểm tay 100% giảm về kiểm mẫu 10%, xóa sạch 36 ca ùn tắc).

### Bằng chứng

- Commit: `8cffcee` (`Sign acceptance criteria`), `1e1160a` (Phiếu B mục B3 dữ liệu và drift), `da37c6d` (Phiếu B B7.4 và cổng kinh doanh), `1d0ca5a` (Phiếu C C5 specification cho S8).
- Lần chạy: `runs/R-base-before-20261119-154243-bde05c`, `runs/R-base-prepared-20261119-164242-adb4d3`, `runs/R-S8-after-20261119-170659-5df4a6`, `runs/R-S8-grade-20261119-171014-69c5f7.json` (PASS-VISIBLE).
- Phiếu: Form A (A1–A5), Form B (B3, B7.4, B8), Form C (C5 mục 3.2, C12).

### Exit ticket

Học được: Thiết kế an toàn cho hệ thống AI phải kết hợp chặt chẽ giữa logic kỹ thuật và ràng buộc tài chính/vận hành (guardrails bên ngoài model). Việc định lượng bằng specification rõ ràng là chìa khóa để khôi phục niềm tin của người vận hành.

Chưa chắc: Trong môi trường production thực tế, các dạng gian lận chia nhỏ giao dịch hoặc lạm dụng mã phê duyệt có thể biến thiên phức tạp hơn nhiều so với bộ dữ liệu giả lập (mock data).

## BuiDinhQuyAnh-2A202603969

### Phần việc phụ trách

Vai **Vận hành và pháp lý**.
- Khối 1: câu 1.2 (Phiếu A mục A1: mục tiêu nhìn từ chị Oanh và chị Hạnh), câu 1.4 (Phiếu A mục A2, cột Telemetry production).
- Khối 2: câu 2.4 (Phiếu B mục B4 HAZOP vòng 1 trên `file_carrier_fault` + dòng ngoài kỹ thuật; mục B5 checklist 9 nhóm việc có PIC), câu 2.5
  (mục B6 pre-mortem bốn lăng kính, cùng cả bàn), câu 2.10 (mục B7.5 runbook phần 1–3, mục B7.6 giờ cao điểm).
- Khối 3: câu 3.1 phần riêng của thẻ (Phiếu C mục C3.4 hiệu chỉnh lòng tin + một dòng C3.1; mục C4 HAZOP của thẻ), câu 3.3 (mục C5),
  câu 3.7 (mục C9 fault tree sau khi sửa, C10 risk register, C11 cập nhật checklist và runbook phần 4–5).
- File: `config/operating_gates.json` (mục `operations`, `legal`), `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md`,
  `templates/form-c-incident.md`.

### Đóng góp cụ thể

- Đặt cổng con người, vận hành, pháp lý trong `config/operating_gates.json`: PIC `NV-TUNG`, người duyệt đứng tên `NV-HANH`, 1 người trực,
  6 ca/giờ, chờ tối đa 60 phút, 5 điều kiện dừng, kênh báo tin; bật `decision_note`, kiểm mẫu 10%; chặn `recipient_contact`, `customer_note`
  gửi cho hãng; ghi lỗi hãng phải có nguyên nhân trong tracking. Bộ nền vẫn đạt hết, không ca nào hỏng (Phiếu B mục B0 dòng 6).
- Ba con số `decision_note`, kiểm mẫu 10%, `approver_id = NV-HANH` đặt từ vòng 1 (dựa trên B4 dòng "Người đứng tên duyệt" và B6 P6)
  chính là 3/4 điều kiện để nhân viên thôi kiểm tay ở thẻ S8: khi Kỹ sư cổng lấp điều kiện thứ tư, kiểm lại giảm từ 100% về 10%
  mà không phải đổi con số nào ở vòng 2.
- HAZOP vòng 1 tìm ra ba nhánh chưa thấy trên trace (ghi lỗi nhầm kiện đầu tiên, nguyên nhân trống bị đổ cho hãng, lộ tên và SĐT người nhận quà);
  HAZOP của thẻ thêm hai nhánh chưa thấy: mã phê duyệt do người không có thẩm quyền cấp (cổng hiện chưa kiểm `approver_id`)
  và hàng chờ ngập khi REFUND-v4 hạ hạn mức tự động xuống 100.000đ từ 01/12.
- Runbook 1–5: ai được bấm tắt, ngưỡng vàng/đỏ cho từng tín hiệu (khớp ngưỡng đã ký và chỉ số ở Phiếu C mục C8), dừng xong trong 15 phút,
  giờ cao điểm 14 ca/giờ thì lên 2 người, cách báo cho chị Hạnh và cho hãng bị ghi lỗi sau sự cố S8.
- Risk register 4 dòng sau sự cố (bảng `approvals` chậm cập nhật, chưa kiểm người đứng tên, REFUND-v4, ghi chú thiếu lý do), mỗi dòng có PIC,
  dấu hiệu trong report hoặc `monitors.py` và quyết định nó làm đổi.

### Bằng chứng

- Commit: `7caf328` (Phiếu A câu 1.2, 1.4), `653134a` (B4 HAZOP vòng 1), `4277a12` (B6 pre-mortem), `60b359b` (B5 checklist),
  `c94817b` (B7.5 runbook 1–3, B7.6 giờ cao điểm, cổng `operations` và `legal`), `b8192df` (Phiếu C mục C3.4, C4, C5 câu 3.3, C9, C10, C11).
- Lần chạy: bộ nền sau khi đặt cổng `operations`, `legal` (Phiếu B mục B0 dòng 6); prepared `runs/R-base-prepared-20261119-164242-adb4d3`;
  S8 after `runs/R-S8-after-20261119-170659-5df4a6`; grade S8 trong bài nộp `R-S8-grade-20261119-173004-69c5f7` (PASS-VISIBLE).
- Phiếu: A mục A1 (câu 1.2), A2 (câu 1.4); B mục B4, B5, B6, B7.5, B7.6; C mục C3.1 (một dòng), C3.4, C4, C5 (câu 3.3), C9, C10, C11.
- Có dùng trợ lý AI để đọc code, đối chiếu dữ liệu `data/world.json` / gói thẻ với trace, và soát câu chữ trong phiếu; mọi con số
  trong `operations`, `legal` và runbook do bàn chọn và giải thích được (`RULES.md`).

### Exit ticket

Học được: Phần lớn rủi ro của trợ lý không nằm ở model mà ở người và quy trình quanh nó. Ở thẻ S8, code chỉ sai ở 5/52 ticket nhưng cả ca
CSKH mất lòng tin và kiểm tay 100%; con số và tên người đặt đúng từ trước (ghi chú, kiểm mẫu, người đứng tên) chỉ có tác dụng khi đi cùng
một cổng code chặn đúng chỗ.

Chưa chắc: Lòng tin của nhân viên ngoài đời có quay lại nhanh như trong lab (mock coi là bật/tắt tức thì) không, và bao lâu thì chị Hạnh
thật sự chuyển từ kiểm tay sang kiểm mẫu 10%.

