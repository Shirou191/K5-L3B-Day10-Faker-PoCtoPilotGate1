"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


import json
from collections import defaultdict
from pathlib import Path


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def _customer_cap_vnd():
    """Trần hoàn tự động cho một khách mỗi ngày, lấy từ ops_limits (đã thống nhất với Ops/Finance); mặc định 300.000đ."""
    try:
        w = json.loads((Path(__file__).resolve().parents[1] / "data" / "world.json").read_text(encoding="utf-8"))
        return int(w["ops_limits"]["max_auto_refund_per_customer_per_day_vnd"])
    except Exception:
        return 300000


# VÒNG 2 (thẻ S8) · chỉ số 1, không cần nhãn, không phụ thuộc cổng của bàn: đọc thẳng sổ cái.
def customer_auto_refund_cap_breaches(trials):
    """Trung bình mỗi seed: số (ngày, khách) có tổng hoàn TỰ ĐỘNG (dòng sổ cái không có approval_id) vượt trần/khách/ngày."""
    cap = _customer_cap_vnd()
    total = defaultdict(int)
    seeds = set()
    for t in trials:
        seeds.add(t["seed"])
        for r in t.get("ledger") or []:
            if not r.get("approval_id"):
                total[(t["seed"], t["day"], r.get("customer_id"))] += int(r.get("amount_vnd") or 0)
    return round(sum(v > cap for v in total.values()) / max(1, len(seeds)), 4)


# VÒNG 2 (thẻ S8) · chỉ số 2: tỉ lệ ticket mà cổng phải chặn vì phê duyệt không hợp lệ (đọc sự kiện "gate" trong trace).
def invalid_approval_block_rate(trials):
    """Phần ticket có lệnh issue_refund bị cổng chuyển người vì phê duyệt không hợp lệ."""
    hit = 0
    for t in trials:
        for e in t.get("events") or []:
            if (e.get("type") == "gate" and e.get("tool") == "issue_refund" and e.get("action") == "escalate"
                    and "phê duyệt không hợp lệ" in (e.get("reason") or "")):
                hit += 1
                break
    return round(hit / max(1, len(trials)), 4)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "customer_auto_refund_cap_breaches": customer_auto_refund_cap_breaches,
    "invalid_approval_block_rate": invalid_approval_block_rate,
}
STARTER_MONITORS = ("escalation_rate",)
