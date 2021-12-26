""" Test stutility """
import unittest2
from itertools import count
import itermd


class StutilityTestCase(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        super(StutilityTestCase, self).__init__(*args, **kwargs)

    def test_firstof(self):
        self.assertEqual(4, itermd.firstof(lambda x: x > 2, [0, 4, 2, 3]))
        self.assertEqual(7, itermd.firstof(lambda __: True, count(7)))

        with self.assertRaises(StopIteration):
            itermd.firstof(lambda x: x > 8, range(3))

    def test_skipn(self):
        self.assertEqual([0,1,2], list(itermd.skipn(0, range(3))))
        self.assertEqual([2,3,4], list(itermd.skipn(2, range(5))))
        self.assertEqual([], list(itermd.skipn(5, range(5))))

        with self.assertRaises(ValueError):
            list(itermd.skipn(-1, [1,2]))   # must use list to trigger the
                                            # error because generator is lazy

    # end of test_skipn()

# end of class StutilityTestCase()


if __name__ == '__main__':
    unittest2.main()