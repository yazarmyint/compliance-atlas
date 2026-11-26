"""Regression tests for the build guards.

Run from the repository root:

    python -m unittest discover -s tests -v

Every guard in the build was, until now, proven only by a one-off manual test written up in
AUDIT-FINDINGS. These tests make that proof repeatable. Each one copies the build into a
temporary directory, breaks exactly one thing, runs the real entry point as a subprocess, and
asserts two things: the build fails, AND the failure message is the one the guard owns. The
second half matters. Without it, a test would pass when some unrelated check fired first, and
the guard it claims to cover could be dead.

The committed repository is never touched: every mutation happens in the temporary copy, and
the copy is deleted afterwards. Standard library only; no test framework to install.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# What a build needs in order to run in isolation. The two JSON outputs are copied so that the
# baseline --check reports no drift; the spelling-lint targets are copied so build_html.py can
# scan them.
COPY_FILES = [
    "compliance-atlas.json", "compliance-atlas.html", "index.html",
    "reference/row-ids.txt", "reference/dependency-migration-log.json",
    "README.md", "CHANGELOG.md", "LICENSE-CONTENT.md",
    "docs/AUTHORING.md", "docs/MAINTENANCE.md", "tools/README.md",
]


class BuildCopy:
    """A throwaway copy of the build, with helpers to break one thing and run it."""

    def __init__(self):
        self.dir = tempfile.mkdtemp(prefix="atlas-guard-test-")
        shutil.copytree(os.path.join(ROOT, "build"), os.path.join(self.dir, "build"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        for rel in COPY_FILES:
            dst = os.path.join(self.dir, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(os.path.join(ROOT, rel), dst)

    def path(self, rel):
        return os.path.join(self.dir, rel)

    def append(self, rel, code):
        """Append Python to a build module. Module-level code runs after everything above it, so
        this mutates finished data structures without having to match source text."""
        with open(self.path(rel), "a", encoding="utf-8", newline="\n") as f:
            f.write("\n\n# ---- injected by tests/test_guards.py ----\n" + code + "\n")

    def replace(self, rel, old, new):
        with open(self.path(rel), encoding="utf-8", newline="") as f:
            text = f.read()
        assert text.count(old) == 1, f"test fixture: {old!r} occurs {text.count(old)} times in {rel}"
        with open(self.path(rel), "w", encoding="utf-8", newline="") as f:
            f.write(text.replace(old, new))

    def run(self, script="build/assemble.py", *args):
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        proc = subprocess.run([sys.executable, self.path(script), *args], cwd=self.dir,
                              capture_output=True, text=True, encoding="utf-8", env=env, timeout=180)
        return proc.returncode, proc.stdout + proc.stderr

    def cleanup(self):
        shutil.rmtree(self.dir, ignore_errors=True)


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.copy = BuildCopy()
        self.addCleanup(self.copy.cleanup)

    def assertFailsWith(self, needle, *args, script="build/assemble.py"):
        code, out = self.copy.run(script, *args)
        self.assertNotEqual(code, 0, f"build succeeded but should have failed on: {needle}\n{out[-1500:]}")
        self.assertIn(needle, out, f"build failed, but not on the guard under test:\n{out[-1500:]}")

    def check(self):
        """assemble.py --check: every assertion runs, nothing is written."""
        return self.copy.run("build/assemble.py", "--check")


class Baseline(GuardTest):
    """The unmutated copy must pass, or every failure test below proves nothing."""

    def test_unmutated_build_passes_and_matches_committed_json(self):
        code, out = self.check()
        self.assertEqual(code, 0, out[-1500:])
        self.assertIn("all integrity checks passed; nothing written", out)

    def test_full_build_is_byte_identical_to_committed_json(self):
        with open(self.copy.path("compliance-atlas.json"), "rb") as f:
            before = f.read()
        code, out = self.copy.run("build/assemble.py")
        self.assertEqual(code, 0, out[-1500:])
        with open(self.copy.path("compliance-atlas.json"), "rb") as f:
            after = f.read()
        self.assertEqual(before.replace(b"\r\n", b"\n"), after,
                         "a rebuild with no source change altered compliance-atlas.json")

    def test_check_flags_a_stale_committed_json(self):
        with open(self.copy.path("compliance-atlas.json"), "a", encoding="utf-8") as f:
            f.write(" ")
        self.assertFailsWith("the committed output is stale", "--check")


class StaleBytecode(GuardTest):
    """PR-058: the build deletes build/__pycache__ before importing any sibling module."""

    def test_pycache_is_purged(self):
        cache = self.copy.path("build/__pycache__")
        os.makedirs(cache)
        with open(os.path.join(cache, "common.cpython-99.pyc"), "wb") as f:
            f.write(b"stale")
        code, out = self.check()
        self.assertEqual(code, 0, out[-1500:])
        self.assertFalse(os.path.exists(cache), "build/__pycache__ survived a build")


class RowIntegrity(GuardTest):
    def test_bad_coverage_value(self):
        self.copy.append("build/rows_ferpa.py", 'ROWS[0]["coverage"] = "Full Support"')
        self.assertFailsWith("bad coverage", "--check")

    def test_non_boundary_row_without_microsoft_source(self):
        self.copy.append("build/rows_ferpa.py", 'ROWS[0]["sources"] = ROWS[0]["sources"][:1]')
        self.assertFailsWith("has no Microsoft source", "--check")

    def test_future_last_verified(self):
        self.copy.append("build/common.py", 'REVERIFY_DATE_3 = "2999-01-01"')
        self.assertFailsWith("last_verified is in the future", "--check")


class RowIdInventory(GuardTest):
    """PR-004: published row ids are permanent."""

    def test_renamed_id_fails(self):
        self.copy.append("build/rows_ferpa.py", 'ROWS[0]["id"] = ROWS[0]["id"] + "-renamed"')
        self.assertFailsWith("no longer exist in the rows", "--check")

    def test_unblessed_new_id_fails(self):
        self.copy.replace("reference/row-ids.txt", "ferpa-99-10\n", "")
        self.assertFailsWith("not yet in the published roster", "--check")


class LicenseBands(GuardTest):
    """PR-015 guards G1 to G4."""

    def test_g1_constant_without_band(self):
        self.copy.append("build/common.py", 'LIC["new_feature"] = "New feature: Microsoft 365 E5"')
        self.assertFailsWith("licensing constants with no BAND_MAP entry", "--check")

    def test_g2_license_string_matching_no_constant(self):
        self.copy.append("build/rows_ferpa.py",
                         'ROWS[0]["license_requirement"] = "Requires a paid plan"')
        self.assertFailsWith("matches no licensing constant", "--check")

    def test_g3_band_disagrees_with_licensing_model(self):
        self.copy.append("build/rows_ferpa.py", 'ROWS[0]["licensing_model"] = "consumption"')
        self.assertFailsWith("disagrees with licensing_model 'consumption' about consumption pricing",
                             "--check")

    def test_g4_tier_token_outside_any_constant(self):
        self.copy.append("build/rows_ferpa.py",
                         'ROWS[0]["license_requirement"] += "; advanced review features need E5"')
        self.assertFailsWith("carries the tier token", "--check")


class MaintenanceTable(GuardTest):
    """PR-050 structural validation, plus the pass-3 framework-coverage rule."""

    def test_unknown_trigger_type(self):
        self.copy.append("build/common.py", 'MAINTENANCE[0]["type"] = "someday"')
        self.assertFailsWith("bad type", "--check")

    def test_trigger_names_missing_constant(self):
        self.copy.append("build/common.py",
                         'MAINTENANCE[0]["affects"] = [("LIC", "no_such_key")]')
        self.assertFailsWith("names missing key", "--check")

    def test_licensing_constant_with_no_trigger(self):
        self.copy.append("build/common.py",
                         'MAINTENANCE[:] = [t for t in MAINTENANCE '
                         'if ("SENTINEL_LIC", "soar") not in t["affects"]]')
        self.assertFailsWith("licensing constants with no maintenance trigger", "--check")

    def test_framework_with_no_currency_trigger(self):
        self.copy.append("build/common.py",
                         'MAINTENANCE[:] = [t for t in MAINTENANCE if t.get("framework") != "gdpr"]')
        self.assertFailsWith("frameworks with no framework-type maintenance trigger: gdpr", "--check")

    def test_last_executed_in_the_future(self):
        self.copy.append("build/common.py", 'MAINTENANCE[0]["last_executed"] = "2999-01-01"')
        self.assertFailsWith("last_executed is in the future", "--check")

    def test_strict_maintenance_fails_when_a_trigger_is_due(self):
        # A full build, not --check: moving a trigger date changes meta.maintenance in the JSON,
        # so --check would (correctly) fail on drift and hide the behavior under test.
        self.copy.append("build/common.py", 'MAINTENANCE[0]["next_review"] = "2000-01-01"')
        code, out = self.copy.run("build/assemble.py")
        self.assertEqual(code, 0, "an overdue trigger must be advisory without --strict-maintenance")
        self.assertIn("TRIGGER  " + "TRG-CMMC-PHASE2", out)
        self.assertFailsWith("--strict-maintenance set", "--strict-maintenance")


class NextPassDue(GuardTest):
    """E-03: the next-pass date shown to readers must follow the last pass, within the promise."""

    def test_next_pass_before_latest_pass_fails(self):
        self.copy.append("build/common.py", 'NEXT_PASS_DUE = "2026-01-01"')
        self.assertFailsWith("is not after the latest pass", "--check")

    def test_next_pass_beyond_twice_a_year_fails(self):
        self.copy.append("build/common.py", 'NEXT_PASS_DUE = "2027-12-31"')
        self.assertFailsWith("promises a pass at least twice a year", "--check")


class ProseGuards(GuardTest):
    def test_glossary_rejects_em_dash(self):
        self.copy.append("build/glossary.py", 'GLOSSARY["ZZZ"] = "A test term — with an em dash."')
        self.assertFailsWith("glossary term 'ZZZ' contains an em/en dash", "--check")

    def test_stack_rationale_must_be_a_live_spread(self):
        self.copy.append("build/stack_rationales.py",
                         'STACK_RATIONALES.setdefault("ferpa", {})["no-such-ref"] = "A rationale."')
        self.assertFailsWith("is not a coverage-tier spread group", "--check")

    def test_em_dash_in_published_string_fails(self):
        self.copy.append("build/rows_ferpa.py",
                         'ROWS[0]["how_it_supports"] += " A test clause — with an em dash."')
        self.assertFailsWith("em dash in published strings", "--check")

    def test_em_dash_in_framework_title_is_allowed(self):
        # The ISO and SOC 2 formal titles quote the publisher's own em dashes; --check must pass.
        code, out = self.check()
        self.assertEqual(code, 0, out[-1500:])

    def test_em_dash_in_reader_visible_template_text_fails(self):
        self.copy.replace("build/template.html", "<h1>About this atlas</h1>",
                          "<h1>About this atlas — a test</h1>")
        self.assertFailsWith("em dash(es) in reader-visible template text", script="build/build_html.py")

    def test_em_dash_in_template_comment_is_allowed(self):
        self.copy.replace("build/template.html", "<h1>About this atlas</h1>",
                          "<h1>About this atlas</h1><!-- a comment — with a dash -->")
        code, out = self.copy.run("build/build_html.py")
        self.assertEqual(code, 0, out[-1500:])

    def test_spelling_lint_fails_build_html(self):
        with open(self.copy.path("README.md"), "a", encoding="utf-8") as f:
            f.write("\nThis line uses the British spelling licence.\n")
        self.assertFailsWith("banned-spelling violation", script="build/build_html.py")


if __name__ == "__main__":
    unittest.main()
