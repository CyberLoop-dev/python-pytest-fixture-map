import tempfile
import unittest
from pathlib import Path
from pytest_fixture_map import scan

class FixtureMapTests(unittest.TestCase):
    def test_detects_fixture_and_test_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "conftest.py").write_text(
                "import pytest\n@pytest.fixture(scope='module')\ndef db(): return object()\n",
                encoding="utf-8",
            )
            (root / "test_sample.py").write_text(
                "def test_reads_db(db): assert db is not None\n", encoding="utf-8"
            )
            data = scan(root)
            self.assertEqual(data["fixtures"]["db"]["scope"], "module")
            self.assertEqual(data["tests"][0]["dependencies"], ["db"])

if __name__ == "__main__":
    unittest.main()
