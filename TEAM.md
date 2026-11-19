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
|   2 |           |      |     |             |
|   3 |           |      |     |             |
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

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
