try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestPyCorpora(unittest.TestCase):

    def test_import(self):
        import pycorpora
        self.assertTrue(hasattr(pycorpora, 'pycorpora_test'))
        self.assertTrue(hasattr(pycorpora, 'hyphenated_dirname'))

    def test_load_corpus(self):
        import pycorpora
        self.assertEqual(type(pycorpora.pycorpora_test.test), dict)
        self.assertEqual(pycorpora.pycorpora_test.test['tests'],
                         ["one", "two", "three"])

        self.assertEqual(type(pycorpora.hyphenated_dirname.test), dict)
        self.assertEqual(pycorpora.hyphenated_dirname.test['tests'],
                         ["one", "two", "three"])

    def test_subdir(self):
        import pycorpora
        self.assertEqual(type(pycorpora.pycorpora_test.subdir.another_test),
                         dict)
        self.assertEqual(pycorpora.pycorpora_test.subdir.another_test['tests'],
                         ["four", "five", "six"])

    def test_getitem(self):
        import pycorpora
        self.assertEqual(type(pycorpora.pycorpora_test['test-filename']), dict)
        self.assertEqual(pycorpora.pycorpora_test['test-filename']['tests'],
                         ["one", "two", "three"])
        self.assertEqual(pycorpora.pycorpora_test['test'],
                         pycorpora.pycorpora_test.test)
        self.assertEqual(pycorpora.pycorpora_test['subdir']['another_test'],
                         pycorpora.pycorpora_test.subdir.another_test)

    def test_attr_errors(self):
        import pycorpora
        self.assertRaises(AttributeError, lambda: pycorpora.pycorpora_schmest)
        self.assertRaises(AttributeError,
                          lambda: pycorpora.pycorpora_test.not_here)
        self.assertRaises(AttributeError,
                          lambda: pycorpora.pycorpora_test.subdir.not_here)

    def test_from_import(self):
        from pycorpora import pycorpora_test
        self.assertEqual(type(pycorpora_test.test), dict)
        self.assertEqual(pycorpora_test.test['tests'], ["one", "two", "three"])

    def test_get_categories(self):
        import pycorpora
        cats = pycorpora.get_categories()
        self.assertIn('pycorpora_test', cats)
        subcats = pycorpora.get_categories("pycorpora_test")
        self.assertEqual(subcats, ['subdir'])

    def test_loader_get_categories(self):
        import pycorpora
        cats = pycorpora.pycorpora_test.get_categories()
        self.assertEqual(cats, ['subdir'])

    def test_get_files(self):
        import pycorpora
        files = pycorpora.get_files('pycorpora_test')
        self.assertEqual(set(files), set(['test-filename', 'test']))
        subfiles = pycorpora.get_files('pycorpora_test/subdir')
        self.assertEqual(subfiles, ['another_test'])

    def test_loader_get_files(self):
        import pycorpora
        files = pycorpora.pycorpora_test.get_files()
        self.assertEqual(set(files), set(['test-filename', 'test']))
        subfiles = pycorpora.pycorpora_test.subdir.get_files()
        self.assertEqual(subfiles, ['another_test'])

    def test_get_file(self):
        import pycorpora
        data = pycorpora.get_file('pycorpora_test', 'test')
        self.assertEqual(type(data), dict)
        self.assertEqual(data['tests'], ["one", "two", "three"])
        subdata = pycorpora.get_file('pycorpora_test/subdir', 'another_test')
        self.assertIsNotNone(subdata)
        self.assertEqual(type(data), dict)
        self.assertEqual(data['tests'], ["one", "two", "three"])

    def test_loader_get_file(self):
        import pycorpora
        data = pycorpora.pycorpora_test.get_file('test')
        self.assertEqual(type(data), dict)
        self.assertEqual(data['tests'], ["one", "two", "three"])
        subdata = pycorpora.pycorpora_test.subdir.get_file('another_test')
        self.assertIsNotNone(subdata)
        self.assertEqual(type(data), dict)
        self.assertEqual(data['tests'], ["one", "two", "three"])

    def test_cache(self):
        import pycorpora
        self.assertNotIn('data/pycorpora_test/test.json', pycorpora.cache)
        data = pycorpora.get_file('pycorpora_test', 'test')
        self.assertIn('data/pycorpora_test/test.json', pycorpora.cache)
        data = pycorpora.pycorpora_test.subdir.another_test
        self.assertIsNotNone(data)
        self.assertIn('data/pycorpora_test/subdir/another_test.json',
                      pycorpora.cache)

if __name__ == '__main__':
    unittest.main()
