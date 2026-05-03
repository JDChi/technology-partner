import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "knowledge_index.py"


def load_module():
    spec = importlib.util.spec_from_file_location("knowledge_index", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class KnowledgeIndexTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.knowledge_dir = self.root / "knowledge"
        self.templates_dir = self.root / "templates"

        for relative_dir in [
            "knowledge/patterns",
            "knowledge/scenarios",
            "knowledge/workflows",
            "knowledge/decisions",
            "templates",
        ]:
            (self.root / relative_dir).mkdir(parents=True, exist_ok=True)

        (self.templates_dir / "knowledge-entry-template.md").write_text(
            "# Title\n\n## Summary\n- Placeholder\n",
            encoding="utf-8",
        )
        (self.templates_dir / "decision-record-template.md").write_text(
            "# Decision Title\n\n## Date\n- YYYY-MM-DD\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def read_index(self):
        return json.loads((self.knowledge_dir / "index.json").read_text(encoding="utf-8"))

    def test_sync_bootstraps_index_json_from_filesystem(self):
        module = load_module()

        (self.knowledge_dir / "patterns" / "sample-pattern.md").write_text(
            "# Sample Pattern\n",
            encoding="utf-8",
        )
        (self.knowledge_dir / "decisions" / "2026-05-03-script-first.md").write_text(
            "# Script First\n\n## Date\n- 2026-05-03\n",
            encoding="utf-8",
        )

        module.sync_index(self.root)

        data = self.read_index()
        self.assertEqual(data["entries"]["pattern"][0]["path"], "patterns/sample-pattern.md")
        self.assertEqual(data["entries"]["pattern"][0]["title"], "Sample Pattern")
        self.assertEqual(data["entries"]["decision"][0]["slug"], "script-first")
        self.assertEqual(data["entries"]["decision"][0]["date"], "2026-05-03")

    def test_create_pattern_generates_file_and_updates_index(self):
        module = load_module()

        created_path = module.create_entry(self.root, "pattern", "本地 ASR 选型")

        self.assertEqual(created_path.relative_to(self.knowledge_dir).as_posix(), "patterns/asr.md")
        self.assertTrue(created_path.exists())
        self.assertIn("# 本地 ASR 选型", created_path.read_text(encoding="utf-8"))

        data = self.read_index()
        self.assertEqual(data["entries"]["pattern"][0]["title"], "本地 ASR 选型")
        self.assertEqual(data["entries"]["pattern"][0]["slug"], "asr")

    def test_create_decision_uses_date_prefix_and_template_date(self):
        module = load_module()

        created_path = module.create_entry(self.root, "decision", "脚本优先自动化")
        created_text = created_path.read_text(encoding="utf-8")

        self.assertRegex(created_path.name, r"^\d{4}-\d{2}-\d{2}-")
        self.assertIn("## Date", created_text)
        self.assertRegex(created_text, r"- \d{4}-\d{2}-\d{2}")

        data = self.read_index()
        self.assertEqual(data["entries"]["decision"][0]["title"], "脚本优先自动化")

    def test_create_fails_when_target_exists(self):
        module = load_module()

        module.create_entry(self.root, "workflow", "Repo 抽象")

        with self.assertRaises(FileExistsError):
            module.create_entry(self.root, "workflow", "Repo 抽象")

    def test_sync_removes_deleted_entry(self):
        module = load_module()

        created_path = module.create_entry(self.root, "scenario", "本地 ASR 后端选择")
        created_path.unlink()

        module.sync_index(self.root)

        data = self.read_index()
        self.assertEqual(data["entries"]["scenario"], [])


if __name__ == "__main__":
    unittest.main()
