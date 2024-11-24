import time
from typing import List

from util.logger import log_results
from hilos import AlgorithmResult, TimedThread
from util.numbers_generator import generate_numbers
from sorting_algorithms.algorithms import bubble_sort, selection_sort, insertion_sort, merge_sort


# Limpiar archivo de log
with open("log.txt", "w") as log_file:
    log_file.write("")

cases = ["average"]
elements = [10_000]
algorithms = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort
}

for case in cases:
    for element in elements:
        try:
            numbers = generate_numbers(case, element)

            # Crear y comenzar todos los hilos
            threads: List[TimedThread] = []
            for name, func in algorithms.items():
                thread = TimedThread(target=func, args=(numbers.copy(),), name=name)
                threads.append(thread)
                thread.start()

            # Esperar a que todos los hilos terminen
            results: List[AlgorithmResult] = []
            for thread in threads:
                thread.join()
                results.append(AlgorithmResult(thread.algorithm_name, thread.execution_time))

            # Registrar resultados
            for i, result in enumerate(results):
                is_last = i == len(results) - 1
                log_results(case, element, result.name, result.execution_time, is_last)

        except ValueError as e:
            print('Error al generar los números:', e)
            continue
