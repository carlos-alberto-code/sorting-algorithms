import time
from typing import List
from dataclasses import dataclass

from sorting_algorithms.algorithms import SortingAlgorithm


@dataclass
class AlgorithmResult:
    case: str
    element: int
    algorithm: str
    time_taken: float

def run_algorithm(algorithm: SortingAlgorithm, case: str, n: int, results: List[AlgorithmResult]):
    print(f'Iniciando {algorithm.__class__.__name__} para el caso {case} con {n} elementos.')
    start_time = time.time()
    algorithm.sort()
    end_time = time.time()
    time_taken = end_time - start_time
    results.append(AlgorithmResult(case, n, algorithm.__class__.__name__, time_taken))
    print(f'Finalizado {algorithm.__class__.__name__} para el caso {case} con {n} elementos. Tiempo tomado: {time_taken:.2f} segundos\n')
