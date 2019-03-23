import unittest
import multiprocessing as mp
from pooling import ProcessPool, heavy_computation


class PoolTests(unittest.TestCase):

    def test_create_pool(self):
        pool = ProcessPool(min_workers=2, max_workers=10, mem_usage='3gb')
        self.assertEqual(2, pool.min_workers)
        self.assertEqual(10, pool.max_workers)
        self.assertEqual(3, pool.mem_usage)

    def test_change_mem(self):
        gb = ProcessPool(min_workers=2, max_workers=10, mem_usage='5Gb').mem_usage
        mb = ProcessPool(min_workers=2, max_workers=10, mem_usage='3075mB').mem_usage
        kb = ProcessPool(min_workers=2, max_workers=10, mem_usage='100000kb').mem_usage
        b = ProcessPool(min_workers=2, max_workers=10, mem_usage='8500000B').mem_usage
        self.assertEqual([gb, mb, kb, b], [5.0, 3.003, 0.095, 0.008])

    def test_mem_err_one(self):
        pool = ProcessPool(min_workers=100, max_workers=110, mem_usage='1gb')
        q = mp.Queue()
        q.put(8)
        q.put(13)
        try:
            pool.map(heavy_computation, q)
        except Warning:
            pass
        else:
            raise Warning

    def test_mem_err_two(self):
        pool = ProcessPool(min_workers=2, max_workers=10, mem_usage='5000kb')
        q = mp.Queue()
        q.put(8)
        q.put(13)
        try:
            pool.map(heavy_computation, q)
        except Warning:
            pass
        else:
            raise Warning

    def test_min_workers_err(self):
        pool = ProcessPool(min_workers=50, max_workers=60, mem_usage='1gb')
        q = mp.Queue()
        q.put(2)
        q.put(6)
        try:
            pool.map(heavy_computation, q)
        except Warning:
            pass
        else:
            raise Warning

    def test_max_workers_change(self):
        pool = ProcessPool(min_workers=1, max_workers=1, mem_usage='1Gb')
        q = mp.Queue()
        q.put(4)
        q.put(10)
        pool.map(heavy_computation, q)
        self.assertEqual(pool.amt_workers, 1)

    def test_correct_mem(self):
        pool = ProcessPool(min_workers=2, max_workers=10, mem_usage='512mb')
        q = mp.Queue()
        q.put(4)
        q.put(12)
        amt_workers, p_mem_usage = pool.map(heavy_computation, q)
        self.assertLessEqual(amt_workers * p_mem_usage, 0.5)


if __name__ == '__main__':
    unittest.main()
