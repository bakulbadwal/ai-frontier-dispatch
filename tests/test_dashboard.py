import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard"
SCHEMA = ROOT / "schemas" / "dashboard-issue.schema.json"

CONFIDENCE = {"verified", "reported", "unverified"}
TELL_STATUS = {"with", "against", "mixed", "quiet"}


def all_items(issue):
    for part in issue["parts"]:
        for section in part["sections"]:
            for item in section.get("items", []):
                yield item


class DashboardIssueTest(unittest.TestCase):
    """Checks the invariants the page relies on, without a jsonschema dependency."""

    def setUp(self):
        self.index = json.loads((DASHBOARD / "issues" / "index.json").read_text())
        self.issues = [
            json.loads((DASHBOARD / "issues" / entry["file"]).read_text())
            for entry in self.index["issues"]
        ]

    def test_schema_is_valid_json(self):
        schema = json.loads(SCHEMA.read_text())
        self.assertEqual(schema["title"], "Dashboard issue")

    def test_index_points_at_existing_issues(self):
        self.assertTrue(self.index["issues"])
        for entry in self.index["issues"]:
            self.assertTrue((DASHBOARD / "issues" / entry["file"]).exists(), entry["file"])

    def test_required_fields(self):
        for issue in self.issues:
            for key in ("date", "window", "why", "top", "parts"):
                self.assertIn(key, issue)

    def test_item_ids_unique_and_top_resolves(self):
        for issue in self.issues:
            ids = [item["id"] for item in all_items(issue)]
            self.assertEqual(len(ids), len(set(ids)), "duplicate item ids")
            for top_id in issue["top"]:
                self.assertIn(top_id, ids, f"top id {top_id} has no item")

    def test_item_fields(self):
        for issue in self.issues:
            for item in all_items(issue):
                self.assertIn(item["confidence"], CONFIDENCE, item["id"])
                self.assertIsInstance(item["score"], int, item["id"])
                self.assertTrue(0 <= item["score"] <= 6, item["id"])
                for link in item.get("links", []):
                    self.assertRegex(link["url"], r"^https?://", item["id"])

    def test_tell_statuses(self):
        for issue in self.issues:
            for part in issue["parts"]:
                for section in part["sections"]:
                    for row in section.get("tells", {}).get("rows", []):
                        self.assertIn(row["status"], TELL_STATUS)

    def test_template_has_no_private_paths(self):
        html = (DASHBOARD / "index.html").read_text()
        self.assertNotIn("~/.claude", html)
        self.assertNotIn("/Users/", html)


if __name__ == "__main__":
    unittest.main()
