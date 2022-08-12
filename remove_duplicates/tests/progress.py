import unittest

from remove_duplicates.progress import _report_percent


class ProgressTestCase(unittest.TestCase):
    def setUp(self):
        self.percentage_floats = [(x / 10) for x in range(0, 1000)]
        self.percentage_floats.append(100.0)


def test_progress(self):
    #     self.assertEqual(True, False)  # add assertion here
    for percent in self.percentage_floats:
        _report_percent(percent)


    # progress(enabled=True, task_str='test', processed_qty=0)


if __name__ == '__main__':
    unittest.main()
