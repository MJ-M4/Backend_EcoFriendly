"""
Reports & Charts
Route pattern:  /api/reports/<type>?format=json|csv|png

<type> ∈  { fullness , collections , payroll , activity }

• JSON   – default, always returned if no ?format given.
• CSV    – text/csv  (for spreadsheet download)
• PNG    – JSON payload { "png_base64": "<...>" }  suitable for <img src="data:image/png;base64,..." />

The blueprint never emits numeric HTTP codes in the source.
"""

import base64
import io
import csv
from http import HTTPStatus
from typing import Any, List, Dict

import matplotlib.pyplot as plt
from flask import Blueprint, Response, jsonify, make_response, request

from src.dal.database import get_session
from src.dal._base import _row_to_model
from src.errors import ErrorMessage
from src.errors.handlers import ApiError
from src.interface.auth import auth_required
from src.models.bin import Bin
from src.models.payroll import Payroll

bp = Blueprint("reports", __name__, url_prefix="/reports")


# ────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────
def _to_csv(rows: List[Dict[str, Any]]) -> str:
    """Return CSV string from list-of-dicts."""
    if not rows:
        return ""
    header = rows[0].keys()
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def _chart_base64(labels: List[str], values: List[int | float], title: str) -> str:
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title(title)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def _respond(rows: List[Dict[str, Any]], chart_title: str):
    fmt = request.args.get("format", "json").lower()

    if fmt == "csv":
        csv_text = _to_csv(rows)
        return Response(csv_text, mimetype="text/csv")

    if fmt == "png":
        labels = [str(r["label"]) for r in rows]
        values = [r["value"] for r in rows]
        png_b64 = _chart_base64(labels, values, chart_title)
        return jsonify(png_base64=png_b64)

    # default JSON
    return jsonify(rows)


# ────────────────────────────────────────────────────────────────
# Report implementations
# ────────────────────────────────────────────────────────────────
def _report_fullness():
    """
    Latest level_pct per bin (lower → needs emptying).
    """
    query = """
        SELECT b.bin_id, b.location, IFNULL(br.level_pct, 0) AS level
        FROM Bins b
        LEFT JOIN (
            SELECT bin_id, level_pct
            FROM BinReadings br1
            WHERE br1.ts = (
                SELECT MAX(ts) FROM BinReadings WHERE bin_id = br1.bin_id
            )
        ) br ON br.bin_id = b.bin_id;
    """
    with get_session() as sess:
        rows = sess.execute(query).mappings().all()

    data = [
        {"label": f"{r['location']} ({r['bin_id']})", "value": int(r["level"])}
        for r in rows
    ]
    return _respond(data, "Current Bin Fullness (%)")


def _report_collections():
    """
    Count of empties in last 30 days per bin.
    We treat 'collection' as last_emptied updates.
    """
    query = """
        SELECT bin_id, location,
               SUM(CASE WHEN last_emptied >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 ELSE 0 END) AS collections_30d
        FROM Bins
        GROUP BY bin_id, location
    """
    with get_session() as sess:
        rows = sess.execute(query).mappings().all()

    data = [
        {"label": f"{r['location']} ({r['bin_id']})", "value": int(r["collections_30d"])}
        for r in rows
    ]
    return _respond(data, "Collections in Last 30 Days")


def _report_payroll():
    """
    Total payroll per employee (current year).
    """
    query = """
        SELECT employee_id,
               SUM(amount_nis) AS total
        FROM Payroll
        WHERE MONTH BETWEEN CONCAT(YEAR(CURRENT_DATE), '01') AND CONCAT(YEAR(CURRENT_DATE), '12')
        GROUP BY employee_id
    """
    with get_session() as sess:
        rows = sess.execute(query).mappings().all()

    data = [{"label": r["employee_id"], "value": float(r["total"])} for r in rows]
    return _respond(data, "Payroll Totals (Current Year)")


def _report_activity():
    """
    Shifts per employee in last 30 days.
    """
    query = """
        SELECT employee_id, COUNT(*) AS shifts_30d
        FROM Shifts
        WHERE start_ts >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        GROUP BY employee_id
    """
    with get_session() as sess:
        rows = sess.execute(query).mappings().all()

    data = [{"label": r["employee_id"], "value": int(r["shifts_30d"])} for r in rows]
    return _respond(data, "Shifts in Last 30 Days")


_REPORT_MAP = {
    "fullness": _report_fullness,
    "collections": _report_collections,
    "payroll": _report_payroll,
    "activity": _report_activity,
}


# ────────────────────────────────────────────────────────────────
# Entry route
# ────────────────────────────────────────────────────────────────
@bp.get("/<string:report_type>")
@auth_required(role="manager")
def run_report(report_type: str):
    report_func = _REPORT_MAP.get(report_type.lower())
    if not report_func:
        raise ApiError(ErrorMessage.DB_ERROR, HTTPStatus.NOT_FOUND)  # textual msg only
    return report_func()