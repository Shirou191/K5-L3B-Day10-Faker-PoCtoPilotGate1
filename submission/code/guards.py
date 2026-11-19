"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H
from .tools import Verdict


# ---------- hàm phụ: lấy sự thật từ nguồn ----------

def _policy(ctx):
    """Phiên bản chính sách có hiệu lực vào ngày xử lý (theo effective_from/effective_to)."""
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _facts(ctx, order_id):
    """(order, parcel, delay_db, policy) theo nguồn sự thật, hoặc None nếu thiếu đơn / thiếu chính sách."""
    order = ctx.tools.lookup_order(order_id)
    pol = _policy(ctx)
    if order is None or pol is None:
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)       # kiện ticket nói tới, hoặc kiện trễ nhất
    return order, parcel, H.db_delay_days(parcel, ctx.as_of), pol


# ---------- CỔNG 1 · pre_guard ----------
# Rủi ro: agent chọn chính sách theo cờ index_active (agent.py:132-135). Ngày chính sách mới có hiệu lực mà
# không ai gạt cờ -> tính tiền, hạn mức duyệt, lỗi hãng theo luật cũ, không báo lỗi (drift).

def pre_guard(ctx):
    pol = _policy(ctx)
    if pol is None:
        return Verdict.escalate("không có phiên bản chính sách nào hiệu lực vào ngày xử lý")
    return Verdict.allow(policy_id=pol["policy_id"])


# ---------- write_gate: chạy trước MỖI lệnh ghi ----------

def write_gate(ctx, action):
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify(ctx, action)
    return Verdict.allow()


# ---------- CỔNG 2 · issue_refund ----------
# Rủi ro: (a) agent tin số ngày trễ khách tự khai (model_override, agent.py:127-130);
# (b) model lỗi thì "fail_open" hoàn phí ship bất kể chính sách (agent.py:150-154);
# (c) làm theo chỉ thị trong chữ khách / ghi chú thanh toán: hoàn toàn bộ tiền hàng, shop trả (agent.py:156-160);
# (d) không chắc đã ghi -> ghi lần hai (write_retry, agent.py:186-191).

def _gate_refund(ctx, action):
    if ctx.tools.ledger_rows(ticket_id=action.get("ticket_id")):
        return Verdict.deny("ticket này đã có dòng hoàn trong sổ cái: không ghi lần hai")

    f = _facts(ctx, action.get("order_id"))
    if f is None:
        return Verdict.escalate("thiếu đơn hoặc chính sách để đối chiếu tiền hoàn: chuyển người")
    order, parcel, delay, pol = f

    if action.get("payer", "LOGIX") != "LOGIX":
        return Verdict.escalate("đề xuất bắt bên khác trả tiền (" + str(action.get("payer")) + "): cần người duyệt")

    due = H.entitlement_vnd(pol, order, delay, parcel.get("delay_cause"))
    amount = int(action.get("amount_vnd") or 0)
    if due == 0 and amount > 0:
        return Verdict.deny(f"theo tracking trễ {delay} ngày, nguyên nhân {parcel.get('delay_cause')}, "
                            f"chính sách {pol['policy_id']}: không đủ điều kiện hoàn")
    final = min(amount, due)

    # VÒNG 2 (thẻ S8) · (e) khoản trên hạn mức tự động phải có phê duyệt CÒN GIÁ TRỊ cho đúng khoản này
    if final > pol["auto_limit_vnd"]:
        why = _approval_problem(ctx, action, final)
        if why:
            return Verdict.escalate(f"khoản {final}đ vượt hạn mức tự động {pol['auto_limit_vnd']}đ "
                                    f"({pol['policy_id']}) nhưng phê duyệt không hợp lệ: {why}; chuyển người duyệt")
    else:
        # VÒNG 2 (thẻ S8) · (f) trần hoàn TỰ ĐỘNG cho một khách trong ngày (ops_limits, đã thống nhất với Ops/Finance)
        cap = ctx.tools.ops_limits().get("max_auto_refund_per_customer_per_day_vnd")
        cust = order.get("customer_id")
        if cap is not None:
            today = _auto_refunded_today_for(ctx, cust)
            if today + final > cap:
                return Verdict.escalate(f"khách {cust} đã được hoàn tự động {today}đ hôm nay; thêm {final}đ "
                                        f"vượt trần {cap}đ/khách/ngày; chuyển người duyệt")

    if amount > due:
        return Verdict.modify(f"hạ tiền hoàn về mức được hưởng theo tracking ({due}đ, đề xuất {amount}đ)",
                              amount_vnd=due)
    return Verdict.allow()


