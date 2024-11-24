import time
from util.logger import log_results
from util.numbers_generator import generate_numbers
from sorting_algorithms.algorithms import bubble_sort, selection_sort, insertion_sort, merge_sort

with open("log.txt", "w") as log_file:
    log_file.write("")

cases = ["best", "average", "worst"]
elements = [1_000]
algorithms = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort
}

for case in cases:
    for element in elements:
        numbers = generate_numbers(case, element)
        for i, (name, func) in enumerate(algorithms.items()):
            start = time.time()
            func(numbers.copy())
            end = time.time()
            is_last_algorithm = i == len(algorithms) - 1
            log_results(case, element, name, end - start, is_last_algorithm)
