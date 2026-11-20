import unittest
from research.scripts.addressed_guard_audit import audit


def run(*ins):
    return audit([{'address': hex(0x1000 + 4*i), 'instruction': v} for i,v in enumerate(ins)])[0]['status']


class AddressedGuardAuditTests(unittest.TestCase):
    def test_nan_branch_targets_conversion(self):
        self.assertEqual(run('fcmp d0, d0','b.vs loc_1008','fcvtzs w0, d0','ret'), 'nan_path_enters_conversion')

    def test_nan_fallthrough_targets_conversion(self):
        self.assertEqual(run('fcmp d0, d0','b.vc loc_100c','fcvtzs w0, d0','ret'), 'nan_path_enters_conversion')

    def test_candidate_only(self):
        self.assertEqual(run('fcmp d0, d0','b.vs loc_100c','fcvtzs w0, d0','ret'), 'candidate_local_pair_unverified')

    def test_different_register(self):
        self.assertEqual(run('fcmp d1, d1','b.vs loc_100c','fcvtzs w0, d0','ret'), 'unknown_different_register_or_width')

    def test_width_alias_not_verified(self):
        self.assertEqual(run('fcmp s0, s0','b.vs loc_100c','fcvtzs w0, d0','ret'), 'unknown_different_register_or_width')

    def test_intervening_redefinition(self):
        self.assertEqual(run('fcmp d0, d0','b.vs loc_1010','fmov d0, d1','fcvtzs w0, d0','ret'), 'unknown_intervening_instructions')

    def test_missing_target(self):
        self.assertEqual(run('fcmp d0, d0','b.vs loc_9999','fcvtzs w0, d0','ret'), 'unknown_branch_target')

    def test_no_candidate(self):
        self.assertEqual(run('nop','fcvtzs w0, d0','ret'), 'unknown_no_candidate')

    def test_multiple_conversions(self):
        records=[{'address':hex(0x1000+4*i),'instruction':v} for i,v in enumerate(('fcvtzs w0, d0','fcvtzs w1, d1'))]
        self.assertEqual(len(audit(records)),2)


if __name__ == '__main__':
    unittest.main()
