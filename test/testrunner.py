import sys
import os
import unittest
import random

if __name__ == '__main__':
    test_runner = unittest.TextTestRunner(verbosity=2)

    search_path = os.path.abspath(os.path.dirname(__file__))
    files = os.listdir(search_path)
    random.shuffle(files)
    suites = []
    for filename in files:
        if filename.startswith("test_") and filename[-3:] == '.py':
            try:
                data = __import__(filename[:-3])
            except ImportError as e:
                print ('Error to import: %s' % (e))
                data = None

            if data is not None:
                names = dir(data)
                for name in names:
                    obj = getattr(data, name)
                    if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
                        suite = unittest.TestLoader().loadTestsFromTestCase(obj)
                        suites.append(suite)

    if suites and test_runner:
        res = test_runner.run(unittest.TestSuite(suites))
        if res.errors or res.failures:
            sys.exit(1)
