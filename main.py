import time
from threading import Thread
from typing import List, Callable
from dataclasses import dataclass

from util.logger import log_results
from util.numbers_generator import generate_numbers
from sorting_algorithms.algorithms import bubble_sort, selection_sort, insertion_sort, merge_sort

@dataclass
class AlgorithmResult:
    name: str
    execution_time: float

class TimedThread(Thread):
    def __init__(self, target: Callable, args: tuple, name: str):
        super().__init__()
        self.target = target
        self.args = args
        self.algorithm_name = name
        self.execution_time = 0

    def run(self):
        print(f"Inicio del hilo: {self.algorithm_name}")
        start = time.time()
        self.target(*self.args)
        self.execution_time = time.time() - start
        print(f"Fin del hilo: {self.algorithm_name} - Tiempo de ejecución: {self.execution_time:.2f} segundos")

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

total_start = time.time()

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
                print(f"Hilo {name} iniciado.")

            # Esperar a que todos los hilos terminen
            results: List[AlgorithmResult] = []
            for thread in threads:
                thread.join()
                results.append(AlgorithmResult(thread.algorithm_name, thread.execution_time))
                print(f"Hilo {thread.algorithm_name} terminado.")

            # Registrar resultados
            for i, result in enumerate(results):
                is_last = i == len(results) - 1
                log_results(case, element, result.name, result.execution_time, is_last)

        except ValueError as e:
            print('Error al generar los números:', e)
            continue

total_time = time.time() - total_start
print(f"Tiempo total de ejecución: {total_time:.2f} segundos")
