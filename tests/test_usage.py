import unittest
from datetime import datetime, timedelta, timezone

from metering.usage import bucket_for, export_csv, totals_by_bucket


class BucketTest(unittest.TestCase):
    def test_bucket_is_utc_hour(self):
        ts = datetime(2026, 11, 3, 14, 59, tzinfo=timezone.utc)
        self.assertEqual(bucket_for(ts), "2026-11-03T14")

    def test_bucket_converts_to_utc(self):
        ts = datetime(2026, 11, 3, 9, 30, tzinfo=timezone(timedelta(hours=-5)))
        self.assertEqual(bucket_for(ts), "2026-11-03T14")

    def test_recent_event_counts_in_current_hour(self):
        now = datetime.now(timezone.utc)
        recent = now - timedelta(minutes=10)
        self.assertEqual(bucket_for(recent), bucket_for(now))


class TotalsTest(unittest.TestCase):
    def test_totals_group_by_hour(self):
        events = [
            (datetime(2026, 11, 3, 14, 5, tzinfo=timezone.utc), 3),
            (datetime(2026, 11, 3, 14, 50, tzinfo=timezone.utc), 4),
            (datetime(2026, 11, 3, 15, 0, tzinfo=timezone.utc), 2),
        ]
        self.assertEqual(totals_by_bucket(events), {"2026-11-03T14": 7, "2026-11-03T15": 2})


class ExportTest(unittest.TestCase):
    def test_export_is_sorted(self):
        totals = {"2026-11-03T15": 2, "2026-11-03T14": 7}
        self.assertEqual(export_csv(totals), "2026-11-03T14,7\n2026-11-03T15,2")


if __name__ == "__main__":
    unittest.main()
