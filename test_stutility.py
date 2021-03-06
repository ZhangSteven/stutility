""" Test stutility """
import os
from itertools import count, repeat
from datetime import datetime
import unittest2
import itermd
import excel


class StutilityTestCase(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        super(StutilityTestCase, self).__init__(*args, **kwargs)

    def test_firstof(self):
        self.assertEqual(4, itermd.firstof(lambda x: x > 2, [0, 4, 2, 3]))
        self.assertEqual(4, itermd.firstof(lambda x: x > 3, count()))

        with self.assertRaises(ValueError):
            itermd.firstof(lambda x: x > 8, range(3))

    def test_firstn(self):
        self.assertEqual([0,1], list(itermd.firstn(2, count())))
        self.assertEqual([], list(itermd.firstn(0, count())))
        self.assertEqual([0], list(itermd.firstn(1, range(5))))
        self.assertEqual([0,1], list(itermd.firstn(2, range(2))))
        self.assertEqual([0,1,2], list(itermd.firstn(5, range(3))))
        self.assertEqual([], list(itermd.firstn(8, [])))

        with self.assertRaises(ValueError):
            list(itermd.firstn(-1, [1,2]))   # must use list to trigger the
                                            # error because generator is lazy

    def test_skipn(self):
        self.assertEqual([0,1,2], list(itermd.skipn(0, range(3))))
        self.assertEqual([2,3,4], list(itermd.skipn(2, range(5))))
        self.assertEqual([], list(itermd.skipn(5, range(5))))

        with self.assertRaises(ValueError):
            list(itermd.skipn(-1, [1,2]))   # must use list to trigger the
                                            # error because generator is lazy

    def test_firstn_skipn(self):
        self.assertEqual(
            [3,4], 
            list(itermd.firstn(2, itermd.skipn(3, count())))
        )

    def test_allequal(self):
        self.assertTrue(itermd.allequal([]))
        self.assertTrue(itermd.allequal(range(0)))  # empty
        self.assertTrue(
            itermd.allequal(filter(lambda x: x < 1, range(8))))
        self.assertTrue(itermd.allequal(zip(repeat('x'), [1, 1, 1])))
        self.assertFalse(itermd.allequal([1, 1, 2]))

    def test_num_elements(self):
        self.assertEqual(0, itermd.num_elements([]))
        self.assertEqual(0, itermd.num_elements(range(0)))
        self.assertEqual(1, itermd.num_elements(range(5,6)))
        self.assertEqual(
            2, 
            itermd.num_elements(filter(lambda x: x < 2, range(8)))
        )

    def test_excel(self):
        file = os.path.join('samples', 'sample 01.xlsx')
        positions = list(excel.workbook_to_positions(file))
        self.assertEqual(3, len(positions))

        p = positions[0]
        self.assertEqual('Isaac', p['Name'])
        self.assertEqual(datetime(2021,12,1), p['Date'])
        self.assertEqual(100, p['Score'])
        self.assertEqual(None, p['Remarks'])

        p = positions[1]
        self.assertEqual(4, len(p))
        self.assertEqual('Andy', p['Name'])
        self.assertEqual(datetime(2021,11,8), p['Date'])
        self.assertEqual(95, p['Score'])
        self.assertEqual('Andy has improved', p['Remarks'])

    def test_excel_2(self):
        file = os.path.join('samples', 'sample 02.xlsx')
        positions = list(excel.workbook_to_positions(file, 3))
        self.assertEqual(3, len(positions))

        p = positions[2]
        self.assertEqual('Isaac', p['Name'])
        self.assertEqual(datetime(2021,9,30), p['Date'])
        self.assertEqual(88, p['Score'])

    def test_xls_excel(self):
        file = os.path.join('samples', 'sample 03.xls')
        positions = list(excel.xls_workbook_to_positions(file))
        self.assertEqual(3, len(positions))

        p = positions[0]
        self.assertEqual('Isaac', p['Name'])
        self.assertEqual(
            '2021-12-01',
            excel.get_ymd_date_from_oridinal(p['Date'])
        )
        self.assertEqual(100, p['Score'])
        self.assertEqual('', p['Remarks'])

        p = positions[1]
        self.assertEqual(4, len(p))
        self.assertEqual('Andy', p['Name'])
        self.assertEqual(95, p['Score'])
        self.assertEqual('Andy has improved', p['Remarks'])

    def test_xls_excel_2(self):
        file = os.path.join('samples', 'sample 04.xls')
        positions = list(excel.xls_workbook_to_positions(file, 3))
        self.assertEqual(3, len(positions))

        p = positions[2]
        self.assertEqual('Isaac', p['Name'])
        self.assertEqual(
            '2021-09-30',
            excel.get_ymd_date_from_oridinal(p['Date'])
        )
        self.assertEqual(88, p['Score'])

# end of class StutilityTestCase()


if __name__ == '__main__':
    unittest2.main()