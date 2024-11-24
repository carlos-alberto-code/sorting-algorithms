import time
from util.logger import log_results
from util.numbers_generator import generate_numbers
from sorting_algorithms.algorithms import * # Importamos todas las clases de algoritmos

with open("log.txt", "w") as log_file:
    log_file.write("")

cases = ["average", "worst"]
elements = [1_000]
algorithms = [
    BubbleSort(), SelectionSort(),
    InsertionSort(), MergeSort()
]

for case in cases:
    for element in elements:
        try:
            numbers = generate_numbers(case, element)
        except ValueError as e:
            print(f'Error al generar los números: {e}')
            continue
        for i, algorithm in enumerate(algorithms):
            start = time.time()
            algorithm.sort(numbers.copy())
            end = time.time()
            is_last_algorithm = i == len(algorithms) - 1
            log_results(
                case, element, algorithm.__class__.__name__, end - start, is_last_algorithm
            )
