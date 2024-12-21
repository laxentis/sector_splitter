from unittest import TestCase

from esefile import COPX


class TestCOPX(TestCase):
    def test_from_string(self):
        line = "FIR_COPX:*:*:BUDOP:LHBP:*:BPM:BUD:*:28000:BUDOP"
        generated = COPX.from_string(line)
        self.assertEqual(line, str(generated))
