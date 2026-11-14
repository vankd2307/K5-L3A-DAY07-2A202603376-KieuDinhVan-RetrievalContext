"""Report regeneration must never overwrite assignment README files."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import scripts.report as report


class ReportReadmeTests(unittest.TestCase):
    def test_report_writes_student_guide_and_preserves_assignment_readmes(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            original=b'# Assignment README\nKeep teacher instructions.\n'
            (root/'README.md').write_bytes(original)
            (root/'src').mkdir()
            source_original=b'# Original code instructions\n'
            (root/'src/README.md').write_bytes(source_original)
            (root/'report/individual').mkdir(parents=True)
            experiment={'agent_model':'offline-test','configs':[],'selection_rule':'dev only'}
            with patch.object(report,'ROOT',root), patch.object(report,'read',return_value=experiment), \
                 patch.object(report,'aggregate_reviews',return_value=[]), patch('builtins.print'):
                report.main()
            self.assertEqual((root/'README.md').read_bytes(),original)
            self.assertEqual((root/'src/README.md').read_bytes(),source_original)
            self.assertTrue((root/'README_STUDENT.md').is_file())
            self.assertTrue((root/'report/individual/2A202603376_KieuDinhVan.md').is_file())


if __name__=='__main__':
    unittest.main()
