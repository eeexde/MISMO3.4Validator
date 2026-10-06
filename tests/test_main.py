import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "your_project"))

import main  # noqa: E402

VALID = os.path.join(REPO_ROOT, "test", "valid_complete")
INVALID = os.path.join(REPO_ROOT, "test", "test")


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main.main(list(args))
    return code, out.getvalue(), err.getvalue()


class ValidateMismoTest(unittest.TestCase):
    def test_valid_file_exits_zero(self):
        code, out, _ = run(VALID)
        self.assertEqual(code, main.EXIT_VALID)
        self.assertIn("VALID", out)

    def test_invalid_file_exits_one_and_lists_errors(self):
        code, out, _ = run(INVALID)
        self.assertEqual(code, main.EXIT_INVALID)
        self.assertIn("LastName", out)

    def test_missing_file_exits_two(self):
        code, _, err = run(os.path.join(REPO_ROOT, "does_not_exist.xml"))
        self.assertEqual(code, main.EXIT_ERROR)
        self.assertIn("could not parse", err)

    def test_worst_result_wins_for_multiple_files(self):
        code, _, _ = run(VALID, INVALID)
        self.assertEqual(code, main.EXIT_INVALID)

    def test_does_not_change_working_directory(self):
        before = os.getcwd()
        run(VALID)
        self.assertEqual(os.getcwd(), before)

    def test_external_entities_are_not_expanded(self):
        with tempfile.TemporaryDirectory() as tmp:
            secret = os.path.join(tmp, "secret.txt")
            with open(secret, "w") as f:
                f.write("TOPSECRET")
            xml = os.path.join(tmp, "xxe.xml")
            with open(xml, "w") as f:
                f.write(
                    '<?xml version="1.0"?>\n'
                    f'<!DOCTYPE m [<!ENTITY x SYSTEM "file:///{secret}">]>\n'
                    '<MESSAGE xmlns="http://www.mismo.org/residential/2009/schemas">&x;</MESSAGE>'
                )
            _, out, _ = run(xml)
        self.assertNotIn("TOPSECRET", out)

    def test_cli_runs_from_any_directory_on_legacy_console_encoding(self):
        env = dict(os.environ, PYTHONIOENCODING="cp1252")
        result = subprocess.run(
            [sys.executable, os.path.join(REPO_ROOT, "your_project", "main.py")],
            cwd=os.path.join(REPO_ROOT, "tools"),
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, main.EXIT_VALID, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