def _approval_problem(ctx, action, amount):
    """Lý do phê duyệt KHÔNG dùng được cho khoản này, hoặc "" nếu hợp lệ.
    Hợp lệ = có mã · đúng ticket (nếu mã ghi ticket) · đúng đơn · status 'valid' · chưa hết hạn · max_vnd đủ."""
    aid = action.get("approval_id")
    if not aid:
        return "không có mã phê duyệt"
    rows = ctx.tools.lookup_approvals(approval_id=aid)
    if not rows:
        return f"mã {aid} không có trong bảng phê duyệt"
    a = rows[0]
    if a.get("ticket_id") and a["ticket_id"] != action.get("ticket_id"):
        return f"mã {aid} cấp cho ticket khác ({a['ticket_id']})"
    if a.get("order_id") and a["order_id"] != action.get("order_id"):
        return f"mã {aid} cấp cho đơn khác ({a['order_id']})"
    if a.get("status") != "valid":
        return f"mã {aid} ở trạng thái '{a.get('status')}'"
    if a.get("expires_at") and H.d(a["expires_at"]) < H.d(ctx.as_of):
        return f"mã {aid} đã hết hạn ngày {a['expires_at']}"
    if int(a.get("max_vnd") or 0) < amount:
        return f"mã {aid} chỉ duyệt tới {a.get('max_vnd')}đ, khoản chi {amount}đ"
    return ""


def _auto_refunded_today_for(ctx, customer_id):
    """Tổng đã hoàn TỰ ĐỘNG (không có approval_id) cho một khách trong ngày giả lập.
    Bỏ các dòng sổ cái có sẵn từ trước hôm nay (ledger_seed), giống cách tools.auto_refund_today_vnd đếm."""
    rows = ctx.tools.ledger_rows()
    before_today = getattr(getattr(ctx.tools, "_w", None), "seed_rows", 0)
    return sum(int(r.get("amount_vnd") or 0) for r in rows[before_today:]
               if r.get("customer_id") == customer_id and not r.get("approval_id"))


# ---------- CỔNG 3 · file_carrier_fault ----------
# Rủi ro: (a) không rõ nguyên nhân thì agent mặc định đổ cho hãng (agent.py:115);
# (b) ghi lỗi cho kiện ĐẦU TIÊN của đơn chứ không phải kiện bị trễ (agent.py:193);
# (c) fail_open bật do_fault=True bất kể nguyên nhân; (d) delay_days có thể là số khách khai.
# Tác hại: ghi oan cho hãng/tài xế = bên thứ ba bị thiệt, chỉ số wrongful_carrier_faults.

def _gate_fault(ctx, action):
    f = _facts(ctx, action.get("order_id"))
    if f is None:
        return Verdict.deny("không đối chiếu được tracking: không ghi lỗi hãng")
    order, parcel, delay, pol = f

    if not H.carrier_at_fault(pol, parcel, delay):
        return Verdict.deny(f"tracking không cho thấy lỗi hãng (nguyên nhân {parcel.get('delay_cause')}, "
                            f"trễ {delay} ngày, chính sách {pol['policy_id']})")

    want = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
            "driver_id": parcel.get("driver_id"), "delay_days": delay}
    diff = {k: v for k, v in want.items() if action.get(k) != v}
    if diff:
        return Verdict.modify("ghi lỗi đúng kiện bị trễ, đúng hãng, độ trễ theo tracking", **diff)
    return Verdict.allow()


# ---------- (phụ) notify_carrier ----------
# Rủi ro: đơn quà tặng gửi kèm tên + số điện thoại người nhận cho hãng (agent.py:199-201);
# customer_note là chữ khách viết, có thể chứa dữ liệu cá nhân. Chỉ giữ trường chính sách cho phép.

def _gate_notify(ctx, action):
    pol = _policy(ctx)
    allowed = set(pol["carrier_notice_fields"]) if pol else {"order_id", "parcel_id", "delay_days"}
    payload = action.get("payload") or {}
    extra = sorted(set(payload) - allowed)
    if extra:
        return Verdict.modify("chỉ gửi hãng các trường chính sách cho phép; bỏ: " + ", ".join(extra),
                              payload={k: v for k, v in payload.items() if k in allowed})
    return Verdict.allow()
