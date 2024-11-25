from typing import List
import time
from threading import Thread

from util.logger import log_results
from util.numbers_generator import generate_numbers
from sorting_algorithms.algorithms import *
from util.thread_runner import AlgorithmResult, run_algorithm  # Importamos todas las clases de algoritmos


# Limpiar archivo de log
with open("log.txt", "w") as log_file:
    log_file.write("")

cases = ["best", "average", "worst"]
elements = [1_000, 5_000]
algorithms: List[SortingAlgorithm] = []

for case in cases:
    for n in elements:
        try:
            nums = generate_numbers(case, n)
            algorithms = [
                BubbleSort(nums.copy()),
                SelectionSort(nums.copy()),
                InsertionSort(nums.copy()),
                MergeSort(nums.copy())
            ]
        except ValueError as e:
            print(f'Error al generar los números: {e}')
            continue

        threads: List[Thread] = []
        results: List[AlgorithmResult] = []
        for algorithm in algorithms:
            thread = Thread(target=run_algorithm, args=(algorithm, case, n, results))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for result in results:
            log_results(result.case, result.element, result.algorithm, result.time_taken, result == results[-1])
