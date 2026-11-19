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

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
