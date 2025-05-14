"""
Sensor-simulator Lambda  –  scheduled every 5 min by serverless.yaml.

• Randomly bumps each bin’s fullness % (0-100).
• When a bin drops to ≤20 %, we treat it as emptied.
  → last_emptied is updated, and the next cycle starts from 0 %.
"""

from datetime import datetime
import random
from http import HTTPStatus

from sqlalchemy import text

from src.dal.database import get_session
from src.errors import ErrorMessage
from src.errors.handlers import ApiError


def _latest_levels():
    """Return dict {bin_id: current_level_pct} based on most-recent reading."""
    query = text(
        """
        SELECT b.bin_id,
               COALESCE(
                   (SELECT level_pct
                    FROM BinReadings br
                    WHERE br.bin_id = b.bin_id
                    ORDER BY ts DESC
                    LIMIT 1),
                   0
               ) AS level_pct
        FROM Bins b
        """
    )
    with get_session() as sess:
        return {row.bin_id: int(row.level_pct) for row in sess.execute(query)}


def handler(event, context):  # noqa: D401   (Lambda entry-point signature)
    levels = _latest_levels()

    inserts = []
    updates = []

    for bid, lvl in levels.items():
        # simulate ±5 % change biased upward until ~90 %, then downward
        delta = random.randint(-3, 5) if lvl < 90 else random.randint(-10, -3)
        new_lvl = max(0, min(100, lvl + delta))

        # Empty the bin if it reaches ≤20 %
        if new_lvl <= 20:
            updates.append({"bin_id": bid, "last_emptied": datetime.utcnow()})
            new_lvl = 0  # start fresh after emptying

        inserts.append({"bin_id": bid, "level": new_lvl})

    if not inserts:
        return {"message": "No bins found"}

    with get_session() as sess:
        # Insert readings
        sess.execute(
            text(
                "INSERT INTO BinReadings(bin_id, level_pct) VALUES "
                + ", ".join("(:bin_id{i}, :level{i})".format(i=i) for i in range(len(inserts)))
            ),
            {f"bin_id{i}": ins["bin_id"] for i, ins in enumerate(inserts)}
            | {f"level{i}": ins["level"] for i, ins in enumerate(inserts)}
        )

        # Update emptied timestamps
        for upd in updates:
            sess.execute(
                text("UPDATE Bins SET last_emptied=:ts WHERE bin_id=:bid"),
                {"ts": upd["last_emptied"], "bid": upd["bin_id"]},
            )

    return {"inserted": len(inserts), "emptied": len(updates)}