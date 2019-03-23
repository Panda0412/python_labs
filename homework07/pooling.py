import random
import time
import numpy
import multiprocessing as mp
import psutil


def heavy_computation(data_chunk):
    a = numpy.array([[random.randint(1000 * (-data_chunk), 1000 * data_chunk)
                      for _ in range(1000)] for _ in range(1000)])
    b = numpy.array([[random.randint(1000 * (-data_chunk), 1000 * data_chunk)
                      for _ in range(1000)] for _ in range(1000)])
    c = numpy.array([[random.randint(1000 * (-data_chunk), 1000 * data_chunk)
                      for _ in range(1000)] for _ in range(1000)])
    x = a * b * c
    return x


def memory(mem_usage):
    m = mem_usage.upper()
    try:
        size = int(m)
        return size
    except:
        if not m[-2:-1].isdigit():
            size = int(m[:-2])
            units = m[-2:]
            units_dict = {
                'GB': 1,
                'MB': 1024,
                'KB': 1024 * 1024,
            }
            size = size / units_dict[units]
        else:
            size = int(m[:-1]) / 1024 ** 3
        return round(size, 3)


class ProcessPool:

    def __init__(self, min_workers=2, max_workers=40, mem_usage='1gb'):
        self.mem_usage = memory(mem_usage)
        self.p_mem_usage = 0
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.amt_workers = 0
        self.mem_queue = mp.Queue()

    def map(self, computations, data):
        # первый процесс (для теста) и расчёт возможного количества процессов
        t_p = mp.Process(target=computations,
                         name='test process', args=(data.get(),))
        t_p.start()
        t_m = mp.Process(target=self.memory_test,
                         name='test memory', args=(t_p.pid,))
        t_m.start()
        t_p.join()
        t_m.join()
        mem_list = []
        print('Вычисление памяти для одного процесса')
        while not self.mem_queue.empty():
            m = self.mem_queue.get()
            mem_list.append(m)
        self.p_mem_usage = max(mem_list)
        print('Вычисление завершено, для одного процесса необходимо:',
              self.p_mem_usage)
        if self.p_mem_usage > self.mem_usage:
            raise Warning('У Вас недостаточно памяти даже для одного процесса')
        self.amt_workers = int(self.mem_usage // self.p_mem_usage)
        if self.amt_workers > self.max_workers:
            self.amt_workers = self.max_workers
        elif self.amt_workers < self.min_workers:
            raise Warning('У Вас не хватает памяти для работы '
                          'даже заданного min_workers')
        else:
            self.amt_workers = int(self.mem_usage // self.p_mem_usage)
        # пул процессов
        print('Запуск пула процессов')
        p_list = []
        for _ in range(self.amt_workers):
            if not data.empty():
                print('Создание процесса')
                p = mp.Process(target=computations, args=(data.get(),))
                p.start()
                p_list.append(p)
                print(p.pid)
            else:
                for pp in p_list:
                    pp.join()
                return self.amt_workers, self.p_mem_usage
        while True:
            for p in p_list:
                p.join(0.001)
                if not p.is_alive():
                    print('Процесс', p.pid, 'завершил работу')
                    p.terminate()
                    if not data.empty():
                        print('Создание нового процесса вместо старого')
                        p_list.remove(p)
                        pp = mp.Process(target=computations,
                                        args=(data.get(),))
                        pp.start()
                        p_list.append(pp)
                    else:
                        for pp in p_list:
                            pp.join()
                        return self.amt_workers, self.p_mem_usage

    def memory_test(self, pid):
        print('Создание mem_queue')
        p_mem = psutil.Process(pid)
        while psutil.pid_exists(pid):
            try:
                self.mem_queue.put(p_mem.memory_info().rss // 1000000 / 1000)
            except:
                pass
            time.sleep(0.01)
        print('Создание завершено')


if __name__ == '__main__':
    q = mp.Queue()
    for i in range(5):
        q.put(i * 100)
    pool = ProcessPool()
    print(pool.map(heavy_computation, q))
