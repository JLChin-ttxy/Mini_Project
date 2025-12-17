"""
Deadline Tracker helper for important admission dates.
"""
from datetime import datetime


class DeadlineTracker:
    """Provide helpers to fetch important dates for admissions."""

    def __init__(self, db_connection):
        self.conn = db_connection

    def get_upcoming_dates(self, limit=10):
        """Return upcoming important dates ordered by start date."""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id.event_type,
                       id.start_date,
                       id.end_date,
                       id.description,
                       p.program_name,
                       p.program_id
                FROM IMPORTANT_DATE id
                JOIN PROGRAM p ON id.program_id = p.program_id
                WHERE id.end_date >= CURDATE()
                ORDER BY id.start_date ASC
                LIMIT %s
                """,
                (limit,),
            )
            dates = cursor.fetchall()
            cursor.close()
            return dates
        except Exception as exc:  # pragma: no cover - defensive
            print(f"Error fetching upcoming dates: {exc}")
            return []

    def get_all_dates(self):
        """Return all important dates sorted by most recent first."""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id.event_type,
                       id.start_date,
                       id.end_date,
                       id.description,
                       p.program_name,
                       p.program_id,
                       p.level,
                       CASE 
                           WHEN id.end_date < CURDATE() THEN 'expired'
                           WHEN id.start_date <= CURDATE() AND (id.end_date IS NULL OR id.end_date >= CURDATE()) THEN 'active'
                           ELSE 'upcoming'
                       END as status,
                       CASE 
                           WHEN id.end_date IS NOT NULL AND id.end_date < DATE_ADD(CURDATE(), INTERVAL 7 DAY) THEN 'critical'
                           WHEN id.end_date IS NOT NULL AND id.end_date < DATE_ADD(CURDATE(), INTERVAL 30 DAY) THEN 'high'
                           ELSE 'normal'
                       END as urgency,
                       DATEDIFF(id.end_date, CURDATE()) as days_remaining
                FROM IMPORTANT_DATE id
                JOIN PROGRAM p ON id.program_id = p.program_id
                ORDER BY id.start_date ASC
                """
            )
            dates = cursor.fetchall()
            cursor.close()
            return dates
        except Exception as exc:  # pragma: no cover - defensive
            print(f"Error fetching all dates: {exc}")
            return []


