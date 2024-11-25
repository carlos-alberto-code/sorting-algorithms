from functools import wraps
import time
from typing import List
from threading import Thread

from sorting_algorithms.algorithms import SortingAlgorithm
from util.logger import Logger


class ThreadAlgorithm(Thread):
    def __init__(self, algorithm: SortingAlgorithm, logger: Logger, case: str, element: int, is_last_algorithm: bool):
        super().__init__(name=algorithm.__class__.__name__)
        self.algorithm = algorithm
        self.logger = logger
        self.case = case
        self.element = element
        self.is_last_algorithm = is_last_algorithm

    def run(self):
        start = time.time()
        self.algorithm.sort()
        end = time.time()
        time_taken = end - start
        self.logger.log_results(self.case, self.element, self.algorithm.__class__.__name__, time_taken, self.is_last_algorithm)




def ejecutar_algoritmos_en_hilos(algorithms: List[SortingAlgorithm], logger: Logger, case: str, element: int):
    threads: List[Thread] = []
    for algorithm in algorithms:
        thread = ThreadAlgorithm(algorithm, logger, case, element, algorithm == algorithms[-1])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

