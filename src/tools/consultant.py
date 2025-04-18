from datetime import date, timedelta
import requests

API_BASE = "http://127.0.0.1:8000"
EMAIL     = "patrickloops808@gmail.com"
PASSWORD  = "Maystro808"
SHOP_ID   = "1b06a2d6-9e4f-4afd-9aa6-aed77b67119e"


def date_range(period: str | int = "week") -> tuple[str, str]:
    """Return (start, end) ISO strings for the given period.

    • "week"  → last 7 full days (Mon‑Sun style)
    • "month" → last 30 days
    • int     → that many days back from today
    """
    today = date.today()
    if period == "week":
        delta = timedelta(days=7)
    elif period == "month":
        delta = timedelta(days=30)
    elif isinstance(period, int):
        delta = timedelta(days=period)
    else:
        raise ValueError("period must be 'week', 'month', or an int")
    start = today - delta
    return start.isoformat(), today.isoformat()

def get_token() -> str:
    r = requests.post(f"{API_BASE}/auth/login/", json={"email": EMAIL, "password": PASSWORD})
    r.raise_for_status()
    return r.json()["access"]

def auth_hdr(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}

# ---------- fetchers -------------------------------------------------

def fetch_dashboard_stats(token: str):
    url = f"{API_BASE}/api/shops/{SHOP_ID}/dashboard-stats/"
    r = requests.get(url, headers=auth_hdr(token))
    r.raise_for_status()
    return r.json()

def fetch_order_status(token: str):
    url = f"{API_BASE}/api/shops/{SHOP_ID}/order-status-count/"
    r = requests.get(url, headers=auth_hdr(token))
    r.raise_for_status()
    return r.json()

def fetch_general_stats(token: str, start_date: str | None = None, end_date: str | None = None):
    if not (start_date and end_date):
        start_date, end_date = date_range("week")
    url = f"{API_BASE}/api/shops/{SHOP_ID}/analytics/general-stats/?start_date={start_date}&end_date={end_date}"
    r = requests.get(url, headers=auth_hdr(token))
    r.raise_for_status()
    return r.json()

def fetch_top_sales(token: str, start_date: str | None = None, end_date: str | None = None):
    if not (start_date and end_date):
        start_date, end_date = date_range("week")
    url = f"{API_BASE}/api/shops/{SHOP_ID}/analytics/top-sales/?start_date={start_date}&end_date={end_date}"
    r = requests.get(url, headers=auth_hdr(token))
    r.raise_for_status()
    return r.json()

def fetch_order_analytics(token: str):
    url = f"{API_BASE}/api/shops/{SHOP_ID}/analytics/orders/"
    r = requests.get(url, headers=auth_hdr(token))
    r.raise_for_status()
    return r.json()

def competitor_analysis_tool(business_data: dict | None = None) -> dict:
    token = get_token()

    this_start, today         = date_range("week")
    last_start, last_end      = date_range(14)           # 8‑14 days ago

    this_week = {
        "dashboard":   fetch_dashboard_stats(token),
        "order_stats": fetch_order_status(token),
        "general":     fetch_general_stats(token, this_start, today),
        "top_sales":   fetch_top_sales(token,  this_start, today),
        "orders_tl":   fetch_order_analytics(token),
    }
    last_week = {
        "general":     fetch_general_stats(token, last_start, last_end),
        "top_sales":   fetch_top_sales(token,  last_start, last_end),
    }

    return {
        "json_data": {
            "this_week":     this_week,
            "last_week":     last_week,
            "business_data": business_data or {},
            "meta": {
                "this_week_start": this_start,
                "last_week_start": last_start,
                "today": today,
            },
        }
    }
