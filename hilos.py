import time
from typing import List
from threading import Thread
from dataclasses import dataclass

from sorting_algorithms.algorithms import SortingAlgorithm


@dataclass
class AlgorithmContext:
    algorithm: SortingAlgorithm
    case: str
    elements: int


class ThreadAlgorithm(Thread):
    def __init__(self, context: AlgorithmContext, logger):
        super().__init__(name=context.algorithm.__class__.__name__)
        self.context = context
        self.logger = logger

    def run(self):
        start = time.time()
        self.context.algorithm.sort()
        end = time.time()
        time_taken = end - start
        self.logger.log_finish(
            self.context.case,
            self.context.elements,
            self.context.algorithm.__class__.__name__,
            time_taken
        )


def ejecutar_algoritmos_en_hilos(algorithm_contexts: List[AlgorithmContext], logger):
    threads = []
    for context in algorithm_contexts:
        thread = ThreadAlgorithm(context, logger)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
