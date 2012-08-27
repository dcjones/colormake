#!/usr/bin/env python

import unittest
import colormake as cm


class TestBase(unittest.TestCase):

    def setUp(self):
        self.line = None

    def _check(self, color):
        self.assertIsNotNone(self.line)
        lout = cm.line_add_color(self.line)
        self.assertEqual(lout, color + self.line + cm.col_norm)


class TestMake(TestBase):
 
    def test_enter_directory1(self):
        self.line = "make[1]: Entering directory `/home/user/test'"
        self._check(cm.col_cyan)

    def test_enter_directory2(self):
        self.line = "make[3451]: Entering directory `/home/user/test'"
        self._check(cm.col_cyan)

    def test_making_all(self):
        self.line = "Making all in test"
        self._check(cm.col_cyan + cm.col_brighten)

    def test_CC(self):
        self.line = "  CC     libtest.lo"
        self._check(cm.col_norm + cm.col_brighten)

    def test_CXX(self):
        self.line = "  CXX     libtest++.lo"
        self._check(cm.col_norm + cm.col_brighten)

    def test_CCLD(self):
        self.line = "  CCLD   libtest++.la"
        self._check(cm.col_norm + cm.col_brighten)

    def test_CXXLD(self):
        self.line = "  CXXLD   libtest++.la"
        self._check(cm.col_norm + cm.col_brighten)



class TestGcc(TestBase):

    def test_in_function(self):
        self.line = "file.c: In function 'test_create':"
        self._check(cm.col_yellow + cm.col_brighten)

    def test_warning(self):
        self.line = "test.c:2098:5: warning: no previous prototype for '_column' [-Wmissing-prototypes]"
        self._check(cm.col_yellow)

    def test_error(self):
        self.line = "test.c:393:3: error: invalid use of void expression"
        self._check(cm.col_red)

    def test_other_message(self):
        self.line = "test.c:22:3: "
        self._check(cm.col_yellow + cm.col_brighten)



if __name__ == '__main__':
    suiteMake = unittest.TestLoader().loadTestsFromTestCase(TestMake)
    suiteGcc = unittest.TestLoader().loadTestsFromTestCase(TestGcc)
    suite = unittest.TestSuite([suiteMake, suiteGcc])
    unittest.TextTestRunner(verbosity=2).run(suite)

