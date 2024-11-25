import time
from typing     import List
from threading  import Thread


class ThreadAlgorithm(Thread):
    def __init__(self, algorithm, logger, case: str, element: int):
        super().__init__(name=algorithm.__class__.__name__)
        self.algorithm = algorithm
        self.logger = logger
        self.case = case
        self.element = element

    def run(self):
        start = time.time()
        self.algorithm.sort()
        end = time.time()
        time_taken = end - start
        self.logger.log_finish(self.case, self.element, self.algorithm.__class__.__name__, time_taken)


def ejecutar_algoritmos_en_hilos(algorithms: List, logger, case: str, element: int):
    threads = []
    for algorithm in algorithms:
        thread = ThreadAlgorithm(algorithm, logger, case, element)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
