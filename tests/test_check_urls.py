"""Unit tests for the URL checker's verdict logic (tools/check_urls.py). No network access."""
import datetime
import os
import sys
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import check_urls  # noqa: E402


class Classify(unittest.TestCase):
    def verdict(self, url, status, final=None):
        return check_urls.classify(url, status, final or url)

    def test_locale_insertion_and_trailing_slash_are_not_drift(self):
        self.assertEqual(self.verdict("https://learn.microsoft.com/purview/audit", 200,
                                      "https://learn.microsoft.com/en-us/purview/audit/"), "OK")

    def test_moved_page_is_a_redirect(self):
        self.assertEqual(self.verdict("https://learn.microsoft.com/a/old", 200,
                                      "https://learn.microsoft.com/en-us/a/new"), "REDIRECT")

    def test_any_2xx_is_success(self):
        # EUR-Lex answers scripted clients with 202 while serving the right document.
        self.assertEqual(self.verdict("https://eur-lex.europa.eu/eli/reg/2016/679/oj", 202), "OK")

    def test_waf_status_is_matched_per_host(self):
        self.assertEqual(self.verdict("https://www.ftc.gov/legal-library/x", 404), "WAF")
        self.assertEqual(self.verdict("https://www.hhs.gov/hipaa/x", 404), "BROKEN",
                         "404 is accepted as a WAF refusal for ftc.gov only")
        self.assertEqual(self.verdict("https://www.nist.gov/x", 403), "BROKEN",
                         "a 403 from a host not on the WAF list is a real failure")

    def test_transport_failure_is_broken(self):
        self.assertEqual(self.verdict("https://www.iso.org/standard/27001", None), "BROKEN")


class WafRegistry(unittest.TestCase):
    def test_every_entry_has_a_real_hand_check_date_and_note(self):
        today = datetime.date.today()
        for host, entry in check_urls.WAF_HOSTS.items():
            with self.subTest(host=host):
                checked = datetime.date.fromisoformat(entry["checked"])
                self.assertLessEqual(checked, today, "hand-check date is in the future")
                self.assertTrue(entry["saw"].strip(), "record what the browser showed")
                self.assertTrue(entry["statuses"], "list the status the host returns to scripts")


if __name__ == "__main__":
    unittest.main()
